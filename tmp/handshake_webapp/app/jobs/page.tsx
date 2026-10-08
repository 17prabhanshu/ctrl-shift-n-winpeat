import { RoleSalaryTable } from "@/app/components/market/table-card";
import { SkillDemandChart } from "@/app/components/market/skill-chart-card";
import { sampleJobPostings } from "@/lib/data";
import Link from "next/link";
import { RecentJobsFeed } from "@/app/components/market/recent-jobs-feed";

export const metadata = {
  title: "Jobs",
  description: "Browse data and analytics roles with salary estimates and skill requirements.",
};

export default function JobsPage() {
  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Jobs</h1>
        <p className="mt-2 text-gray-600">
          Explore in-demand data and analytics roles. Salary estimates are derived from real market data.
        </p>
      </div>

      <section className="mb-12">
        <div className="flex flex-col gap-4 sm:flex-row sm:items-center sm:justify-between">
          <div>
            <h2 className="text-xl font-semibold text-gray-900">Browse roles</h2>
            <p className="text-sm text-gray-500">5 featured roles to start</p>
          </div>
          <Link
            href="/jobs?role=all"
            className="inline-flex items-center justify-center rounded-lg border border-gray-300 bg-white px-4 py-2 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50"
          >
            Show all
          </Link>
        </div>
        <RecentJobsFeed />
      </section>

      <section className="mb-12 grid gap-8 lg:grid-cols-2">
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Role salary and demand</h2>
          <p className="mt-1 text-sm text-gray-500">Compare average salaries, demand, and experience requirements across role families.</p>
          <div className="mt-4">
            <RoleSalaryTable />
          </div>
        </div>
        <div>
          <h2 className="text-xl font-semibold text-gray-900">Top skills by demand</h2>
          <p className="mt-1 text-sm text-gray-500">Which skills show up most often across postings.</p>
          <div className="mt-4">
            <SkillDemandChart />
          </div>
        </div>
      </section>

      <section className="rounded-2xl border border-gray-200 bg-gray-50/50 px-6 py-8 text-center sm:text-left">
        <h2 className="text-xl font-semibold text-gray-900">Want targeted recommendations?</h2>
        <p className="mt-2 text-gray-600">
          Tell us your profile and we will surface the skills that matter most for your target role.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 justify-center sm:justify-start">
          <Link
            href="/profile"
            className="inline-flex items-center justify-center rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
          >
            Build my profile
          </Link>
          <Link
            href="/salary"
            className="inline-flex items-center justify-center rounded-xl border border-gray-300 bg-white px-5 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50"
          >
            Explore salaries
          </Link>
        </div>
      </section>
    </>
  );
}
