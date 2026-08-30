import { SlidersHorizontal } from "lucide-react";

export default function SearchLoading() {
  return (
    <div className="min-h-screen bg-[#F8FAFC]">
      {/* Sticky Search bar skeleton */}
      <div className="sticky top-16 z-30 w-full bg-white border-b border-slate-200 py-4 px-4 sm:px-6 lg:px-8 shadow-sm">
        <div className="max-w-7xl mx-auto flex gap-4 items-center justify-between">
          <div className="h-10 bg-slate-200 rounded-xl flex-1 max-w-xl animate-pulse" />
          <div className="h-10 w-28 bg-slate-200 rounded-xl animate-pulse" />
        </div>
      </div>

      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 py-8 flex flex-col md:flex-row gap-8">
        {/* Left sidebar filters skeleton */}
        <aside className="w-full md:w-64 shrink-0 space-y-6">
          <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-5">
            <div className="flex justify-between items-center pb-2 border-b border-slate-100">
              <h2 className="text-sm font-extrabold text-slate-400 flex items-center gap-1.5 uppercase tracking-wider">
                <SlidersHorizontal className="w-3.5 h-3.5" />
                Filters
              </h2>
            </div>
            {[1, 2, 3].map((i) => (
              <div key={i} className="space-y-2">
                <div className="h-3 w-16 bg-slate-200 rounded animate-pulse" />
                <div className="space-y-1.5">
                  <div className="h-4 w-full bg-slate-200 rounded animate-pulse" />
                  <div className="h-4 w-3/4 bg-slate-200 rounded animate-pulse" />
                </div>
              </div>
            ))}
          </div>
        </aside>

        {/* Right side cards skeleton */}
        <main className="flex-1 space-y-6">
          <div className="flex justify-between items-center">
            <div className="space-y-2">
              <div className="h-7 w-48 bg-slate-200 rounded animate-pulse" />
              <div className="h-3.5 w-24 bg-slate-200 rounded animate-pulse" />
            </div>
            <div className="h-8 w-32 bg-slate-200 rounded animate-pulse" />
          </div>

          <div className="space-y-6">
            {[1, 2].map((i) => (
              <div key={i} className="bg-white p-6 rounded-2xl border border-slate-200 shadow-sm flex flex-col gap-6">
                <div className="flex flex-col md:flex-row gap-4">
                  <div className="w-full md:w-1/4 h-32 bg-slate-200 rounded-xl animate-pulse" />
                  <div className="flex-1 space-y-3">
                    <div className="h-5 w-1/2 bg-slate-200 rounded animate-pulse" />
                    <div className="h-4 w-1/4 bg-slate-200 rounded animate-pulse" />
                    <div className="h-3.5 w-1/3 bg-slate-200 rounded animate-pulse" />
                  </div>
                </div>
                <div className="grid grid-cols-4 gap-4">
                  {[1, 2, 3, 4].map((j) => (
                    <div key={j} className="h-16 bg-slate-100 rounded-xl animate-pulse" />
                  ))}
                </div>
              </div>
            ))}
          </div>
        </main>
      </div>
    </div>
  );
}
