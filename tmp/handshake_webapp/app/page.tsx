import { AnimatedSection } from "@/app/components/ui/animated-section";
import { HeroMetrics } from "@/app/components/market/hero-metrics";
import { ValueProps } from "@/app/components/market/value-props";
import { RecentJobsFeed } from "@/app/components/market/recent-jobs-feed";
import { SkillsCloud } from "@/app/components/skills/skills-cloud";
import Link from "next/link";

const marqueeItems = [
  "Data Scientist",
  "Data Engineer",
  "ML Engineer",
  "Data Analyst",
  "Business Analyst",
  "Software Engineer",
  "Product Manager",
  "Analytics Lead",
];

export default function HomePage() {
  return (
    <>
      <AnimatedSection variant="hero">
        <div className="relative overflow-hidden rounded-3xl bg-gradient-to-b from-brand-50 via-white to-gray-50 px-4 py-16 sm:px-6 sm:py-20 lg:px-8">
          <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_top_right,rgba(99,102,241,0.18),transparent_60%)]" />
          <div className="absolute inset-0 -z-10 bg-[radial-gradient(ellipse_at_bottom_left,rgba(79,70,229,0.08),transparent_60%)]" />

          <div className="mx-auto max-w-3xl text-center">
            <span className="inline-flex items-center gap-1.5 rounded-full border border-brand-200 bg-brand-50 px-3 py-1 text-xs font-semibold uppercase tracking-wide text-brand-700 mb-4 shadow-sm">
              <span className="relative flex h-2 w-2">
                <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-brand-400 opacity-75" />
                <span className="relative inline-flex rounded-full h-2 w-2 bg-brand-500" />
              </span>
              Live market data
            </span>
            <h1 className="text-4xl font-extrabold leading-tight tracking-tight text-gray-900 sm:text-5xl lg:text-6xl">
              Find your next{" "}
              <span className="bg-gradient-to-r from-brand-600 to-indigo-700 bg-clip-text text-transparent">
                data career
              </span>
            </h1>
            <p className="mt-6 text-lg leading-relaxed text-gray-600 sm:text-xl">
              Explore in-demand roles, compare salaries, and understand which skills move the needle — based on real market data, not gut feel.
            </p>
            <div className="mt-8 flex flex-wrap items-center justify-center gap-3">
              <Link
                href="/jobs?role=Data+Scientist"
                className="inline-flex items-center justify-center rounded-xl bg-brand-600 px-6 py-3 text-base font-semibold text-white shadow-lg shadow-brand-200 transition hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-400 focus:ring-offset-2"
              >
                Explore roles
                <svg className="ml-2 h-5 w-5" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                  <path strokeLinecap="round" strokeLinejoin="round" d="M17 8l4 4m0 0l-4 4m4-4H3" />
                </svg>
              </Link>
              <Link
                href="/salary"
                className="inline-flex items-center justify-center rounded-xl border border-gray-300 bg-white px-6 py-3 text-base font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50 focus:outline-none focus:ring-2 focus:ring-brand-400 focus:ring-offset-2"
              >
                Salary explorer
              </Link>
            </div>
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="marquee" className="mt-10 py-6">
        <div className="mx-auto max-w-7xl">
          <div className="text-center text-xs font-semibold uppercase tracking-widest text-gray-500 mb-3">
            Top roles across Indian tech and analytics
          </div>
          <div className="mx-auto flex max-w-4xl">
            {marqueeItems.map((item) => (
              <span key={item} className="whitespace-nowrap text-sm font-semibold tracking-wide uppercase text-gray-500">
                {item}
              </span>
            ))}
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="stats" className="mt-10">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-2xl font-bold text-gray-900">Why this matters</h2>
          <p className="mt-2 text-gray-600">Built from thousands of real postings and validated predictive models.</p>
          <div className="mt-8 grid gap-6 sm:grid-cols-2 lg:grid-cols-4">
            <HeroMetrics metric="roles" subtext="distinct role families analyzed" />
            <HeroMetrics metric="skills" subtext="canonical skills mapped" />
            <HeroMetrics metric="postings" subtext="job postings in our market view" />
            <HeroMetrics metric="models" subtext="validated predictive models" />
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mt-16">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-2xl font-bold text-gray-900">What you can do</h2>
          <div className="mt-6 grid gap-6 sm:grid-cols-2 lg:grid-cols-3">
            <ValueProps
              title="Role comparison"
              description="See how salaries, demand, and experience differ across roles like Data Scientist, Data Engineer, and ML Engineer."
              href="/salary"
              icon="bar-chart"
            />
            <ValueProps
              title="Skill signal"
              description="Understand which skills show up most in postings and which are associated with higher salary bands."
              href="/skills"
              icon="lightning-bolt"
            />
            <ValueProps
              title="Career paths"
              description="Explore common transition paths and the key skills that bridge one role to the next."
              href="/profile"
              icon="route"
            />
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mt-16">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-2xl font-bold text-gray-900">Recent roles</h2>
          <p className="mt-2 text-gray-600">A snapshot of live opportunities.</p>
          <div className="mt-6">
            <RecentJobsFeed />
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mt-16">
        <div className="mx-auto max-w-6xl">
          <h2 className="text-2xl font-bold text-gray-900">Skills in demand</h2>
          <div className="mt-6">
            <SkillsCloud />
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mt-16 pb-10">
        <div className="mx-auto max-w-3xl text-center bg-gradient-to-br from-brand-50 to-indigo-50 rounded-2xl border border-brand-100 p-8 shadow-inner">
          <h2 className="text-2xl font-bold text-gray-900">Ready to compare your profile?</h2>
          <p className="mt-2 text-gray-600">See where you stand against market demand and get focused skill recommendations.</p>
          <div className="mt-6">
            <Link
              href="/profile"
              className="inline-flex items-center justify-center rounded-xl bg-brand-600 px-6 py-3 text-base font-semibold text-white shadow-lg transition hover:bg-brand-700 focus:outline-none focus:ring-2 focus:ring-brand-400 focus:ring-offset-2"
            >
              Start my profile
            </Link>
          </div>
        </div>
      </AnimatedSection>
    </>
  );
}
