"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { useState, useEffect } from "react";
import { cn } from "@/lib/utils";
import { MenuIcon, XMarkIcon } from "@heroicons/react/24/solid";

const navLinks = [
  { href: "/jobs", label: "Jobs" },
  { href: "/salary", label: "Salaries" },
  { href: "/skills", label: "Skills" },
  { href: "/companies", label: "Companies" },
  { href: "/profile", label: "My Profile" },
];

export function SiteHeader() {
  const pathname = usePathname();
  const [menuOpen, setMenuOpen] = useState(false);
  const [scrolled, setScrolled] = useState(false);

  useEffect(() => {
    const onScroll = () => setScrolled(window.scrollY > 12);
    window.addEventListener("scroll", onScroll, { passive: true });
    return () => window.removeEventListener("scroll", onScroll);
  }, []);

  useEffect(() => {
    setMenuOpen(false);
  }, [pathname]);

  const linkClass = ({ href }: { href: string }) =>
    cn(
      "rounded-lg px-3 py-1.5 text-sm font-medium transition-colors hover:bg-brand-50 hover:text-brand-700",
      pathname === href ? "bg-brand-50 text-brand-700" : "text-gray-600"
    );

  return (
    <header
      className={cn(
        "sticky top-0 z-50 w-full border-b transition-all duration-200",
        scrolled ? "border-gray-200/80 bg-white/90 backdrop-blur-sm shadow-sm" : "border-transparent bg-transparent"
      )}
    >
      <div className="mx-auto flex h-16 max-w-7xl items-center justify-between px-4 sm:px-6 lg:px-8">
        <Link href="/" className="flex items-center gap-2 text-xl font-bold tracking-tight text-gray-900">
          <span className="flex h-8 w-8 items-center justify-center rounded-lg bg-gradient-to-br from-brand-400 to-brand-600 text-white text-sm shadow-sm">
            H
          </span>
          <span className="hidden sm:block">Handshake for Data Careers</span>
        </Link>

        <nav className="hidden md:flex md:items-center md:gap-1">
          {navLinks.map((link) => (
            <Link key={link.href} href={link.href} className={linkClass(link)}>
              {link.label}
            </Link>
          ))}
          <Link href="/register" className="ml-2 inline-flex items-center justify-center rounded-lg bg-brand-600 px-4 py-1.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-400 focus:ring-offset-2">
            Sign Up
          </Link>
        </nav>

        <div className="flex items-center gap-2">
          <button
            className="md:hidden rounded-lg p-2 text-gray-600 hover:bg-gray-100"
            aria-label="Toggle menu"
            onClick={() => setMenuOpen((prev) => !prev)}
          >
            {menuOpen ? <XMarkIcon className="h-5 w-5" /> : <MenuIcon className="h-5 w-5" />}
          </button>
        </div>
      </div>

      {menuOpen && (
        <div className="md:hidden border-t border-gray-200 bg-white px-4 py-4 shadow-lg">
          <nav className="flex flex-col gap-1">
            {navLinks.map((link) => (
              <Link key={link.href} href={link.href} className={linkClass(link)}>
                {link.label}
              </Link>
            ))}
            <Link
              href="/register"
              className="mt-2 inline-flex w-full items-center justify-center rounded-lg bg-brand-600 px-4 py-2 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
            >
              Sign Up
            </Link>
          </nav>
        </div>
      )}
    </header>
  );
}
