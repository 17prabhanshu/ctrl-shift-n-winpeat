import Link from "next/link";

export const metadata = {
  title: "Companies",
  description: "Explore companies hiring for data and analytics roles.",
};

const companies = [
  { name: "AnalyticsCorp", roles: 3, locations: ["Bangalore", "Hyderabad"] },
  { name: "DataInfra Pvt Ltd", roles: 2, locations: ["Hyderabad", "Pune"] },
  { name: "AIFirst Labs", roles: 2, locations: ["Bangalore"] },
  { name: "InsightWorks", roles: 2, locations: ["Pune", "Mumbai"] },
  { name: "StrategyBridge", roles: 1, locations: ["Mumbai"] },
];

export default function CompaniesPage() {
  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Companies</h1>
        <p className="mt-2 text-gray-600">
          Explore companies hiring for data and analytics roles.
        </p>
      </div>

      <div className="mb-8 rounded-2xl border border-gray-200 bg-white p-6 shadow-sm">
        <h2 className="text-lg font-semibold text-gray-900">Featured companies</h2>
        <p className="mt-1 text-sm text-gray-500">Companies with roles in our current market extract.</p>
        <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
          {companies.map((company) => (
            <div key={company.name} className="rounded-xl border border-gray-200 bg-white p-4 shadow-sm transition hover:border-brand-300 hover:shadow-md">
              <div className="flex items-center gap-3">
                <div className="flex h-10 w-10 items-center justify-center rounded-lg bg-brand-50 text-brand-600 font-bold">
                  {company.name[0]}
                </div>
                <div>
                  <div className="font-semibold text-gray-900">{company.name}</div>
                  <div className="text-sm text-gray-500">
                    {company.locations.join(" · ")}
                  </div>
                </div>
              </div>
              <div className="mt-3 flex items-center justify-between">
                <span className="text-sm text-gray-500">{company.roles} role company</span>
                <Link
                  href="/jobs"
                  className="text-sm font-medium text-brand-600 hover:text-brand-700"
                >
                  View roles
                </Link>
              </div>
            </div>
          ))}
        </div>
      </div>

      <section className="rounded-2xl border border-gray-200 bg-gray-50/50 px-6 py-8 text-center sm:text-left">
        <h2 className="text-xl font-semibold text-gray-900">Explore opportunities</h2>
        <p className="mt-2 text-gray-600">
          Browse roles across companies and see which skills they value.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 justify-center sm:justify-start">
          <Link
            href="/jobs"
            className="inline-flex items-center justify-center rounded-xl bg-brand-600 px-5 py-2.5 text-sm font-semibold text-white shadow-sm transition hover:bg-brand-700"
          >
            Browse jobs
          </Link>
          <Link
            href="/profile"
            className="inline-flex items-center justify-center rounded-xl border border-gray-300 bg-white px-5 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50"
          >
            Build my profile
          </Link>
        </div>
      </section>
    </>
  );
}
