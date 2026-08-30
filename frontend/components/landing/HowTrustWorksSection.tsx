import { Database, Activity, CheckCircle2 } from "lucide-react";
import { useReveal } from "./useReveal";

export function HowTrustWorksSection() {
  const { ref, isRevealed } = useReveal();

  return (
    <section className="w-full bg-white py-24">
      <div 
        ref={ref}
        className={`max-w-[1024px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="text-center mb-16">
          <h2 className="text-3xl font-bold text-[#0F172A] tracking-tight">How TrustLayer-AI Works</h2>
          <p className="text-[#475569] mt-4 font-medium text-lg">Our multi-stage analysis pipeline ensures every recommendation is grounded in reality.</p>
        </div>

        <div className="relative flex flex-col md:flex-row justify-between items-start md:items-center gap-12 md:gap-4">
          
          {/* Connector Line for Desktop */}
          <div className="hidden md:block absolute top-8 left-[10%] right-[10%] h-0.5 bg-slate-100 -z-10" />

          {/* Step 1 */}
          <div className="flex-1 flex flex-col items-center text-center relative w-full">
            <div className="w-16 h-16 rounded-full bg-white border-4 border-slate-100 flex items-center justify-center text-blue-600 mb-6 shadow-sm">
              <Database className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-[#0F172A] mb-2">1. Analyze Reviews</h3>
            <p className="text-[#475569]">Process verified traveler feedback from our extensive hotel database to understand actual guest experiences.</p>
          </div>

          {/* Step 2 */}
          <div className="flex-1 flex flex-col items-center text-center relative w-full">
            <div className="w-16 h-16 rounded-full bg-white border-4 border-slate-100 flex items-center justify-center text-blue-600 mb-6 shadow-sm">
              <Activity className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-[#0F172A] mb-2">2. Calculate Trust</h3>
            <p className="text-[#475569]">Generate transparent scores for cleanliness, service, location, and value using advanced sentiment analysis.</p>
          </div>

          {/* Step 3 */}
          <div className="flex-1 flex flex-col items-center text-center relative w-full">
            <div className="w-16 h-16 rounded-full bg-blue-600 border-4 border-blue-100 flex items-center justify-center text-white mb-6 shadow-md">
              <CheckCircle2 className="w-6 h-6" />
            </div>
            <h3 className="text-xl font-bold text-[#0F172A] mb-2">3. Explain Insights</h3>
            <p className="text-[#475569]">Show evidence-backed reasons and provenance for every AI insight so you can book with total confidence.</p>
          </div>

        </div>
      </div>
    </section>
  );
}
