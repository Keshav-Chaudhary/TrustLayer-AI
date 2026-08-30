import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import Providers from "./providers";
import { Header } from "@/components/Header";
import { ChatDrawer } from "@/components/ChatDrawer";

const inter = Inter({
  variable: "--font-sans",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: "TrustLayer-AI - Verified AI-Powered Hotel Recommendations",
  description: "transparent, grounded, and evidence-backed travel recommendations powered by hybrid RAG.",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html
      lang="en"
      className={`${inter.variable} h-full antialiased`}
    >
      <body className="min-h-full flex flex-col bg-slate-50 text-slate-900 font-sans">
        <Providers>
          <Header />
          <div className="flex-1 flex flex-col">
            {children}
          </div>
          <ChatDrawer />
        </Providers>
      </body>
    </html>
  );
}
