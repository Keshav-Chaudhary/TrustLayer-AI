"use client";

import { useMetrics, useFeaturedHotels } from "@/hooks/useHotels";
import { HeroSection } from "@/components/landing/HeroSection";
import { FeaturedCarousel } from "@/components/landing/FeaturedCarousel";
import { PopularDestinations } from "@/components/landing/PopularDestinations";
import { ValuePropsSection } from "@/components/landing/ValuePropsSection";
import { HowTrustWorksSection } from "@/components/landing/HowTrustWorksSection";
import { AIAssistantShowcase } from "@/components/landing/AIAssistantShowcase";
import { ComparisonPreview } from "@/components/landing/ComparisonPreview";
import { RecentlyViewed } from "@/components/landing/RecentlyViewed";
import { StatsSection } from "@/components/landing/StatsSection";
import { PremiumFooter } from "@/components/landing/PremiumFooter";

export default function LandingPage() {
  const { data: featuredData, isLoading: isLoadingFeatured } = useFeaturedHotels();
  const { data: metrics, isLoading: isLoadingMetrics } = useMetrics();

  return (
    <main className="flex flex-col w-full min-h-screen bg-white font-sans overflow-x-hidden">
      <HeroSection />
      <FeaturedCarousel hotels={featuredData?.hotels} isLoading={isLoadingFeatured} />
      <PopularDestinations />
      <ValuePropsSection />
      <HowTrustWorksSection />
      <AIAssistantShowcase />
      <ComparisonPreview />
      <RecentlyViewed />
      <StatsSection metrics={metrics} isLoading={isLoadingMetrics} />
      <PremiumFooter />
    </main>
  );
}
