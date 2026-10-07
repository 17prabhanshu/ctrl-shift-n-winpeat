import type { Metadata } from "next";
import { Inter } from "next/font/google";
import "./globals.css";
import { Sidebar } from "@/components/Sidebar";

const inter = Inter({ subsets: ["latin"], display: "swap" });

export const metadata: Metadata = {
  title: "WIE | Workforce Intelligence Engine",
  description: "Does the market pay for what progression rewards?",
};

export default function RootLayout({
  children,
}: Readonly<{
  children: React.ReactNode;
}>) {
  return (
    <html lang="en">
      <body className={`${inter.className} bg-[#F9FAFB] text-brand-textPrimary min-h-screen flex antialiased`}>
        <Sidebar />
        <main className="flex-1 relative overflow-x-hidden">
          {children}
        </main>
      </body>
    </html>
  );
}
