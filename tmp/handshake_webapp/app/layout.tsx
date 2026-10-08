import type { Metadata, Viewport } from "next";
import { Geist, Geist_Mono } from "next/font/google";
import { Providers } from "@/components/providers";
import { ANIMATED_SECTION_WRAPPER } from "./layout.client";
import "./globals.css";

const geistSans = Geist({
  variable: "--font-geist-sans",
  subsets: ["latin"],
});

const geistMono = Geist_Mono({
  variable: "--font-geist-mono",
  subsets: ["latin"],
});

export const metadata: Metadata = {
  title: {
    default: "Handshake — Careers",
    template: "%s | Handshake",
  },
  description:
    "Explore entry-level professional opportunities, compare roles, and find your next career move.",
  metadata: {
    "theme-color": "#4f46e5",
  },
};

export const viewport: Viewport = {
  themeColor: "#4f46e5",
};

export default function RootLayout({
  children,
}: {
  children: React.ReactNode;
}) {
  return (
    <html lang="en" className={`${geistSans.variable} ${geistMono.variable}`}>
      <body className="min-h-screen bg-white text-gray-900 antialiased">
        <Providers>
          <ANIMATED_SECTION_WRAPPER>{children}</ANIMATED_SECTION_WRAPPER>
        </Providers>
      </body>
    </html>
  );
}
