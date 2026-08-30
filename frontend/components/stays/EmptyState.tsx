import { SearchX } from "lucide-react";
import Link from "next/link";
import { useRouter } from "next/navigation";

export function EmptyState() {
  const router = useRouter();

  return (
    <div className="w-full bg-white rounded-[20px] border border-[#E2E8F0] shadow-sm p-16 flex flex-col items-center justify-center text-center">
      <div className="w-24 h-24 bg-slate-50 rounded-full flex items-center justify-center mb-6 border border-slate-100">
        <SearchX className="w-10 h-10 text-slate-400" />
      </div>
      <h2 className="text-2xl font-bold text-[#0F172A] mb-2">No hotels found</h2>
      <p className="text-[#475569] mb-8 text-lg">Try adjusting your filters or searching a nearby area.</p>
      
      <div className="flex items-center gap-4">
        <button 
          onClick={() => router.push("/stays")}
          className="px-6 py-3 bg-slate-100 hover:bg-slate-200 text-slate-700 font-bold rounded-[12px] transition-colors"
        >
          Clear Filters
        </button>
        <Link 
          href="/stays"
          className="px-6 py-3 bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-[12px] shadow-sm transition-colors"
        >
          Browse All Hotels
        </Link>
      </div>
    </div>
  );
}
