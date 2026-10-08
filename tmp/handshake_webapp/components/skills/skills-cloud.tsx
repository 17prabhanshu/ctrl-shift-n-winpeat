"use client";

import { useRef, useState } from "react";
import { topSkills } from "@/lib/data";
import { animateOnScroll } from "@/lib/domestic-animate";
import { cn } from "@/lib/utils";

const dimensionColor: Record<string, string> = {
  "Coding": "bg-blue-50 text-blue-700 border-blue-200",
  "AI/ML": "bg-purple-50 text-purple-700 border-purple-200",
  "Maths/Stats": "bg-emerald-50 text-emerald-700 border-emerald-200",
  "Dashboard/Storytelling": "bg-amber-50 text-amber-700 border-amber-200",
  "Big Data": "bg-rose-50 text-rose-700 border-rose-200",
};

export function SkillsCloud() {
  const ref = useRef<HTMLElement | null>(null);
  const [selected, setSelected] = useState<string | null>(null);
  animateOnScroll(ref, { duration: 600, classNames: ["opacity-100 translate-y-0", "transition-all duration-500 ease-out"] });

  return (
    <div ref={ref} className="card-interactive p-6">
      <div className="mb-4">
        <h3 className="text-base font-semibold text-gray-900">Skill cloud</h3>
        <p className="mt-1 text-sm text-gray-500">Click a skill to see its details.</p>
      </div>
      <div className="relative">
        <div className="flex flex-wrap gap-2">
          {topSkills.map((skill) => {
            const size = Math.max(12, Math.round(14 + (skill.demand / 3210) * 6));
            const dimColor = dimensionColor[skill.dimension] ?? "bg-gray-50 text-gray-700 border-gray-200";
            return (
              <button
                key={skill.skill}
                className={cn(
                  "rounded-2xl border px-3 py-1.5 text-sm font-medium transition-all",
                  dimColor,
                  selected === skill.skill ? "shadow-md scale-110 ring-2 ring-brand-300" : "shadow-sm hover:scale-105",
                  "leading-tight"
                )}
                style={{ fontSize: `${size}px` }}
                onClick={() => setSelected((prev) => (prev === skill.skill ? null : skill.skill))}
              >
                {skill.skill}
              </button>
            );
          })}
        </div>
        {selected && (
          <div className="mt-4 rounded-xl border border-brand-200 bg-brand-50 p-4 text-sm text-gray-800 shadow-sm">
            <p className="font-semibold text-brand-800">{selected}</p>
            <div className="mt-1 flex flex-wrap gap-2 text-xs">
              <span className="rounded-full bg-white px-2 py-0.5 text-gray-600 border border-gray-200">{topSkills.find((s) => s.skill === selected)?.dimension}</span>
              <span className="rounded-full bg-white px-2 py-0.5 text-gray-600 border border-gray-200">{topSkills.find((s) => s.skill === selected)?.demand.toLocaleString()} postings</span>
              <span className="rounded-full bg-white px-2 py-0.5 text-gray-600 border border-gray-200">Salary impact: {topSkills.find((s) => s.skill === selected)?.salaryAssociation}</span>
            </div>
          </div>
        )}
      </div>
    </div>
  );
}
