import { useQuery, useMutation, keepPreviousData } from '@tanstack/react-query';
import { getMetrics, getRecommendations, getHotelAnalysis, saveHotel, compareHotels, getEvidence, getExplanation, analyzeHotel, getHotelsCatalog, getFeaturedHotels } from '../lib/api';

export const useMetrics = () => {
  return useQuery({
    queryKey: ['metrics'],
    queryFn: getMetrics,
  });
};

export const useRecommendations = () => {
  return useMutation({
    mutationFn: getRecommendations,
  });
};

export const useHotelAnalysis = (id: string) => {
  return useQuery({
    queryKey: ['hotel', id],
    queryFn: () => getHotelAnalysis(id),
    enabled: !!id,
  });
};

export const useEvidence = (id: string, isExpanded: boolean) => {
  return useQuery({
    queryKey: ['evidence', id],
    queryFn: () => getEvidence(id),
    enabled: !!id && isExpanded,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useExplanation = (id: string, isExpanded: boolean) => {
  return useQuery({
    queryKey: ['explanation', id],
    queryFn: () => getExplanation(id),
    enabled: !!id && isExpanded,
    staleTime: 5 * 60 * 1000, // 5 minutes
  });
};

export const useAnalyze = () => {
  return useMutation({
    mutationFn: ({ hotelId, query }: { hotelId: string; query: string }) => analyzeHotel(hotelId, query),
  });
};

export const useCompare = () => {
  return useMutation({
    mutationFn: (hotelIds: string[]) => compareHotels(hotelIds),
  });
};

export const useHotelsCatalog = (filters: import('../lib/api').CatalogFilters, enabled: boolean = true) => {
  const { page = 1, limit = 20, sort_by = "trust_score_desc", ...restFilters } = filters;
  return useQuery({
    queryKey: ['hotels', restFilters, sort_by, page, limit],
    queryFn: () => getHotelsCatalog(filters),
    placeholderData: keepPreviousData,
    enabled,
  });
};

export const useFeaturedHotels = () => {
  return useQuery({
    queryKey: ['featured_hotels'],
    queryFn: () => import('../lib/api').then(m => m.getFeaturedHotels()),
  });
};
