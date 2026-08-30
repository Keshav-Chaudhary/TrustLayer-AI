"use client";

import { Card } from "@/components/ui/card";

export function HotelCardSkeleton() {
  return (
    <Card className="flex flex-col bg-white border border-[#E2E8F0] rounded-[20px] shadow-sm overflow-hidden w-full max-w-[1200px] mx-auto p-6 gap-6 animate-pulse">
      {/* Header Row */}
      <div className="flex flex-col md:flex-row gap-6">
        {/* Left: Thumbnail & Rating Overlays */}
        <div className="flex flex-col items-center gap-3 shrink-0">
          <div className="w-full md:w-[220px] h-[180px] rounded-[16px] bg-slate-200"></div>
          <div className="flex items-center gap-2">
            <div className="h-6 w-16 bg-slate-200 rounded-full"></div>
            <div className="h-6 w-24 bg-slate-200 rounded-full"></div>
          </div>
        </div>

        {/* Right: Info and Pricing details */}
        <div className="flex-1 flex flex-col justify-between gap-4">
          <div className="flex flex-col sm:flex-row justify-between items-start gap-4">
            <div className="space-y-3 min-w-0 w-full max-w-sm">
              <div className="h-8 w-3/4 bg-slate-200 rounded-md"></div>
              <div className="h-4 w-1/2 bg-slate-200 rounded-md"></div>
            </div>
            <div className="space-y-2 text-left sm:text-right shrink-0">
              <div className="h-4 w-20 bg-slate-200 rounded-md sm:ml-auto"></div>
              <div className="h-8 w-32 bg-slate-200 rounded-md sm:ml-auto"></div>
            </div>
          </div>
          <div className="mt-4 pt-4 border-t border-slate-100 flex flex-wrap gap-2">
            <div className="h-8 w-24 bg-slate-200 rounded-lg"></div>
            <div className="h-8 w-28 bg-slate-200 rounded-lg"></div>
            <div className="h-8 w-20 bg-slate-200 rounded-lg"></div>
          </div>
        </div>
      </div>
    </Card>
  );
}
