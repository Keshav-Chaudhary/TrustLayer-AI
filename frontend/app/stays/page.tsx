"use client";

import { useHotelsCatalog } from "@/hooks/useHotels";
import { SearchHeader } from "@/components/stays/SearchHeader";
import { FilterSidebar } from "@/components/stays/FilterSidebar";
import { ResultsHeader } from "@/components/stays/ResultsHeader";
import { HotelCatalogCard } from "@/components/stays/HotelCatalogCard";
import { EmptyState } from "@/components/stays/EmptyState";
import { CatalogSkeleton } from "@/components/stays/CatalogSkeleton";
import { Pagination } from "@/components/stays/Pagination";
import { Suspense, useState, useEffect, useRef } from "react";
import { fetchNearestAreas, getHotelsCatalog } from "@/lib/api";
import { useSearchFilters } from "@/lib/search-state";
import { useQueryClient } from "@tanstack/react-query";
import { Info, X, Loader2 } from "lucide-react";

function StaysContent() {
  const {
    area,
    budget,
    purpose,
    cleanliness,
    rating,
    sortBy,
    page,
    setPage,
    removeFilter,
    clearAllFilters
  } = useSearchFilters();
  
  const queryClient = useQueryClient();
  const resultsRef = useRef<HTMLDivElement>(null);

  const [fallbackBanner, setFallbackBanner] = useState<{ message: string, cluster: string | null } | null>(null);
  const [effectiveArea, setEffectiveArea] = useState<string | undefined>(area || undefined);

  // Sync effectiveArea when the URL area changes
  useEffect(() => {
    setEffectiveArea(area || undefined);
    setFallbackBanner(null);
  }, [area]);

  const filterParams = {
    page,
    limit: 20,
    area: effectiveArea,
    budget: budget || undefined,
    cleanliness: cleanliness ? Number(cleanliness) : undefined,
    rating: rating ? Number(rating) : undefined,
    sort_by: sortBy || "trust_score_desc",
  };

  const { data, isLoading, isFetching } = useHotelsCatalog(filterParams);

  const hotels = data?.hotels || [];
  const pagination = data?.pagination;
  const total = pagination?.total_hotels || 0;
  const totalPages = pagination?.total_pages || 1;
  const hasActiveFilters = !!(budget || purpose || cleanliness || rating);

  // Prefetch adjacent pages for instant navigation
  useEffect(() => {
    if (pagination) {
      const { page: currentPage, total_pages: maxPages } = pagination;
      const { page: _p, ...restFilters } = filterParams;

      // Prefetch Next Page
      if (currentPage < maxPages) {
        const nextFilters = { ...filterParams, page: currentPage + 1 };
        queryClient.prefetchQuery({
          queryKey: ['hotels', restFilters, filterParams.sort_by, currentPage + 1, filterParams.limit],
          queryFn: () => getHotelsCatalog(nextFilters),
        });
      }

      // Prefetch Previous Page
      if (currentPage > 1) {
        const prevFilters = { ...filterParams, page: currentPage - 1 };
        queryClient.prefetchQuery({
          queryKey: ['hotels', restFilters, filterParams.sort_by, currentPage - 1, filterParams.limit],
          queryFn: () => getHotelsCatalog(prevFilters),
        });
      }
    }
  }, [pagination, filterParams, queryClient]);

  // Frontend URL Normalization / Clamping: if page > totalPages, normalize URL
  useEffect(() => {
    if (!isLoading && pagination && page > totalPages && totalPages > 0) {
      setPage(totalPages, { replace: true });
    }
  }, [isLoading, pagination, page, totalPages, setPage]);

  // Fallback Logic for zero/low results in area
  useEffect(() => {
    if (!isLoading && area && hotels.length < 5 && effectiveArea === area) {
      fetchNearestAreas(area).then((res) => {
         if (res.nearby_areas && res.nearby_areas.length > 0) {
            setFallbackBanner({ message: res.message, cluster: res.cluster });
            setEffectiveArea(res.nearby_areas.join(","));
         }
      }).catch(err => console.error("Failed to fetch nearest areas:", err));
    }
  }, [isLoading, area, hotels.length, effectiveArea]);

  // Explicit Page Change handler with targeted smooth scrolling
  const handlePageChange = (newPage: number) => {
    setPage(newPage);
    if (resultsRef.current) {
      resultsRef.current.scrollIntoView({ behavior: "smooth" });
    }
  };

  return (
    <div className="min-h-screen bg-[#F8FAFC] font-sans overflow-x-hidden">
      
      {/* Search Header Container */}
      <div className="w-full bg-[#F8FAFC] pt-8 px-4 sm:px-6 lg:px-8 max-w-[1440px] mx-auto">
        <SearchHeader />
      </div>

      <div className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 pb-24 flex flex-col lg:flex-row gap-8">
        
        {/* Left Sidebar */}
        <aside className="w-full lg:w-[320px] shrink-0">
          <FilterSidebar />
        </aside>

        {/* Right Results Area */}
        <div className="flex-1 min-w-0 flex flex-col" ref={resultsRef}>
          <ResultsHeader totalCount={total} isLoading={isLoading || isFetching} />

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
                {rating && (
                  <span className="h-8 px-3 rounded-full bg-[#2563EB]/10 border border-[#2563EB]/20 text-[#2563EB] text-xs font-bold flex items-center gap-1.5 transition-all">
                    <span>Rating: {rating}+</span>
                    <button onClick={() => removeFilter("rating")} className="w-3.5 h-3.5 rounded-full hover:bg-[#2563EB]/20 flex items-center justify-center cursor-pointer">
                      <X className="w-2.5 h-2.5" />
                    </button>
                  </span>
                )}
                <button onClick={() => clearAllFilters()} className="text-xs font-bold text-[#2563EB] hover:text-blue-700 ml-2 transition-colors cursor-pointer">
                  Clear all filters
                </button>
              </div>
              <span className="text-xs text-slate-500 font-bold">
                Showing {total} {total === 1 ? "hotel" : "hotels"} matching your selected filters
              </span>
            </div>
          )}

          {/* Fallback Banner */}
          {fallbackBanner && (
            <div className="mb-6 p-4 bg-blue-50 border border-blue-200 rounded-[12px] flex items-start gap-3">
              <Info className="w-5 h-5 text-blue-600 mt-0.5 shrink-0" />
              <div>
                <h3 className="text-blue-800 font-semibold text-[15px]">We expanded your search</h3>
                <p className="text-blue-600 text-sm mt-0.5">{fallbackBanner.message}</p>
              </div>
            </div>
          )}

          {/* Results List with Smooth Overlay for Page Transitions */}
          <div className="relative flex flex-col gap-6 min-h-[400px]">
            {isFetching && !isLoading && (
              <div className="absolute inset-0 bg-slate-50/40 backdrop-blur-[1px] z-10 rounded-[20px] flex items-start justify-center pt-24 transition-opacity duration-200">
                <div className="bg-white border border-slate-200 rounded-full px-4 py-2 shadow-md flex items-center gap-2.5 text-xs font-extrabold text-blue-600">
                  <Loader2 className="w-4 h-4 animate-spin" />
                  <span>Loading page {page}...</span>
                </div>
              </div>
            )}

            {isLoading ? (
              Array.from({ length: 3 }).map((_, i) => <CatalogSkeleton key={i} />)
            ) : hotels.length > 0 ? (
              hotels.map((hotel: any) => (
                <HotelCatalogCard key={hotel.hotel_id} hotel={hotel} />
              ))
            ) : (
              <EmptyState />
            )}
          </div>
          
          {/* Reusable Production Pagination Component */}
          {!isLoading && totalPages > 1 && (
            <Pagination
              page={page}
              totalPages={totalPages}
              onPageChange={handlePageChange}
              isFetching={isFetching}
            />
          )}
        </div>
        
      </div>
    </div>
  );
}

export default function StaysPage() {
  return (
    <Suspense fallback={<div className="p-8 text-center text-slate-500 font-medium">Loading catalog...</div>}>
      <StaysContent />
    </Suspense>
  );
}
