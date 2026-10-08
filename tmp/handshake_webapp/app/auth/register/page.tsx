import { RegisterCard } from "@/app/components/ui/register-card";
import { AnimatedSection } from "@/app/components/ui/animated-section";
import Link from "next/link";

export const metadata = {
  title: "Sign Up",
  description: "Create your Handshake account and start exploring data careers.",
};

export default function RegisterPage() {
  return (
    <>
      <div className="mb-8">
        <nav className="text-sm text-gray-500">
          <Link href="/" className="hover:text-brand-600">Home</Link>
          <span aria-hidden="true"> / </span>
          <span>Sign up</span>
        </nav>
        <h1 className="mt-1 text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">Create your account</h1>
        <p className="mt-2 text-gray-600">
          Join to save your profile, track roles you like, and get personalized recommendations.
        </p>
      </div>

      <AnimatedSection variant="card-grid">
        <div className="mx-auto max-w-lg">
          <RegisterCard />
        </div>
      </AnimatedSection>

      <section className="mt-12 rounded-2xl border border-gray-200 bg-gray-50/50 px-6 py-8 text-center sm:text-left">
        <h2 className="text-xl font-semibold text-gray-900">Why join?</h2>
        <ul className="mt-4 space-y-3 text-sm text-gray-600">
          <li className="flex gap-3">
            <span className="mt-0.5 shrink-0 h-5 w-5 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">1</span>
            <span>Save your profile and skill gaps across sessions.</span>
          </li>
          <li className="flex gap-3">
            <span className="mt-0.5 shrink-0 h-5 w-5 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">2</span>
            <span>Get role-specific recommendations based on your skills.</span>
          </li>
          <li className="flex gap-3">
            <span className="mt-0.5 shrink-0 h-5 w-5 flex items-center justify-center rounded-full bg-brand-50 text-brand-600 text-xs font-bold">3</span>
            <span>See salary estimates and demand for roles you care about.</span>
          </li>
        </ul>
      </section>
    </>
  );
}
