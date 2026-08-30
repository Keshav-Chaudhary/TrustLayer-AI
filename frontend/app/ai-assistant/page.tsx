"use client";

import { useState, useRef, useEffect } from "react";
import { useChatStore } from "@/hooks/useChatStore";
import { streamChat } from "@/lib/stream";
import { Button } from "@/components/ui/button";
import { Bot, Send, Sparkles, AlertCircle, Compass, HelpCircle } from "lucide-react";
import { getHotelAnalysis } from "@/lib/api";

export default function AIAssistantPage() {
  const { activeHotelId, activeHotelName, openChat } = useChatStore();
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState<{ role: "user" | "ai"; content: string; time: string }[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);

  // We can let user choose a hotel to chat about in a dropdown
  const [hotelsList, setHotelsList] = useState<any[]>([]);

  useEffect(() => {
    // Look up saved hotels to populate as context options
    const saved = JSON.parse(localStorage.getItem("savedHotels") || "[]");
    if (saved.length > 0) {
      Promise.all(
        saved.slice(0, 5).map(async (id: string) => {
          try {
            const h = await getHotelAnalysis(id);
            return { hotel_id: h.hotel_id, name: h.name };
          } catch {
            return { hotel_id: id, name: id };
          }
        })
      ).then(setHotelsList);
    }
  }, []);

  useEffect(() => {
    if (messagesEndRef.current) {
      messagesEndRef.current.scrollIntoView({ behavior: "smooth" });
    }
  }, [chatHistory]);

  const handleSend = async (e?: React.FormEvent) => {
    if (e) e.preventDefault();
    if (!query.trim() || isStreaming) return;

    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }
    abortControllerRef.current = new AbortController();

    const userMsg = query;
    const timeStr = new Date().toLocaleTimeString([], { hour: '2-digit', minute: '2-digit' });
    setQuery("");
    setChatHistory((prev) => [
      ...prev,
      { role: "user", content: userMsg, time: timeStr },
      { role: "ai", content: "", time: timeStr }
    ]);
    setIsStreaming(true);

    try {
      await streamChat(
        userMsg,
        activeHotelId || "",
        (chunk) => {
          setChatHistory((prev) => {
            const newHistory = [...prev];
            const last = newHistory[newHistory.length - 1];
            if (last && last.role === "ai") {
              last.content += chunk;
            }
            return newHistory;
          });
        },
        abortControllerRef.current.signal
      );
    } catch (err: any) {
      if (err.name !== 'AbortError') {
        console.error("Chat error:", err);
      }
    } finally {
      setIsStreaming(false);
    }
  };

  return (
    <div className="max-w-6xl mx-auto px-4 sm:px-6 lg:px-8 py-8 h-[calc(100vh-4rem)] flex flex-col md:flex-row gap-6 text-slate-900 bg-[#F8FAFC]">
      
      {/* Left panel: Context chooser and tips */}
      <div className="w-full md:w-80 shrink-0 flex flex-col gap-6">
        
        {/* Title details */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-2">
          <h1 className="text-2xl font-black text-slate-950 tracking-tight leading-none flex items-center gap-1.5">
            <Bot className="w-6 h-6 text-blue-600 animate-pulse" />
            AI Travel Copilot
          </h1>
          <p className="text-xs text-slate-500 font-semibold leading-relaxed">
            A full-screen workspace to analyze review evidence and cross-examine recommendations.
          </p>
        </div>

        {/* Context card selector */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-4">
          <h3 className="text-xs font-black uppercase text-slate-400 tracking-wider">Select Active Context</h3>
          
          <div className="space-y-2">
            <label className="text-[10px] font-bold text-slate-500 uppercase tracking-wider block">Currently Auditing</label>
            <select
              value={activeHotelId || ""}
              onChange={(e) => {
                const sel = hotelsList.find(h => h.hotel_id === e.target.value);
                if (sel) {
                  openChat(sel.hotel_id, sel.name);
                } else if (e.target.value === "") {
                  openChat(null, null);
                }
              }}
              className="w-full bg-slate-50 border border-slate-200 rounded-xl px-3 py-2.5 text-xs text-slate-800 focus:outline-none focus:border-blue-500 cursor-pointer"
            >
              <option value="">General Database Search</option>
              {hotelsList.map(h => (
                <option key={h.hotel_id} value={h.hotel_id}>
                  {h.name}
                </option>
              ))}
            </select>
          </div>

          {activeHotelId ? (
            <div className="p-3.5 bg-blue-50/50 border border-blue-100 rounded-xl space-y-1.5">
              <span className="text-[9px] uppercase font-bold text-blue-500 tracking-wider">Active Hotel</span>
              <p className="font-extrabold text-xs text-slate-800 truncate">{activeHotelName}</p>
            </div>
          ) : (
            <div className="p-3.5 bg-slate-50 border border-slate-100 rounded-xl text-xs text-slate-400">
              No active hotel page context attached. Prompt search queries will scan the entire hybrid database collections.
            </div>
          )}
        </div>

        {/* Tips / FAQ */}
        <div className="bg-white p-5 rounded-2xl border border-slate-200 shadow-sm space-y-3.5">
          <h3 className="text-xs font-black uppercase text-slate-400 tracking-wider">Example Prompts</h3>
          <ul className="space-y-2 text-xs">
            {["Is the breakfast really good for children?", "Are there check-in delays or parking issues?", "Compare value score evidence."].map(pr => (
              <li
                key={pr}
                onClick={() => setQuery(pr)}
                className="p-2 border border-slate-100 rounded-lg hover:bg-slate-50 text-slate-600 hover:text-blue-600 transition-colors cursor-pointer"
              >
                "{pr}"
              </li>
            ))}
          </ul>
        </div>

      </div>

      {/* Right panel: Chat UI */}
      <div className="flex-1 bg-slate-900 border border-slate-800 rounded-2xl text-white flex flex-col h-full overflow-hidden shadow-xl">
        {/* Chat Feed */}
        <div className="flex-1 overflow-y-auto p-6 space-y-4">
          {chatHistory.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-500 max-w-sm mx-auto">
              <Sparkles className="w-12 h-12 text-slate-700 mb-4 animate-bounce" />
              <p className="text-sm font-bold text-slate-400">Welcome to your explainable Travel Assistant workspace</p>
              <p className="text-xs text-slate-500 mt-2">
                Type queries to run hybrid search logic. All summaries are strictly verified against ChromaDB review evidence.
              </p>
            </div>
          )}

          {chatHistory.map((msg, i) => (
            <div key={i} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"} gap-1.5`}>
              <div className="flex items-center gap-1.5 text-xs text-slate-400 font-medium px-1">
                <span>{msg.role === "user" ? "You" : "AI Copilot"}</span>
                <span className="text-[10px] text-slate-600">•</span>
                <span>{msg.time}</span>
              </div>
              <div
                className={`max-w-[80%] rounded-2xl px-4 py-3.5 text-sm leading-relaxed border ${
                  msg.role === "user"
                    ? "bg-blue-950 text-blue-50 border-blue-900/50"
                    : "bg-slate-800 text-slate-100 border-slate-700/50"
                }`}
              >
                {msg.content === "" && isStreaming ? (
                  <span className="flex items-center gap-1">
                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce delay-75" />
                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce delay-150" />
                    <span className="w-1.5 h-1.5 bg-blue-400 rounded-full animate-bounce delay-225" />
                  </span>
                ) : (
                  <p className="whitespace-pre-line">{msg.content}</p>
                )}
              </div>
            </div>
          ))}
        </div>

        {/* Input Bar */}
        <form onSubmit={handleSend} className="p-4 border-t border-slate-800 bg-slate-950/40 flex flex-col gap-2">
          <div className="relative flex items-center bg-slate-850 rounded-xl border border-slate-700 focus-within:border-blue-500 transition-colors">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask about cleanliness, breakfast, family friendly reviews..."
              className="flex-1 bg-transparent px-4 py-3.5 outline-none resize-none text-sm placeholder-slate-500 h-12 text-white"
              rows={1}
            />
            <Button
              type="submit"
              size="icon"
              className="absolute right-2 bg-blue-600 hover:bg-blue-500 text-white rounded-lg w-9 h-9 flex items-center justify-center shrink-0 shadow cursor-pointer"
              disabled={!query.trim() || isStreaming}
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <div className="flex justify-between items-center text-[10px] text-slate-500 px-1">
            <span>Verified evidence-backed grounding validation active</span>
            {isStreaming && (
              <button
                type="button"
                onClick={() => {
                  if (abortControllerRef.current) abortControllerRef.current.abort();
                  setIsStreaming(false);
                }}
                className="text-red-400 hover:text-red-300 font-bold cursor-pointer"
              >
                Stop generation
              </button>
            )}
          </div>
        </form>
      </div>

    </div>
  );
}
