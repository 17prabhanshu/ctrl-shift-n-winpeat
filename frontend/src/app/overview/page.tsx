"use client";

import { motion } from "framer-motion";
import { ShieldCheck, Info } from "lucide-react";

export default function Overview() {
  return (
    <div className="p-10 max-w-6xl mx-auto bg-[#F9FAFB] min-h-screen">
      <motion.header 
        initial={{ opacity: 0, y: -10 }}
        animate={{ opacity: 1, y: 0 }}
        className="mb-12"
      >
        <h1 className="text-4xl font-extrabold tracking-tight text-brand-black mb-2">Command Center</h1>
        <p className="text-lg text-brand-textSecondary font-medium">Real-time workforce intelligence and construct alignment.</p>
      </motion.header>

      {/* The Big Finding Insight Card */}
      <motion.section
        initial={{ opacity: 0, scale: 0.98 }}
        animate={{ opacity: 1, scale: 1 }}
        transition={{ delay: 0.1 }}
        className="mb-12"
      >
        <div className="text-xs font-bold tracking-widest text-brand-textSecondary uppercase mb-3">The Big Finding</div>
        
        <div className="bg-white rounded-2xl p-8 shadow-sm border border-gray-100 relative overflow-hidden">
          <div className="absolute top-0 left-0 w-1.5 h-full bg-brand-orange" />
          
          <h2 className="text-3xl md:text-4xl font-bold leading-tight text-brand-black mb-8 max-w-4xl tracking-tight">
            Technical and communication capabilities show <span className="text-brand-orange">positive complementarity</span> in market compensation.
          </h2>
          
          <div className="grid grid-cols-2 md:grid-cols-4 gap-6 text-sm bg-gray-50 p-6 rounded-xl border border-gray-100">
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs font-bold uppercase tracking-wider">Status</div>
              <div className="flex items-center space-x-2 text-green-600">
                <ShieldCheck className="w-5 h-5" />
                <span className="font-bold">VERIFIED</span>
              </div>
            </div>
            
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs font-bold uppercase tracking-wider">Dataset</div>
              <div className="font-bold text-brand-black text-base">Analytics Jobs</div>
              <div className="text-brand-textSecondary text-xs font-medium mt-0.5">n = 15,841</div>
            </div>
            
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs font-bold uppercase tracking-wider">Method</div>
              <div className="font-bold text-brand-black text-base">Interaction Model</div>
              <div className="text-brand-textSecondary text-xs font-medium mt-0.5">OLS + HC3</div>
            </div>
            
            <div>
              <div className="text-brand-textSecondary mb-1 text-xs font-bold uppercase tracking-wider">Evidence Class</div>
              <div className="inline-block px-3 py-1.5 bg-brand-black text-white rounded-md text-xs font-bold shadow-sm">
                OBSERVED + DERIVED
              </div>
            </div>
          </div>
        </div>
      </motion.section>

      {/* Metric Grid */}
      <div className="grid grid-cols-1 md:grid-cols-4 gap-6 mb-12">
        {METRICS.map((m, i) => (
          <motion.div 
            key={m.label}
            initial={{ opacity: 0, y: 10 }}
            animate={{ opacity: 1, y: 0 }}
            transition={{ delay: 0.2 + (i * 0.05) }}
            className="p-6 rounded-xl border border-gray-100 bg-white shadow-sm hover:shadow-md transition-shadow"
          >
            <div className="flex justify-between items-start mb-4">
              <div className="text-xs font-bold text-brand-textSecondary uppercase tracking-wider">{m.label}</div>
              <m.icon className="w-5 h-5 text-brand-orange" />
            </div>
            <div className="text-4xl font-extrabold text-brand-black tabular-nums tracking-tight">{m.value}</div>
            <div className="text-sm font-medium text-brand-textSecondary mt-2">{m.sub}</div>
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
