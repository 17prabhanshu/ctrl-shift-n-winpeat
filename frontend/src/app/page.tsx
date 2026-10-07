"use client";

import { motion } from "framer-motion";
import { ArrowRight, Search, Briefcase, TrendingUp, ShieldCheck } from "lucide-react";
import Link from "next/link";

export default function Home() {
  return (
    <div className="min-h-screen bg-[#F9FAFB]">
      {/* Top Banner */}
      <div className="bg-brand-black text-white px-6 py-3 text-sm font-medium flex justify-between items-center">
        <span>Workforce Intelligence Engine</span>
        <span className="bg-white/10 px-2 py-1 rounded text-xs">SAS CU Hackathon 2026</span>
      </div>

      <div className="max-w-6xl mx-auto px-8 py-20">
        <motion.div
          initial={{ opacity: 0, y: 20 }}
          animate={{ opacity: 1, y: 0 }}
          transition={{ duration: 0.5 }}
          className="max-w-3xl"
        >
          <h1 className="text-5xl md:text-6xl font-extrabold text-brand-black leading-tight mb-6 tracking-tight">
            Does the market pay for what progression rewards?
          </h1>
          <p className="text-xl text-brand-textSecondary mb-10 leading-relaxed font-medium">
            Discover the fundamental disconnect between what employers ask for in job postings, and what actually drives internal career progression and executive success.
          </p>
          
          <div className="flex gap-4">
            <Link 
              href="/overview" 
              className="bg-brand-orange hover:bg-brand-orangeHover text-white px-8 py-4 rounded-lg font-bold text-lg flex items-center shadow-md transition-colors"
            >
              Explore the Data
              <ArrowRight className="w-5 h-5 ml-2" />
            </Link>
            <Link 
              href="/evidence" 
              className="bg-white border border-gray-200 hover:border-gray-300 text-brand-black px-8 py-4 rounded-lg font-bold text-lg flex items-center shadow-sm transition-colors"
            >
              View Evidence Registry
            </Link>
          </div>
        </motion.div>

        {/* Feature Cards below hero */}
        <div className="grid grid-cols-1 md:grid-cols-3 gap-6 mt-20">
          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.2 }}
            className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm"
          >
            <div className="w-12 h-12 bg-[#FFF0ED] text-brand-orange rounded-lg flex items-center justify-center mb-4">
              <Briefcase className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-brand-black mb-2">Market Radar</h3>
            <p className="text-brand-textSecondary text-sm">Analyze salary, experience, and role demands across 15,000+ real-world postings.</p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.3 }}
            className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm"
          >
            <div className="w-12 h-12 bg-[#FFF0ED] text-brand-orange rounded-lg flex items-center justify-center mb-4">
              <TrendingUp className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-brand-black mb-2">Career Progression</h3>
            <p className="text-brand-textSecondary text-sm">Discover how Technical and Communication skills interact to drive promotions.</p>
          </motion.div>

          <motion.div 
            initial={{ opacity: 0, y: 20 }} animate={{ opacity: 1, y: 0 }} transition={{ delay: 0.4 }}
            className="bg-white p-6 rounded-xl border border-gray-100 shadow-sm"
          >
            <div className="w-12 h-12 bg-[#FFF0ED] text-brand-orange rounded-lg flex items-center justify-center mb-4">
              <ShieldCheck className="w-6 h-6" />
            </div>
            <h3 className="text-lg font-bold text-brand-black mb-2">Scientific Integrity</h3>
            <p className="text-brand-textSecondary text-sm">Context-isolated models preventing Ecological Fallacies. 100% reproducible.</p>
          </motion.div>
        </div>
      </div>
    </div>
  );
}
