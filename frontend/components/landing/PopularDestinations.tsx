import Link from "next/link";
import { useReveal } from "./useReveal";
import { DESTINATIONS_CONFIG } from "@/lib/ui-config";

export function PopularDestinations() {
  const { ref, isRevealed } = useReveal();

  return (
    <section className="w-full bg-white py-24">
      <div 
        ref={ref}
        className={`max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="mb-12">
          <h2 className="text-3xl font-bold text-[#0F172A] tracking-tight">Popular Destinations</h2>
          <p className="text-[#475569] mt-2 font-medium">Explore top-rated stays in these trending locations</p>
        </div>

        <div className="grid grid-cols-2 md:grid-cols-3 lg:grid-cols-4 gap-4 sm:gap-6">
          {DESTINATIONS_CONFIG.map((dest) => (
            <Link
              key={dest.name}
              href={`/stays?area=${encodeURIComponent(dest.name)}`}
              className="group relative h-64 sm:h-72 lg:h-80 rounded-[24px] overflow-hidden block shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
            >
              <img 
                src={dest.image} 
                alt={dest.name}
                className="absolute inset-0 w-full h-full object-cover group-hover:scale-105 transition-transform duration-700"
              />
              <div className="absolute inset-0 bg-gradient-to-t from-slate-900/90 via-slate-900/40 to-transparent" />
              
              <div className="absolute bottom-0 left-0 right-0 p-6">
                <h3 className="text-2xl font-bold text-white mb-1 tracking-tight">{dest.name}</h3>
                <span className="inline-block bg-white/20 backdrop-blur-md px-3 py-1 rounded-full text-xs font-semibold text-white border border-white/20">
                  {dest.count} hotels
                </span>
              </div>
            </Link>
          ))}
        </div>
      </div>
    </section>
  );
}
