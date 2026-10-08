"use client";

import { useRef, useEffect, useState } from "react";
import { topSkills } from "@/lib/data";
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
  const [visible, setVisible] = useState(false);
  const [hovered, setHovered] = useState<string | null>(null);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setTimeout(() => setVisible(true), 140);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  const maxDemand = Math.max(...topSkills.map((s) => s.demand));

  return (
    <div
      ref={ref}
      className={cn(
        "card-interactive transition-all duration-500",
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      )}
    >
      <div className="px-6 py-4">
        <h3 className="text-base font-semibold text-gray-900">Top skills by demand</h3>
        <p className="mt-1 text-sm text-gray-500">Number of postings mentioning each skill across the market.</p>
      </div>
      <div className="px-6 pb-6 space-y-3">
        {topSkills.map((skill) => {
          const pct = (skill.demand / maxDemand) * 100;
          const isHover = hovered === skill.skill;
          return (
            <div key={skill.skill} className="group">
              <div className="flex items-center justify-between gap-2">
                <div className="flex items-center gap-2 min-w-0">
                  <span className={cn("text-sm font-medium", isHover ? "text-brand-700" : "text-gray-900")}>
                    {skillLabel(skill.skill)}
                  </span>
                  <span className="text-xs text-gray-500">{skill.dimension}</span>
                </div>
                <div className="text-right shrink-0">
                  <span className={cn("text-sm font-semibold", isHover ? "text-brand-600" : "text-gray-900")}>
                    {skill.demand.toLocaleString()}
                  </span>
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
