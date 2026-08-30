"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useChatStore } from "@/hooks/useChatStore";
import { Bot, Heart, Compass, GitCompare, User } from "lucide-react";
import { cn } from "@/lib/utils";

export function Header() {
  const pathname = usePathname();
  const toggleChat = useChatStore((state) => state.toggleChat);

  const navLinks = [
    { href: "/stays", label: "Stays", icon: Compass },
    { href: "/saved", label: "Saved Hotels", icon: Heart },
    { href: "/compare", label: "Compare", icon: GitCompare },
  ];

  return (
    <header className="sticky top-0 z-40 w-full h-[72px] bg-white/95 backdrop-blur-md border-b border-[#E2E8F0] text-slate-900 shadow-sm flex items-center">
      <div className="max-w-7xl mx-auto px-4 sm:px-6 lg:px-8 w-full flex items-center justify-between">
        
        {/* Logo */}
        <Link href="/" className="flex items-center gap-2 group shrink-0">
          <div className="w-9 h-9 rounded-xl bg-[#2563EB] flex items-center justify-center font-bold text-white group-hover:bg-blue-700 transition-colors shadow-sm">
            T
          </div>
          <span className="font-extrabold text-xl tracking-tight text-[#0F172A]">
            TrustLayer-AI
          </span>
        </Link>

        {/* Center navigation */}
        <nav className="hidden md:flex items-center gap-2">
          {navLinks.map((link) => {
            const Icon = link.icon;
            const isActive = pathname === link.href;
            return (
              <Link
                key={link.href}
                href={link.href}
                className={cn(
                  "flex items-center gap-2 text-sm font-semibold transition-all duration-200 py-2 px-3.5 rounded-[10px]",
                  isActive 
                    ? "bg-[#F1F5F9] text-[#2563EB]" 
                    : "text-[#475569] hover:bg-[#F1F5F9] hover:text-[#0F172A]"
                )}
              >
                <Icon className="w-4 h-4" />
                <span>{link.label}</span>
              </Link>
            );
          })}
        </nav>

        {/* Right side buttons */}
        <div className="flex items-center gap-3 shrink-0">
          {/* AI assistant trigger */}
          <button
            onClick={() => toggleChat()}
            className="flex items-center gap-2 bg-[#072D62] hover:bg-blue-900 text-white font-bold text-xs px-4.5 py-2.5 rounded-[12px] shadow-sm transition-all duration-200 hover:scale-[1.02] cursor-pointer focus:outline-none focus:ring-2 focus:ring-[#2563EB]"
          >
            <Bot className="w-4 h-4 text-blue-400" />
            <span>AI Travel Assistant</span>
          </button>

          {/* About Link */}
          <Link
            href="/about"
            className="hidden sm:inline-block text-xs font-bold text-[#475569] hover:text-[#0F172A] border border-[#E2E8F0] hover:bg-slate-50 px-3.5 py-2.5 rounded-[12px] transition-all duration-200"
          >
            How it works
          </Link>

          {/* User profile dropdown placeholder */}
          <div className="w-9 h-9 rounded-[12px] bg-slate-50 border border-[#E2E8F0] flex items-center justify-center text-slate-500 hover:text-slate-900 cursor-pointer hover:bg-slate-100 transition-colors focus:outline-none focus:ring-2 focus:ring-[#2563EB]">
            <User className="w-4.5 h-4.5" />
          </div>
        </div>
      </div>
    </header>
  );
}
