"use client";

import { useRef, useEffect, useState, useMemo } from "react";
import { topSkills } from "@/lib/data";
import { cn } from "@/lib/utils";
import { ChevronUpDownIcon } from "@heroicons/react/24/solid";
import type { ReactNode } from "react";

const salaryLabel: Record<string, string> = {
  high: "High impact",
  moderate: "Moderate impact",
  low: "Low impact",
  variable: "Variable",
};

export function SkillDetailTable() {
  const ref = useRef<HTMLElement | null>(null);
  const [visible, setVisible] = useState(false);
  const [sortKey, setSortKey] = useState<keyof typeof topSkills[0]>("demand");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setTimeout(() => setVisible(true), 150);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  const sorted = useMemo(() => {
    const copy = [...topSkills];
    copy.sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      const cmp =
        typeof aVal === "number" && typeof bVal === "number"
          ? aVal - bVal
          : String(aVal).localeCompare(String(bVal));
      return sortDir === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [sortKey, sortDir]);

  return (
    <div
      ref={ref}
      className={cn(
        "card-interactive overflow-hidden transition-all duration-500",
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      )}
    >
      <div className="px-6 py-4">
        <h3 className="text-base font-semibold text-gray-900">Skill detail</h3>
        <p className="mt-1 text-sm text-gray-500">Sortable skill table with salary impact.</p>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              <th className="whitespace-nowrap rounded-tl-lg border-b border-gray-200 bg-gray-50 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                Skill
              </th>
              <th
                className="whitespace-nowrap border-b border-gray-200 bg-gray-50 px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-500 cursor-pointer select-none"
                onClick={() => {
                  setSortKey("demand");
                  setSortDir("desc");
                }}
              >
                <span className="flex items-center justify-end gap-1">
                  Demand
                  <ChevronUpDownIcon className="h-4 w-4" />
                </span>
              </th>
              <th
                className="whitespace-nowrap border-b border-gray-200 bg-gray-50 px-4 py-3 text-right text-xs font-semibold uppercase tracking-wider text-gray-500 cursor-pointer select-none"
                onClick={() => {
                  setSortKey("salaryAssociation");
                  setSortDir("desc");
                }}
              >
                <span className="flex items-center justify-end gap-1">
                  Salary impact
                  <ChevronUpDownIcon className="h-4 w-4" />
                </span>
              </th>
              <th className="whitespace-nowrap rounded-tr-lg border-b border-gray-200 bg-gray-50 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500">
                Dimension
              </th>
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sorted.map((skill) => {
              const dimColor =
                skill.dimension === "Coding"
                  ? "bg-blue-50 text-blue-700 border-blue-200"
                  : skill.dimension === "AI/ML"
                  ? "bg-purple-50 text-purple-700 border-purple-200"
                  : skill.dimension === "Maths/Stats"
                  ? "bg-emerald-50 text-emerald-700 border-emerald-200"
                  : skill.dimension === "Dashboard/Storytelling"
                  ? "bg-amber-50 text-amber-700 border-amber-200"
                  : "bg-rose-50 text-rose-700 border-rose-200";
              return (
                <tr key={skill.skill} className="group hover:bg-brand-50 transition-colors">
                  <td className="whitespace-nowrap px-4 py-3 text-sm font-medium text-gray-900 group-hover:text-brand-700">
                    {skill.skill}
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700 text-right">
                    {skill.demand.toLocaleString()}
                  </td>
                  <td className="whitespace-nowrap px-4 py-3 text-sm text-gray-700 text-right">
                    <span
                      className={cn(
                        "inline-flex items-center rounded-full px-2 py-0.5 text-xs font-semibold",
                        skill.salaryAssociation === "high"
                          ? "bg-green-50 text-green-700"
                          : skill.salaryAssociation === "moderate"
                          ? "bg-amber-50 text-amber-700"
                          : skill.salaryAssociation === "low"
                          ? "bg-gray-100 text-gray-600"
                          : "bg-purple-50 text-purple-700"
                      )}
                    >
                      {salaryLabel[skill.salaryAssociation] ?? skill.salaryAssociation}
                    </span>
                  </td>
                  <td className="whitespace-nowrap px-4 py-3">
                    <span className={cn("inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium", dimColor)}>
                      {skill.dimension}
                    </span>
                  </td>
                </tr>
              );
            })}
          </tbody>
        </table>
      </div>
    </div>
  );
}
