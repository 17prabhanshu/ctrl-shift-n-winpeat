"use client";

import { useRef, useEffect, useState } from "react";
import { cn } from "@/lib/utils";

type MetricKind = "roles" | "skills" | "postings" | "models";

const metricConfig: Record<MetricKind, { value: number; label: string }> = {
  roles: { value: 7, label: "roles" },
  skills: { value: 10, label: "skills" },
  postings: { value: 15.8, label: "postings (K)" },
  models: { value: 8, label: "models" },
};

export function HeroMetrics({ metric, subtext }: { metric: MetricKind; subtext: string }) {
  const ref = useRef<HTMLElement | null>(null);
  const target = metricConfig[metric]?.value ?? 0;
  const [display, setDisplay] = useState(0);

  useEffect(() => {
    const start = performance.now();
    const duration = 1200;
    const step = (now: number) => {
      const t = Math.min((now - start) / duration, 1);
      const eased = 1 - Math.pow(1 - t, 3);
      setDisplay(target * eased);
      if (t < 1) requestAnimationFrame(step);
    };
    requestAnimationFrame(step);
  }, [target]);

  const formatted =
    metric === "postings"
      ? display.toFixed(1) + "K"
      : Math.round(display).toString();

  return (
    <div ref={ref} className="card-interactive p-5 group">
      <div className="flex flex-col space-y-1">
        <span className="text-xs font-semibold uppercase tracking-widest text-brand-600">{subtext}</span>
        <span className="text-4xl font-extrabold tracking-tight text-gray-900 transition-colors group-hover:text-brand-700">
          {formatted}
        </span>
        <span className="text-sm text-gray-500">
          {metric === "postings" ? "job postings" : metricConfig[metric]?.label}
        </span>
      </div>
      <div className="mt-4 h-px w-full bg-gradient-to-r from-transparent via-brand-200 to-transparent opacity-0 transition-opacity group-hover:opacity-100" />
    </div>
  );
}
