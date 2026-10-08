import { useEffect, useRef, useState, type RefObject } from "react";

type AnimationOptions = {
  delay?: number;
  duration?: number;
  easing?: string;
  direction?: "normal" | "alternate";
  classNames?: string[];
  onComplete?: () => void;
};

export function useDomesticAnimate(
  ref: RefObject<HTMLElement | null>,
  opts: AnimationOptions = {},
  deps: React.DependencyList = []
): { running: boolean; elapsed: number } {
  const [running, setRunning] = useState(false);
  const [elapsed, setElapsed] = useState(0);
  const startedAt = useRef(0);

  useEffect(() => {
    const el = ref.current;
    if (!el) return;
    setRunning(true);
    startedAt.current = performance.now();
    const duration = opts.duration ?? 600;
    runAnimation(el, opts);
    const timer = window.setInterval(() => {
      setElapsed(Math.min(performance.now() - startedAt.current, duration));
    }, 16);
    return () => {
      setRunning(false);
      window.clearInterval(timer);
    };
  // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [ref.current, opts.duration, opts.delay, ...deps]);

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
          runAnimation(entry.target, opts);
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

function runAnimation(
  target: HTMLElement | null,
  opts: AnimationOptions
): void {
  if (!target) return;

  const cls = opts.classNames ?? [];
  if (cls.length) {
    cls.forEach((c) => target.classList.add(c));
  }

  const duration = opts.duration ?? 600;
  const delay = opts.delay ?? 0;

  setTimeout(() => {
    try {
      if (typeof window !== "undefined" && typeof (window as any).anime === "function") {
        const r = (window as any).anime(target, {
          duration,
          easing: opts.easing ?? "easeOutCubic",
          direction: opts.direction ?? "normal",
          ...(cls.length ? { begin: () => cls.forEach((c) => target.classList.add(c)) } : {}),
        });
        if (opts.onComplete) {
          if (typeof r?.complete === "function") {
            r.complete = opts.onComplete;
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
        requestAnimationFrame(step);
        return;
      }
      if (t >= 1) {
        target.classList.add("a-visible");
        target.classList.add("a-end");
        opts.onComplete?.();
        return;
      }
      const eased = 1 - Math.pow(1 - t, 3);
      target.style.opacity = String(0.2 + 0.8 * eased);
      target.style.transform = `translateY(${(1 - eased) * 10}px)`;
      requestAnimationFrame(step);
    });
  }, delay);
}
