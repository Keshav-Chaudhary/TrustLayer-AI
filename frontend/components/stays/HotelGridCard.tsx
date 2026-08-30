"use client";

import Link from "next/link";
import { Star, MapPin, ArrowRight, ShieldCheck } from "lucide-react";
import { Recommendation } from "@/types/api";

export function HotelGridCard({ hotel }: { hotel: Recommendation }) {
  const trustScore = hotel.trust_score || 90.0;
  const rating = hotel.rating || 4.0;
  const aspectScores = hotel.aspect_scores || {};

  return (
    <Link href={`/hotel/${hotel.hotel_id}`} className="group block h-full text-left">
      <div className="bg-white border border-[#E2E8F0] rounded-[20px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] hover:shadow-[0_8px_24px_rgba(15,23,42,0.12)] hover:border-blue-300 transition-all duration-300 overflow-hidden flex flex-col h-full">
        
        {/* Image Section */}
        <div className="aspect-[16/10] w-full relative overflow-hidden bg-slate-100 shrink-0">
          <img 
            src={hotel.hero_image || "https://images.unsplash.com/photo-1566073771259-6a8506099945?auto=format&fit=crop&w=600&q=80"}
            alt={hotel.name}
            className="w-full h-full object-cover group-hover:scale-105 transition-transform duration-500"
          />
          {/* Floating Rating Pill */}
          <div className="absolute top-3 left-3 bg-white/95 backdrop-blur-md px-2.5 py-1 rounded-lg flex items-center gap-1 shadow-xs">
            <Star className="w-3.5 h-3.5 fill-[#F59E0B] stroke-[#F59E0B]" />
            <span className="font-bold text-[#0F172A] text-xs">{rating.toFixed(1)}/5</span>
          </div>

          {/* Trust Score Badge */}
          {trustScore > 0 && (
            <div className="absolute top-3 right-3 bg-blue-600/90 backdrop-blur-md text-white px-2.5 py-1 rounded-lg text-[10px] font-black uppercase tracking-wider shadow-xs flex items-center gap-1">
              <ShieldCheck className="w-3 h-3 text-white" />
              <span>Trust {trustScore.toFixed(1)}</span>
            </div>
          )}
        </div>

        {/* Content Section */}
        <div className="p-5 flex-1 flex flex-col justify-between">
          <div className="space-y-2 mb-4">
            <h3 className="font-bold text-base text-[#0F172A] leading-snug line-clamp-1 group-hover:text-[#2563EB] transition-colors">
              {hotel.name}
            </h3>
            
            <div className="flex items-center gap-1.5 text-xs text-[#475569] font-medium">
              <MapPin className="w-3.5 h-3.5 text-slate-400 shrink-0" />
              <span className="truncate">{hotel.area}</span>
              <span>•</span>
              <span className="shrink-0">{hotel.reviews_count ? `${hotel.reviews_count.toLocaleString()} reviews` : "Catalog stay"}</span>
            </div>

            {/* Aspect score mini badges */}
            {Object.keys(aspectScores).length > 0 && (
              <div className="flex flex-wrap gap-1.5 pt-1">
                {Object.entries(aspectScores).slice(0, 3).map(([aspect, score]) => (
                  <span key={aspect} className="text-[10px] font-bold px-2 py-0.5 rounded-md bg-slate-50 border border-slate-200 text-slate-700 capitalize">
                    {aspect}: <strong className={score >= 4.5 ? 'text-emerald-600' : 'text-blue-600'}>{score.toFixed(1)}</strong>
                  </span>
                ))}
              </div>
            )}
          </div>

          {/* Card Footer: Price & CTA */}
          <div className="pt-3 border-t border-[#E2E8F0] flex items-center justify-between">
            <div>
              <span className="block text-[10px] text-slate-400 font-bold uppercase tracking-wider">Starting from</span>
              <span className="block text-base font-black text-[#0F172A]">
                {hotel.price && hotel.price !== "Price unavailable" ? (hotel.price.startsWith("₹") ? hotel.price : `₹${hotel.price}`) : "Price unavailable"}
              </span>
            </div>
            
            <span className="h-8 px-3.5 rounded-[10px] border border-slate-200 text-[#0F172A] text-xs font-bold flex items-center gap-1 bg-slate-50 group-hover:bg-[#2563EB] group-hover:text-white group-hover:border-[#2563EB] transition-all select-none shadow-2xs">
              <span>View details</span>
              <ArrowRight className="w-3.5 h-3.5" />
            </span>
          </div>

        </div>

      </div>
    </Link>
  );
}
