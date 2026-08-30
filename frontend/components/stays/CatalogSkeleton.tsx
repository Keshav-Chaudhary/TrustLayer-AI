export function CatalogSkeleton() {
  return (
    <div className="w-full bg-white rounded-[20px] border border-[#E2E8F0] shadow-[0_1px_3px_rgba(0,0,0,0.08)] overflow-hidden flex flex-col md:flex-row animate-pulse">
      
      {/* Left: Image Placeholder */}
      <div className="relative w-full md:w-[280px] h-[220px] md:h-auto shrink-0 p-4 pb-0 md:pb-4">
        <div className="w-full h-full bg-slate-200 rounded-[16px]"></div>
      </div>

      {/* Center & Right: Content */}
      <div className="flex-1 p-6 flex flex-col">
        <div className="flex flex-col md:flex-row justify-between gap-4 mb-4">
          
          {/* Title and Info */}
          <div className="flex-1 space-y-3">
            <div className="h-6 bg-slate-200 rounded-md w-3/4"></div>
            <div className="h-3 bg-slate-200 rounded-md w-1/4"></div>
            <div className="h-4 bg-slate-200 rounded-md w-1/2 mt-4"></div>
            <div className="flex gap-2 mt-4">
              <div className="h-6 bg-slate-200 rounded-md w-24"></div>
              <div className="h-6 bg-slate-200 rounded-md w-24"></div>
            </div>
          </div>

          {/* Pricing Block */}
          <div className="md:w-32 flex flex-col md:items-end space-y-2">
            <div className="h-3 bg-slate-200 rounded-md w-16"></div>
            <div className="h-8 bg-slate-200 rounded-md w-24"></div>
            <div className="h-10 bg-slate-200 rounded-[12px] w-full mt-4"></div>
          </div>
        </div>

        {/* AI Aspect Grid */}
        <div className="grid grid-cols-2 md:grid-cols-4 gap-3 mb-6 bg-slate-50 p-4 rounded-[12px] border border-slate-100">
          {[1, 2, 3, 4].map((i) => (
            <div key={i} className="space-y-2">
              <div className="h-3 bg-slate-200 rounded-md w-16"></div>
              <div className="h-5 bg-slate-200 rounded-md w-12"></div>
            </div>
          ))}
        </div>

        {/* Verified Review Evidence & Amenities */}
        <div className="mt-auto pt-4 border-t border-slate-100 flex flex-col md:flex-row justify-between items-start md:items-center gap-4">
          <div className="flex-1 space-y-2 w-full">
            <div className="h-4 bg-slate-200 rounded-md w-1/3 mb-4"></div>
            <div className="h-3 bg-slate-200 rounded-md w-full"></div>
            <div className="h-3 bg-slate-200 rounded-md w-5/6"></div>
          </div>
          <div className="flex flex-col md:items-end space-y-3 shrink-0">
             <div className="flex gap-2">
               <div className="h-5 bg-slate-200 rounded-md w-16"></div>
               <div className="h-5 bg-slate-200 rounded-md w-16"></div>
             </div>
             <div className="h-4 bg-slate-200 rounded-md w-24"></div>
          </div>
        </div>

      </div>
    </div>
  );
}
