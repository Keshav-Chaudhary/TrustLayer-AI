import { ShieldCheck, Sparkles, FileText, ArrowLeftRight } from "lucide-react";
import { useReveal } from "./useReveal";

const features = [
  {
    icon: <ShieldCheck className="w-8 h-8 text-blue-600" />,
    title: "Transparent Trust Scores",
    description: "Every recommendation is backed by measurable review signals. No hidden marketing bias."
  },
  {
    icon: <Sparkles className="w-8 h-8 text-blue-600" />,
    title: "Explainable AI",
    description: "See exactly why a hotel was recommended based on your unique travel needs and preferences."
  },
  {
    icon: <FileText className="w-8 h-8 text-blue-600" />,
    title: "Verified Evidence",
    description: "Review insights are grounded in real traveler feedback, securely analyzed from our vast database."
  },
  {
    icon: <ArrowLeftRight className="w-8 h-8 text-blue-600" />,
    title: "Side-by-Side Comparison",
    description: "Compare hotels across cleanliness, service, value, and location with absolute clarity."
  }
];

export function ValuePropsSection() {
  const { ref, isRevealed } = useReveal();

  return (
    <section className="w-full bg-[#F8FAFC] py-24 border-t border-b border-slate-200">
      <div 
        ref={ref}
        className={`max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8 transition-all duration-1000 ${
          isRevealed ? "translate-y-0 opacity-100" : "translate-y-10 opacity-0"
        }`}
      >
        <div className="text-center max-w-3xl mx-auto mb-16">
          <h2 className="text-3xl font-bold text-[#0F172A] tracking-tight">Why Travelers Choose TrustLayer-AI</h2>
          <p className="text-[#475569] mt-4 font-medium text-lg">We believe booking a hotel shouldn't feel like a gamble. Our AI engine brings unprecedented transparency to your travel decisions.</p>
        </div>

        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-6">
          {features.map((feature, i) => (
            <div 
              key={i}
              className="bg-white rounded-[24px] p-8 border border-slate-200 shadow-sm hover:shadow-xl hover:-translate-y-1 transition-all duration-300"
            >
              <div className="w-14 h-14 rounded-2xl bg-blue-50 flex items-center justify-center mb-6">
                {feature.icon}
              </div>
              <h3 className="text-xl font-bold text-[#0F172A] mb-3">{feature.title}</h3>
              <p className="text-[#475569] leading-relaxed">
                {feature.description}
              </p>
            </div>
          ))}
        </div>
      </div>
    </section>
  );
}
