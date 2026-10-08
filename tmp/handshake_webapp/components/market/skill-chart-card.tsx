"use client";

import { useRef, useState, useEffect } from "react";
import { topSkills, formatCurrency } from "@/lib/data";
import { animateOnScroll } from "@/lib/domestic-animate";
import { cn } from "@/lib/utils";

function skillLabel(skill: string): string {
  const map: Record<string, string> = {
    "Machine Learning": "Machine Learning",
    Python: "Python",
    Java: "Java",
    SQL: "SQL",
    Excel: "Excel",
    Tableau: "Tableau",
    Statistics: "Statistics",
    SAS: "SAS",
    R: "R",
    "Big Data": "Big Data",
  };
  return map[skill] ?? skill;
}

export function SkillDemandChart() {
  const ref = useRef<HTMLElement | null>(null);
  const [hovered, setHovered] = useState<string | null>(null);
  animateOnScroll(ref, { duration: 600, classNames: ["opacity-100 translate-y-0", "transition-all duration-500 ease-out"] });

  const maxDemand = Math.max(...topSkills.map((s) => s.demand));

  return (
    <div ref={ref} className="card-interactive">
      <div className="px-6 py-4">
        <h3 className="text-base font-semibold text-gray-900">Top skills by demand</h3>
        <p className="mt-1 text-sm text-gray-500">Number of postings mentioning each skill across the market.</p>
      </div>
      <div className="px-6 pb-6 space-y-3">
        {topSkills.map((skill, index) => {
          const pct = (skill.demand / maxDemand) * 100;
          const isHover = hovered === skill.skill;
          return (
            <div key={skill.skill} className="group">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span className={cn("text-sm font-medium", isHover ? "text-brand-700" : "text-gray-900")}>{skillLabel(skill.skill)}</span>
                  <span className="text-xs text-gray-500">{skill.dimension}</span>
                </div>
                <div className="text-right shrink-0">
                  <span className={cn("text-sm font-semibold", isHover ? "text-brand-600" : "text-gray-900")}>{skill.demand.toLocaleString()}</span>
                  <span className="ml-1 text-xs text-gray-500">posts</span>
                </div>
              </div>
              <div className="mt-1.5 w-full overflow-hidden rounded-full bg-gray-100">
                <div
                  className={cn(
                    "h-2 rounded-full transition-all duration-700 ease-out",
                    isHover ? "bg-brand-500" : "bg-brand-200"
                  )}
                  style={{ width: `${pct}%` }}
                  onMouseEnter={() => setHovered(skill.skill)}
                  onMouseLeave={() => setHovered(null)}
                />
              </div>
            </div>
          );
        })}
      </div>
    </div>
  );
}
