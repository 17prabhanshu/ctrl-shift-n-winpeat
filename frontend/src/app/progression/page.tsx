"use client";
import { motion } from "framer-motion";
export default function Progression() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Early-Career Progression Signal</h1>
      <p className="text-brand-textSecondary mb-8">Interaction surface mapping technical vs communication impact.</p>
      <div className="grid grid-cols-1 md:grid-cols-2 gap-8">
        <div className="h-[400px] rounded-xl hairline-border glass-panel flex items-center justify-center text-brand-textSecondary">
          [JDS Radar Chart: Big Data, Math, Coding, AI, Dashboard]
        </div>
        <div className="h-[400px] rounded-xl hairline-border glass-panel flex items-center justify-center text-brand-textSecondary">
          [SHAP Feature Importance Beeswarm]
        </div>
      </div>
    </div>
  );
}
