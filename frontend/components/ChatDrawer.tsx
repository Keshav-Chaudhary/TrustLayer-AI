"use client";

import { useState, useRef, useEffect } from "react";
import { useChatStore } from "@/hooks/useChatStore";
import { streamChat } from "@/lib/stream";
import { Button } from "@/components/ui/button";
import { X, Send, Bot, Sparkles } from "lucide-react";
import { usePathname } from "next/navigation";

export function ChatDrawer() {
  const { isOpen, closeChat, activeHotelId, activeHotelName, openChat } = useChatStore();
  const [query, setQuery] = useState("");
  const [chatHistory, setChatHistory] = useState<{ role: "user" | "ai"; content: string; time: string }[]>([]);
  const [isStreaming, setIsStreaming] = useState(false);
  const abortControllerRef = useRef<AbortController | null>(null);
  const messagesEndRef = useRef<HTMLDivElement | null>(null);
  const pathname = usePathname();

  // Handle auto-attaching hotel context based on pathname URL
  useEffect(() => {
    if (pathname.startsWith("/hotel/")) {
      const hotelId = pathname.split("/hotel/")[2]?.split("/")[0] || pathname.split("/hotel/")[1];
      if (hotelId && hotelId !== activeHotelId) {
        const cachedName = localStorage.getItem(`hotel_name_${hotelId}`) || "This Hotel";
        openChat(hotelId, cachedName);
      }
    }
  }, [pathname, activeHotelId, openChat]);

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

  if (!isOpen) return null;

  return (
    <div className="fixed inset-0 z-50 flex justify-end bg-black/40 backdrop-blur-sm transition-all duration-300">
      {/* Click outside to close */}
      <div className="flex-1" onClick={closeChat} />

      {/* Drawer Body - Re-styled to exact spec */}
      <div className="w-[420px] bg-[#FFFFFF] rounded-l-[24px] text-[#0F172A] flex flex-col h-full shadow-modal relative overflow-hidden">
        
        {/* Drawer Header */}
        <div className="flex justify-between items-center p-5 border-b border-[#E2E8F0] bg-white">
          <div className="flex items-center gap-2 text-[#2563EB] font-extrabold text-lg">
            <Bot className="w-5.5 h-5.5" />
            <span>AI Travel Assistant</span>
          </div>
          <button onClick={closeChat} className="p-1.5 hover:bg-slate-100 rounded-full text-slate-400 hover:text-slate-900 transition-colors cursor-pointer">
            <X className="w-5 h-5" />
          </button>
        </div>

        {/* Current Context Card */}
        {activeHotelId && (
          <div className="m-4 p-4.5 bg-[#F1F5F9] rounded-[16px] border border-[#E2E8F0] flex flex-col gap-1.5 shadow-xs">
            <div className="flex justify-between items-center">
              <span className="text-[10px] uppercase font-bold text-[#475569] tracking-wider">Current context</span>
              <span className="text-[9px] px-2.5 py-0.5 bg-blue-50 text-[#2563EB] font-bold rounded-full border border-blue-200 shadow-xs">
                Hotel page
              </span>
            </div>
            <h4 className="font-extrabold text-slate-900 text-sm truncate">{activeHotelName || activeHotelId}</h4>
            <p className="text-xs text-[#475569] leading-relaxed">
              Ask about cleanliness, family suitability, business travel, or complaints.
            </p>
          </div>
        )}

        {/* Message Feed */}
        <div className="flex-1 overflow-y-auto p-5 space-y-4 scrollbar-thin bg-[#F8FAFC]">
          {chatHistory.length === 0 && (
            <div className="h-full flex flex-col items-center justify-center text-center p-6 text-slate-400 max-w-[280px] mx-auto">
              <Sparkles className="w-10 h-10 text-slate-300 mb-3 animate-bounce" />
              <p className="text-sm font-bold text-slate-700">Audit hotel review evidence</p>
              <p className="text-xs text-slate-500 mt-1">Grounded analysis checks are active. Hallucinations are prevented.</p>
            </div>
          )}

          {chatHistory.map((msg, i) => (
            <div key={i} className={`flex flex-col ${msg.role === "user" ? "items-end" : "items-start"} gap-1`}>
              <div className="flex items-center gap-1.5 text-[10px] text-slate-400 font-semibold px-1">
                <span>{msg.role === "user" ? "You" : "AI Assistant"}</span>
                <span>•</span>
                <span>{msg.time}</span>
              </div>
              <div
                className={`max-w-[85%] rounded-[16px] px-4 py-3 text-sm leading-relaxed border ${
                  msg.role === "user"
                    ? "bg-[#2563EB] text-white border-[#2563EB] shadow-xs"
                    : "bg-[#F1F5F9] text-[#0F172A] border-[#E2E8F0] shadow-xs"
                }`}
              >
                {msg.content === "" && isStreaming ? (
                  <span className="flex items-center gap-1 py-1">
                    <span className="w-1.5 h-1.5 bg-[#2563EB] rounded-full animate-bounce delay-75" />
                    <span className="w-1.5 h-1.5 bg-[#2563EB] rounded-full animate-bounce delay-150" />
                    <span className="w-1.5 h-1.5 bg-[#2563EB] rounded-full animate-bounce delay-225" />
                  </span>
                ) : (
                  <p className="whitespace-pre-line">{msg.content}</p>
                )}
              </div>
            </div>
          ))}
          <div ref={messagesEndRef} />
        </div>

        {/* Input Bar - White background, soft shadow */}
        <form onSubmit={handleSend} className="p-5 border-t border-[#E2E8F0] bg-white shadow-[0_-4px_12px_rgba(0,0,0,0.05)] flex flex-col gap-2.5">
          <div className="relative flex items-center bg-white rounded-[12px] border border-[#E2E8F0] focus-within:border-[#2563EB] focus-within:ring-1 focus-within:ring-[#2563EB] transition-colors shadow-xs">
            <textarea
              value={query}
              onChange={(e) => setQuery(e.target.value)}
              onKeyDown={(e) => {
                if (e.key === "Enter" && !e.shiftKey) {
                  e.preventDefault();
                  handleSend();
                }
              }}
              placeholder="Ask about cleanliness, family suitability..."
              className="flex-1 bg-transparent px-4 py-3.5 outline-none resize-none text-sm placeholder-slate-400 h-12 text-[#0F172A]"
              rows={1}
            />
            <Button
              type="submit"
              size="icon"
              className="absolute right-2 bg-[#2563EB] hover:bg-blue-700 text-white rounded-[10px] w-9 h-9 flex items-center justify-center shrink-0 shadow-sm cursor-pointer"
              disabled={!query.trim() || isStreaming}
            >
              <Send className="w-4 h-4" />
            </Button>
          </div>
          <div className="flex justify-between items-center text-[10px] text-slate-450 px-1 font-bold">
            <span>Uses verified review evidence only</span>
            {isStreaming && (
              <button
                type="button"
                onClick={() => {
                  if (abortControllerRef.current) abortControllerRef.current.abort();
                  setIsStreaming(false);
                }}
                className="text-red-500 hover:text-red-700 transition-colors cursor-pointer"
              >
                Stop generating
              </button>
            )}
          </div>
        </form>
      </div>
    </div>
  );
}
