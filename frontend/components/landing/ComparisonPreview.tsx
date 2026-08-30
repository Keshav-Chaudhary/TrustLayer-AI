import { ArrowRight, Trophy } from "lucide-react";
import Link from "next/link";
import { useReveal } from "./useReveal";

const mockComparison = [
  {
    name: "Pullman New Delhi",
    image: "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=400&q=80",
    trustScore: 98,
    cleanliness: 5.0,
    service: 4.8,
    winner: true
  },
  {
    name: "Holiday Inn Aerocity",
    image: "https://images.unsplash.com/photo-1551882547-ff40eb0d1e73?auto=format&fit=crop&w=400&q=80",
    trustScore: 85,
    cleanliness: 4.2,
    service: 4.5,
    winner: false
  },
  {
    name: "Radisson Blu Plaza",
    image: "https://images.unsplash.com/photo-1582719478250-c89cae4dc85b?auto=format&fit=crop&w=400&q=80",
    trustScore: 92,
    cleanliness: 4.7,
    service: 4.6,
    winner: false
  }
];

export function ComparisonPreview() {
  const { ref, isRevealed } = useReveal();

  return (
    <section className="w-full bg-[#F8FAFC] py-24 border-t border-slate-200 overflow-hidden relative">
      <div 
        ref={ref}
        className={`max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="text-center max-w-2xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-[#0F172A] tracking-tight">Compare Before You Decide</h2>
          <p className="text-[#475569] mt-4 font-medium text-lg">Put hotels head-to-head based on the metrics that matter most to you.</p>
        </div>

        {/* Desktop Comparison Table Mockup */}
        <div className="relative max-w-5xl mx-auto hidden md:block">
          <div className="absolute -inset-10 bg-gradient-to-r from-transparent via-blue-100/50 to-transparent blur-3xl z-0" />
          
          <div className="relative z-10 bg-white rounded-[24px] border border-slate-200 shadow-2xl p-8 overflow-hidden">
            <div className="grid grid-cols-4 gap-6">
              
              {/* Labels Column */}
              <div className="flex flex-col justify-end space-y-10 pb-8 text-right font-bold text-slate-400 text-sm uppercase tracking-wider">
                <div>Trust Score</div>
                <div>Cleanliness</div>
                <div>Service</div>
              </div>

              {/* Hotel Columns */}
              {mockComparison.map((hotel, i) => (
                <div key={i} className={`flex flex-col items-center p-6 rounded-[20px] ${hotel.winner ? 'bg-blue-50 border border-blue-200 relative' : 'bg-slate-50 border border-slate-100'}`}>
                  {hotel.winner && (
                    <div className="absolute -top-4 bg-amber-400 text-amber-900 text-[10px] font-black uppercase tracking-widest px-3 py-1 rounded-full flex items-center gap-1 shadow-sm">
                      <Trophy className="w-3 h-3" /> Top Pick
                    </div>
                  )}
                  <img src={hotel.image} alt={hotel.name} className="w-full h-32 object-cover rounded-[12px] mb-4 shadow-sm" />
                  <h4 className="font-bold text-[#0F172A] text-center mb-8 h-10 line-clamp-2">{hotel.name}</h4>
                  
                  <div className="space-y-10 text-center w-full">
                    <div className={`text-3xl font-black ${hotel.winner ? 'text-blue-600' : 'text-slate-700'}`}>{hotel.trustScore}</div>
                    <div className="text-xl font-bold text-slate-700">{hotel.cleanliness.toFixed(1)}</div>
                    <div className="text-xl font-bold text-slate-700">{hotel.service.toFixed(1)}</div>
                  </div>
                </div>
              ))}
            </div>
            
            <div className="absolute bottom-0 left-0 right-0 h-32 bg-gradient-to-t from-white via-white/90 to-transparent flex items-end justify-center pb-8">
              <Link 
                href="/compare"
                className="px-8 py-3.5 bg-slate-900 hover:bg-slate-800 text-white font-bold rounded-xl flex items-center gap-2 transition-transform hover:-translate-y-1 shadow-xl"
              >
                Open Full Comparison <ArrowRight className="w-4 h-4" />
              </Link>
            </div>
          </div>
        </div>

        {/* Mobile View Mockup */}
        <div className="md:hidden flex flex-col gap-6">
           <Link 
            href="/compare"
            className="w-full px-6 py-4 bg-slate-900 text-white font-bold rounded-xl flex items-center justify-center gap-2 shadow-xl"
          >
            Try Comparison Tool <ArrowRight className="w-4 h-4" />
          </Link>
        </div>

      </div>
    </section>
  );
}
