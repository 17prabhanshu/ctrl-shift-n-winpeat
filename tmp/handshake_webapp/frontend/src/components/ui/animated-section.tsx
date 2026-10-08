"use client";

import { useRef, useEffect, useState, type ReactNode } from "react";
import { cn } from "@/lib/utils";

type SectionVariant = "hero" | "marquee" | "stats" | "card-grid";

interface AnimatedSectionProps {
  variant: SectionVariant;
  children: ReactNode;
  className?: string;
  delay?: number;
  as?: keyof JSX.IntrinsicElements;
}

const DEFAULT_CLASSES: Record<SectionVariant, string> = {
  hero: "hero-fade-in",
  marquee: "marquee-wrapper",
  stats: "stats-fade-in",
  "card-grid": "card-grid-fade-in",
};

export function AnimatedSection({
  variant,
  children,
  className,
  delay = 0,
  as: Tag = "section",
}: AnimatedSectionProps) {
  const ref = useRef<HTMLDivElement>(null);
  const [visible, setVisible] = useState(false);
  const classes = DEFAULT_CLASSES[variant];

  useEffect(() => {
    const observer = new IntersectionObserver(
      (entries) => {
        entries.forEach((entry) => {
          if (entry.isIntersecting) {
            setTimeout(() => setVisible(true), delay);
            observer.unobserve(entry.target);
          }
        });
      },
      { threshold: 0.1 }
    );
    if (ref.current) observer.observe(ref.current);
    return () => observer.disconnect();
  }, [delay]);

  return (
    <Tag
      ref={ref}
      className={cn(
        "w-full transition-all duration-700",
        visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4",
        classes,
        className
      )}
    >
      {children}
    </Tag>
  );
}
