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
