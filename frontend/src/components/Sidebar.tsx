"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Home, Briefcase, Target, TrendingUp, 
  Award, ShieldCheck, Database 
} from "lucide-react";

const NAV_ITEMS = [
  { name: "Overview", href: "/", icon: Home },
  { name: "Market Radar", href: "/market", icon: Briefcase },
  { name: "Skill Intelligence", href: "/skills", icon: Target },
  { name: "Career Progression", href: "/progression", icon: TrendingUp },
  { name: "Senior Success", href: "/senior", icon: Award },
  { name: "Evidence", href: "/evidence", icon: ShieldCheck },
  { name: "Model Lab", href: "/lab", icon: Database },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-brand-border bg-white flex flex-col h-screen sticky top-0 shadow-sm">
      <div className="p-6 pb-2">
        <h1 className="text-xl font-bold tracking-tight text-brand-black flex items-center gap-2">
          <div className="w-6 h-6 bg-brand-orange rounded-md flex items-center justify-center text-white font-bold text-xs">
            CS
          </div>
          Ctrl Shift N
        </h1>
      </div>
      
      <nav className="flex-1 px-4 space-y-1 mt-6">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link 
              key={item.href} 
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-semibold transition-all duration-200 ${
                isActive 
                  ? "bg-[#FFF0ED] text-brand-orange" 
                  : "text-brand-textSecondary hover:bg-gray-100 hover:text-brand-black"
              }`}
            >
              <Icon className="w-[18px] h-[18px]" strokeWidth={isActive ? 2.5 : 2} />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-6 border-t border-brand-border mt-auto">
        <button className="w-full flex items-center justify-between px-4 py-2 bg-gray-50 border border-brand-border rounded-lg text-sm text-brand-textSecondary hover:bg-gray-100 transition-colors shadow-sm">
          <span className="font-medium">Search...</span>
          <kbd className="font-mono bg-white border border-gray-200 px-1.5 py-0.5 rounded text-[10px] font-bold text-gray-500 shadow-sm">⌘K</kbd>
        </button>
      </div>
    </aside>
  );
}
