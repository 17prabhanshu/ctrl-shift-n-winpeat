import { SkillDemandChart } from "@/app/components/market/skill-chart-card";
import { SkillsCloud } from "@/app/components/skills/skills-cloud";
import { AnimatedSection } from "@/app/components/ui/animated-section";
import { SkillDetailTable } from "@/app/components/skills/skill-detail-table";
import Link from "next/link";

export const metadata = {
  title: "Skills",
  description: "See which skills are in demand and how they relate to salary.",
};

export default function SkillsPage() {
  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Skills</h1>
        <p className="mt-2 text-gray-600">
          Understand which skills appear most often in postings and how they relate to salary.
        </p>
      </div>

      <AnimatedSection variant="card-grid" className="mb-12 grid gap-8 lg:grid-cols-2">
        <SkillDemandChart />
        <SkillsCloud />
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mb-12">
        <SkillDetailTable />
      </AnimatedSection>

      <section className="rounded-2xl border border-gray-200 bg-gray-50/50 px-6 py-8 text-center sm:text-left">
        <h2 className="text-xl font-semibold text-gray-900">Want a personalized view?</h2>
        <p className="mt-2 text-gray-600">
          See which of these skills matter most for your target role.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 justify-center sm:justify-start">
          <Link
            href="/profile"
            className="inline-flex items-center justify-center rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
          >
            Build my profile
          </Link>
          <Link
            href="/jobs"
            className="inline-flex items-center justify-center rounded-xl border border-gray-300 bg-white px-5 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50"
          >
            Browse roles
          </Link>
        </div>
      </section>
    </>
  );
}
