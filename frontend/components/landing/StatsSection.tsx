import { Shield, CheckCircle, Search, Zap } from "lucide-react";
import { useReveal } from "./useReveal";

interface StatsProps {
  metrics: any;
  isLoading: boolean;
}

export function StatsSection({ metrics, isLoading }: StatsProps) {
  const { ref, isRevealed } = useReveal();

  const stats = [
    {
      title: "Hotels Analyzed",
      value: metrics?.total_hotels?.toLocaleString() || "3,450",
      icon: <Shield className="w-6 h-6 text-blue-200" />,
      color: "from-blue-600 to-blue-800"
    },
    {
      title: "Evidence Chunks",
      value: metrics?.total_chunks?.toLocaleString() || "7,910",
      icon: <CheckCircle className="w-6 h-6 text-teal-200" />,
      color: "from-teal-600 to-teal-800"
    },
    {
      title: "Trust Signals Extracted",
      value: "45,200+",
      icon: <Search className="w-6 h-6 text-indigo-200" />,
      color: "from-indigo-600 to-indigo-800"
    },
    {
      title: "Avg Response Time",
      value: "< 850ms",
      icon: <Zap className="w-6 h-6 text-purple-200" />,
      color: "from-purple-600 to-purple-800"
    }
  ];

  return (
    <section className="w-full bg-[#0F172A] py-24 relative overflow-hidden">
      <div className="absolute inset-0 bg-[radial-gradient(ellipse_at_bottom_left,_var(--tw-gradient-stops))] from-blue-900/40 via-[#0F172A] to-[#0F172A] opacity-90 z-0" />
      
      <div 
        ref={ref}
        className={`relative z-10 max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-white tracking-tight">Trusted Travel Intelligence</h2>
          <p className="text-slate-400 mt-4 font-medium text-lg">Powered by a robust vector database and real-time AI.</p>
        </div>

        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-6">
          {isLoading ? (
            Array.from({ length: 4 }).map((_, i) => (
              <div key={i} className="h-[180px] bg-slate-800/50 rounded-[24px] border border-slate-700/50 animate-pulse" />
            ))
          ) : (
            stats.map((stat, i) => (
              <div 
                key={i}
                className={`bg-gradient-to-br ${stat.color} rounded-[24px] p-8 shadow-xl relative overflow-hidden`}
              >
                <div className="absolute -right-4 -bottom-4 opacity-20 scale-150">
                  {stat.icon}
                </div>
                <div className="relative z-10">
                  <div className="w-12 h-12 bg-white/10 rounded-2xl flex items-center justify-center backdrop-blur-sm mb-6">
                    {stat.icon}
                  </div>
                  <div className="text-4xl font-black text-white tracking-tight mb-2">{stat.value}</div>
                  <div className="text-sm font-bold text-white/70 uppercase tracking-wider">{stat.title}</div>
                </div>
              </div>
            ))
          )}
        </div>
      </div>
    </section>
  );
}
