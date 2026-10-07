"use client";
import { motion } from "framer-motion";
export default function Lab() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Model Lab</h1>
      <p className="text-brand-textSecondary mb-8">Cross-validation benchmarks and calibration curves.</p>
      <div className="w-full rounded-xl hairline-border glass-panel overflow-hidden">
        <table className="w-full text-sm text-left">
          <thead className="bg-white/5 border-b border-white/10 text-brand-textSecondary">
            <tr>
              <th className="px-6 py-4 font-medium uppercase text-xs tracking-wider">Model</th>
              <th className="px-6 py-4 font-medium uppercase text-xs tracking-wider">Dataset</th>
              <th className="px-6 py-4 font-medium uppercase text-xs tracking-wider">AUC</th>
              <th className="px-6 py-4 font-medium uppercase text-xs tracking-wider">Accuracy</th>
            </tr>
          </thead>
          <tbody className="divide-y divide-white/5 text-brand-textPrimary">
            <tr className="hover:bg-white/5">
              <td className="px-6 py-4">Logistic Regression</td>
              <td className="px-6 py-4">Junior (JDS)</td>
              <td className="px-6 py-4 text-brand-cyan">0.904</td>
              <td className="px-6 py-4">0.865</td>
            </tr>
            <tr className="hover:bg-white/5">
              <td className="px-6 py-4">ExtraTrees</td>
              <td className="px-6 py-4">Senior (SDS)</td>
              <td className="px-6 py-4 text-brand-red">0.998</td>
              <td className="px-6 py-4">0.972</td>
            </tr>
          </tbody>
        </table>
      </div>
    </div>
  );
}
