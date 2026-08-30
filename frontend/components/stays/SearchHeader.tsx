import { useState, useEffect, useRef } from "react";
import { useRouter, useSearchParams } from "next/navigation";
import { MapPin, Wallet, Building2, Search, Map, Check, X, History, ArrowRight } from "lucide-react";
import { useDebounce } from "@/hooks/useDebounce";
import { fetchSearchSuggestions } from "@/lib/api";
import { SearchSuggestion } from "@/types/api";
import { detectQueryIntent } from "@/lib/intent";
import { useSearchFilters } from "@/lib/search-state";

export function SearchHeader() {
  const router = useRouter();
  const searchParams = useSearchParams();
  
  const { 
    budget: activeBudget, 
    purpose: activePurpose, 
    cleanliness: activeCleanliness, 
    toggleFilter, 
    setFilter 
  } = useSearchFilters();
  
  const [destination, setDestination] = useState(
    searchParams?.get("q") || searchParams?.get("area") || ""
  );
  const [budget, setBudget] = useState(searchParams?.get("budget") || "");
  const [purpose, setPurpose] = useState(searchParams?.get("purpose") || "");
  
  const [loadingPills, setLoadingPills] = useState<Record<string, boolean>>({});
  const [recentSearches, setRecentSearches] = useState<string[]>([]);

  useEffect(() => {
    if (typeof window !== "undefined") {
      const saved = JSON.parse(localStorage.getItem("trustlayer_recent_searches") || "[]");
      setRecentSearches(saved);
    }
  }, []);

  const saveRecentSearch = (queryStr: string) => {
    if (!queryStr.trim() || typeof window === "undefined") return;
    const existing = JSON.parse(localStorage.getItem("trustlayer_recent_searches") || "[]");
    const filtered = existing.filter((q: string) => q.toLowerCase() !== queryStr.toLowerCase());
    const updated = [queryStr, ...filtered].slice(0, 5);
    localStorage.setItem("trustlayer_recent_searches", JSON.stringify(updated));
    setRecentSearches(updated);
  };

  useEffect(() => {
    setDestination(searchParams?.get("q") || searchParams?.get("area") || "");
    setBudget(searchParams?.get("budget") || "");
    setPurpose(searchParams?.get("purpose") || "");
  }, [searchParams]);
  
  const [suggestions, setSuggestions] = useState<SearchSuggestion[]>([]);
  const [showSuggestions, setShowSuggestions] = useState(false);
  const [activeSuggestionIndex, setActiveSuggestionIndex] = useState(-1);
  const dropdownRef = useRef<HTMLDivElement>(null);
  
  const debouncedDestination = useDebounce(destination, 300);

  useEffect(() => {
    async function loadSuggestions() {
      if (!debouncedDestination.trim()) {
        setSuggestions([]);
        return;
      }
      try {
        const res = await fetchSearchSuggestions(debouncedDestination);
        setSuggestions(res.suggestions || []);
        setActiveSuggestionIndex(-1);
      } catch (err) {
        console.error("Failed to fetch suggestions:", err);
      }
    }
    // Only fetch if user is typing and dropdown is expected to show
    if (showSuggestions) {
      loadSuggestions();
    }
  }, [debouncedDestination, showSuggestions]);

  // Handle clicking outside to close suggestions
  useEffect(() => {
    function handleClickOutside(event: MouseEvent) {
      if (dropdownRef.current && !dropdownRef.current.contains(event.target as Node)) {
        setShowSuggestions(false);
        setActiveSuggestionIndex(-1);
      }
    }
    document.addEventListener("mousedown", handleClickOutside);
    return () => document.removeEventListener("mousedown", handleClickOutside);
  }, []);

  const handleKeyDown = (e: React.KeyboardEvent<HTMLInputElement>) => {
    if (showSuggestions && suggestions.length > 0) {
      if (e.key === "ArrowDown") {
        e.preventDefault();
        setActiveSuggestionIndex((prev) => (prev + 1) % suggestions.length);
      } else if (e.key === "ArrowUp") {
        e.preventDefault();
        setActiveSuggestionIndex((prev) => (prev - 1 + suggestions.length) % suggestions.length);
      } else if (e.key === "Enter") {
        if (activeSuggestionIndex >= 0 && activeSuggestionIndex < suggestions.length) {
          e.preventDefault();
          const selected = suggestions[activeSuggestionIndex];
          setDestination(selected.area);
          setShowSuggestions(false);
          setActiveSuggestionIndex(-1);
        }
      } else if (e.key === "Escape") {
        setShowSuggestions(false);
        setActiveSuggestionIndex(-1);
      }
    }
  };

  const handleSearch = async (e: React.FormEvent) => {
    e.preventDefault();
    setShowSuggestions(false);
    
    if (destination.trim()) {
      saveRecentSearch(destination.trim());
      const intent = await detectQueryIntent(destination);
      if (intent.type === "ai") {
        let queryStr = destination;
        if (budget) queryStr += ` ${budget}`;
        if (purpose) queryStr += ` for ${purpose}`;
        router.push(`/search?q=${encodeURIComponent(queryStr)}`);
        return;
      }
    }

    const params = new URLSearchParams(searchParams?.toString() || "");
    if (destination) params.set("area", destination);
    else params.delete("area");
    
    if (budget) params.set("budget", budget);
    else params.delete("budget");
    
    if (purpose) params.set("purpose", purpose);
    else params.delete("purpose");
    
    router.push(`/stays?${params.toString()}`);
  };

  const handlePillClick = (key: string, value: string) => {
    const pillKey = `${key}-${value}`;
    if (loadingPills[pillKey]) return;
    
    setLoadingPills(prev => ({ ...prev, [pillKey]: true }));
    toggleFilter(key, value);
    
    setTimeout(() => {
      setLoadingPills(prev => ({ ...prev, [pillKey]: false }));
    }, 300);
  };

  const handleSelectSuggestion = (suggestion: SearchSuggestion) => {
    setDestination(suggestion.area);
    setShowSuggestions(false);
    saveRecentSearch(suggestion.area);
    const params = new URLSearchParams(searchParams?.toString() || "");
    params.set("area", suggestion.area);
    router.push(`/stays?${params.toString()}`);
  };

  return (
    <div className="w-full bg-white rounded-[20px] shadow-[0_1px_3px_rgba(0,0,0,0.08)] p-6 mb-8 border border-slate-200 sticky top-[88px] z-30">
      <form onSubmit={handleSearch} className="grid grid-cols-1 md:grid-cols-12 gap-4">
        
        {/* Destination */}
        <div className="md:col-span-5 relative" ref={dropdownRef}>
          <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 ml-1 text-left flex items-center justify-between">
            <span>Destination or AI Custom Query</span>
            <span className="text-[10px] text-[#2563EB] font-extrabold flex items-center gap-1 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-100">
              AI Search
            </span>
          </label>
          <div className="relative">
            <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <input
              type="text"
              placeholder="Where are you going, or ask AI anything..."
              value={destination}
              onChange={(e) => {
                setDestination(e.target.value);
                setShowSuggestions(true);
              }}
              onKeyDown={handleKeyDown}
              onFocus={() => setShowSuggestions(true)}
              className="w-full h-[52px] bg-slate-50 border border-slate-200 rounded-[12px] pl-11 pr-10 text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all font-medium text-[16px]"
              autoComplete="off"
            />

            {/* Quick Clear Input Button */}
            {destination && (
              <button
                type="button"
                onClick={() => {
                  setDestination("");
                  setShowSuggestions(false);
                }}
                className="absolute right-3 top-1/2 -translate-y-1/2 w-6 h-6 rounded-full text-slate-400 hover:text-slate-600 hover:bg-slate-200/60 flex items-center justify-center transition-colors cursor-pointer"
                title="Clear search"
              >
                <X className="w-3.5 h-3.5" />
              </button>
            )}

            {/* Recent Searches Dropdown (Empty input focus) */}
            {showSuggestions && !destination.trim() && recentSearches.length > 0 && (
              <div className="absolute top-[60px] left-0 w-full bg-white border border-slate-200 rounded-[12px] shadow-lg overflow-hidden z-50 text-left">
                <div className="px-4 py-2 bg-slate-50 border-b border-slate-100 flex items-center justify-between text-xs font-bold text-slate-500 uppercase tracking-wider">
                  <span className="flex items-center gap-1.5"><History className="w-3.5 h-3.5 text-blue-600" /> Recent Searches</span>
                  <button 
                    type="button"
                    onClick={() => {
                      localStorage.removeItem("trustlayer_recent_searches");
                      setRecentSearches([]);
                    }}
                    className="text-[10px] text-slate-400 hover:text-red-600 transition-colors cursor-pointer"
                  >
                    Clear history
                  </button>
                </div>
                {recentSearches.map((qs, idx) => (
                  <div
                    key={idx}
                    onClick={() => {
                      setDestination(qs);
                      setShowSuggestions(false);
                      saveRecentSearch(qs);
                      router.push(`/search?q=${encodeURIComponent(qs)}`);
                    }}
                    className="px-4 py-3 cursor-pointer flex items-center justify-between group border-b border-slate-100 last:border-0 hover:bg-blue-50/70 transition-colors"
                  >
                    <span className="font-semibold text-slate-800 text-[14px] group-hover:text-blue-600 transition-colors">{qs}</span>
                    <ArrowRight className="w-4 h-4 text-slate-400 group-hover:text-blue-600 transition-colors" />
                  </div>
                ))}
              </div>
            )}

            {/* Autocomplete Suggestions Dropdown */}
            {showSuggestions && destination.trim().length > 0 && suggestions.length > 0 && (
              <div className="absolute top-[60px] left-0 w-full bg-white border border-slate-200 rounded-[12px] shadow-lg overflow-hidden z-50">
                {suggestions.map((s, idx) => {
                  const matchIdx = s.area.toLowerCase().indexOf(destination.toLowerCase());
                  const hasMatch = matchIdx >= 0 && destination.length > 0;
                  
                  const renderAreaLabel = () => {
                    if (!hasMatch) return s.area;
                    const part1 = s.area.substring(0, matchIdx);
                    const part2 = s.area.substring(matchIdx, matchIdx + destination.length);
                    const part3 = s.area.substring(matchIdx + destination.length);
                    return (
                      <span>
                        {part1}
                        <strong className="text-blue-600 font-extrabold">{part2}</strong>
                        {part3}
                      </span>
                    );
                  };

                  return (
                    <div
                      key={idx}
                      onClick={() => handleSelectSuggestion(s)}
                      className={`px-4 py-3 cursor-pointer flex items-center justify-between group border-b border-slate-100 last:border-0 transition-colors ${
                        idx === activeSuggestionIndex ? "bg-blue-50/70" : "hover:bg-slate-50"
                      }`}
                    >
                      <div className="flex flex-col text-left">
                        <span className="font-semibold text-slate-800 text-[15px]">{renderAreaLabel()}</span>
                        <span className="text-xs text-slate-500 font-medium flex items-center gap-1 mt-0.5">
                          <Map className="w-3 h-3 text-slate-400" /> {s.cluster}
                        </span>
                      </div>
                      <span className="text-xs font-bold text-slate-400 bg-slate-100 px-2 py-1 rounded-full group-hover:bg-[#2563EB] group-hover:text-white transition-colors">
                        {s.count} {s.count === 1 ? 'hotel' : 'hotels'}
                      </span>
                    </div>
                  );
                })}
              </div>
            )}
          </div>
        </div>

        {/* Travel Purpose */}
        <div className="md:col-span-3 relative">
          <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 ml-1">Travel Purpose</label>
          <div className="relative">
            <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <select
              value={purpose}
              onChange={(e) => setPurpose(e.target.value)}
              className="w-full h-[52px] bg-slate-50 border border-slate-200 rounded-[12px] pl-11 pr-10 text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all font-medium text-[16px] appearance-none cursor-pointer"
            >
              <option value="">Select...</option>
              <option value="family">Family Friendly</option>
              <option value="business">Business</option>
              <option value="couple">Couples</option>
            </select>
            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>
        </div>

        {/* Budget */}
        <div className="md:col-span-2 relative">
          <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 ml-1">Budget</label>
          <div className="relative">
            <Wallet className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
            <select
              value={budget}
              onChange={(e) => setBudget(e.target.value)}
              className="w-full h-[52px] bg-slate-50 border border-slate-200 rounded-[12px] pl-11 pr-10 text-[#0F172A] focus:outline-none focus:ring-2 focus:ring-[#2563EB]/20 focus:border-[#2563EB] transition-all font-medium text-[16px] appearance-none cursor-pointer"
            >
              <option value="">Select...</option>
              <option value="budget">Budget</option>
              <option value="mid-range">Mid-range</option>
              <option value="luxury">Luxury</option>
            </select>
            <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
              <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
            </div>
          </div>
        </div>

        {/* Search Button */}
        <div className="md:col-span-2 flex items-end">
          <button
            type="submit"
            className="w-full h-[52px] bg-[#2563EB] hover:bg-blue-700 text-white font-bold rounded-[12px] flex items-center justify-center gap-2 shadow-sm transition-all hover:-translate-y-0.5 cursor-pointer"
          >
            <Search className="w-5 h-5" />
            <span>Update Search</span>
          </button>
        </div>
        
      </form>

      {/* Quick Filter Pills */}
      <div className="mt-5 pt-5 border-t border-slate-100 flex flex-wrap items-center gap-[12px]">
        {/* Family Friendly */}
        {activePurpose === "family" ? (
          <button
            type="button"
            onClick={() => handlePillClick("purpose", "family")}
            disabled={loadingPills["purpose-family"]}
            className="h-[32px] px-3 gap-1.5 flex items-center justify-between text-xs rounded-full border bg-[#2563EB]/10 border-[#2563EB]/30 text-[#2563EB] font-bold shadow-[0_4px_12px_rgba(37,99,235,0.15)] hover:bg-[#2563EB]/15 transition-all duration-180 select-none cursor-pointer"
          >
            <div className="flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5 text-[#2563EB] fill-none stroke-2" />
              <span>Family Friendly</span>
            </div>
            <X className="w-3 h-3 text-[#2563EB]/70 hover:text-[#2563EB] ml-0.5 shrink-0" />
          </button>
        ) : (
          <button
            type="button"
            onClick={() => handlePillClick("purpose", "family")}
            disabled={loadingPills["purpose-family"]}
            className="h-[32px] px-3 gap-1.5 flex items-center text-xs rounded-full border bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100 hover:border-slate-350 transition-all duration-180 select-none cursor-pointer"
          >
            <span className="w-3 h-3 rounded-full bg-slate-300 shrink-0" />
            <span>Family Friendly</span>
          </button>
        )}

        {/* Luxury Stays */}
        {activeBudget === "luxury" ? (
          <button
            type="button"
            onClick={() => handlePillClick("budget", "luxury")}
            disabled={loadingPills["budget-luxury"]}
            className="h-[32px] px-3 gap-1.5 flex items-center justify-between text-xs rounded-full border bg-[#2563EB]/10 border-[#2563EB]/30 text-[#2563EB] font-bold shadow-[0_4px_12px_rgba(37,99,235,0.15)] hover:bg-[#2563EB]/15 transition-all duration-180 select-none cursor-pointer"
          >
            <div className="flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5 text-[#2563EB] fill-none stroke-2" />
              <span>Luxury Stays</span>
            </div>
            <X className="w-3 h-3 text-[#2563EB]/70 hover:text-[#2563EB] ml-0.5 shrink-0" />
          </button>
        ) : (
          <button
            type="button"
            onClick={() => handlePillClick("budget", "luxury")}
            disabled={loadingPills["budget-luxury"]}
            className="h-[32px] px-3 gap-1.5 flex items-center text-xs rounded-full border bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100 hover:border-slate-350 transition-all duration-180 select-none cursor-pointer"
          >
            <span className="w-3 h-3 rounded-full bg-slate-300 shrink-0" />
            <span>Luxury Stays</span>
          </button>
        )}

        {/* Business Hotels */}
        {activePurpose === "business" ? (
          <button
            type="button"
            onClick={() => handlePillClick("purpose", "business")}
            disabled={loadingPills["purpose-business"]}
            className="h-[32px] px-3 gap-1.5 flex items-center justify-between text-xs rounded-full border bg-[#2563EB]/10 border-[#2563EB]/30 text-[#2563EB] font-bold shadow-[0_4px_12px_rgba(37,99,235,0.15)] hover:bg-[#2563EB]/15 transition-all duration-180 select-none cursor-pointer"
          >
            <div className="flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5 text-[#2563EB] fill-none stroke-2" />
              <span>Business Hotels</span>
            </div>
            <X className="w-3 h-3 text-[#2563EB]/70 hover:text-[#2563EB] ml-0.5 shrink-0" />
          </button>
        ) : (
          <button
            type="button"
            onClick={() => handlePillClick("purpose", "business")}
            disabled={loadingPills["purpose-business"]}
            className="h-[32px] px-3 gap-1.5 flex items-center text-xs rounded-full border bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100 hover:border-slate-350 transition-all duration-180 select-none cursor-pointer"
          >
            <span className="w-3 h-3 rounded-full bg-slate-300 shrink-0" />
            <span>Business Hotels</span>
          </button>
        )}

        {/* Best Cleanliness */}
        {activeCleanliness === "4.5" ? (
          <button
            type="button"
            onClick={() => handlePillClick("cleanliness", "4.5")}
            disabled={loadingPills["cleanliness-4.5"]}
            className="h-[32px] px-3 gap-1.5 flex items-center justify-between text-xs rounded-full border bg-[#2563EB]/10 border-[#2563EB]/30 text-[#2563EB] font-bold shadow-[0_4px_12px_rgba(37,99,235,0.15)] hover:bg-[#2563EB]/15 transition-all duration-180 select-none cursor-pointer"
          >
            <div className="flex items-center gap-1.5">
              <Check className="w-3.5 h-3.5 text-[#2563EB] fill-none stroke-2" />
              <span>Best Cleanliness</span>
            </div>
            <X className="w-3 h-3 text-[#2563EB]/70 hover:text-[#2563EB] ml-0.5 shrink-0" />
          </button>
        ) : (
          <button
            type="button"
            onClick={() => handlePillClick("cleanliness", "4.5")}
            disabled={loadingPills["cleanliness-4.5"]}
            className="h-[32px] px-3 gap-1.5 flex items-center text-xs rounded-full border bg-slate-50 border-slate-200 text-slate-600 hover:bg-slate-100 hover:border-slate-350 transition-all duration-180 select-none cursor-pointer"
          >
            <span className="w-3 h-3 rounded-full bg-slate-300 shrink-0" />
            <span>Best Cleanliness</span>
          </button>
        )}
      </div>
    </div>
  );
}
