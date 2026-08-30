"use client";

import { useEffect, useState } from "react";
import { useCompare } from "@/hooks/useHotels";
import { Button } from "@/components/ui/button";
import { GitCompare, MapPin, Star, ShieldCheck, CheckCircle2, AlertTriangle, Bot, ChevronDown, ChevronUp } from "lucide-react";
import Link from "next/link";
import { getHotelAnalysis } from "@/lib/api";

export default function ComparePage() {
  const [comparedIds, setComparedIds] = useState<string[]>([]);
  const [hotelsData, setHotelsData] = useState<any[]>([]);
  const [isLoadingHotels, setIsLoadingHotels] = useState(false);
  const [expandedEvidence, setExpandedEvidence] = useState<Record<string, boolean>>({});
  const [expandedSnippets, setExpandedSnippets] = useState<Record<string, boolean>>({});

  const toggleSnippet = (key: string) => {
    setExpandedSnippets(prev => ({ ...prev, [key]: !prev[key] }));
  };

  const { mutate: runCompare, data: compareData, isPending: isComparing } = useCompare();

  const loadComparedHotels = async () => {
    setIsLoadingHotels(true);
    const ids = JSON.parse(localStorage.getItem("compareHotels") || "[]");
    setComparedIds(ids);

    if (ids.length > 0) {
      try {
        const fetched = await Promise.all(
          ids.map(async (id: string) => {
            try {
              const res = await getHotelAnalysis(id);
              return res;
            } catch {
              return { hotel_id: id, name: `Hotel ${id.slice(0,6)}`, trust_score: 0, aspect_scores: {}, positive_themes: [], common_complaints: [], professional_evidence: [] };
            }
          })
        );
        setHotelsData(fetched);
        
        if (ids.length >= 2) {
          runCompare(ids);
        }
      } catch (err) {
        console.error(err);
      }
    } else {
      setHotelsData([]);
    }
    setIsLoadingHotels(false);
  };

  useEffect(() => {
    loadComparedHotels();
  }, []);

  const clearAll = () => {
    localStorage.removeItem("compareHotels");
    loadComparedHotels();
  };

  const getWinnerValue = (aspect: string) => {
    if (hotelsData.length === 0) return null;
    let maxVal = -1;
    let winnerId = "";
    hotelsData.forEach(h => {
      const val = aspect === 'trust_score' ? h.trust_score : (aspect === 'rating' ? h.rating : h.aspect_scores?.[aspect]);
      const checkVal = val || 0;
      if (checkVal > maxVal) {
        maxVal = checkVal;
        winnerId = h.hotel_id;
      }
    });
    return winnerId;
  };

  const toggleEvidence = (id: string) => {
    setExpandedEvidence(prev => ({ ...prev, [id]: !prev[id] }));
  };

  const aspects = [
    { key: "trust_score", label: "Trust Score", isScore: false },
    { key: "rating", label: "Rating", isScore: false },
    { key: "cleanliness", label: "Cleanliness", isScore: true },
    { key: "service", label: "Service", isScore: true },
    { key: "location", label: "Location", isScore: true },
    { key: "value", label: "Value", isScore: true },
  ];

  if (comparedIds.length === 0) {
    return (
      <div className="min-h-screen bg-[#F8FAFC] py-20 px-8 flex items-center justify-center">
        <div className="p-12 text-center bg-white border border-[#E2E8F0] rounded-[20px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] max-w-xl w-full space-y-6">
          <GitCompare className="w-16 h-16 text-slate-300 mx-auto" />
          <h2 className="text-2xl font-bold text-[#0F172A]">No hotels selected</h2>
          <p className="text-[16px] text-[#475569] max-w-sm mx-auto">
            Browse stays or use search to add hotels to your comparison tray.
          </p>
          <div className="pt-4 border-t border-slate-100">
            <Link href="/stays">
              <Button variant="outline" className="h-[48px] px-8 text-[16px] font-bold rounded-[12px] border-[#E2E8F0] text-[#0F172A]">Browse Stays</Button>
            </Link>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="min-h-screen bg-[#F8FAFC] pb-20">
      <div className="max-w-[1440px] mx-auto px-4 md:px-8 pt-10">
        
        {/* SECTION 1: Comparison Header */}
        <div className="flex flex-col md:flex-row justify-between items-start md:items-end gap-6 mb-8">
          <div>
            <h1 className="text-4xl font-bold text-slate-900 leading-tight">
              Compare Hotels
            </h1>
            <p className="text-lg text-slate-600 mt-2">
              Weigh trade-offs based on verified reviews and dynamic aspect scores.
            </p>
          </div>
          <Button variant="outline" onClick={clearAll} className="h-[48px] px-6 text-[16px] font-bold border-transparent bg-transparent text-[#475569] hover:bg-slate-100 hover:text-slate-900 rounded-[12px] cursor-pointer">
            Clear comparison
          </Button>
        </div>

        {/* SECTION 2: Compact Hotel Grid */}
        <div className="grid grid-cols-1 lg:grid-cols-3 gap-[24px] mb-[32px]">
          {hotelsData.map(h => (
            <div key={h.hotel_id} className="bg-white rounded-[20px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] p-[20px] flex flex-col items-center text-center border border-slate-100">
              <img 
                src={h.hero_image || "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80"} 
                alt={h.name} 
                className="w-[96px] h-[96px] object-cover rounded-[16px] mb-3"
              />
              <h3 className="text-[17px] leading-tight font-semibold text-slate-900 mb-1">{h.name}</h3>
              <p className="text-[11px] text-slate-400 font-mono mb-2">ID: {h.hotel_id}</p>
              <div className="flex items-center gap-1.5 text-[13px] text-slate-600 mb-4">
                <MapPin className="w-3.5 h-3.5" /> {h.area || "Area unavailable"}
              </div>
              
              <div className="flex items-center justify-center gap-2 mb-4 w-full">
                <div className="flex items-center gap-1 bg-slate-50 px-2 py-1 rounded-md border border-slate-100">
                  <Star className="w-3.5 h-3.5 fill-amber-500 stroke-amber-500" />
                  <span className="font-bold text-slate-900 text-[13px]">{h.rating?.toFixed(1) || "4.0"}</span>
                </div>
                <span className="text-[12px] text-slate-500 font-medium">{h.reviews_count > 0 ? "Review evidence" : "Reviews"}</span>
              </div>

              <div className="mt-auto w-full pt-3 border-t border-slate-100 flex justify-center">
                <div className="inline-flex items-center gap-1.5 bg-[#F0FDF4] px-3 py-1.5 rounded-full">
                  <ShieldCheck className="w-4 h-4 text-[#166534]" />
                  <span className="text-[13px] font-bold text-[#166534] uppercase tracking-wide">Trust Score {h.trust_score?.toFixed(1) || "N/A"}</span>
                </div>
              </div>
            </div>
          ))}
        </div>

        {/* SECTION 3: Comparison Matrix */}
        <div className="bg-white rounded-[20px] p-[24px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] mb-[32px]">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Comparison Matrix</h2>
          <div className="w-full">
            {aspects.map((aspect, index) => {
              const winnerId = getWinnerValue(aspect.key);
              const isLast = index === aspects.length - 1;
              return (
                <div key={aspect.key} className={`flex flex-col lg:flex-row items-start lg:items-center min-h-[64px] ${!isLast ? 'border-b border-slate-100' : ''} py-3`}>
                  <div className="w-full lg:w-1/4 text-[14px] font-bold text-slate-500 uppercase tracking-wide mb-2 lg:mb-0 shrink-0">
                    {aspect.label}
                  </div>
                  <div className="w-full lg:w-3/4 grid grid-cols-1 lg:grid-cols-3 gap-[24px]">
                    {hotelsData.map(h => {
                      const val = aspect.key === 'trust_score' ? h.trust_score : (aspect.key === 'rating' ? h.rating : h.aspect_scores?.[aspect.key]);
                      const displayVal = val?.toFixed(1) || "N/A";
                      const isHighest = h.hotel_id === winnerId && hotelsData.length > 1;
                      
                      return (
                        <div key={h.hotel_id} className={`flex items-center justify-center gap-1.5 rounded-[10px] h-[44px] px-3 transition-colors ${isHighest ? 'bg-emerald-50 text-emerald-800 font-bold border border-emerald-200' : 'bg-slate-50 text-slate-700 font-semibold'}`}>
                          <span>{displayVal}</span>
                          {isHighest && (
                            <span className="text-[10px] font-black uppercase tracking-wider text-amber-900 bg-amber-100 border border-amber-300 px-1.5 py-0.5 rounded flex items-center gap-0.5">
                              🏆 Top
                            </span>
                          )}
                        </div>
                      );
                    })}
                  </div>
                </div>
              );
            })}
          </div>
        </div>

        {/* SECTION 4: Strengths & Considerations */}
        <div className="mb-[32px]">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Strengths & Considerations</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-[24px]">
            {hotelsData.map(h => (
              <div key={h.hotel_id} className="bg-white rounded-[20px] p-[24px] shadow-[0_1px_3px_rgba(0,0,0,0.08)]">
                <h3 className="text-lg font-bold text-slate-900 mb-6 truncate">{h.name}</h3>
                
                <div className="mb-6">
                  <h4 className="text-[13px] font-bold text-slate-500 uppercase tracking-wide mb-4">Strengths</h4>
                  <ul className="space-y-3">
                    {h.positive_themes?.length > 0 ? h.positive_themes.map((theme: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-[14px] text-slate-700">
                        <CheckCircle2 className="w-4 h-4 text-[#16A34A] shrink-0 mt-0.5" />
                        <span className="capitalize">{theme.replace(/_/g, " ")}</span>
                      </li>
                    )) : (
                      <li className="text-[14px] text-slate-500 italic">No significant strengths identified yet.</li>
                    )}
                  </ul>
                </div>

                <div>
                  <h4 className="text-[13px] font-bold text-slate-500 uppercase tracking-wide mb-4">Considerations</h4>
                  <ul className="space-y-3">
                    {h.common_complaints?.length > 0 ? h.common_complaints.map((complaint: string, i: number) => (
                      <li key={i} className="flex items-start gap-2 text-[14px] text-slate-700">
                        <AlertTriangle className="w-4 h-4 text-[#EA580C] shrink-0 mt-0.5" />
                        <span className="capitalize">{complaint.replace(/_/g, " ")}</span>
                      </li>
                    )) : (
                      <li className="text-[14px] text-slate-500 italic">No significant concerns identified in analyzed reviews.</li>
                    )}
                  </ul>
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* SECTION 5: Verified Evidence */}
        <div className="mb-[40px]">
          <h2 className="text-2xl font-bold text-slate-900 mb-6">Verified Evidence</h2>
          <div className="grid grid-cols-1 lg:grid-cols-3 gap-[24px]">
            {hotelsData.map(h => (
              <div key={h.hotel_id} className="bg-white rounded-[20px] p-[24px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] flex flex-col">
                <h3 className="text-lg font-bold text-slate-900 mb-6 truncate">{h.name}</h3>
                
                <div className="space-y-4 flex-1">
                  {h.professional_evidence?.flatMap((ev: any) => {
                    const parts = (ev.snippet || "").split(/\s*\|\s*/);
                    return parts.map((part: string, idx: number) => ({
                      ...ev,
                      snippet: part,
                      sub_id: idx
                    }));
                  }).filter((ev: any) => {
                    let text = ev.snippet || "";
                    if (text.includes("Snippets: ")) text = text.split("Snippets: ")[1];
                    text = text.trim();
                    return text && text !== "." && text.length >= 20;
                  }).slice(0, 5).map((ev: any, i: number) => {
                    let text = ev.snippet;
                    if (text.includes("Snippets: ")) text = text.split("Snippets: ")[1];
                    text = text.trim();
                    
                    // Parse category & signal
                    const tLower = text.toLowerCase();
                    let category = "General";
                    let signal = "Sentiment signal";
                    
                    if (tLower.includes("clean") || tLower.includes("room") || tLower.includes("dirty") || tLower.includes("housekeeping") || tLower.includes("hygiene")) {
                      category = "Cleanliness";
                      signal = "Cleanliness signal";
                    } else if (tLower.includes("staff") || tLower.includes("service") || tLower.includes("helpful") || tLower.includes("front desk") || tLower.includes("courteous")) {
                      category = "Service";
                      signal = "Service sentiment";
                    } else if (tLower.includes("location") || tLower.includes("near") || tLower.includes("close to") || tLower.includes("convenient") || tLower.includes("airport") || tLower.includes("aerocity")) {
                      category = "Location";
                      signal = "Location convenience";
                    } else if (tLower.includes("value") || tLower.includes("price") || tLower.includes("cheap") || tLower.includes("worth") || tLower.includes("budget") || tLower.includes("expensive")) {
                      category = "Value";
                      signal = "Value indicator";
                    } else if (tLower.includes("family") || tLower.includes("kids") || tLower.includes("children") || tLower.includes("family friendly")) {
                      category = "Family";
                      signal = "Family suitability";
                    }

                    const badgeColors: Record<string, string> = {
                      Cleanliness: "bg-blue-50 text-blue-700 border-blue-100",
                      Service: "bg-green-50 text-green-700 border-green-100",
                      Location: "bg-purple-50 text-purple-700 border-purple-100",
                      Value: "bg-amber-50 text-amber-700 border-amber-100",
                      Family: "bg-rose-50 text-rose-700 border-rose-100",
                      General: "bg-slate-50 text-slate-700 border-slate-100"
                    };

                    const selectedColor = badgeColors[category] || badgeColors.General;

                    return (
                      <div key={i} className="border-b border-slate-100 pb-4 last:border-b-0 last:pb-0">
                        <div className="flex flex-wrap items-center gap-2 mb-2">
                          <span className={`px-2 py-0.5 text-[11px] font-bold uppercase rounded-md border ${selectedColor}`}>
                            {category}
                          </span>
                          <span className="text-[11px] font-semibold text-slate-400">Verified guest review</span>
                        </div>
                        <p className="text-[12px] text-slate-500 font-medium mb-2">Source: Guest review · {signal}</p>
                        <p className="text-[14px] text-slate-600 italic font-medium leading-relaxed border-l-2 border-slate-200 pl-3">
                          "{expandedSnippets[h.hotel_id + "_" + i] ? text : (text.length > 140 ? `${text.slice(0, 140)}...` : text)}"
                          {text.length > 140 && (
                            <button 
                              onClick={() => toggleSnippet(h.hotel_id + "_" + i)}
                              className="ml-1.5 text-[13px] not-italic font-bold text-[#2563EB] hover:text-blue-700 inline-block transition-colors cursor-pointer"
                            >
                              {expandedSnippets[h.hotel_id + "_" + i] ? "Read less" : "Read more"}
                            </button>
                          )}
                        </p>
                        
                        {expandedEvidence[h.hotel_id + i] && ev.chunk_id && (
                          <div className="mt-3 bg-slate-50 p-3 rounded-lg border border-slate-100">
                            <p className="text-[10px] font-mono text-slate-400 break-all">Source: {ev.chunk_id}</p>
                          </div>
                        )}
                        <button 
                          onClick={() => toggleEvidence(h.hotel_id + i)}
                          className="mt-2 text-[12px] font-semibold text-[#2563EB] hover:text-blue-700 flex items-center gap-1 cursor-pointer transition-colors"
                        >
                          {expandedEvidence[h.hotel_id + i] ? (
                            <>Hide verification sources <ChevronUp className="w-3 h-3" /></>
                          ) : (
                            <>View verification sources <ChevronDown className="w-3 h-3" /></>
                          )}
                        </button>
                      </div>
                    );
                  })}
                  
                  {(!h.professional_evidence || h.professional_evidence.filter((e: any) => e.snippet && e.snippet.trim() !== "." && e.snippet.trim().length >= 20).length === 0) && (
                    <p className="text-[14px] text-slate-500 italic">Detailed review evidence available in the full analysis view.</p>
                  )}
                </div>
              </div>
            ))}
          </div>
        </div>

        {/* SECTION 6: AI Trade-Off Analysis */}
        {comparedIds.length >= 2 && (
          <div className="bg-[#072D62] text-white rounded-[24px] p-8 md:p-10 shadow-[0_12px_32px_rgba(15,23,42,0.12)]">
            <div className="max-w-4xl">
              <div className="flex items-center gap-3 mb-2">
                <Bot className="w-6 h-6 text-blue-300" />
                <h2 className="text-2xl font-bold text-white">AI Trade-Off Analysis</h2>
              </div>
              <p className="text-[14px] font-medium text-blue-200/80 mb-8 pb-6 border-b border-blue-800/50">
                Generated from verified review evidence and aspect scores.
              </p>
              
              {isComparing ? (
                <div className="animate-pulse space-y-4">
                  <div className="h-4 bg-blue-800 rounded w-full"></div>
                  <div className="h-4 bg-blue-800 rounded w-5/6"></div>
                  <div className="h-4 bg-blue-800 rounded w-4/6"></div>
                </div>
              ) : compareData ? (
                <div 
                  className="space-y-3 text-[15px] text-slate-200 leading-relaxed font-medium"
                  dangerouslySetInnerHTML={{ __html: formatMarkdown(compareData.grounded_summary, hotelsData) }}
                />
              ) : (
                <p className="text-[16px] text-blue-300 italic">Analysis unavailable.</p>
              )}
            </div>
          </div>
        )}

      </div>
    </div>
  );
}

function formatMarkdown(md: string, hotelsData: any[] = []) {
  if (!md) return "";
  
  // Escape HTML tags to prevent XSS
  let html = md
    .replace(/&/g, "&amp;")
    .replace(/</g, "&lt;")
    .replace(/>/g, "&gt;")
    .replace(/"/g, "&quot;")
    .replace(/'/g, "&#039;");
  
  // Format section headings (### Hotel Name or ### Title)
  html = html.replace(/###\s*(.*?)(?=\n|$)/g, '<h4 class="text-[16px] font-bold text-blue-200 mt-4 mb-2">$1</h4>');
  
  // Format bold text (**bold**)
  html = html.replace(/\*\*(.*?)\*\*/g, '<strong class="text-white font-bold">$1</strong>');
  
  // Convert list items / hyphens to clean break-spaced bullet points
  html = html.replace(/\s+-\s+/g, '<br/>• ');
  html = html.replace(/\n-\s+/g, '<br/>• ');
  
  // Convert newlines to breaks to preserve spacing
  html = html.replace(/\n/g, '<br/>');

  // Format any hotel name on its own line as a header
  if (hotelsData && hotelsData.length > 0) {
    hotelsData.forEach(h => {
      if (!h.name) return;
      const escapedName = h.name.replace(/[-\/\\^$*+?.()|[\]{}]/g, '\\$&');
      // Match name when it stands alone as a paragraph or line
      const regex = new RegExp(`(?:^|<br\\s*\\/?>)\\s*(${escapedName})\\s*(?:$|<br\\s*\\/?>)`, 'gi');
      html = html.replace(regex, (match, p1) => `<h4 class="text-[17px] font-bold text-blue-200 mt-6 mb-2 border-b border-blue-800/30 pb-1">${p1}</h4>`);
    });
  }
  
  return html;
}
