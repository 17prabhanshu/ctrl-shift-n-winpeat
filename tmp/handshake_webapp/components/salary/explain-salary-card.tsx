"use client";

import { useRef } from "react";
import { animateOnScroll } from "@/lib/domestic-animate";

export function ExplainSalaryCard() {
  const ref = useRef<HTMLElement | null>(null);
  animateOnScroll(ref, { duration: 600, classNames: ["opacity-100 translate-y-0", "transition-all duration-500 ease-out"] });

  return (
    <div ref={ref} className="card-interactive p-6">
      <h2 className="text-lg font-semibold text-gray-900">How to read these numbers</h2>
      <ul className="mt-4 space-y-4 text-sm text-gray-600">
        <li className="flex gap-3">
          <span className="mt-0.5 shrink-0 h-5 w-5 shrink-0 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">1</span>
          <span>Avg salary is the mean across all postings for that role in the current extract.</span>
        </li>
        <li className="flex gap-3">
          <span className="mt-0.5 shrink-0 h-5 w-5 shrink-0 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">2</span>
          <span>Estimated range is centered on the median with a modest band around it.</span>
        </li>
        <li className="flex gap-3">
          <span className="mt-0.5 shrink-0 h-5 w-5 shrink-0 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">3</span>
          <span>Demand shows how many postings mention the role family.</span>
        </li>
        <li className="flex gap-3">
          <span className="mt-0.5 shrink-0 h-5 w-5 shrink-0 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">4</span>
          <span>Experience is the average years requested across those postings.</span>
        </li>
      </ul>
      <p className="mt-4 text-xs text-gray-400">Salary figures are descriptive and not adjusted for individual negotiation or benefits.</p>
    </div>
  );
}
