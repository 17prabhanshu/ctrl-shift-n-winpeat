"use client";

import { useRef, useEffect, useState } from "react";

export function ExplainSalaryCard() {
  const ref = useRef<HTMLElement | null>(null);
  const [visible, setVisible] = useState(false);

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setTimeout(() => setVisible(true), 120);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, []);

  return (
    <div
      ref={ref}
      className={`card-interactive p-6 transition-all duration-500 ${visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"}`}
    >
      <h2 className="text-lg font-semibold text-gray-900">How to read these numbers</h2>
      <ul className="mt-4 space-y-4 text-sm text-gray-600">
        {[
          "Avg salary is the mean across all postings for that role in the current extract.",
          "Estimated range is centered on the median with a modest band around it.",
          "Demand shows how many postings mention the role family.",
          "Experience is the average years requested across those postings.",
        ].map((text, index) => (
          <li key={index} className="flex gap-3">
            <span className="mt-0.5 shrink-0 h-5 w-5 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">
              {index + 1}
            </span>
            <span>{text}</span>
          </li>
        ))}
      </ul>
      <p className="mt-4 text-xs text-gray-400">Salary figures are descriptive and not adjusted for individual negotiation or benefits.</p>
    </div>
  );
}
