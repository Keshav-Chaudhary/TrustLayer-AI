import { useState, useEffect, useRef } from "react";
import { useRouter } from "next/navigation";
import { Sparkles, MapPin, Building2, Wallet, Map } from "lucide-react";
import { useReveal } from "./useReveal";
import { detectQueryIntent } from "@/lib/intent";
import { useDebounce } from "@/hooks/useDebounce";
import { fetchSearchSuggestions } from "@/lib/api";
import { SearchSuggestion } from "@/types/api";

export function HeroSection() {
  const router = useRouter();
  const [destination, setDestination] = useState("");
  const [budget, setBudget] = useState("");
  const [purpose, setPurpose] = useState("");
  
  const { ref, isRevealed } = useReveal();

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
    if (showSuggestions) {
      loadSuggestions();
    }
  }, [debouncedDestination, showSuggestions]);

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
    if (destination.trim()) {
      let queryStr = `${destination}`;
      if (budget && budget !== "Select...") queryStr += ` ${budget}`;
      if (purpose && purpose !== "Select...") queryStr += ` for ${purpose}`;
      
      const intent = await detectQueryIntent(queryStr);
      if (intent.type === "catalog" && intent.area) {
        const params = new URLSearchParams();
        params.set("area", intent.area);
        if (budget) params.set("budget", budget);
        if (purpose) params.set("purpose", purpose);
        router.push(`/stays?${params.toString()}`);
      } else {
        router.push(`/search?q=${encodeURIComponent(queryStr)}`);
      }
    } else {
      router.push(`/stays`);
    }
  };

  const handleQuickSearch = async (chip: string) => {
    const intent = await detectQueryIntent(chip);
    if (intent.type === "catalog" && intent.area) {
      router.push(`/stays?area=${encodeURIComponent(intent.area)}`);
    } else {
      router.push(`/search?q=${encodeURIComponent(`${chip} hotels in delhi`)}`);
    }
  };

  return (
    <section className="relative w-full overflow-hidden bg-slate-900">
      {/* Background Image */}
      <div 
        className="absolute inset-0 z-0 bg-cover bg-center bg-no-repeat opacity-40"
        style={{ backgroundImage: 'url("https://images.unsplash.com/photo-1542314831-c6a4d14d285b?auto=format&fit=crop&w=2000&q=80")' }}
      />
      <div className="absolute inset-0 z-0 bg-gradient-to-t from-slate-950 via-slate-900/60 to-transparent" />

      {/* Content Container */}
      <div 
        ref={ref}
        className={`relative z-10 w-full max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 pt-32 pb-24 flex flex-col items-center text-center transition-all duration-1000 transform ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <h1 className="text-4xl sm:text-[56px] lg:text-[64px] font-extrabold text-white leading-[1.1] tracking-tight max-w-4xl drop-shadow-lg">
          Find Hotels You Can <span className="text-blue-400">Actually Trust</span>
        </h1>
        <p className="mt-6 text-lg sm:text-xl text-slate-200 max-w-2xl font-medium drop-shadow-md">
          AI-powered recommendations backed by verified reviews, transparent scoring, and explainable insights.
        </p>

        {/* Search Card */}
        <div className="w-full max-w-5xl mt-12 bg-white p-4 sm:p-6 rounded-[24px] shadow-2xl border border-slate-200 backdrop-blur-sm bg-white/95">
          <form onSubmit={handleSearch} className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-12 gap-4">
            
            <div className="lg:col-span-5 relative" ref={dropdownRef}>
              <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 ml-1 text-left flex items-center justify-between">
                <span>Destination or AI Custom Query</span>
                <span className="text-[10px] text-blue-600 font-extrabold flex items-center gap-1 bg-blue-50 px-2 py-0.5 rounded-full border border-blue-100">
                  <Sparkles className="w-3 h-3 text-blue-600" /> AI Powered
                </span>
              </label>
              <div className="relative">
                <MapPin className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <input
                  type="text"
                  placeholder="Where are you going? Or type 'Couple friendly with bathtub', 'Cleanliness >= 4.5'..."
                  value={destination}
                  onChange={(e) => {
                    setDestination(e.target.value);
                    setShowSuggestions(true);
                  }}
                  onKeyDown={handleKeyDown}
                  onFocus={() => setShowSuggestions(true)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-[16px] pl-12 pr-4 py-3.5 text-slate-900 placeholder-slate-400 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium text-base"
                  autoComplete="off"
                />
                {/* Suggestions Dropdown */}
                {showSuggestions && suggestions.length > 0 && (
                  <div className="absolute top-[60px] left-0 w-full bg-white border border-slate-200 rounded-[12px] shadow-lg overflow-hidden z-50 text-left">
                    {suggestions.map((s, idx) => {
                      // Highlight matching substring helper
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
                          onClick={() => {
                            setDestination(s.area);
                            setShowSuggestions(false);
                            setActiveSuggestionIndex(-1);
                          }}
                          className={`px-4 py-3 cursor-pointer flex items-center justify-between group border-b border-slate-100 last:border-0 transition-colors ${
                            idx === activeSuggestionIndex ? "bg-blue-50/70" : "hover:bg-slate-50"
                          }`}
                        >
                          <div className="flex flex-col">
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

            <div className="lg:col-span-3 relative">
              <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 ml-1 text-left">Travel Purpose</label>
              <div className="relative">
                <Building2 className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <select
                  value={purpose}
                  onChange={(e) => setPurpose(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-[16px] pl-12 pr-10 py-3.5 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium text-base appearance-none cursor-pointer"
                >
                  <option value="">Any Purpose</option>
                  <option value="family">Family Friendly</option>
                  <option value="business">Business</option>
                  <option value="couple">Couples</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
                  <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
              </div>
            </div>

            <div className="lg:col-span-2 relative">
              <label className="block text-[11px] font-bold text-slate-500 uppercase tracking-wider mb-1.5 ml-1 text-left">Budget</label>
              <div className="relative">
                <Wallet className="absolute left-4 top-1/2 -translate-y-1/2 w-5 h-5 text-slate-400" />
                <select
                  value={budget}
                  onChange={(e) => setBudget(e.target.value)}
                  className="w-full bg-slate-50 border border-slate-200 rounded-[16px] pl-12 pr-10 py-3.5 text-slate-900 focus:outline-none focus:ring-2 focus:ring-blue-500/20 focus:border-blue-500 transition-all font-medium text-base appearance-none cursor-pointer"
                >
                  <option value="">Any</option>
                  <option value="budget">Budget</option>
                  <option value="mid-range">Mid-range</option>
                  <option value="luxury">Luxury</option>
                </select>
                <div className="absolute right-4 top-1/2 -translate-y-1/2 pointer-events-none">
                  <svg className="w-4 h-4 text-slate-400" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path strokeLinecap="round" strokeLinejoin="round" strokeWidth="2" d="M19 9l-7 7-7-7"></path></svg>
                </div>
              </div>
            </div>

            <div className="lg:col-span-2 flex items-end">
              <button
                type="submit"
                className="w-full h-[52px] bg-blue-600 hover:bg-blue-700 text-white font-bold rounded-[16px] flex items-center justify-center gap-2 shadow-lg shadow-blue-600/20 transition-all hover:shadow-blue-600/40 hover:-translate-y-0.5"
              >
                <Sparkles className="w-5 h-5" />
                <span>AI Search</span>
              </button>
            </div>
            
          </form>

          {/* Quick Chips */}
          <div className="mt-5 pt-5 border-t border-slate-100 flex flex-wrap items-center gap-2">
            <span className="text-[11px] font-bold text-slate-400 uppercase tracking-wider mr-2">Try AI Queries:</span>
            {[
              "Couple friendly with bathtub", 
              "Best cleanliness ratings", 
              "Near Connaught Place under 4000", 
              "Quiet business stay with Wi-Fi", 
              "Luxury pool & spa in Aerocity"
            ].map((chip) => (
              <button
                key={chip}
                onClick={() => handleQuickSearch(chip)}
                className="px-3.5 py-1.5 text-xs font-semibold bg-slate-50 hover:bg-blue-50 text-slate-600 hover:text-blue-700 rounded-full border border-slate-200 hover:border-blue-200 transition-all cursor-pointer flex items-center gap-1"
              >
                <Sparkles className="w-3 h-3 text-blue-500" />
                <span>{chip}</span>
              </button>
            ))}
          </div>
        </div>

      </div>
    </section>
  );
}
