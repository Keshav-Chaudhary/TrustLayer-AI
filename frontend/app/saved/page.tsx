"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import { Button } from "@/components/ui/button";
import { Heart, Trash2, MapPin, Star, ShieldCheck, ArrowRight, Bookmark, FileText } from "lucide-react";
import { getHotelAnalysis } from "@/lib/api";
import { SAVED_COLLECTIONS } from "@/lib/ui-config";

export default function SavedPage() {
  const [savedIds, setSavedIds] = useState<string[]>([]);
  const [hotelsData, setHotelsData] = useState<any[]>([]);
  const [isLoading, setIsLoading] = useState(true);
  const [activeCollection, setActiveCollection] = useState("all");
  const [notes, setNotes] = useState<Record<string, string>>({});
  const [editingNoteId, setEditingNoteId] = useState<string | null>(null);
  const [tempNoteText, setTempNoteText] = useState("");

  const loadSavedHotels = async () => {
    setIsLoading(true);
    const saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    setSavedIds(saved);

    const savedNotes = JSON.parse(localStorage.getItem("trustlayer_hotel_notes") || "{}");
    setNotes(savedNotes);

    if (saved.length > 0) {
      try {
        const fetched = await Promise.all(
          saved.map(async (id: string) => {
            try {
              const res = await getHotelAnalysis(id);
              return res;
            } catch {
              return { hotel_id: id, name: `Bookmarked Hotel (${id})`, trust_score: 85, aspect_scores: {}, area: "Primary Location" };
            }
          })
        );
        setHotelsData(fetched);
      } catch (err) {
        console.error(err);
      }
    } else {
      setHotelsData([]);
    }
    setIsLoading(false);
  };

  useEffect(() => {
    loadSavedHotels();
  }, []);

  const handleSaveNote = (hotelId: string) => {
    const updated = { ...notes, [hotelId]: tempNoteText };
    setNotes(updated);
    localStorage.setItem("trustlayer_hotel_notes", JSON.stringify(updated));
    setEditingNoteId(null);
  };

  const handleRemove = (id: string) => {
    let saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    saved = saved.filter((sid: string) => sid !== id);
    localStorage.setItem("savedHotels", JSON.stringify(saved));
    loadSavedHotels();
  };

  const clearAll = () => {
    localStorage.removeItem("savedHotels");
    loadSavedHotels();
  };

  return (
    <div className="max-w-5xl mx-auto p-6 space-y-8 min-h-screen text-slate-900 bg-[#F8FAFC]">
      <div className="flex flex-col sm:flex-row justify-between sm:items-center border-b border-slate-200 pb-4 gap-4">
        <div>
          <h1 className="text-3xl font-extrabold tracking-tight text-slate-950 flex items-center gap-2">
            <Heart className="w-7 h-7 text-red-500 fill-red-500 animate-pulse" />
            Saved Collections
          </h1>
          <p className="text-xs text-slate-500 font-semibold mt-1">Organize your wishlist and custom stay notes.</p>
        </div>
        {savedIds.length > 0 && (
          <Button variant="outline" onClick={clearAll} className="h-9 px-4 text-xs font-bold border-slate-200 text-slate-700 rounded-xl flex items-center gap-1.5 cursor-pointer self-start sm:self-auto">
            <Trash2 className="w-3.5 h-3.5" />
            Clear All
          </Button>
        )}
      </div>

      {/* Collection Category Filter Pills */}
      <div className="flex items-center gap-2 overflow-x-auto pb-2">
        {SAVED_COLLECTIONS.map(col => (
          <button
            key={col.id}
            onClick={() => setActiveCollection(col.id)}
            className={`px-4 py-2 rounded-xl text-xs font-bold transition-all cursor-pointer whitespace-nowrap ${
              activeCollection === col.id
                ? "bg-blue-600 text-white shadow-xs"
                : "bg-white text-slate-600 border border-slate-200 hover:bg-slate-50"
            }`}
          >
            {col.label}
          </button>
        ))}
      </div>

      {isLoading ? (
        <div className="space-y-4">
          {[1, 2].map(i => (
            <div key={i} className="h-28 bg-slate-200 rounded-2xl animate-pulse" />
          ))}
        </div>
      ) : savedIds.length === 0 ? (
        <div className="text-center p-12 bg-white rounded-2xl border border-slate-200 shadow-sm max-w-md mx-auto space-y-4">
          <Heart className="w-12 h-12 text-slate-200 mx-auto" />
          <h2 className="text-lg font-bold text-slate-800">Your wishlist is empty</h2>
          <p className="text-xs text-slate-500 max-w-xs mx-auto">
            Search for trusted hotels, view AI analysis insights, and save your favorites here.
          </p>
          <div className="pt-2">
            <Link href="/stays">
              <Button className="h-9 px-5 text-xs font-bold rounded-xl shadow-sm cursor-pointer">Go to Stays</Button>
            </Link>
          </div>
        </div>
      ) : (
        <div className="space-y-4">
          {hotelsData.map(h => (
            <div key={h.hotel_id} className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm flex flex-col sm:flex-row gap-5 items-center justify-between hover:shadow-md transition-shadow">
              
              <div className="flex flex-col sm:flex-row gap-4 items-center w-full sm:w-auto">
                {/* Visual Thumbnail */}
                <div className="w-20 h-20 rounded-xl bg-slate-100 border border-slate-200 shrink-0 flex items-center justify-center text-slate-400">
                  <svg className="w-6 h-6" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path strokeLinecap="round" strokeLinejoin="round" strokeWidth="1.5" d="M19 21V5a2 2 0 00-2-2H7a2 2 0 00-2 2v16m14 0h2m-2 0h-5m-9 0H3m2 0h5M9 7h1m-1 4h1m4-4h1m-1 4h1m-5 10v-5a1 1 0 011-1h2a1 1 0 011 1v5m-4 0h4" />
                  </svg>
                </div>

                <div className="space-y-1.5 text-center sm:text-left min-w-0">
                  <div className="flex flex-wrap items-center justify-center sm:justify-start gap-2">
                    <h3 className="font-extrabold text-lg text-slate-950 truncate max-w-[250px]">{h.name}</h3>
                    <span className="text-[9px] px-2 py-0.5 bg-amber-50 text-amber-700 font-bold rounded-full border border-amber-200">
                      Saved
                    </span>
                  </div>
                  <div className="flex flex-wrap items-center justify-center sm:justify-start text-xs text-[#475569] gap-x-2.5 gap-y-1">
                    <span className="flex items-center gap-0.5">
                      <MapPin className="w-3.5 h-3.5" />
                      {h.area || "Primary Location"}
                    </span>
                    <span>•</span>
                    <span className="flex items-center gap-0.5 font-bold text-slate-700">
                      <Star className="w-3.5 h-3.5 fill-amber-400 stroke-amber-400" />
                      4.7
                    </span>
                    <span className="text-slate-400">(Reviews available)</span>
                  </div>
                  {/* Custom User Stay Note */}
                  <div className="pt-2 text-left">
                    {editingNoteId === h.hotel_id ? (
                      <div className="flex items-center gap-2 mt-1">
                        <input
                          type="text"
                          value={tempNoteText}
                          onChange={(e) => setTempNoteText(e.target.value)}
                          placeholder="Add custom note (e.g. booked room with balcony)..."
                          className="text-xs bg-slate-50 border border-slate-300 rounded-lg px-2.5 py-1 text-slate-800 focus:outline-none focus:ring-1 focus:ring-blue-500 w-full sm:w-64"
                        />
                        <button
                          onClick={() => handleSaveNote(h.hotel_id)}
                          className="text-[11px] font-bold bg-blue-600 text-white px-2.5 py-1 rounded-lg hover:bg-blue-700 transition-colors"
                        >
                          Save
                        </button>
                      </div>
                    ) : (
                      <div className="flex items-center gap-2 text-[11px] text-slate-600 bg-slate-50 border border-slate-200/80 px-2.5 py-1 rounded-lg inline-flex">
                        <FileText className="w-3 h-3 text-slate-400 shrink-0" />
                        <span className="truncate max-w-[200px]">
                          {notes[h.hotel_id] || "No custom note added"}
                        </span>
                        <button
                          onClick={() => {
                            setEditingNoteId(h.hotel_id);
                            setTempNoteText(notes[h.hotel_id] || "");
                          }}
                          className="text-[10px] text-blue-600 font-bold hover:underline cursor-pointer ml-1"
                        >
                          {notes[h.hotel_id] ? "Edit" : "+ Add Note"}
                        </button>
                      </div>
                    )}
                  </div>
                </div>
              </div>

              {/* Right actions */}
              <div className="flex items-center gap-5 w-full sm:w-auto justify-between sm:justify-end border-t sm:border-t-0 border-slate-100 pt-4 sm:pt-0 shrink-0">
                <div className="text-left sm:text-right">
                  <span className="block text-[10px] uppercase font-bold text-slate-400 tracking-wider">Trust Score</span>
                  <div className="flex items-center gap-1 mt-0.5">
                    <ShieldCheck className="w-3.5 h-3.5 text-green-600" />
                    <span className="text-lg font-black text-slate-900">{h.trust_score.toFixed(1)}</span>
                  </div>
                </div>

                <div className="flex items-center gap-2">
                  <Button 
                    onClick={() => handleRemove(h.hotel_id)} 
                    variant="outline" 
                    className="h-9 w-9 p-0 rounded-xl border-slate-200 text-slate-400 hover:text-red-600 hover:bg-red-50 hover:border-red-100 cursor-pointer"
                  >
                    <Trash2 className="w-4 h-4" />
                  </Button>
                  <Link href={`/hotel/${h.hotel_id}`}>
                    <Button className="h-9 px-4 text-xs font-bold bg-slate-100 hover:bg-slate-200 text-slate-900 rounded-xl border border-slate-200 flex items-center gap-1 cursor-pointer">
                      <span>View</span>
                      <ArrowRight className="w-3.5 h-3.5" />
                    </Button>
                  </Link>
                </div>
              </div>

            </div>
          ))}
        </div>
      )}
    </div>
  );
}
