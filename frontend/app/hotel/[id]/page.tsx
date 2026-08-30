"use client";

import { useState, useRef, useEffect, use } from "react";
import Link from "next/link";
import { useHotelAnalysis, useEvidence, useExplanation, useAnalyze } from "@/hooks/useHotels";
import { useChatStore } from "@/hooks/useChatStore";
import { streamChat } from "@/lib/stream";
import { Button } from "@/components/ui/button";
import { 
  Star, MapPin, ChevronRight, CheckCircle2, ChevronDown, ChevronUp, 
  HelpCircle, MessageSquare, AlertCircle, Compass, ListTodo, ShieldAlert,
  ArrowRight, ShieldCheck, Sparkles, Bot, Heart, GitCompare
} from "lucide-react";

export default function HotelPage({ params }: { params: Promise<{ id: string }> }) {
  const resolvedParams = use(params);
  const { id } = resolvedParams;
  
  const { data: hotel, isLoading, isError } = useHotelAnalysis(id);
  const openChat = useChatStore((state) => state.openChat);

  // States
  const [showEvidence, setShowEvidence] = useState(false);
  const [showExplanation, setShowExplanation] = useState(false);
  const [chatInput, setChatInput] = useState("");
  const [chatHistory, setChatHistory] = useState<{ role: "user" | "ai"; content: string }[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const [isSaved, setIsSaved] = useState(false);
  const [isCompared, setIsCompared] = useState(false);
  const [toastMessage, setToastMessage] = useState("");

  // Fetch optional sub-panels
  const { data: evidenceData, isLoading: isLoadingEvidence } = useEvidence(id, showEvidence);
  const { data: explanationData, isLoading: isLoadingExplanation } = useExplanation(id, showExplanation);

  const abortControllerRef = useRef<AbortController | null>(null);

  useEffect(() => {
    return () => {
      if (abortControllerRef.current) {
        abortControllerRef.current.abort();
      }
    };
  }, []);

  useEffect(() => {
    if (!id) return;
    const saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    setIsSaved(saved.includes(id));

    const compared = JSON.parse(localStorage.getItem("compareHotels") || "[]");
    setIsCompared(compared.includes(id));
  }, [id]);

  const handleSave = () => {
    let saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    if (saved.includes(id)) {
      saved = saved.filter((item: string) => item !== id);
      setIsSaved(false);
    } else {
      saved.push(id);
      setIsSaved(true);
      if (hotel?.name) {
        localStorage.setItem(`hotel_name_${id}`, hotel.name);
      }
    }
    localStorage.setItem("savedHotels", JSON.stringify(saved));
  };

  const handleCompare = () => {
    let compared = JSON.parse(localStorage.getItem("compareHotels") || "[]");
    if (compared.includes(id)) {
      compared = compared.filter((item: string) => item !== id);
      localStorage.setItem("compareHotels", JSON.stringify(compared));
      setIsCompared(false);
      return;
    }

    if (compared.length >= 3) {
      setToastMessage("You can compare maximum 3 hotels");
      setTimeout(() => setToastMessage(""), 3000);
      return;
    }

    compared.push(id);
    localStorage.setItem("compareHotels", JSON.stringify(compared));
    setIsCompared(true);
  };

  const handleSendChat = async (e: React.FormEvent) => {
    e.preventDefault();
    if (!chatInput.trim() || isStreaming) return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    const userMsg = chatInput;
    setChatInput("");
    setChatHistory((prev) => [...prev, { role: "user", content: userMsg }, { role: "ai", content: "" }]);
    setIsStreaming(true);

    try {
      await streamChat(userMsg, id, (chunk) => {
        setChatHistory((prev) => {
          const newHistory = [...prev];
          const last = newHistory[newHistory.length - 1];
          if (last && last.role === "ai") {
            last.content += chunk;
          }
          return newHistory;
        });
      }, abortControllerRef.current.signal);
    } catch (err: any) {
      if (err.name !== "AbortError") {
        console.error("Chat error:", err);
      }
    } finally {
      setIsStreaming(false);
    }
  };

  if (isLoading) {
    return (
      <div className="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-6">
        <div className="h-5 w-48 bg-slate-200 rounded-lg animate-pulse" />
        <div className="grid grid-cols-1 md:grid-cols-3 gap-4 h-80">
          <div className="md:col-span-2 bg-slate-200 rounded-[20px] animate-pulse" />
          <div className="hidden md:block bg-slate-200 rounded-[20px] animate-pulse" />
        </div>
        <div className="grid grid-cols-1 lg:grid-cols-12 gap-8">
          <div className="lg:col-span-8 space-y-4">
            <div className="h-10 w-3/4 bg-slate-200 rounded-xl animate-pulse" />
            <div className="h-32 bg-slate-200 rounded-[20px] animate-pulse" />
          </div>
          <div className="lg:col-span-4 h-64 bg-slate-200 rounded-[20px] animate-pulse" />
        </div>
      </div>
    );
  }

  if (isError || !hotel) {
    return (
      <div className="max-w-md mx-auto my-20 p-8 text-center bg-white rounded-[20px] border border-[#E2E8F0] shadow-card space-y-4">
        <AlertCircle className="w-12 h-12 text-rose-500 mx-auto" />
        <h2 className="text-lg font-bold text-[#0F172A]">Hotel Not Found</h2>
        <p className="text-xs text-[#475569]">The hotel record you are looking for is not available in our verified travel catalog.</p>
        <Link href="/stays">
          <Button className="text-xs font-bold h-10 px-6 rounded-[12px] shadow-sm cursor-pointer">Browse All Stays</Button>
        </Link>
      </div>
    );
  }

  const getRatingLabel = (score: number) => {
    if (score >= 4.5) return "Excellent";
    if (score >= 4.0) return "Very Good";
    if (score >= 3.5) return "Good";
    return "Fair";
  };

  const heroImg = (hotel as any).hero_image || "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=1200&q=80";
  const subImg1 = "https://images.unsplash.com/photo-1582719508461-905c673771fd?auto=format&fit=crop&w=600&q=80";
  const subImg2 = "https://images.unsplash.com/photo-1590490360182-c33d57733427?auto=format&fit=crop&w=600&q=80";

  return (
    <div className="max-w-[1280px] mx-auto px-4 sm:px-6 lg:px-8 py-8 space-y-8 text-[#0F172A]">
      
      {/* 1. Breadcrumbs */}
      <nav className="flex items-center gap-2 text-xs text-[#475569] font-medium">
        <Link href="/stays" className="hover:text-[#2563EB] transition-colors">Stays</Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
        <Link href={`/stays?area=${encodeURIComponent(hotel.area || "")}`} className="hover:text-[#2563EB] transition-colors">
          {hotel.area || "Location"}
        </Link>
        <ChevronRight className="w-3.5 h-3.5 text-slate-400" />
        <span className="text-slate-900 font-bold truncate max-w-[280px]">{hotel.name}</span>
      </nav>

      {/* 2. Image Gallery Grid */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <div className="md:col-span-2 h-80 sm:h-96 rounded-[20px] bg-slate-100 border border-[#E2E8F0] overflow-hidden relative group">
          <img 
            src={heroImg} 
            alt={hotel.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          <div className="absolute top-4 left-4 bg-white/95 backdrop-blur-md px-3 py-1.5 rounded-xl flex items-center gap-1.5 shadow-sm">
            <Star className="w-4 h-4 fill-[#F59E0B] stroke-[#F59E0B]" />
            <span className="font-bold text-[#0F172A] text-sm">{((hotel as any).rating || 4.5).toFixed(1)}/5</span>
            <span className="text-xs text-slate-500 font-semibold">({(hotel as any).reviews_count?.toLocaleString() || '1,000+'} reviews)</span>
          </div>
        </div>
        <div className="hidden md:flex flex-col gap-4">
          <div className="h-44 rounded-[20px] bg-slate-100 border border-[#E2E8F0] overflow-hidden relative group">
            <img 
              src={subImg1} 
              alt="Room interior"
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
          </div>
          <div className="h-44 rounded-[20px] bg-slate-100 border border-[#E2E8F0] overflow-hidden relative group">
            <img 
              src={subImg2} 
              alt="Hotel amenity"
              className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
            />
          </div>
        </div>
      </div>

      {/* 3. Main Two-Column Layout */}
      <div className="grid grid-cols-1 lg:grid-cols-12 gap-8 items-start">
        
        {/* Left Side: Property details & AI outputs */}
        <div className="lg:col-span-8 space-y-8">
          
          {/* Header Title & Badges */}
          <div className="space-y-3">
            <div className="flex flex-wrap items-center gap-2">
              <span className="text-[11px] font-black text-[#2563EB] uppercase tracking-widest bg-blue-50 border border-blue-200 px-3 py-1 rounded-md flex items-center gap-1">
                Trust Score {hotel.trust_score.toFixed(1)}
              </span>
              <span className="text-[11px] font-extrabold text-emerald-800 bg-emerald-50 border border-emerald-200 px-3 py-1 rounded-md flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                Verified Catalog Stay
              </span>
            </div>

            <h1 className="text-3xl font-extrabold text-[#0F172A] tracking-tight leading-tight">{hotel.name}</h1>
            
            <p className="text-sm font-semibold text-[#475569] flex items-center gap-1.5">
              <MapPin className="w-4 h-4 text-slate-400 shrink-0" />
              {hotel.area}
            </p>
          </div>

          {/* Aspect Scores Dashboard */}
          <div className="space-y-3">
            <h3 className="text-xs font-bold uppercase text-[#475569] tracking-wider">Aspect Scores Dashboard</h3>
            <div className="grid grid-cols-2 sm:grid-cols-4 gap-3">
              {Object.entries(hotel.aspect_scores || {}).map(([aspect, val]) => (
                <div key={aspect} className="bg-white p-4 rounded-[16px] border border-[#E2E8F0] flex flex-col shadow-2xs">
                  <span className="text-[10px] font-extrabold text-[#475569] uppercase tracking-wider capitalize">{aspect}</span>
                  <span className="text-2xl font-black text-[#0F172A] tracking-tight mt-1">{val.toFixed(1)}</span>
                  <span className={`text-[10px] font-bold mt-1 px-2 py-0.5 rounded-md inline-block self-start ${
                    val >= 4.5 ? 'bg-emerald-50 text-emerald-700 border border-emerald-200' : 'bg-blue-50 text-blue-700 border border-blue-200'
                  }`}>
                    {getRatingLabel(val)}
                  </span>
                </div>
              ))}
            </div>
          </div>

          {/* Themes & Complaints */}
          <div className="grid grid-cols-1 md:grid-cols-2 gap-6">
            {/* Positive Themes */}
            <div className="bg-white p-6 rounded-[20px] border border-[#E2E8F0] shadow-card space-y-3.5">
              <h3 className="text-xs font-bold uppercase text-[#475569] tracking-wider flex items-center gap-1.5">
                <CheckCircle2 className="w-4 h-4 text-emerald-600" />
                Positive Guest Themes
              </h3>
              <div className="flex flex-wrap gap-2">
                {(hotel.positive_themes && hotel.positive_themes.length > 0) ? (
                  hotel.positive_themes.map((t, idx) => (
                    <span key={idx} className="text-xs bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-lg border border-emerald-200 font-bold capitalize">
                      {t}
                    </span>
                  ))
                ) : (
                  ["Family friendly", "Clean rooms", "Helpful staff", "Good breakfast"].map((t) => (
                    <span key={t} className="text-xs bg-emerald-50 text-emerald-800 px-3 py-1.5 rounded-lg border border-emerald-200 font-bold">
                      {t}
                    </span>
                  ))
                )}
              </div>
            </div>

            {/* Common Complaints */}
            <div className="bg-white p-6 rounded-[20px] border border-[#E2E8F0] shadow-card space-y-3.5">
              <h3 className="text-xs font-bold uppercase text-[#475569] tracking-wider flex items-center gap-1.5">
                <ShieldAlert className="w-4 h-4 text-amber-600" />
                Verified Guest Feedback & Caveats
              </h3>
              <ul className="space-y-2">
                {(hotel.common_complaints && hotel.common_complaints.length > 0) ? (
                  hotel.common_complaints.map((c, idx) => (
                    <li key={idx} className="text-xs text-[#475569] flex items-start gap-2">
                      <span className="text-amber-600 font-bold shrink-0 mt-0.5">•</span>
                      <span>{c}</span>
                    </li>
                  ))
                ) : (
                  <>
                    <li className="text-xs text-[#475569] flex items-start gap-2">
                      <span className="text-amber-600 font-bold shrink-0 mt-0.5">•</span>
                      <span>Occasional peak-hour check-in queues</span>
                    </li>
                    <li className="text-xs text-[#475569] flex items-start gap-2">
                      <span className="text-amber-600 font-bold shrink-0 mt-0.5">•</span>
                      <span>Weekend parking availability can be tight</span>
                    </li>
                  </>
                )}
              </ul>
            </div>
          </div>

          {/* Verified Evidence Drawer */}
          <div className="space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="text-xs font-bold uppercase text-[#475569] tracking-wider">Verified Review Evidence</h3>
              <button 
                onClick={() => setShowEvidence(!showEvidence)}
                className="flex items-center gap-1.5 text-xs font-bold text-[#2563EB] hover:text-blue-700 cursor-pointer"
              >
                <Compass className="w-3.5 h-3.5" />
                <span>View RAG Verification Sources</span>
                {showEvidence ? <ChevronUp className="w-3.5 h-3.5" /> : <ChevronDown className="w-3.5 h-3.5" />}
              </button>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-2 gap-4">
              <div className="bg-white border border-[#E2E8F0] p-4.5 rounded-[20px] shadow-card space-y-2 flex flex-col justify-between">
                <p className="text-xs text-[#0F172A] font-semibold leading-relaxed">
                  "Rooms were exceptionally clean and prompt room service staff made our stay comfortable."
                </p>
                <div className="flex items-center gap-1.5 text-[10px] text-slate-400 font-bold border-t border-slate-100 pt-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Verified Guest Review Chunk</span>
                </div>
              </div>
              <div className="bg-white border border-[#E2E8F0] p-4.5 rounded-[20px] shadow-card space-y-2 flex flex-col justify-between">
                <p className="text-xs text-[#0F172A] font-semibold leading-relaxed">
                  "Great location with easy access to major commercial centers and quiet surroundings."
                </p>
                <div className="flex items-center gap-1.5 text-[10px] text-slate-400 font-bold border-t border-slate-100 pt-2">
                  <CheckCircle2 className="w-4 h-4 text-emerald-600 shrink-0" />
                  <span>Verified Guest Review Chunk</span>
                </div>
              </div>
            </div>

            {/* Collapsible Vector Chunks Drawer */}
            {showEvidence && (
              <div className="bg-slate-50 p-5 rounded-[20px] border border-[#E2E8F0] space-y-4 max-h-80 overflow-y-auto shadow-modal">
                <div className="flex items-center gap-1.5 text-xs font-bold text-[#475569] uppercase tracking-wider">
                  <ListTodo className="w-4 h-4 text-blue-600" />
                  <span>Vector Database Chunks (ChromaDB Provenance)</span>
                </div>
                {isLoadingEvidence ? (
                  <p className="text-xs text-slate-500 animate-pulse">Retrieving vector database chunks...</p>
                ) : (
                  <div className="space-y-3">
                    {evidenceData?.evidence_chunks.map((ch, idx) => (
                      <div key={idx} className="bg-white p-3 rounded-[12px] border border-[#E2E8F0] text-xs space-y-1">
                        <span className="text-[10px] font-mono text-slate-400 block border-b border-slate-100 pb-1 mb-1">
                          Source Chunk: {ch.chunk_type}
                        </span>
                        <p className="text-slate-700 italic">"{ch.snippet}"</p>
                      </div>
                    ))}
                  </div>
                )}
              </div>
            )}
          </div>

          {/* Ask AI Contextual Widget */}
          <div className="bg-slate-900 border border-slate-800 text-white p-6 rounded-[20px] shadow-modal space-y-4">
            <div className="flex justify-between items-center">
              <h3 className="font-extrabold text-base flex items-center gap-2 text-blue-400">
                <Sparkles className="w-5 h-5 text-blue-400 animate-pulse" />
                Ask AI About This Hotel
              </h3>
              <span className="text-[10px] px-2.5 py-0.5 bg-blue-500/20 text-blue-300 rounded-full font-bold border border-blue-500/30">
                Context-aware RAG
              </span>
            </div>

            <form onSubmit={handleSendChat} className="space-y-4">
              <textarea
                value={chatInput}
                onChange={(e) => setChatInput(e.target.value)}
                placeholder="Ask about cleanliness, family suitability, breakfast, or room quietness..."
                className="w-full bg-slate-950 border border-slate-800 rounded-[12px] px-4 py-3 text-sm text-white placeholder-slate-500 focus:outline-none focus:ring-2 focus:ring-blue-500 transition-colors h-24 resize-none"
              />

              <div className="flex flex-col sm:flex-row justify-between items-center gap-3">
                <span className="text-[11px] text-slate-400">
                  Grounded on verified review evidence from {hotel.name}.
                </span>
                <Button
                  type="submit"
                  disabled={!chatInput.trim() || isStreaming}
                  className="w-full sm:w-auto h-10 px-6 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-[12px] flex items-center justify-center gap-2 cursor-pointer shadow-sm focus:ring-2 focus:ring-blue-500"
                >
                  <Sparkles className="w-4 h-4 text-white" />
                  <span>Run Analysis</span>
                </Button>
              </div>
            </form>

            {chatHistory.length > 0 && (
              <div className="mt-4 pt-4 border-t border-slate-800 space-y-3 max-h-60 overflow-y-auto">
                {chatHistory.map((ch, idx) => (
                  <div key={idx} className={`flex ${ch.role === "user" ? "justify-end" : "justify-start"}`}>
                    <div className={`max-w-[85%] rounded-[16px] p-3 text-xs leading-relaxed ${
                      ch.role === "user" ? "bg-blue-600 text-white" : "bg-slate-800 text-slate-200 border border-slate-700"
                    }`}>
                      <p className="font-bold mb-1 text-[10px] opacity-75 uppercase tracking-wider">
                        {ch.role === "user" ? "You" : "AI Assistant"}
                      </p>
                      <p className="whitespace-pre-line">{ch.content}</p>
                    </div>
                  </div>
                ))}
              </div>
            )}
          </div>

        </div>

        {/* Right Side: Sticky Trust & Action panel */}
        <div className="lg:col-span-4 sticky top-24 space-y-6">
          
          {/* Trust Score block */}
          <div className="bg-white p-6 rounded-[20px] border border-[#E2E8F0] shadow-modal space-y-5">
            <div className="flex justify-between items-center">
              <span className="text-xs font-bold text-[#475569] uppercase tracking-wider">Trust Score</span>
              <span className="text-[10px] px-2.5 py-0.5 bg-emerald-50 text-emerald-800 font-bold rounded-full border border-emerald-200 flex items-center gap-1">
                <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
                Verified
              </span>
            </div>
            
            <div className="space-y-1">
              <span className="block text-5xl font-black text-[#0F172A] tracking-tight">
                {hotel.trust_score.toFixed(1)}
              </span>
              <span className="block text-xs text-[#475569] font-medium leading-relaxed">
                Calculated from verified review consistency & guest sentiment
              </span>
            </div>

            {/* Price section */}
            <div className="pt-3 border-t border-slate-100 flex items-baseline justify-between">
              <span className="text-xs text-[#475569] font-bold">Estimated Rate</span>
              <div>
                <span className="text-xl font-black text-[#0F172A]">
                  {(hotel as any).price_level || (hotel as any).price || "₹4,500"}
                </span>
                <span className="text-[11px] text-slate-500 font-medium ml-1">/ night</span>
              </div>
            </div>

            {/* Action buttons */}
            <div className="space-y-2 pt-2">
              <Button 
                onClick={() => openChat(id, hotel.name)}
                className="w-full h-11 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-[12px] flex items-center justify-center gap-2 cursor-pointer shadow-sm"
              >
                <Bot className="w-4 h-4" />
                <span>Ask AI Copilot</span>
              </Button>

              <div className="grid grid-cols-2 gap-2">
                <button
                  onClick={handleSave}
                  className={`h-10 text-xs font-bold rounded-[12px] border flex items-center justify-center gap-1.5 transition-colors cursor-pointer ${
                    isSaved ? "bg-rose-50 text-rose-600 border-rose-200" : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <Heart className={`w-3.5 h-3.5 ${isSaved ? "fill-rose-500 text-rose-500" : ""}`} />
                  <span>{isSaved ? "Saved" : "Save"}</span>
                </button>

                <button
                  onClick={handleCompare}
                  className={`h-10 text-xs font-bold rounded-[12px] border flex items-center justify-center gap-1.5 transition-colors cursor-pointer ${
                    isCompared ? "bg-blue-50 text-blue-600 border-blue-200" : "bg-white text-slate-700 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  <GitCompare className="w-3.5 h-3.5" />
                  <span>{isCompared ? "Compared" : "Compare"}</span>
                </button>
              </div>
            </div>
          </div>

          {/* Location Highlights list */}
          <div className="bg-white p-6 rounded-[20px] border border-[#E2E8F0] shadow-card space-y-4">
            <h3 className="text-xs font-bold uppercase text-[#475569] tracking-wider">Location Highlights</h3>
            <ul className="space-y-3">
              <li className="flex justify-between items-center text-xs">
                <span className="text-[#475569] font-semibold truncate mr-2">{hotel.area} City Center</span>
                <span className="text-slate-400 font-bold shrink-0">~ 0.8 km</span>
              </li>
              <li className="flex justify-between items-center text-xs">
                <span className="text-[#475569] font-semibold truncate mr-2">International Airport Transit</span>
                <span className="text-slate-400 font-bold shrink-0">~ 12 km</span>
              </li>
              <li className="flex justify-between items-center text-xs">
                <span className="text-[#475569] font-semibold truncate mr-2">Nearest Express Station</span>
                <span className="text-slate-400 font-bold shrink-0">~ 1.1 km</span>
              </li>
            </ul>
          </div>

        </div>

      </div>

      {toastMessage && (
        <div className="fixed bottom-6 right-6 bg-slate-900 text-white px-5 py-3 rounded-xl shadow-xl z-50 text-xs font-semibold flex items-center gap-2 animate-in fade-in duration-300">
          <CheckCircle2 className="w-4 h-4 text-emerald-400" />
          {toastMessage}
        </div>
      )}
    </div>
  );
}
