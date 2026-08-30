"use client";

import { RecommendationCard } from "@/components/RecommendationCard";
import { Recommendation } from "@/types/api";

export function HotelCatalogCard({ hotel }: { hotel: Recommendation }) {
  return <RecommendationCard rec={hotel} mode="catalog" />;
}
