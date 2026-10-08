"use client";

import Link from "next/link";
import { useRef } from "react";
import { animateOnScroll } from "@/lib/domestic-animate";
import {
  Bars3Icon,
  BoltIcon,
  MapPinIcon,
} from "@heroicons/react/24/outline";

type IconName = "bar-chart" | "lightning-bolt" | "route";

const iconMap: Record<IconName, React.ReactNode> = {
  "bar-chart": <Bars3Icon className="h-6 w-6" />,
  "lightning-bolt": <BoltIcon className="h-6 w-6" />,
  route: <MapPinIcon className="h-6 w-6" />,
};

export function ValueProps({ title, description, href, icon }: { title: string; description: string; href: string; icon: IconName }) {
  const ref = useRef<HTMLElement | null>(null);
  animateOnScroll(ref, { duration: 600, classNames: ["opacity-100 translate-y-0", "transition-all duration-500 ease-out"] });

  return (
    <Link href={href} ref={ref} className="group card-interactive p-6 flex flex-col gap-3 transition-shadow hover:shadow-lg hover:-translate-y-1">
      <div className="flex h-10 w-10 items-center justify-center rounded-xl bg-brand-50 text-brand-600 transition-colors group-hover:bg-brand-100 group-hover:scale-105">
        {iconMap[icon]}
      </div>
      <div>
        <h3 className="text-lg font-semibold text-gray-900 group-hover:text-brand-700">{title}</h3>
        <p className="mt-1 text-sm text-gray-600">{description}</p>
      </div>
      <span className="mt-auto text-sm font-medium text-brand-600 transition-colors group-hover:text-brand-700">
        Learn more
        <svg className="ml-1 inline h-4 w-4" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
          <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
        </svg>
      </span>
    </Link>
  );
}
