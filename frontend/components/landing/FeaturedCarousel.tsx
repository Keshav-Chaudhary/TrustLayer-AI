import { useState, useRef } from "react";
import { ChevronLeft, ChevronRight, Star, MapPin } from "lucide-react";
import Link from "next/link";
import { useReveal } from "./useReveal";
import { Recommendation } from "@/types/api";

interface FeaturedCarouselProps {
  hotels: Recommendation[] | undefined;
  isLoading: boolean;
}

export function FeaturedCarousel({ hotels, isLoading }: FeaturedCarouselProps) {
  const scrollRef = useRef<HTMLDivElement>(null);
  const { ref, isRevealed } = useReveal();

  const scroll = (direction: "left" | "right") => {
    if (scrollRef.current) {
      const { scrollLeft, clientWidth } = scrollRef.current;
      const scrollTo = direction === "left" ? scrollLeft - clientWidth : scrollLeft + clientWidth;
      scrollRef.current.scrollTo({ left: scrollTo, behavior: "smooth" });
    }
  };

  return (
    <section className="w-full bg-[#F8FAFC] py-20 border-b border-slate-200">
      <div 
        ref={ref}
        className={`max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="flex flex-col md:flex-row md:items-end justify-between gap-4 mb-10">
          <div>
            <h2 className="text-3xl font-bold text-[#0F172A] tracking-tight">Featured Hotels</h2>
            <p className="text-[#475569] mt-2 font-medium">Top-rated properties from our trusted database</p>
          </div>
          
          <div className="flex gap-2">
            <button 
              onClick={() => scroll("left")}
              className="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-600 hover:bg-slate-50 hover:text-blue-600 transition-colors shadow-sm"
              aria-label="Scroll left"
            >
              <ChevronLeft className="w-5 h-5" />
            </button>
            <button 
              onClick={() => scroll("right")}
              className="w-10 h-10 rounded-full bg-white border border-slate-200 flex items-center justify-center text-slate-600 hover:bg-slate-50 hover:text-blue-600 transition-colors shadow-sm"
              aria-label="Scroll right"
            >
              <ChevronRight className="w-5 h-5" />
            </button>
          </div>
        </div>

        <div 
          ref={scrollRef}
          className="flex overflow-x-auto gap-6 pb-8 snap-x snap-mandatory hide-scrollbar -mx-4 px-4 sm:mx-0 sm:px-0"
          style={{ scrollbarWidth: 'none', msOverflowStyle: 'none' }}
        >
          {isLoading ? (
            Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="min-w-[85vw] sm:min-w-[45vw] md:min-w-[30vw] lg:min-w-[320px] snap-start bg-white rounded-[20px] border border-slate-200 p-4 h-[400px] flex flex-col gap-4 animate-pulse shrink-0 shadow-sm">
                <div className="w-full h-48 bg-slate-100 rounded-[12px]"></div>
                <div className="w-3/4 h-6 bg-slate-100 rounded"></div>
                <div className="w-1/2 h-4 bg-slate-100 rounded"></div>
                <div className="mt-auto flex justify-between">
                  <div className="w-16 h-8 bg-slate-100 rounded-full"></div>
                  <div className="w-24 h-8 bg-slate-100 rounded-full"></div>
                </div>
              </div>
            ))
          ) : (
            hotels?.map((hotel) => (
              <Link 
                href={`/hotel/${hotel.hotel_id}`} 
                key={hotel.hotel_id}
                className="group min-w-[85vw] sm:min-w-[45vw] md:min-w-[30vw] lg:min-w-[320px] snap-start bg-white rounded-[20px] border border-slate-200 hover:border-blue-300 p-4 shrink-0 shadow-sm hover:shadow-xl hover:shadow-blue-900/5 hover:-translate-y-1 transition-all duration-300 flex flex-col cursor-pointer"
              >
                <div className="relative w-full h-48 rounded-[12px] overflow-hidden bg-slate-100 mb-4">
                  <img 
                    src={hotel.hero_image || "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80"} 
                    alt={hotel.name}
                    className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
                  />
                  <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-sm px-2.5 py-1 rounded-full text-xs font-bold text-[#0F172A] flex items-center gap-1 shadow-sm">
                    <Star className="w-3 h-3 fill-amber-400 stroke-amber-400" />
                    {hotel.rating.toFixed(1)}
                  </div>
                </div>
                
                <h3 className="text-lg font-bold text-[#0F172A] leading-tight line-clamp-1">{hotel.name}</h3>
                <p className="text-sm font-medium text-slate-500 flex items-center gap-1 mt-1.5 line-clamp-1">
                  <MapPin className="w-3.5 h-3.5" />
                  {hotel.area}
                </p>
                
                <div className="mt-auto pt-4 border-t border-slate-100 flex items-center justify-between">
                  <div>
                    <p className="text-[10px] font-bold text-slate-400 uppercase tracking-wider">Trust Score</p>
                    <p className="text-lg font-black text-blue-600">{hotel.trust_score.toFixed(0)}</p>
                  </div>
                  <span className="text-sm font-bold text-blue-600 bg-blue-50 px-3 py-1.5 rounded-full group-hover:bg-blue-600 group-hover:text-white transition-colors">
                    View Details
                  </span>
                </div>
              </Link>
            ))
          )}
        </div>
      </div>
    </section>
  );
}
