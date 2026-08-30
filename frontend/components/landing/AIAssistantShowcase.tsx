import { Bot, Sparkles, MessagesSquare, Check } from "lucide-react";
import { useReveal } from "./useReveal";
import { useChatStore } from "@/hooks/useChatStore";

export function AIAssistantShowcase() {
  const { ref, isRevealed } = useReveal();
  const toggleChat = useChatStore((state) => state.toggleChat);

  return (
    <section className="w-full bg-[#0F172A] py-24 text-white overflow-hidden relative">
      {/* Decorative Background */}
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_top_right,_var(--tw-gradient-stops))] from-blue-900/40 via-[#0F172A] to-[#0F172A] opacity-90 z-0" />
      
      <div 
        ref={ref}
        className={`relative z-10 max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="grid grid-cols-1 lg:grid-cols-2 gap-16 items-center">
          
          {/* Left: Illustration / Graphic */}
          <div className="order-2 lg:order-1 relative">
            <div className="absolute -inset-4 bg-gradient-to-r from-blue-500 to-purple-600 rounded-[32px] blur-2xl opacity-20 animate-pulse" />
            <div className="relative bg-slate-900 border border-slate-800 rounded-[24px] p-8 shadow-2xl">
              <div className="flex items-center gap-4 mb-8 pb-6 border-b border-slate-800">
                <div className="w-12 h-12 bg-blue-600 rounded-full flex items-center justify-center">
                  <Bot className="w-6 h-6 text-white" />
                </div>
                <div>
                  <h4 className="font-bold text-lg">TrustLayer-AI</h4>
                  <p className="text-sm text-slate-400">Online</p>
                </div>
              </div>
              
              <div className="space-y-6">
                <div className="flex gap-4 w-4/5">
                  <div className="w-8 h-8 rounded-full bg-slate-800 shrink-0 flex items-center justify-center">
                    <span className="text-xs font-bold text-slate-400">You</span>
                  </div>
                  <div className="bg-slate-800 rounded-2xl rounded-tl-none p-4 text-sm text-slate-300">
                    Which of these family hotels has the best cleanliness rating?
                  </div>
                </div>
                
                <div className="flex gap-4 w-[90%] ml-auto justify-end">
                  <div className="bg-blue-600 rounded-2xl rounded-tr-none p-4 text-sm text-white shadow-md">
                    Based on verified reviews, <span className="font-bold">Holiday Inn Aerocity</span> has the highest cleanliness score (5.0/5.0). Recent guests specifically mentioned "spotless rooms" and "hygienic bathrooms". Would you like to see the full evidence?
                  </div>
                  <div className="w-8 h-8 rounded-full bg-blue-700 shrink-0 flex items-center justify-center">
                    <Bot className="w-4 h-4 text-white" />
                  </div>
                </div>
              </div>
            </div>
          </div>

          {/* Right: Content */}
          <div className="order-1 lg:order-2 space-y-8">
            <div>
              <div className="inline-flex items-center gap-2 px-3 py-1.5 rounded-full bg-blue-900/50 border border-blue-800 text-blue-300 text-sm font-semibold mb-6">
                <Sparkles className="w-4 h-4" />
                Meet Your AI Travel Assistant
              </div>
              <h2 className="text-3xl sm:text-4xl lg:text-5xl font-extrabold tracking-tight leading-tight">
                Ask anything. <br/><span className="text-transparent bg-clip-text bg-gradient-to-r from-blue-400 to-blue-200">Book with confidence.</span>
              </h2>
              <p className="text-slate-400 mt-6 text-lg max-w-lg leading-relaxed">
                Need help deciding? Our contextual AI assistant is always ready to compare hotels, analyze deep review trends, and explain trust scores on demand.
              </p>
            </div>

            <ul className="space-y-4">
              {[
                "Find family-friendly or business hotels",
                "Compare destinations side-by-side",
                "Analyze cleanliness and service reviews",
                "Explain trust scores with verified evidence"
              ].map((item, i) => (
                <li key={i} className="flex items-center gap-3 text-slate-300 font-medium">
                  <div className="w-6 h-6 rounded-full bg-blue-900/50 flex items-center justify-center shrink-0">
                    <Check className="w-3.5 h-3.5 text-blue-400" />
                  </div>
                  {item}
                </li>
              ))}
            </ul>

            <button 
              onClick={() => toggleChat()}
              className="mt-4 px-8 py-4 bg-white hover:bg-slate-100 text-slate-900 font-bold rounded-xl flex items-center gap-3 transition-transform hover:-translate-y-1 shadow-xl"
            >
              <MessagesSquare className="w-5 h-5" />
              Try AI Assistant Now
            </button>
          </div>

        </div>
      </div>
    </section>
  );
}
