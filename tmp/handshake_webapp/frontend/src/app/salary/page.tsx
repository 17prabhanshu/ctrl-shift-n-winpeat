import { RoleSalaryTable } from "@/components/market/table-card";
import { estimateSalaryForRole } from "@/lib/data";
import { SalaryEstimateWidget } from "@/components/salary/salary-estimate-widget";
import { AnimatedSection } from "@/components/ui/animated-section";
import { ExplainSalaryCard } from "@/components/salary/explain-salary-card";

export const metadata = {
  title: "Salaries",
  description: "Compare salaries across data and analytics roles.",
};

export default function SalaryPage() {
  const sampleEstimate = estimateSalaryForRole("Data Scientist");

  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Salaries</h1>
        <p className="mt-2 text-gray-600">
          Compare salaries across roles. Estimates come from our market data extract and are shown as annual figures.
        </p>
      </div>

      <AnimatedSection variant="card-grid" className="mb-12">
        <SalaryEstimateWidget initialRole="Data Scientist" initialEstimate={sampleEstimate} />
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mb-12 grid gap-8 lg:grid-cols-2">
        <div className="space-y-4">
          <h2 className="text-xl font-semibold text-gray-900">Role salary overview</h2>
          <p className="text-sm text-gray-500">Click column headers to sort.</p>
          <RoleSalaryTable />
        </div>
        <div className="space-y-4">
          <ExplainSalaryCard />
        </div>
      </AnimatedSection>

      <section className="rounded-2xl border border-gray-200 bg-gray-50/50 px-6 py-8 text-center sm:text-left">
        <h2 className="text-xl font-semibold text-gray-900">Put this into context</h2>
        <p className="mt-2 text-gray-600">
          Salary depends on role, experience, location, and company. Use the widget above to estimate for a specific role.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 justify-center sm:justify-start">
          <a
            href="#salary-widget"
            className="inline-flex items-center justify-center rounded-xl border border-brand-300 bg-brand-50 px-5 py-2.5 text-sm font-semibold text-brand-700 transition hover:bg-brand-100 hover:text-brand-800"
          >
            Estimate a salary
          </a>
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
