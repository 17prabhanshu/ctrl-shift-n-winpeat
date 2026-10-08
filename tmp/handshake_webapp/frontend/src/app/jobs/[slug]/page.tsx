import { notFound } from "next/navigation";
import { sampleJobPostings, formatCurrency } from "@/lib/data";
import { JobInsightCard } from "@/components/jobs/job-insight-card";
import Link from "next/link";

export async function generateStaticParams() {
  return sampleJobPostings.map((job) => ({ slug: job.slug }));
}

export async function generateMetadata({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const job = sampleJobPostings.find((j) => j.slug === slug);
  if (!job) return {};
  return {
    title: `${job.title} at ${job.company}`,
    description: `${job.title} in ${job.location} at ${job.company}. Salary estimate and required skills.`,
  };
}

export default async function JobDetailPage({ params }: { params: Promise<{ slug: string }> }) {
  const { slug } = await params;
  const job = sampleJobPostings.find((j) => j.slug === slug);
  if (!job) notFound();

  const related = sampleJobPostings.filter((j) => j.roleFamily === job.roleFamily && j.id !== job.id).slice(0, 3);

  return (
    <>
      <div className="mb-8">
        <nav className="text-sm text-gray-500">
          <Link href="/jobs" className="hover:text-brand-600">Jobs</Link>
          <span aria-hidden="true"> / </span>
          <span>{job.roleFamily}</span>
        </nav>
        <h1 className="mt-1 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">{job.title}</h1>
        <div className="mt-2 flex flex-wrap gap-3 text-sm text-gray-600">
          <span>{job.company}</span>
          <span>{job.location}</span>
          <span>{job.experienceMin === 0 ? "Entry level" : `${job.experienceMin} - ${job.experienceMax} yrs`}</span>
        </div>
      </div>

      <div className="grid gap-8 lg:grid-cols-3">
        <div className="lg:col-span-2 space-y-6">
          <JobInsightCard
            title="Salary insight"
            insight={`This role pays an estimated ${formatCurrency(job.salaryMin)} to ${formatCurrency(job.salaryMax)} per year.`}
          />
          <JobInsightCard
            title="Experience insight"
            insight={`Market data shows similar roles typically require ${job.experienceMin} to ${job.experienceMax} years of experience.`}
          />
          <JobInsightCard
            title="Skill signal"
            insight={`Top skills for this role family include ${job.skills.slice(0, 3).join(", ")}${job.skills.length > 3 ? ` and ${job.skills.length - 3} more` : ""}.`}
          />

          <div className="card-interactive p-6">
            <h2 className="text-lg font-semibold text-gray-900">What you could earn</h2>
            <p className="mt-2 text-sm text-gray-500">Based on current market extract for this role family.</p>
            <div className="mt-4 grid gap-3 sm:grid-cols-2">
              <div className="rounded-xl border border-gray-200 bg-white p-4 text-center">
                <div className="text-sm text-gray-500">Estimated low</div>
                <div className="mt-1 text-2xl font-bold text-gray-900">{formatCurrency(job.salaryMin)}</div>
              </div>
              <div className="rounded-xl border border-gray-200 bg-white p-4 text-center">
                <div className="text-sm text-gray-500">Estimated high</div>
                <div className="mt-1 text-2xl font-bold text-brand-600">{formatCurrency(job.salaryMax)}</div>
              </div>
            </div>
          </div>
        </div>

        <div className="space-y-6">
          <div className="card-interactive p-6">
            <h2 className="text-lg font-semibold text-gray-900">Required skills</h2>
            <p className="mt-2 text-sm text-gray-500">Skills most often requested for this role.</p>
            <ul className="mt-4 space-y-2">
              {job.skills.map((skill) => (
                <li key={skill} className="flex items-center gap-2 rounded-lg bg-brand-50 px-3 py-2 text-sm text-brand-800">
                  <svg className="h-4 w-4 shrink-0" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                    <path strokeLinecap="round" strokeLinejoin="round" d="M9 12.75L11.25 15 15 9.75M21 12a9 9 0 11-18 0 9 9 0 0118 0z" />
                  </svg>
                  {skill}
                </li>
              ))}
            </ul>
          </div>

          <Link
            href="/profile?targetRole=prepare"
            className="block rounded-xl border border-gray-200 bg-white p-6 text-center transition hover:bg-gray-50 hover:border-brand-300"
          >
            <div className="text-sm font-semibold text-brand-700">See skill gaps for this role</div>
            <p className="mt-1 text-sm text-gray-600">Compare your profile and get recommendations.</p>
            <span className="mt-3 inline-flex items-center justify-center rounded-full bg-brand-50 px-3 py-1 text-xs font-semibold text-brand-700">
              Start analysis
            </span>
          </Link>
        </div>
      </div>

      {related.length > 0 && (
        <section className="mt-12">
          <h2 className="text-xl font-semibold text-gray-900">More roles like this</h2>
          <div className="mt-4 grid gap-4 sm:grid-cols-2 lg:grid-cols-3">
            {related.map((r) => (
              <Link key={r.id} href={`/jobs/${r.slug}`} className="card-interactive p-5 flex items-start gap-4 transition hover:-translate-y-1 hover:shadow-lg">
                <div className="flex h-12 w-12 shrink-0 items-center justify-center rounded-xl bg-brand-50 text-brand-600 text-xl font-bold">
                  {r.roleFamily[0]}
                </div>
                <div>
                  <div className="text-base font-semibold text-gray-900">{r.title}</div>
                  <div className="mt-1 text-sm text-gray-500">{r.company} · {r.location}</div>
                  <div className="mt-2 text-base font-semibold text-gray-900">{formatCurrency(r.salaryMin)} - {formatCurrency(r.salaryMax)}</div>
                </div>
              </Link>
            ))}
          </div>
        </section>
      )}
    </>
  );
}
