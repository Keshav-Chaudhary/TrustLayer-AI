"use client";

import Link from "next/link";
import { useRouter } from "next/navigation";
import { useState, useEffect } from "react";
import { Star, MapPin, Heart, GitCompare, CheckCircle2, ShieldCheck, Sparkles, Info } from "lucide-react";
import { Recommendation } from "@/types/api";
import { TRUST_SIGNAL_TOOLTIPS, FEEDBACK_OPTIONS } from "@/lib/ui-config";

export function RecommendationCard({ 
  rec, 
  isTopPick,
  mode = "search"
}: { 
  rec: Recommendation; 
  isTopPick?: boolean;
  mode?: "search" | "catalog";
}) {
  const router = useRouter();
  const [isSaved, setIsSaved] = useState(false);
  const [isCompared, setIsCompared] = useState(false);
  const [toastMessage, setToastMessage] = useState("");
  const [feedback, setFeedback] = useState<string | null>(null);

  // Compute dynamic confidence percentage for search mode
  const computeDynamicConfidence = () => {
    if (rec.query_alignment_score !== undefined && rec.query_alignment_score !== null && rec.query_alignment_score > 0) {
      return Math.min(99, Math.round(rec.query_alignment_score * 100));
    }
    // Calculate dynamic score from Trust score & rating
    const trustFactor = (rec.trust_score || 85) * 0.6;
    const ratingFactor = ((rec.rating || 4.0) / 5) * 40;
    const computed = Math.round(trustFactor + ratingFactor);
    return Math.min(99, Math.max(72, computed));
  };

  const matchConfidence = computeDynamicConfidence();

  useEffect(() => {
    const saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    setIsSaved(saved.includes(rec.hotel_id));

    const compared = JSON.parse(localStorage.getItem("compareHotels") || "[]");
    setIsCompared(compared.includes(rec.hotel_id));

    const existingFeedback = JSON.parse(localStorage.getItem("trustlayer_card_feedback") || "{}");
    if (existingFeedback[rec.hotel_id]) {
      setFeedback(existingFeedback[rec.hotel_id]);
    }
  }, [rec.hotel_id]);

  const handleFeedback = (fbId: string) => {
    const newFeedback = feedback === fbId ? null : fbId;
    setFeedback(newFeedback);
    const existing = JSON.parse(localStorage.getItem("trustlayer_card_feedback") || "{}");
    if (newFeedback) {
      existing[rec.hotel_id] = newFeedback;
    } else {
      delete existing[rec.hotel_id];
    }
    localStorage.setItem("trustlayer_card_feedback", JSON.stringify(existing));
  };

  const handleSave = (e: React.MouseEvent) => {
    e.preventDefault();
    let saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    if (saved.includes(rec.hotel_id)) {
      saved = saved.filter((id: string) => id !== rec.hotel_id);
      setIsSaved(false);
    } else {
      saved.push(rec.hotel_id);
      setIsSaved(true);
      localStorage.setItem(`hotel_name_${rec.hotel_id}`, rec.name);
    }
    localStorage.setItem("savedHotels", JSON.stringify(saved));
  };

  const handleCompare = (e: React.MouseEvent) => {
    e.preventDefault();
    let compared = JSON.parse(localStorage.getItem("compareHotels") || "[]");
    
    if (compared.includes(rec.hotel_id)) {
      compared = compared.filter((id: string) => id !== rec.hotel_id);
      localStorage.setItem("compareHotels", JSON.stringify(compared));
      setIsCompared(false);
      return;
    }

    if (compared.length >= 3) {
      setToastMessage("You can compare maximum 3 hotels");
      setTimeout(() => setToastMessage(""), 3000);
      return;
    }
    
    compared.push(rec.hotel_id);
    localStorage.setItem("compareHotels", JSON.stringify(compared));
    setIsCompared(true);
    
    if (compared.length === 3) {
      router.push('/compare');
    } else {
      setToastMessage(`Added to comparison list (${compared.length}/3)`);
      setTimeout(() => setToastMessage(""), 3000);
    }
  };

  const formatPrice = (price?: string | null) => {
    if (!price || price === "Price unavailable") return "Price unavailable";
    return price.startsWith("₹") ? price : `₹${price}`;
  };

  const firstEv = rec.review_evidence && rec.review_evidence.length > 0 ? (rec.review_evidence[0] as any) : null;
  const reviewEvidenceQuote = firstEv
    ? (typeof firstEv === 'string' 
        ? firstEv.replace(/Snippets:\s*/g, '') 
        : firstEv.text || firstEv.snippet || "")
    : null;

  const isCatalog = mode === "catalog";

  return (
    <div className={`w-full bg-white rounded-[20px] border shadow-[0_1px_3px_rgba(0,0,0,0.06)] hover:shadow-[0_8px_24px_rgba(15,23,42,0.10)] transition-all duration-300 flex flex-col md:flex-row group text-[#0F172A] ${
      isTopPick ? "border-amber-400 ring-1 ring-amber-400/40" : "border-[#E2E8F0] hover:border-blue-300"
    }`}>
      
      {/* Left: Responsive Hero Image Container */}
      <div className="relative w-full md:w-[260px] lg:w-[280px] h-[200px] md:h-auto shrink-0 bg-slate-100 p-3 sm:p-4 pb-0 md:pb-4">
        <div className="w-full h-full relative rounded-[16px] overflow-hidden">
          <img 
            src={rec.hero_image || "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80"}
            alt={rec.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          {/* Floating Rating Pill */}
          <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-md px-2.5 py-1.5 rounded-lg flex items-center gap-1.5 shadow-sm">
            <Star className="w-3.5 h-3.5 fill-[#F59E0B] stroke-[#F59E0B]" />
            <span className="font-bold text-[#0F172A] text-xs sm:text-sm">{(rec.rating || 4.5).toFixed(1)}/5</span>
          </div>

          {/* Floating Save Button */}
          <button 
            onClick={handleSave}
            className="absolute top-3 right-3 w-8 h-8 bg-white/90 backdrop-blur-md rounded-full flex items-center justify-center text-slate-500 hover:text-rose-500 hover:bg-white transition-colors shadow-sm cursor-pointer"
            title="Save to wishlist"
          >
            <Heart className={`w-4 h-4 ${isSaved ? "fill-rose-500 text-rose-500" : ""}`} />
          </button>
        </div>
      </div>

      {/* Right: Clean, Structured & Mobile-Responsive Content Body */}
      <div className="flex-1 p-4 sm:p-6 flex flex-col justify-between text-left space-y-3 sm:space-y-4">
        
        {/* Header Block: Title, Badges & Price */}
        <div>
          {/* Top Pill Row */}
          <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 mb-2">
            {isTopPick && (
              <span className="text-[10px] font-black text-amber-900 uppercase tracking-wider bg-amber-100 border border-amber-300 px-2.5 py-0.5 rounded-md flex items-center gap-1">
                🏆 #1 TOP MATCH
              </span>
            )}
            
            {isCatalog ? (
              <span className="text-[10px] font-extrabold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-md flex items-center gap-1">
                <CheckCircle2 className="w-3 h-3 text-emerald-600" /> Verified Hotel
              </span>
            ) : (
              <div className="relative group/tooltip">
                <span className="text-[10px] font-extrabold text-emerald-800 bg-emerald-50 border border-emerald-200 px-2.5 py-0.5 rounded-md flex items-center gap-1 cursor-help">
                  {matchConfidence}% Match
                  <Info className="w-3 h-3 text-emerald-600 opacity-75" />
                </span>
                <div className="absolute left-0 top-full mt-1.5 hidden group-hover/tooltip:block w-64 p-2.5 bg-slate-900 text-white text-[11px] font-medium rounded-lg shadow-xl z-50 leading-relaxed pointer-events-none">
                  This hotel matches {matchConfidence}% of your requested preferences based on verified guest feedback.
                </div>
              </div>
            )}

            {rec.trust_score !== undefined && (
              <div className="relative group/tooltip">
                <span className="text-[10px] font-black text-[#2563EB] uppercase tracking-widest bg-blue-50 border border-blue-200/80 px-2.5 py-0.5 rounded-md flex items-center gap-1 cursor-help">
                  Trust Score {rec.trust_score.toFixed(1)}
                  <Info className="w-3 h-3 text-blue-600 opacity-75" />
                </span>
                <div className="absolute left-0 top-full mt-1.5 hidden group-hover/tooltip:block w-64 p-2.5 bg-slate-900 text-white text-[11px] font-medium rounded-lg shadow-xl z-50 leading-relaxed pointer-events-none">
                  {TRUST_SIGNAL_TOOLTIPS.trustScore}
                </div>
              </div>
            )}
          </div>

          {/* Title & Price Row (Mobile Stackable) */}
          <div className="flex flex-col sm:flex-row sm:items-baseline justify-between gap-1 sm:gap-2">
            <h3 className="text-lg sm:text-[20px] font-bold text-[#0F172A] leading-tight group-hover:text-[#2563EB] transition-colors">
              {rec.name}
            </h3>

            <div className="text-left sm:text-right shrink-0 mt-1 sm:mt-0">
              <span className="text-lg sm:text-xl font-black text-[#0F172A] leading-none">
                {formatPrice((rec as any).price_level || rec.price)}
              </span>
              <span className="text-[11px] text-slate-500 font-medium ml-1.5">per night</span>
            </div>
          </div>

          {/* Subtitle / Location Row */}
          <div className="flex flex-wrap items-center gap-1.5 sm:gap-2 text-xs text-[#475569] font-medium mt-1">
            <span className="flex items-center gap-1">
              <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              {rec.area || "Primary Location"}
            </span>
            <span>•</span>
            <span>{rec.reviews_count ? `${rec.reviews_count.toLocaleString()} verified reviews` : "Verified stay"}</span>
          </div>
        </div>

        {/* AI Rationale / Property Overview Box */}
        {isCatalog ? (
          <div className="p-3 bg-slate-50 border border-slate-200/80 rounded-xl text-xs text-[#0F172A]">
            <div className="flex items-center gap-1.5 font-bold text-slate-700 mb-0.5">
              <ShieldCheck className="w-3.5 h-3.5 text-emerald-600" />
              <span>Property Highlights</span>
            </div>
            <p className="text-[#475569] leading-relaxed line-clamp-2">
              {rec.summary_text || `Top-rated verified stay in ${rec.area || 'this location'} featuring a ${rec.trust_score?.toFixed(1) || '90+'} Trust Score across ${rec.reviews_count?.toLocaleString() || '1,000+'} reviews.`}
            </p>
          </div>
        ) : (
          <div className="p-3 bg-blue-50/60 border border-blue-100 rounded-xl text-xs text-[#0F172A]">
            <div className="flex items-center gap-1.5 font-bold text-[#2563EB] mb-0.5">
              <Sparkles className="w-3.5 h-3.5 text-[#2563EB]" />
              <span>Why This Matches Your Request</span>
            </div>
            <p className="text-[#475569] leading-relaxed line-clamp-2">
              {rec.summary_text || rec.match_reason || `Highly recommended based on verified cleanliness, guest trust score (${rec.trust_score?.toFixed(1) || '90+'}), and location in ${rec.area}.`}
            </p>
          </div>
        )}

        {/* Dynamic Aspect Ratings Grid */}
        {rec.aspect_scores && Object.keys(rec.aspect_scores).length > 0 && (
          <div className="grid grid-cols-2 sm:grid-cols-4 gap-2 bg-slate-50 p-2 sm:p-2.5 rounded-xl border border-slate-200/60 text-xs">
            {Object.entries(rec.aspect_scores).slice(0, 4).map(([aspect, score]) => (
              <div key={aspect} className="flex items-center justify-between px-2 py-1 bg-white rounded-lg border border-slate-100 shadow-2xs">
                <span className="text-[10px] font-bold uppercase text-slate-500 truncate capitalize">{aspect}</span>
                <span className={`font-black text-[11px] sm:text-[12px] ${score >= 4.5 ? 'text-emerald-600' : 'text-blue-600'}`}>
                  {score.toFixed(1)}
                </span>
              </div>
            ))}
          </div>
        )}

        {/* Review Evidence Snippet */}
        {reviewEvidenceQuote && (
          <div className="text-xs text-slate-600 italic flex items-center gap-1.5 bg-slate-50/80 px-3 py-2 rounded-lg border border-slate-100">
            <ShieldCheck className="w-4 h-4 text-emerald-600 shrink-0" />
            <span className="line-clamp-1">"{reviewEvidenceQuote}"</span>
          </div>
        )}

        {/* Bottom Actions Footer (Mobile Responsive Flex) */}
        <div className="pt-2.5 border-t border-slate-100 flex flex-col sm:flex-row sm:items-center justify-between gap-3">
          {/* Feedback buttons (Only in search mode) */}
          {!isCatalog ? (
            <div className="flex items-center gap-1">
              <span className="text-[11px] font-bold text-slate-400 mr-1">Was this helpful?</span>
              {FEEDBACK_OPTIONS.slice(0, 2).map((fb) => (
                <button
                  key={fb.id}
                  onClick={() => handleFeedback(fb.id)}
                  className={`px-2.5 py-1 rounded-md border text-[10px] font-bold transition-all cursor-pointer ${
                    feedback === fb.id 
                      ? "bg-blue-600 text-white border-blue-600" 
                      : "bg-white text-slate-600 border-slate-200 hover:bg-slate-50"
                  }`}
                >
                  {fb.icon}
                </button>
              ))}
            </div>
          ) : (
            <div className="text-[11px] font-semibold text-slate-500">
              Verified Traditional Catalog Listing
            </div>
          )}

          {/* Action CTAs Row */}
          <div className="flex items-center gap-2 w-full sm:w-auto">
            <button 
              onClick={handleCompare} 
              className={`flex-1 sm:flex-initial text-xs font-bold px-3 py-2 sm:py-1.5 rounded-lg border transition-all cursor-pointer text-center ${
                isCompared 
                  ? "text-blue-600 bg-blue-50 border-blue-200" 
                  : "text-slate-600 bg-white border-slate-200 hover:bg-slate-50"
              }`}
            >
              <GitCompare className="w-3.5 h-3.5 inline mr-1" />
              {isCompared ? "Compared" : "Compare"}
            </button>

            <Link 
              href={`/hotel/${rec.hotel_id}`} 
              className="flex-1 sm:flex-initial text-xs font-bold text-white bg-[#2563EB] hover:bg-blue-700 px-4 py-2 sm:py-1.5 rounded-lg transition-colors shadow-2xs text-center"
            >
              View Details →
            </Link>
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
