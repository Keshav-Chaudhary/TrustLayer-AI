"use client";

import { Shield } from "lucide-react";

export default function PrivacyPage() {
  return (
    <div className="max-w-3xl mx-auto px-4 sm:px-6 lg:px-8 py-12 text-slate-900 space-y-8 bg-[#F8FAFC] min-h-screen">
      <div>
        <h1 className="text-3xl font-extrabold text-slate-950 tracking-tight leading-tight flex items-center gap-2">
          <Shield className="w-7 h-7 text-blue-600" />
          Privacy Policy
        </h1>
        <p className="text-xs text-slate-500 font-semibold mt-1">Last Updated: July 14, 2026</p>
      </div>

      <div className="bg-white p-6 sm:p-8 rounded-2xl border border-slate-200 shadow-sm space-y-6 text-sm leading-relaxed text-slate-700">
        <section className="space-y-2">
          <h2 className="text-base font-extrabold text-slate-950 uppercase tracking-wider">1. Information We Collect</h2>
          <p className="text-xs text-slate-600">
            TrustLayer-AI does not collect or store personal user accounts. We process search queries and chat input context locally using local LLM inference engines. No data is shared with external commercial data brokers or third parties.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-extrabold text-slate-950 uppercase tracking-wider">2. Caching and Storage</h2>
          <p className="text-xs text-slate-600">
            We store Saved Hotels (your wishlist) and Compared Hotel IDs locally in your browser's <code className="bg-slate-100 px-1 py-0.5 rounded font-mono text-[11px]">localStorage</code>. You can clear this anytime by clicking "Clear All" on the respective pages. Search caching queries on the backend are stored in memory (`cache_service.py`) and do not persist to disk.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-extrabold text-slate-950 uppercase tracking-wider">3. AI Evaluation</h2>
          <p className="text-xs text-slate-600">
            Our backend utilizes local open-weights LLM inference (e.g. Ollama Qwen2.5) to run hotel summaries. Your input prompt queries do not train any public foundation models. All outputs are verified locally against our review database index to protect context accuracy.
          </p>
        </section>

        <section className="space-y-2">
          <h2 className="text-base font-extrabold text-slate-950 uppercase tracking-wider">4. Contact Information</h2>
          <p className="text-xs text-slate-600">
            For academic inquiries or database audit requests regarding the RAG indices, please inspect our repository configuration files.
          </p>
        </section>
      </div>
    </div>
  );
}
