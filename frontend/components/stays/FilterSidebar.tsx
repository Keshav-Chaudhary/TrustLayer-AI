import { useSearchFilters } from "@/lib/search-state";

export function FilterSidebar({ availableAreas }: { availableAreas?: string[] }) {
  const {
    area: activeArea,
    budget: activeBudget,
    cleanliness: activeCleanliness,
    purpose: activePurpose,
    rating: activeRating,
    toggleFilter,
    clearAllFilters
  } = useSearchFilters();

  const handleFilterChange = (key: string, value: string) => {
    toggleFilter(key, value);
  };

  const clearFilters = () => {
    clearAllFilters();
  };

  // Derive dynamic areas list
  const defaultAreas = ["All Destinations", "Central Area", "Airport Zone", "North Area", "South Area"];
  const areaOptions = Array.from(
    new Set([
      ...(activeArea ? [activeArea] : []),
      ...(availableAreas && availableAreas.length > 0 ? availableAreas : defaultAreas)
    ])
  ).filter(Boolean);

  return (
    <div className="w-full bg-white rounded-[20px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] border border-slate-200 p-6 sticky top-[240px]">
      <div className="flex items-center justify-between mb-6">
        <h3 className="font-bold text-[#0F172A] text-lg">Filters</h3>
        <button onClick={clearFilters} className="text-[13px] font-bold text-blue-600 hover:text-blue-700 transition-colors">
          Clear all
        </button>
      </div>

      <div className="space-y-8">
        
        {/* Area */}
        <div>
          <h4 className="text-[13px] font-bold text-[#0F172A] mb-3">Area</h4>
          <div className="space-y-2">
            {areaOptions.slice(0, 6).map(areaName => (
              <label key={areaName} className="flex items-center gap-3 cursor-pointer group">
                <input 
                  type="checkbox" 
                  checked={activeArea === areaName}
                  onChange={() => handleFilterChange("area", areaName === "All Destinations" ? "" : areaName)}
                  className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
                <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{areaName}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Budget Category */}
        <div>
          <h4 className="text-[13px] font-bold text-[#0F172A] mb-3">Budget Category</h4>
          <div className="space-y-2">
            {[
              { label: "Budget", value: "budget" },
              { label: "Mid-range", value: "mid-range" },
              { label: "Luxury", value: "luxury" },
            ].map(item => (
              <label key={item.value} className="flex items-center gap-3 cursor-pointer group">
                <input 
                  type="checkbox" 
                  checked={activeBudget === item.value}
                  onChange={() => handleFilterChange("budget", item.value)}
                  className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
                <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{item.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Cleanliness Rating */}
        <div>
          <h4 className="text-[13px] font-bold text-[#0F172A] mb-3">Cleanliness Rating</h4>
          <div className="space-y-2">
            {[
              { label: "4.5+ Excellent", value: "4.5" },
              { label: "4.0+ Very Good", value: "4.0" },
              { label: "3.5+ Good", value: "3.5" },
            ].map(item => (
              <label key={item.value} className="flex items-center gap-3 cursor-pointer group">
                <input 
                  type="checkbox" 
                  checked={activeCleanliness === item.value}
                  onChange={() => handleFilterChange("cleanliness", item.value)}
                  className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
                <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{item.label}</span>
              </label>
            ))}
          </div>
        </div>

        {/* Travel Purpose */}
        <div>
          <h4 className="text-[13px] font-bold text-[#0F172A] mb-3">Travel Purpose</h4>
          <div className="space-y-2">
            {[
              { label: "Family", value: "family" },
              { label: "Business", value: "business" },
              { label: "Couple", value: "couple" },
            ].map(item => (
              <label key={item.value} className="flex items-center gap-3 cursor-pointer group">
                <input 
                  type="checkbox" 
                  checked={activePurpose === item.value}
                  onChange={() => handleFilterChange("purpose", item.value)}
                  className="w-4 h-4 rounded border-slate-300 text-blue-600 focus:ring-blue-500 cursor-pointer"
                />
                <span className="text-sm font-medium text-slate-700 group-hover:text-slate-900 transition-colors">{item.label}</span>
              </label>
            ))}
          </div>
        </div>

      </div>

    </div>
  );
}
