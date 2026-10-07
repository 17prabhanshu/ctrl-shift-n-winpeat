"use client";

import { motion } from "framer-motion";
import { ShieldCheck, Info } from "lucide-react";

export default function Overview() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <motion.header 
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12"
      >
        <h1 className="text-3xl font-bold tracking-tight mb-2">Command Center</h1>
        <p className="text-brand-textSecondary">Real-time workforce intelligence and construct alignment.</p>
      </motion.header>

      {/* The Big Finding Insight Card */}
      <motion.section
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.2 }}
        className="mb-12"
      >
        <div className="text-xs font-mono tracking-widest text-brand-textSecondary uppercase mb-4">The Big Finding</div>
        
        <div className="glass-panel rounded-xl p-8 relative overflow-hidden border-brand-cyan/20">
          <div className="absolute top-0 left-0 w-1 h-full bg-brand-cyan" />
          
          <h2 className="text-2xl md:text-3xl font-medium leading-tight mb-8 max-w-3xl">
            Technical and communication capabilities show <span className="text-brand-cyan font-semibold">positive complementarity</span> in market compensation.
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm">
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs uppercase tracking-wider">Status</div>
              <div className="flex items-center space-x-2 text-brand-green">
                <ShieldCheck className="w-4 h-4" />
                <span className="font-medium">VERIFIED</span>
              </div>
            </div>
            
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs uppercase tracking-wider">Dataset</div>
              <div className="font-medium">Analytics Jobs</div>
              <div className="text-brand-textSecondary text-xs">n = 15,841</div>
            </div>
            
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs uppercase tracking-wider">Method</div>
              <div className="font-medium">Interaction Model</div>
              <div className="text-brand-textSecondary text-xs">OLS + HC3</div>
            </div>
            
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs uppercase tracking-wider">Evidence Class</div>
              <div className="inline-block px-2 py-1 bg-white/10 rounded text-xs font-mono">
                OBSERVED + MODEL DERIVED
              </div>
            </div>
          </div>
        </div>
      </motion.section>

      {/* Metric Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-4 mb-12">
        {METRICS.map((m, i) => (
          <motion.div 
            key={m.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.4 + (i * 0.1) }}
            className="p-5 rounded-lg hairline-border bg-brand-surface hover:bg-brand-surfaceElevated transition-colors"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="text-xs text-brand-textSecondary uppercase tracking-wider">{m.label}</div>
              <m.icon className="w-4 h-4 text-brand-textSecondary" />
            </div>
            <div className="text-3xl font-light tabular-nums">{m.value}</div>
            <div className="text-xs text-brand-cyan mt-2">{m.sub}</div>
          </motion.div>
        ))}
      </div>
    </div>
  );
}

const METRICS = [
  { label: "Market Demand", value: "15,841", sub: "Active Postings", icon: Info },
  { label: "Salary Cap", value: "₹45.0L", sub: "99th Percentile", icon: Info },
  { label: "JDS Progression", value: "0.904", sub: "ROC-AUC Signal", icon: Info },
  { label: "Skill Clusters", value: "12", sub: "Canonical Domains", icon: Info },
];
