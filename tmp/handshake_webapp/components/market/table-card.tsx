"use client";

import { useRef, useState, useMemo } from "react";
import { roleSalaryStats, formatCurrency } from "@/lib/data";
import { animateOnScroll } from "@/lib/domestic-animate";
import { cn } from "@/lib/utils";
import { ChevronUpDownIcon } from "@heroicons/react/24/solid";
import { ReactNode } from "react";

export function RoleSalaryTable() {
  const ref = useRef<HTMLElement | null>(null);
  animateOnScroll(ref, { duration: 600, classNames: ["opacity-100 translate-y-0", "transition-all duration-500 ease-out"] });

  const [sortKey, setSortKey] = useState<keyof typeof roleSalaryStats[0]>("avgSalary");
  const [sortDir, setSortDir] = useState<"asc" | "desc">("desc");

  const sorted = useMemo(() => {
    const copy = [...roleSalaryStats];
    copy.sort((a, b) => {
      const aVal = a[sortKey];
      const bVal = b[sortKey];
      const cmp = typeof aVal === "number" && typeof bVal === "number" ? aVal - bVal : String(aVal).localeCompare(String(bVal));
      return sortDir === "asc" ? cmp : -cmp;
    });
    return copy;
  }, [sortKey, sortDir]);

  const header = (label: string, key: keyof typeof roleSalaryStats[0], align?: "left" | "right" | "center") => (
    <th
      key={key}
      className={cn(
        "whitespace-nowrap rounded-tl-lg border-b border-gray-200 bg-gray-50 px-4 py-3 text-left text-xs font-semibold uppercase tracking-wider text-gray-500 first:rounded-tl-lg last:rounded-tr-lg",
        align === "right" ? "text-right" : "",
        align === "center" ? "text-center" : "",
      )}
      onClick={() => {
        if (sortKey === key) setSortDir((d) => (d === "asc" ? "desc" : "asc"));
        else { setSortKey(key); setSortDir(key === "avgSalary" || key === "demand" ? "desc" : "asc"); }
      }}
    >
      <span className="flex items-center gap-1 cursor-pointer">
        {label}
        {sortKey === key ? (
          <span className="inline-flex"><ChevronUpDownIcon className={cn("h-4 w-4", sortDir === "desc" ? "rotate-180" : "")} /></span>
        ) : (
          <ChevronUpDownIcon className="h-4 w-4 opacity-40" />
        )}
      </span>
    </th>
  );

  const cell = (value: ReactNode, align?: "left" | "right" | "center", className?: string) => (
    <td className={cn(
      "border-b border-gray-100 px-4 py-3 text-sm text-gray-700 first:rounded-bl-lg last:rounded-br-lg",
      align === "right" ? "text-right" : "",
      align === "center" ? "text-center" : "",
      className ?? ""
    )}>
      {value}
    </td>
  );

  return (
    <div ref={ref} className="card-interactive overflow-hidden">
      <div className="px-6 py-4">
        <h3 className="text-base font-semibold text-gray-900">Role salary and demand overview</h3>
        <p className="mt-1 text-sm text-gray-500">Click column headers to sort. Annual salary estimates based on current market extract.</p>
      </div>
      <div className="overflow-x-auto">
        <table className="min-w-full divide-y divide-gray-200">
          <thead className="bg-gray-50">
            <tr>
              {header("Role", "role")}
              {header("Experience (yrs)", "avgExperience", "right")}
              {header("Demand", "demand", "right")}
              {header("Avg salary", "avgSalary", "right")}
              {header("Est. range", "medianSalary", "right")}
              {header("Postings (n)", "n", "right")}
            </tr>
          </thead>
          <tbody className="divide-y divide-gray-100">
            {sorted.map((row) => (
              <tr key={row.role} className="group transition-colors hover:bg-brand-50">
                {cell(
                  <>
                    <span className="font-medium text-gray-900 group-hover:text-brand-700">{row.role}</span>
                  </>
                )}
                {cell(row.avgExperience.toFixed(1), "right")}
                {cell(row.demand.toLocaleString(), "right")}
                {cell(
                  <span className="font-semibold text-gray-900 group-hover:text-brand-600">{formatCurrency(row.avgSalary)}</span>,
                  "right"
                )}
                {cell(
                  row.medianSalary ? (
                    <span>{formatCurrency(Math.round(row.medianSalary * 0.85))} - {formatCurrency(Math.round(row.medianSalary * 1.25))}</span>
                  ) : (
                    <span className="text-gray-400">—</span>
                  ),
                  "right"
                )}
                {cell(row.n.toLocaleString(), "right")}
              </tr>
            ))}
          </tbody>
        </table>
      </div>
    </div>
  );
}
