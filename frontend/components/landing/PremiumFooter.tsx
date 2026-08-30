import Link from "next/link";
import { Shield } from "lucide-react";

export function PremiumFooter() {
  return (
    <footer className="w-full bg-slate-950 text-slate-400 py-16 border-t border-slate-900">
      <div className="max-w-[1440px] mx-auto px-4 sm:px-6 lg:px-8">
        <div className="grid grid-cols-1 md:grid-cols-4 gap-12 mb-16">
          
          <div className="md:col-span-1">
            <Link href="/" className="flex items-center gap-2 mb-6">
              <div className="w-8 h-8 bg-blue-600 rounded-lg flex items-center justify-center">
                <Shield className="w-4 h-4 text-white" />
              </div>
              <span className="font-bold text-xl text-white tracking-tight">TrustLayer-AI</span>
            </Link>
            <p className="text-sm leading-relaxed text-slate-500">
              The world's most transparent hotel recommendation engine, powered by explainable AI and verified review evidence.
            </p>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6 tracking-wide">Platform</h4>
            <ul className="space-y-4 text-sm">
              <li><Link href="/stays" className="hover:text-blue-400 transition-colors">Browse Stays</Link></li>
              <li><Link href="/compare" className="hover:text-blue-400 transition-colors">Compare Hotels</Link></li>
              <li><Link href="/saved" className="hover:text-blue-400 transition-colors">Saved Hotels</Link></li>
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors">AI Assistant</span></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6 tracking-wide">Resources</h4>
            <ul className="space-y-4 text-sm">
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors">How Trust Scores Work</span></li>
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors">Explainable AI</span></li>
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors">Review Methodology</span></li>
            </ul>
          </div>

          <div>
            <h4 className="text-white font-bold mb-6 tracking-wide">Legal</h4>
            <ul className="space-y-4 text-sm">
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors">Privacy Policy</span></li>
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors">Terms of Service</span></li>
              <li><span className="cursor-pointer hover:text-blue-400 transition-colors bg-blue-900/30 text-blue-300 px-2 py-1 rounded-md text-xs">Academic Project</span></li>
            </ul>
          </div>

        </div>

        <div className="pt-8 border-t border-slate-800 text-sm flex flex-col md:flex-row justify-between items-center gap-4">
          <p>TrustLayer-AI © 2026. All rights reserved.</p>
          <div className="flex gap-6">
            <span className="hover:text-white cursor-pointer transition-colors">Twitter</span>
            <span className="hover:text-white cursor-pointer transition-colors">GitHub</span>
            <span className="hover:text-white cursor-pointer transition-colors">LinkedIn</span>
          </div>
        </div>
      </div>
    </footer>
  );
}
