"use client";

import { useEffect, useRef, useState, type ReactNode } from "react";
import { useDomesticAnimate, animateOnScroll, ANIMATION_CLASSES } from "@/lib/domestic-animate";
import { cn } from "@/lib/utils";

type SectionVariant = "hero" | "marquee" | "stats" | "card-grid";

interface AnimatedSectionProps {
  variant: SectionVariant;
  children: ReactNode;
  className?: string;
  delay?: number;
}

function heroContent(ref: React.RefObject<HTMLElement | null>, delay: number, visible: boolean) {
  const opts = { delay, duration: 800, classNames: [ANIMATION_CLASSES["a-visible"]] };
  useDomesticAnimate(ref, opts);
}

interface MarqueeItemProps {
  text: string;
  className?: string;
}

function MarqueeItem({ text, className }: MarqueeItemProps) {
  const ref = useRef<HTMLElement | null>(null);
  animateOnScroll(ref, { duration: 700, classNames: [ANIMATION_CLASSES["a-visible"]] });
  return (
    <span
      ref={ref}
      className={cn("whitespace-nowrap text-sm font-semibold tracking-wide uppercase text-gray-500", className)}
    >
      {text}
    </span>
  );
}

function Marquee({ children }: { children: ReactNode }) {
  const ref = useRef<HTMLElement | null>(null);
  const [trackStyle, setTrackStyle] = useState<React.CSSProperties>({});

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    const clone = el.cloneNode(true) as HTMLElement;
    clone.style.setProperty("translate", "0");
    el.style.setProperty("translate", "0px");
    setTrackStyle({ maskImage: "linear-gradient(to right, transparent, #000 12%, #000 88%, transparent)" });
  }, []);

  return (
    <section
      ref={ref}
      className="overflow-hidden relative w-full select-none"
      style={trackStyle}
    >
      <div className="flex animate-marquee whitespace-nowrap">
        {children}
        {children}
      </div>
      <style>{`
        @keyframes marquee {
          0% { transform: translateX(0); }
          100% { transform: translateX(-50%); }
        }
        .animate-marquee {
          animation: marquee 38s linear infinite;
        }
        @media (prefers-reduced-motion: reduce) {
          .animate-marquee { animation: none; }
        }
      `}</style>
    </section>
  );
}

function Stats({ children }: { children: ReactNode }) {
  const ref = useRef<HTMLElement | null>(null);
  animateOnScroll(ref, { duration: 700, classNames: [ANIMATION_CLASSES["a-visible"]] });
  return <div ref={ref} className="w-full">{children}</div>;
}

export function AnimatedSection({ variant, children, className, delay = 0 }: AnimatedSectionProps) {
  const ref = useRef<HTMLElement | null>(null);

  useEffect(() => {
    if (variant === "hero") heroContent(ref, delay, true);
  }, [variant, delay]);

  if (variant === "marquee") return <Marquee>{children}</Marquee>;
  if (variant === "stats") return <Stats>{children}</Stats>;
  return (
    <section
      ref={ref}
      className={cn(
        "w-full animate-on-scroll",
        variant === "hero" ? "hero-fade-in" : "",
        className
      )}
    >
      {children}
      {variant === "hero" && (
        <style>{`
          @keyframes hero-fade-in {
            from { opacity: 0; transform: translateY(12px); }
            to { opacity: 1; transform: translateY(0); }
          }
          .hero-fade-in { animation: hero-fade-in 800ms cubic-bezier(0.2, 0.8, 0.2, 1) both; }
          @media (prefers-reduced-motion: reduce) {
            .hero-fade-in { animation: none; opacity: 1; transform: none; }
          }
        `}</style>
      )}
    </section>
  );
}

export { MarqueeItem };
