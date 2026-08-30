import { useSearchParams, useRouter } from "next/navigation";

interface ResultsHeaderProps {
  totalCount: number;
  isLoading?: boolean;
}

export function ResultsHeader({ totalCount, isLoading }: ResultsHeaderProps) {
  const searchParams = useSearchParams();
  const router = useRouter();
  
  const activeArea = searchParams?.get("area");
  const sortBy = searchParams?.get("sort_by") || "trust_score";

  const handleSortChange = (e: React.ChangeEvent<HTMLSelectElement>) => {
    const params = new URLSearchParams(searchParams?.toString() || "");
    params.set("sort_by", e.target.value);
    router.push(`/stays?${params.toString()}`);
  };

  return (
    <div className="flex flex-col sm:flex-row sm:items-center justify-between gap-4 mb-6">
      <div>
        <div className="flex items-center gap-2.5">
          <h1 className="text-[24px] font-bold text-[#0F172A] tracking-tight">Browse Stays</h1>
          {isLoading && (
            <span className="text-[11px] font-extrabold text-[#2563EB] bg-[#2563EB]/10 border border-[#2563EB]/20 px-2 py-0.5 rounded-md animate-pulse shrink-0">
              Updating results...
            </span>
          )}
        </div>
        <p className="text-[#475569] font-medium text-[16px]">
          {totalCount} hotels found {activeArea ? `in ${activeArea}` : ""}
        </p>
      </div>

      <div className="flex items-center gap-3">
        <label className="text-sm font-bold text-[#475569]">Sort by</label>
        <select 
          value={sortBy}
          onChange={handleSortChange}
          className="h-[40px] bg-white border border-[#E2E8F0] rounded-[12px] px-4 text-sm font-semibold text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] cursor-pointer shadow-[0_1px_3px_rgba(0,0,0,0.04)]"
        >
          <option value="trust_score">Trust Score (Highest)</option>
          <option value="rating">Rating (Highest)</option>
          <option value="price_asc">Price (Lowest)</option>
          <option value="price_desc">Price (Highest)</option>
          <option value="reviews_count">Most Reviewed</option>
        </select>
      </div>
    </div>
  );
}
