"use client";

import Link from "next/link";
import { useRef, useEffect, useState } from "react";
import { sampleJobPostings, formatCurrency } from "@/lib/data";
import { cn } from "@/lib/utils";
import { BriefcaseIcon, MapPinIcon, ClockIcon } from "@heroicons/react/24/outline";

export function RecentJobsFeed() {
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
      className={cn(
        "card-interactive divide-y divide-gray-100 transition-all duration-500",
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
      )}
    >
      {sampleJobPostings.map((job) => (
        <Link
          key={job.id}
          href={`/jobs/${job.slug}`}
          className="group block px-6 py-4 transition-colors hover:bg-gray-50 first:pt-0 last:pb-0"
        >
          <div className="flex items-start justify-between gap-4">
            <div className="min-w-0 flex-1">
              <div className="flex flex-wrap items-center gap-2">
                <h3 className="text-base font-semibold text-gray-900 group-hover:text-brand-700 truncate">{job.title}</h3>
                <span className="rounded-full bg-gray-100 px-2.5 py-0.5 text-xs font-medium text-gray-600 group-hover:bg-brand-50 group-hover:text-brand-700">
                  {job.roleFamily}
                </span>
              </div>
              <div className="mt-1 flex flex-wrap items-center gap-x-4 text-sm text-gray-500">
                <span className="inline-flex items-center gap-1"><BriefcaseIcon className="h-4 w-4 text-gray-400" /> {job.company}</span>
                <span className="inline-flex items-center gap-1"><MapPinIcon className="h-4 w-4 text-gray-400" /> {job.location}</span>
                <span className="inline-flex items-center gap-1"><ClockIcon className="h-4 w-4 text-gray-400" /> {job.experienceMin === 0 ? "Entry level" : `${job.experienceMin} - ${job.experienceMax} yrs`}</span>
              </div>
              <p className="mt-2 flex flex-wrap gap-1.5 text-sm text-gray-700">
                {job.skills.map((s) => (
                  <span key={s} className="chip">{s}</span>
                ))}
              </p>
            </div>
            <div className="shrink-0 text-right">
              <div className="text-lg font-semibold text-gray-900 group-hover:text-brand-600">
                {formatCurrency(job.salaryMin)} - {formatCurrency(job.salaryMax)}
              </div>
              <div className="text-xs text-gray-500">annual estimate</div>
            </div>
          </div>
        </Link>
      ))}
      <div className="px-6 py-3 text-center">
        <Link
          href="/jobs"
          className="inline-flex items-center justify-center rounded-lg border border-brand-300 bg-brand-50 px-4 py-2 text-sm font-semibold text-brand-700 transition hover:bg-brand-100 hover:text-brand-800"
        >
          View all roles
        </Link>
      </div>
    </div>
  );
}
