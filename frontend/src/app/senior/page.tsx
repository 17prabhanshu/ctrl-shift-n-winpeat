"use client";
import { motion } from "framer-motion";
export default function Senior() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Senior Success Signal & Forensics</h1>
      <p className="text-brand-textSecondary mb-8">Auditing the 0.998 AUC anomaly.</p>
      <div className="p-6 rounded-xl border border-brand-red/30 bg-brand-red/5 mb-8">
        <h3 className="text-brand-red font-bold flex items-center gap-2 mb-2">
          <span>⚠️</span> UNUSUAL SEPARABILITY DETECTED
        </h3>
        <p className="text-sm text-brand-textPrimary">
          The ExtraTrees model achieved an exploratory AUC of 0.998. This triggered an automated forensic audit.
          Shallow tree testing confirmed the dataset labels are likely derived from a deterministic threshold (Openness &gt; 38.5).
        </p>
      </div>
    </div>
  );
}
