"use client";

import { Suspense, useEffect, useState } from "react";
import { useSearchParams } from "next/navigation";
import { useRecommendations } from "@/hooks/useHotels";
import { RecommendationCard } from "@/components/RecommendationCard";
import { HotelCardSkeleton } from "@/components/HotelCardSkeleton";
import { Button } from "@/components/ui/button";
import { Compass, X, Sparkles } from "lucide-react";
import Link from "next/link";
import { detectQueryIntent } from "@/lib/intent";
import { useHotelsCatalog } from "@/hooks/useHotels";
import { HotelGridCard } from "@/components/stays/HotelGridCard";
import { useSearchFilters } from "@/lib/search-state";
import { SearchHeader } from "@/components/stays/SearchHeader";
import { FilterSidebar } from "@/components/stays/FilterSidebar";

function SearchContent() {
  const searchParams = useSearchParams();
  const query = searchParams.get("q") || "";
  
  const { 
    budget, 
    purpose, 
    cleanliness, 
    sortBy,
    setFilter,
    removeFilter, 
    clearAllFilters 
  } = useSearchFilters();
  
  const { mutate, data, isPending, isError } = useRecommendations();
  const [queryIntentLabel, setQueryIntentLabel] = useState("");
  const parsedArea = data?.metadata?.target_area || "";

  const { data: catalogData } = useHotelsCatalog(
    { area: parsedArea, limit: 12, page: 1 },
    !!parsedArea
  );

  useEffect(() => {
    async function checkIntent() {
      if (query) {
        const intent = await detectQueryIntent(query);
        if (intent.type === "ai") {
          setQueryIntentLabel(`Finding "${query}" (AI Recommendation Search)`);
        } else {
          setQueryIntentLabel(`Browsing hotels in "${intent.area || query}" (Catalog Search)`);
        }
      } else {
        setQueryIntentLabel("");
      }
    }
    checkIntent();
  }, [query]);

  useEffect(() => {
    if (query) {
      mutate(query);
    }
  }, [query, mutate]);

  useEffect(() => {
    if (data?.metadata) {
      console.log("TrustLayer-AI Retrieval Telemetry:", {
        total_ms: data.metadata.latency_ms,
        retrieval_ms: data.metadata.retrieval_ms,
        compression_ms: data.metadata.compression_ms,
        llm_ms: data.metadata.llm_ms,
        cache_hit: data.metadata.cache_hit
      });
    }
  }, [data]);

  // Filter recommendations client side
  const recommendations = data?.recommendations?.filter(rec => {
    if (cleanliness) {
      const clean = rec.aspect_scores?.cleanliness || 4.0;
      if (clean < Number(cleanliness)) return false;
    }
    if (budget && rec.price) {
      const priceNum = Number(rec.price.replace(/[^0-9]/g, ""));
      if (budget === "budget" && priceNum > 1500) return false;
      if (budget === "mid-range" && (priceNum < 1500 || priceNum > 4500)) return false;
      if (budget === "luxury" && priceNum < 4500) return false;
    }
    return true;
  }) || [];

  // Sort recommendations based on selected sortBy option
  const sortedRecommendations = [...recommendations].sort((a: any, b: any) => {
    if (sortBy === "rating_desc") {
      return (b.rating || 0) - (a.rating || 0);
    }
    if (sortBy === "cleanliness_desc") {
      const cleanA = a.aspect_scores?.cleanliness || 0;
      const cleanB = b.aspect_scores?.cleanliness || 0;
      return cleanB - cleanA;
    }
    if (sortBy === "reviews_count_desc") {
      return (b.reviews_count || 0) - (a.reviews_count || 0);
    }
    // Default: trust_score_desc
    return (b.trust_score || 0) - (a.trust_score || 0);
  });

  const shownHotelIds = new Set<string>();
  recommendations.forEach((rec: any) => shownHotelIds.add(rec.hotel_id));
  if (data?.catalog_suggestions) {
    data.catalog_suggestions.forEach((sug: any) => shownHotelIds.add(sug.hotel_id));
  }

  const deduplicatedCatalog = catalogData?.hotels?.filter(
    (hotel: any) => !shownHotelIds.has(hotel.hotel_id)
  ) || [];

  const hasActiveFilters = !!(budget || purpose || cleanliness);

  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans overflow-x-hidden">
      
      {/* Search Header Container */}
      <div className="w-full bg-[#F8FAFC] pt-8 px-4 sm:px-6 lg:px-8 max-w-[1440px] mx-auto">
        <SearchHeader />
      </div>

      <div className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 pb-24 flex flex-col lg:flex-row gap-8">
        
        <aside className="w-full lg:w-[320px] shrink-0">
          <FilterSidebar availableAreas={Array.from(new Set(recommendations.map((r: any) => r.area))).filter(Boolean)} />
        </aside>

        {/* Right Results Area */}
        <main className="flex-1 min-w-0 flex flex-col">
          
          {/* Header Section */}
          <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6 text-left">
            <div>
              <div className="flex items-center gap-2 text-xs font-bold text-[#2563EB] uppercase tracking-widest mb-1">
                <Sparkles className="w-3.5 h-3.5 text-[#2563EB]" />
                <span>AI Travel Recommendations</span>
              </div>
              <div className="flex items-center gap-2.5">
                <h1 className="text-[26px] font-extrabold text-[#0F172A] tracking-tight">
                  Recommended Hotels
                </h1>
                {isPending && (
                  <span className="text-[11px] font-extrabold text-[#2563EB] bg-[#2563EB]/10 border border-[#2563EB]/20 px-2.5 py-0.5 rounded-md animate-pulse shrink-0">
                    Updating...
                  </span>
                )}
              </div>
              <p className="text-[#475569] font-medium text-sm mt-1">
                Showing {sortedRecommendations.length} AI-selected recommendations based on your search.
              </p>

              {/* Compact Consumer Badges */}
              <div className="flex flex-wrap items-center gap-2.5 mt-3">
                <span className="px-3 py-1 bg-white border border-slate-200 text-slate-900 rounded-full text-xs font-bold shadow-2xs flex items-center gap-1.5">
                  📍 {parsedArea || "All Destinations"}
                </span>
                <span className="px-3 py-1 bg-white border border-slate-200 text-slate-900 rounded-full text-xs font-bold shadow-2xs flex items-center gap-1.5">
                  👨‍👩‍👧 {purpose ? (purpose.charAt(0).toUpperCase() + purpose.slice(1)) : (query.toLowerCase().includes("family") ? "Family" : "General")}
                </span>
                <span className="px-3 py-1 bg-blue-50 border border-blue-200 text-[#2563EB] rounded-full text-xs font-extrabold shadow-2xs flex items-center gap-1.5">
                  ⭐ {sortedRecommendations.length} AI-selected hotels
                </span>
              </div>
            </div>
            
            <div className="flex items-center gap-3">
              <label className="text-sm font-bold text-[#475569]">Sort by</label>
              <select 
                value={sortBy || "trust_score_desc"}
                onChange={(e) => setFilter("sort_by", e.target.value)}
                className="h-[40px] bg-white border border-[#E2E8F0] rounded-[12px] px-4 text-sm font-semibold text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] cursor-pointer shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
              >
                <option value="trust_score_desc">Trust Score (Highest)</option>
                <option value="rating_desc">Rating (Highest)</option>
                <option value="cleanliness_desc">Cleanliness (Highest)</option>
                <option value="reviews_count_desc">Reviews Count (Highest)</option>
              </select>
            </div>
          </div>

          {/* Active Filters Summary Bar */}
          {hasActiveFilters && (
            <div className="mb-6 p-4 bg-white border border-[#E2E8F0] rounded-[16px] flex flex-wrap items-center justify-between gap-4 text-left shadow-xs">
              <div className="flex flex-wrap items-center gap-2">
                <span className="text-xs font-bold text-[#475569] uppercase tracking-wider mr-2">Active filters:</span>
                {budget && (
                  <span className="h-8 px-3 rounded-full bg-[#2563EB]/10 border border-[#2563EB]/20 text-[#2563EB] text-xs font-bold flex items-center gap-1.5 transition-all">
                    <span>Budget: {budget.charAt(0).toUpperCase() + budget.slice(1)}</span>
                    <button onClick={() => removeFilter("budget")} className="w-3.5 h-3.5 rounded-full hover:bg-[#2563EB]/20 flex items-center justify-center cursor-pointer">
                      <X className="w-2.5 h-2.5" />
                    </button>
                  </span>
                )}
                {purpose && (
                  <span className="h-8 px-3 rounded-full bg-[#2563EB]/10 border border-[#2563EB]/20 text-[#2563EB] text-xs font-bold flex items-center gap-1.5 transition-all">
                    <span>Purpose: {purpose.charAt(0).toUpperCase() + purpose.slice(1)}</span>
                    <button onClick={() => removeFilter("purpose")} className="w-3.5 h-3.5 rounded-full hover:bg-[#2563EB]/20 flex items-center justify-center cursor-pointer">
                      <X className="w-2.5 h-2.5" />
                    </button>
                  </span>
                )}
                {cleanliness && (
                  <span className="h-8 px-3 rounded-full bg-[#2563EB]/10 border border-[#2563EB]/20 text-[#2563EB] text-xs font-bold flex items-center gap-1.5 transition-all">
                    <span>Cleanliness: {cleanliness}+</span>
                    <button onClick={() => removeFilter("cleanliness")} className="w-3.5 h-3.5 rounded-full hover:bg-[#2563EB]/20 flex items-center justify-center cursor-pointer">
                      <X className="w-2.5 h-2.5" />
                    </button>
                  </span>
                )}
                <button onClick={() => clearAllFilters()} className="text-xs font-bold text-[#2563EB] hover:text-blue-700 ml-2 transition-colors cursor-pointer">
                  Clear all filters
                </button>
              </div>
              <span className="text-xs text-slate-500 font-bold">
                Showing {sortedRecommendations.length} {sortedRecommendations.length === 1 ? "recommendation" : "recommendations"} matching your selected filters
              </span>
            </div>
          )}

          {/* Query Intent Summary Card */}
          {!isPending && sortedRecommendations.length > 0 && (
            <div className="mb-6 p-4 bg-white border border-[#E2E8F0] rounded-[16px] flex flex-col md:flex-row items-start md:items-center justify-between gap-4 text-left shadow-xs">
              <div className="space-y-1">
                <div className="flex items-center gap-2 text-xs font-bold text-[#2563EB] uppercase tracking-wider">
                  <Sparkles className="w-3.5 h-3.5 text-[#2563EB]" />
                  <span>Your Search Interpretation</span>
                </div>
                <div className="flex flex-wrap items-center gap-2 pt-0.5 text-xs font-bold text-[#0F172A]">
                  <span>📍 Destination: <strong className="text-[#2563EB]">{parsedArea || "All Destinations"}</strong></span>
                  <span className="text-slate-300">•</span>
                  <span>👨‍👩‍👧 Travel Type: <strong className="text-[#2563EB]">{purpose ? (purpose.charAt(0).toUpperCase() + purpose.slice(1)) : (query.toLowerCase().includes("family") ? "Family" : "General")}</strong></span>
                </div>
              </div>
              <div className="flex flex-wrap items-center gap-1.5 text-[11px] font-semibold text-slate-600">
                <span className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-md text-slate-800">✓ Family Amenities</span>
                <span className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-md text-slate-800">✓ Cleanliness</span>
                <span className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-md text-slate-800">✓ Service Quality</span>
                <span className="px-2.5 py-1 bg-slate-50 border border-slate-200 rounded-md text-slate-800">✓ Neighborhood Safety</span>
              </div>
            </div>
          )}

          {isPending ? (
            <div className="space-y-6">
              {[1, 2, 3].map((i) => (
                <HotelCardSkeleton key={i} />
              ))}
            </div>
          ) : isError ? (
            <div className="p-8 text-center bg-red-50 text-red-600 rounded-[20px] border border-red-100 text-sm font-semibold">
              Failed to load recommendations. Please try a different search or check the server status.
            </div>
          ) : (sortedRecommendations.length === 0 || data?.metadata?.is_terminal_no_match) ? (
            <div className="p-12 text-center text-slate-500 bg-white rounded-[20px] border border-slate-200 shadow-sm space-y-5 flex flex-col items-center">
              <div className="w-16 h-16 bg-slate-100 rounded-full flex items-center justify-center text-slate-400 mb-2">
                <Compass className="w-8 h-8" />
              </div>
              <div>
                <p className="text-lg font-bold text-slate-800">We couldn't find hotels that reliably match your request</p>
                <p className="text-sm text-slate-500 max-w-md mx-auto mt-1">
                  Try broadening the location or removing one or more filters to find suitable properties.
                </p>
              </div>
              <div className="flex gap-3 mt-2">
                <Button onClick={() => clearAllFilters()} className="text-sm font-bold h-10 px-6 rounded-xl">Clear All Filters</Button>
                <Link href="/stays">
                  <Button variant="outline" className="text-sm font-bold h-10 px-6 rounded-xl border-slate-200 text-slate-700">Browse Catalog</Button>
                </Link>
              </div>
            </div>
          ) : (
            <>
              {data?.metadata?.fallback_reason && (!parsedArea || !sortedRecommendations.every((h: any) => h.area?.toLowerCase() === parsedArea.toLowerCase())) && (
                <div className="mb-6 p-4 bg-amber-50/80 border border-amber-200/70 rounded-[16px] flex items-center gap-3 text-left">
                  <Sparkles className="w-5 h-5 text-amber-600 shrink-0" />
                  <p className="text-amber-900 text-xs font-semibold">
                    Expanded your search to nearby areas around {parsedArea || "your target destination"} to find more highly rated options.
                  </p>
                </div>
              )}
              
              {/* Primary AI Recommendations */}
              <div className="space-y-6">
                {sortedRecommendations.map((rec, idx) => (
                  <RecommendationCard key={rec.hotel_id} rec={rec} isTopPick={idx === 0} />
                ))}
              </div>

              {/* Catalog Stays Fallback Fill */}
              {recommendations.length < 3 && data?.catalog_suggestions && data.catalog_suggestions.length > 0 && (
                <div className="mt-12 text-left">
                  <div className="mb-6">
                    <h2 className="text-lg font-extrabold text-[#0F172A] tracking-tight">
                      Additional stays that match your location filters
                    </h2>
                    <p className="text-xs text-slate-500 font-semibold mt-1">
                      Properties matching your destination without full AI recommendations.
                    </p>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {data.catalog_suggestions.map((hotel: any) => (
                      <HotelGridCard key={hotel.hotel_id} hotel={hotel} />
                    ))}
                  </div>
                </div>
              )}

              {/* Traditional Catalog Grid */}
              {parsedArea && deduplicatedCatalog.length > 0 && (
                <div className="mt-16 pt-10 border-t border-slate-200 text-left">
                  <div className="mb-6">
                    <h2 className="text-xl font-extrabold text-[#0F172A] tracking-tight">
                      Browse all hotels in {parsedArea}
                    </h2>
                    <p className="text-xs text-slate-500 font-semibold mt-1">
                      Full inventory of properties from our traditional catalog.
                    </p>
                  </div>
                  <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-6">
                    {deduplicatedCatalog.map((hotel: any) => (
                      <HotelGridCard key={hotel.hotel_id} hotel={hotel} />
                    ))}
                  </div>
                </div>
              )}
            </>
          )}
        </main>
      </div>
    </div>
  );
}

export default function SearchDashboard() {
  return (
    <Suspense fallback={<div className="p-8 text-center">Loading search dashboard...</div>}>
      <SearchContent />
    </Suspense>
  );
}
