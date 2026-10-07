"use client";

import Link from "next/link";
import { usePathname } from "next/navigation";
import { 
  Activity, BarChart2, Network, TrendingUp, 
  Award, ShieldCheck, Beaker 
} from "lucide-react";

const NAV_ITEMS = [
  { name: "Overview", href: "/", icon: Activity },
  { name: "Market Radar", href: "/market", icon: BarChart2 },
  { name: "Skill Intelligence", href: "/skills", icon: Network },
  { name: "Career Progression", href: "/progression", icon: TrendingUp },
  { name: "Senior Success", href: "/senior", icon: Award },
  { name: "Evidence", href: "/evidence", icon: ShieldCheck },
  { name: "Model Lab", href: "/lab", icon: Beaker },
];

export function Sidebar() {
  const pathname = usePathname();

  return (
    <aside className="w-64 border-r border-white/5 bg-brand-surface/50 glass-panel hidden md:flex flex-col h-screen sticky top-0">
      <div className="p-6">
        <h1 className="text-xs font-mono tracking-widest text-brand-textSecondary uppercase font-bold">
          Ctrl Shift N
        </h1>
        <div className="text-lg font-semibold tracking-tight text-brand-textPrimary mt-1">
          Workforce Intel
        </div>
      </div>
      
      <nav className="flex-1 px-4 space-y-1 mt-4">
        {NAV_ITEMS.map((item) => {
          const isActive = pathname === item.href;
          const Icon = item.icon;
          return (
            <Link 
              key={item.href} 
              href={item.href}
              className={`flex items-center space-x-3 px-3 py-2.5 rounded-md text-sm font-medium transition-all duration-200 ${
                isActive 
                  ? "bg-brand-cyan/10 text-brand-cyan" 
                  : "text-brand-textSecondary hover:bg-white/5 hover:text-brand-textPrimary"
              }`}
            >
              <Icon className="w-4 h-4" />
              <span>{item.name}</span>
            </Link>
          );
        })}
      </nav>

      <div className="p-6">
        <button className="w-full flex items-center justify-between px-3 py-2 border border-white/10 rounded-md text-xs text-brand-textSecondary hover:bg-white/5 transition-colors">
          <span>Search...</span>
          <kbd className="font-mono bg-white/10 px-1.5 py-0.5 rounded text-[10px]">⌘K</kbd>
        </button>
      </div>
    </aside>
  );
}
