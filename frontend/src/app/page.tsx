"use client";

import { motion } from "framer-motion";
import { ArrowRight, Activity, Database, Network, LineChart, ShieldCheck } from "lucide-react";
import Link from "next/link";

const NODES = [
  { id: "market", label: "MARKET", icon: Database, desc: "Demand & Compensation" },
  { id: "skills", label: "SKILLS", icon: Network, desc: "Taxonomy & Signal" },
  { id: "junior", label: "JUNIOR", icon: Activity, desc: "Early Career Hike" },
  { id: "senior", label: "SENIOR", icon: LineChart, desc: "Executive Success" },
  { id: "evidence", label: "EVIDENCE", icon: ShieldCheck, desc: "Construct Alignment" },
];

export default function Home() {
  return (
    <div className="relative min-h-screen flex flex-col items-center justify-center overflow-hidden p-6">
      
      {/* Background ambient glow */}
      <div className="absolute top-1/2 left-1/2 -translate-x-1/2 -translate-y-1/2 w-[800px] h-[800px] bg-brand-cyan/5 rounded-full blur-3xl pointer-events-none" />

      <div className="z-10 text-center max-w-4xl mx-auto">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.8, ease: "easeOut" }}
        >
          <h2 className="text-brand-cyan text-sm font-mono tracking-[0.3em] uppercase mb-4">
            Ctrl Shift N
          </h2>
          <h1 className="text-5xl md:text-7xl font-bold tracking-tighter mb-6">
            Workforce Intelligence Engine
          </h1>
          <p className="text-xl md:text-2xl text-brand-textSecondary font-light italic mb-16">
            "Does the market pay for what progression rewards?"
          </p>
        </motion.div>

        {/* The Signal Field */}
        <div className="flex flex-col md:flex-row items-center justify-center gap-4 md:gap-8 mb-16">
          {NODES.map((node, i) => (
            <div key={node.id} className="flex flex-col md:flex-row items-center">
              <motion.div
                initial={{ opacity: 0, scale: 0.8 }}
                animate={{ opacity: 1, scale: 1 }}
                transition={{ duration: 0.5, delay: 0.6 + i * 0.15 }}
                className="group relative"
              >
                <div className="w-20 h-20 rounded-full hairline-border bg-brand-surfaceElevated flex items-center justify-center text-brand-textSecondary hover:text-brand-cyan hover:border-brand-cyan/50 transition-all duration-300 cursor-pointer">
                  <node.icon className="w-8 h-8" />
                </div>
                
                {/* Tooltip */}
                <div className="absolute top-full mt-4 left-1/2 -translate-x-1/2 opacity-0 group-hover:opacity-100 transition-opacity whitespace-nowrap text-center">
                  <div className="text-sm font-bold tracking-widest text-brand-textPrimary">{node.label}</div>
                  <div className="text-xs text-brand-textSecondary mt-1">{node.desc}</div>
                </div>
              </motion.div>

              {i < NODES.length - 1 && (
                <motion.div
                  initial={{ opacity: 0, width: 0 }}
                  animate={{ opacity: 1, width: "auto" }}
                  transition={{ duration: 0.4, delay: 0.8 + i * 0.15 }}
                  className="hidden md:block mx-4"
                >
                  <ArrowRight className="text-white/20 w-5 h-5" />
                </motion.div>
              )}
            </div>
          ))}
        </div>

        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          transition={{ duration: 1, delay: 1.8 }}
        >
          <Link href="/overview" className="inline-flex items-center space-x-2 bg-white text-black px-6 py-3 rounded-full font-medium hover:bg-gray-200 transition-colors">
            <span>Initialize Engine</span>
            <ArrowRight className="w-4 h-4" />
          </Link>
        </motion.div>
      </div>

    </div>
  );
}
