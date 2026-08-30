import { useEffect, useState } from "react";
import Link from "next/link";
import { Clock } from "lucide-react";
import { useReveal } from "./useReveal";

export function RecentlyViewed() {
  const [recent, setRecent] = useState<any[]>([]);
  const { ref, isRevealed } = useReveal();

  useEffect(() => {
    try {
      const stored = JSON.parse(localStorage.getItem("recentHotels") || "[]");
      if (Array.isArray(stored)) {
        setRecent(stored.slice(0, 5));
      }
    } catch (e) {
      console.error("Failed to parse recent hotels");
    }
  }, []);

  if (recent.length === 0) return null;

  return (
    <section className="w-full bg-white py-16 border-t border-slate-100">
      <div 
        ref={ref}
        className={`max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="flex items-center gap-2 mb-8">
          <Clock className="w-6 h-6 text-slate-400" />
          <h2 className="text-2xl font-bold text-[#0F172A] tracking-tight">Recently Viewed</h2>
        </div>

        <div className="flex overflow-x-auto gap-4 pb-4 snap-x snap-mandatory hide-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0">
          {recent.map((hotel, i) => (
            <Link 
              href={`/hotel/${hotel.hotel_id}`}
              key={`${hotel.hotel_id}-${i}`}
              className="flex items-center gap-4 min-w-[280px] w-[280px] snap-start bg-white border border-slate-200 rounded-[16px] p-3 hover:border-blue-300 hover:shadow-lg hover:-translate-y-1 transition-all"
            >
              <img 
                src={hotel.hero_image || "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=200&q=80"} 
                alt={hotel.name}
                className="w-16 h-16 rounded-[10px] object-cover bg-slate-100"
              />
              <div className="flex-1 min-w-0">
                <h4 className="font-bold text-[#0F172A] text-sm truncate">{hotel.name}</h4>
                <p className="text-xs text-slate-500 truncate">{hotel.area}</p>
                <div className="mt-1 flex items-center gap-1.5">
                  <span className="text-[10px] font-bold text-slate-400 uppercase">Trust Score</span>
                  <span className="text-sm font-black text-blue-600">{hotel.trust_score?.toFixed(0) || "N/A"}</span>
                </div>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
