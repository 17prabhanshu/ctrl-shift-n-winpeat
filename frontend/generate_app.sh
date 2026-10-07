#!/bin/bash
# Generate the rest of the pages

mkdir -p src/app/market src/app/skills src/app/progression src/app/senior src/app/lab src/app/evidence

# MARKET RADAR
cat << 'PAGE' > src/app/market/page.tsx
"use client";
import { motion } from "framer-motion";
export default function MarketRadar() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Market Radar</h1>
      <p className="text-brand-textSecondary mb-8">Career Opportunity Frontier mapping.</p>
      <div className="h-[500px] w-full rounded-xl hairline-border glass-panel flex items-center justify-center text-brand-textSecondary">
        [Interactive Scatter Plot: X=Openings, Y=Median Salary, Size=Experience, Color=Role]
        <br/>(Requires Recharts integration with processed JSON data)
      </div>
    </div>
  );
}
PAGE

# SKILL INTELLIGENCE
cat << 'PAGE' > src/app/skills/page.tsx
"use client";
import { motion } from "framer-motion";
export default function Skills() {
  return (
    <div className="p-8 max-w-6xl mx-auto">
      <h1 className="text-3xl font-bold mb-2">Skill Intelligence</h1>
      <p className="text-brand-textSecondary mb-8">The Skill Co-occurrence Graph.</p>
      <div className="h-[500px] w-full rounded-xl hairline-border glass-panel flex items-center justify-center text-brand-textSecondary">
        [Interactive NetworkX Vis Network]
        <br/>(Hover a node to expand neighborhood and display Skill Signal Index)
      </div>
    </div>
  );
}
PAGE

# CAREER PROGRESSION
cat << 'PAGE' > src/app/progression/page.tsx
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
PAGE

# SENIOR SUCCESS
cat << 'PAGE' > src/app/senior/page.tsx
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
PAGE

# MODEL LAB
cat << 'PAGE' > src/app/lab/page.tsx
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
PAGE
