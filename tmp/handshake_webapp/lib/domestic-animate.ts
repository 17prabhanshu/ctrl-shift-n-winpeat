import { useEffect, useRef, useState, type RefObject } from "react";

declare const anime: (target: Element | Element[] | string, vars?: any) => {
  duration?: number;
  complete?: () => void;
  play?: () => void;
  pause?: () => void;
  reset?: () => void;
} | { dur?: number; complete?: () => void; play?: () => void; pause?: () => void; reset?: () => void };

type AnimationOptions = {
  delay?: number;
  duration?: number;
  easing?: string;
  direction?: "normal" | "alternate";
  classNames?: string[];
  onComplete?: () => void;
};

function resolveTarget(ref: RefObject<HTMLElement | null>): HTMLElement | null {
  return ref.current;
}

function runAnimation(
  target: HTMLElement | null,
  opts: AnimationOptions,
  scopeRaf: (cb: () => void) => number
): void {
  if (!target) return;

  const cls = opts.classNames ?? [];
  if (cls.length) {
    cls.forEach((c) => target.classList.add(c));
  }

  const duration = opts.duration ?? 600;
  const delay = opts.delay ?? 0;

  setTimeout(() => {
    scopeRaf(() => {
      try {
        if (typeof anime === "function") {
          const r = anime(target, {
            duration,
            easing: opts.easing ?? "easeOutCubic",
            direction: opts.direction ?? "normal",
            ...(cls.length ? { begin: () => cls.forEach((c) => target.classList.add(c)) } : {}),
          } as any);
          if (opts.onComplete) {
            if (typeof r.complete === "function") {
              r.complete = () => opts.onComplete();
            } else {
              setTimeout(opts.onComplete, duration);
            }
          }
          return;
        }
      } catch (e) {
        /* domestic vendor unavailable, continue with class-based simulation */
      }

      let start = performance.now();
      const startClass = cls[0] ?? "a-visible";
      requestAnimationFrame(function step(now: number) {
        const t = (now - start) / duration;
        if (opts.direction === "alternate") {
          const v = Math.abs(Math.sin(t * Math.PI));
          target.style.opacity = String(1 - v * 0.25);
          target.style.transform = `translateY(${(1 - v) * 8}px)`;
          if (t >= 1) {
            target.classList.add("a-end");
            opts.onComplete?.();
            return;
          }
          scopeRaf(step);
          return;
        }
        if (t >= 1) {
          target.classList.add(startClass);
          target.classList.add("a-end");
          opts.onComplete?.();
          return;
        }
        const eased = 1 - Math.pow(1 - t, 3);
        target.style.opacity = String(0.2 + 0.8 * eased);
        target.style.transform = `translateY(${(1 - eased) * 10}px)`;
        scopeRaf(step);
      });
    });
  }, delay);
}

export function useDomesticAnimate(
  ref: RefObject<HTMLElement | null>,
  opts: AnimationOptions = {},
  deps: React.DependencyList = []
): { running: boolean; elapsed: number } {
  const [running, setRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const startedAt = useRef(0);

  useEffect(() => {
    const el = resolveTarget(ref);
    if (!el) return;
    setRunning(true);
    startedAt.current = performance.now();
    runAnimation(el, opts, window.requestAnimationFrame);
    const timer = window.setInterval(() => {
      setElapsed(Math.min(performance.now() - startedAt.current, opts.duration ?? 600));
    }, 16);
    return () => {
      setRunning(false);
      window.clearInterval(timer);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ref.current, opts, ...deps]);

  return { running, elapsed };
}

export function animateOnScroll(
  ref: RefObject<HTMLElement | null>,
  opts: AnimationOptions = {}
): void {
  const observer = new IntersectionObserver(
    (entries) => {
      entries.forEach((entry) => {
        if (entry.isIntersecting) {
          runAnimation(entry.target, opts, window.requestAnimationFrame);
          observer.unobserve(entry.target);
        }
      });
    },
    { threshold: 0.12, rootMargin: "0px 0px -40px 0px" }
  );

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    observer.observe(el);
    return () => observer.disconnect();
  }, [ref.current]);
}

export function useCrazyParallax(
  ref: RefObject<HTMLElement | null>,
  intensity = 0.5
): { x: number; y: number } {
  const [xy, setXy] = useState({ x: 0, y: 0 });
  const rafRef = useRef<number | null>(null);
  const px = intensity * 6;

  useEffect(() => {
    const el = ref.current;
    if (!el) return;

    const move = (e: MouseEvent) => {
      if (rafRef.current != null) return;
      const rect = el.getBoundingClientRect();
      const cx = rect.left + rect.width / 2;
      const cy = rect.top + rect.height / 2;
      const dx = (e.clientX - cx) / rect.width;
      const dy = (e.clientY - cy) / rect.height;
      rafRef.current = window.requestAnimationFrame(() => {
        setXy({ x: dx * px, y: dy * px });
        rafRef.current = null;
      });
    };

    const leave = () => setXy({ x: 0, y: 0 });
    window.addEventListener("mousemove", move, { passive: true });
    window.addEventListener("mouseleave", leave, { passive: true });

    return () => {
      window.removeEventListener("mousemove", move);
      window.removeEventListener("mouseleave", leave);
      if (rafRef.current != null) {
        window.cancelAnimationFrame(rafRef.current);
        rafRef.current = null;
      }
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [intensity, ref.current]);

  return xy;
}

export const ANIMATION_CLASSES: Record<string, string> = {
  "a-visible": "opacity-100 translate-y-0 transition-[opacity,transform] duration-500 ease-out",
  "a-end": "transition-none",
};
