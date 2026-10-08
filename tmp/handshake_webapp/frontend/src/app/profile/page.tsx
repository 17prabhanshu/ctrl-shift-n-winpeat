"use client";

import { useState, useRef, useEffect } from "react";
import { analyzeSkillGap, expandCareerPaths, estimateSalaryForRole, roleSalaryStats, formatCurrency } from "@/lib/data";
import { AnimatedSection } from "@/components/ui/animated-section";
import { cn } from "@/lib/utils";
import { CheckIcon, SparklesIcon } from "@heroicons/react/24/solid";
import { Link } from "next/link";

const roleOptions = roleSalaryStats.map((r) => r.role);

const skillOptions = [
  "Python", "SQL", "Machine Learning", "Statistics", "R",
  "Excel", "Tableau", "Power BI", "Java", "JavaScript",
  "Big Data", "Spark", "Hadoop", "Deep Learning", "NLP",
  "Data Visualization", "Communication", "Project Management",
];

type Tab = "gap" | "path";

export default function ProfilePage() {
  const [experience, setExperience] = useState(3);
  const [targetRole, setTargetRole] = useState("Data Scientist");
  const [currentSkills, setCurrentSkills] = useState<string[]>(["SQL", "Python"]);
  const [currentRole, setCurrentRole] = useState("Data Analyst");
  const [activeTab, setActiveTab] = useState<Tab>("gap");
  const [visible, setVisible] = useState(false);
  const [focusedSkill, setFocusedSkill] = useState<string | null>(null);

  const gap = analyzeSkillGap({ targetRole, currentSkills });
  const salaryEstimate = estimateSalaryForRole(targetRole);
  const paths = expandCareerPaths({ currentRole });

  const toggleSkill = (skill: string) => {
    setCurrentSkills((prev) =>
      prev.includes(skill) ? prev.filter((s) => s !== skill) : [...prev, skill]
    );
  };

  useEffect(() => {
    const t = setTimeout(() => setVisible(true), 80);
    return () => clearTimeout(t);
  }, []);

  return (
    <>
      <div className="mb-8">
        <h1 className="text-3xl font-bold tracking-tight text-gray-900 sm:text-4xl">My Profile</h1>
        <p className="mt-2 text-gray-600">
          See which skills matter most for your target role and explore common career paths.
        </p>
      </div>

      <AnimatedSection variant="card-grid" className="mb-8">
        <div className={cn(
          "card-interactive p-6 transition-all duration-500",
          visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
        )}>
          <h2 className="text-lg font-semibold text-gray-900">Your profile</h2>
          <p className="mt-1 text-sm text-gray-500">Adjust these to see how your profile stacks up.</p>

          <div className="mt-5 space-y-4">
            <div>
              <label htmlFor="experience" className="block text-sm font-medium text-gray-700">
                Years of experience
              </label>
              <input
                id="experience"
                type="range"
                min={0}
                max={20}
                value={experience}
                onChange={(e) => setExperience(Number(e.target.value))}
                className="mt-2 w-full cursor-pointer rounded-lg bg-gray-200 accent-brand-600"
              />
              <div className="mt-1 flex justify-between text-xs text-gray-500">
                <span>0</span>
                <span className="font-semibold text-gray-900">{experience} yrs</span>
                <span>20</span>
              </div>
            </div>

            <div>
              <label htmlFor="current-role" className="block text-sm font-medium text-gray-700">
                Current role
              </label>
              <select
                id="current-role"
                className="select mt-1 w-full"
                value={currentRole}
                onChange={(e) => setCurrentRole(e.target.value)}
              >
                {roleOptions.map((role) => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>

            <div>
              <label htmlFor="target-role" className="block text-sm font-medium text-gray-700">
                Target role
              </label>
              <select
                id="target-role"
                className="select mt-1 w-full"
                value={targetRole}
                onChange={(e) => setTargetRole(e.target.value)}
              >
                {roleOptions.map((role) => (
                  <option key={role} value={role}>{role}</option>
                ))}
              </select>
            </div>
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="mb-8">
        <div className={cn(
          "card-interactive overflow-hidden transition-all duration-500",
          visible ? "opacity-100 translate-y-0" : "opacity-0 translate-y-4"
        )}>
          <div className="border-b border-gray-200">
            <div className="flex">
              {(["gap", "path"] as const).map((tab) => (
                <button
                  key={tab}
                  onClick={() => setActiveTab(tab)}
                  className={cn(
                    "border-b-2 px-6 py-3 text-sm font-medium transition-colors hover:text-brand-700",
                    activeTab === tab
                      ? "border-brand-500 text-brand-700"
                      : "border-transparent text-gray-500"
                  )}
                >
                  {tab === "gap" ? "Skill gap" : "Career path"}
                </button>
              ))}
            </div>
          </div>

          <div className="p-6">
            {activeTab === "gap" ? (
              <div className="space-y-6">
                <div className="rounded-xl bg-gray-50 p-5">
                  <div className="flex items-center justify-between gap-4">
                    <div>
                      <div className="text-sm text-gray-500">Estimated salary range</div>
                      <div className="mt-1 text-xl font-bold text-gray-900">{formatCurrency(salaryEstimate.estimatedMin)}</div>
                      <div className="mt-0.5 text-base text-gray-600">to {formatCurrency(salaryEstimate.estimatedMax)}</div>
                    </div>
                    <div className="shrink-0 text-right">
                      <div className="text-sm text-gray-500">Demand</div>
                      <div className="mt-1 text-2xl font-bold text-gray-900">{gap.requiredSkills.length} skills</div>
                      <div className="mt-0.5 text-base text-gray-600">in this role</div>
                    </div>
                  </div>
                </div>

                <div>
                  <div className="flex items-center justify-between gap-2">
                    <h3 className="text-base font-semibold text-gray-900">Skills for {targetRole}</h3>
                    <span className="text-xs text-gray-500">{gap.ownedSkills.length} owned · {gap.gaps.length} gaps</span>
                  </div>
                  <p className="mt-1 text-sm text-gray-500">Select the skills you already have to see your gaps.</p>
                </div>

                <div className="flex flex-wrap gap-2">
                  {skillOptions.map((skill) => {
                    const owned = currentSkills.includes(skill);
                    const inRole = gap.requiredSkills.includes(skill);
                    return (
                      <button
                        key={skill}
                        className={cn(
                          "rounded-full border px-3 py-1 text-sm font-medium transition-all",
                          owned
                            ? "border-brand-300 bg-brand-50 text-brand-700"
                            : inRole
                            ? "border-gray-300 bg-white text-gray-700 hover:border-brand-300"
                            : "border-gray-200 bg-gray-50 text-gray-500 opacity-60",
                          focusedSkill === skill && "ring-2 ring-brand-300"
                        )}
                        onClick={() => toggleSkill(skill)}
                        onFocus={() => setFocusedSkill(skill)}
                        onBlur={() => setFocusedSkill(null)}
                      >
                        {owned ? (
                          <>
                            <CheckIcon className="mr-1 inline h-3.5 w-3.5" />
                            {skill}
                          </>
                        ) : (
                          skill
                        )}
                      </button>
                    );
                  })}
                </div>

                {gap.gaps.length > 0 ? (
                  <div className="rounded-xl border border-amber-200 bg-amber-50 p-5">
                    <div className="flex items-start gap-3">
                      <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-amber-100 text-amber-700">
                        <SparklesIcon className="h-4 w-4" />
                      </div>
                      <div>
                        <h3 className="text-sm font-semibold text-amber-800">Skill gaps for {targetRole}</h3>
                        <p className="mt-1 text-sm text-amber-700">These skills are commonly required and could improve your fit.</p>
                        <ul className="mt-3 space-y-2">
                          {gap.gaps.map(({ skill, salaryImpact }) => (
                            <li key={skill} className="flex items-center justify-between gap-2 rounded-lg bg-amber-100/60 px-3 py-2 text-sm">
                              <span className="font-medium text-amber-900">{skill}</span>
                              <span className="text-xs text-amber-600">{salaryImpact}</span>
                            </li>
                          ))}
                        </ul>
                      </div>
                    </div>
                  </div>
                ) : (
                  <div className="rounded-xl border border-green-200 bg-green-50 p-5 text-sm text-green-800">
                    <div className="flex items-center gap-3">
                      <div className="mt-0.5 flex h-8 w-8 shrink-0 items-center justify-center rounded-lg bg-green-100 text-green-700">
                        <CheckIcon className="h-4 w-4" />
                      </div>
                      <div>
                        <h3 className="font-semibold">Good fit</h3>
                        <p>You already have the key skills for {targetRole}.</p>
                      </div>
                    </div>
                  </div>
                )}
              </div>
            ) : (
              <div className="space-y-6">
                <p className="text-sm text-gray-500">Common transition paths based on market demand.</p>
                {paths.map(({ from, paths: pathList }) => (
                  <div key={from}>
                    <div className="text-sm font-medium text-gray-700">From {from}</div>
                    <ul className="mt-3 space-y-3">
                      {pathList.map((path) => (
                        <li
                          key={path.to}
                          className={cn(
                            "rounded-xl border p-4 transition-all",
                            focusedSkill ? (path.keySkills.includes(focusedSkill) ? "border-brand-300 bg-brand-50" : "border-gray-200 bg-white") : "border-gray-200 bg-white"
                          )}
                        >
                          <div className="flex items-center justify-between gap-2">
                            <div className="flex items-center gap-2">
                              <svg className="h-5 w-5 text-brand-600" fill="none" viewBox="0 0 24 24" strokeWidth={2} stroke="currentColor">
                                <path strokeLinecap="round" strokeLinejoin="round" d="M13.5 6H5.25A2.25 2.25 0 003 8.25v10.5A2.25 2.25 0 005.25 21h10.5A2.25 2.25 0 0018 18.75V10.5m-10.5 6L21 3m0 0h-5.25M21 3v5.25" />
                              </svg>
                              <span className="font-semibold text-gray-900">{path.to}</span>
                            </div>
                            <span className="text-xs text-gray-500">{path.demand.toLocaleString()} postings</span>
                          </div>
                          {path.keySkills.length > 0 && (
                            <div className="mt-2 flex flex-wrap gap-1.5">
                              {path.keySkills.map((skill) => (
                                <button
                                  key={skill}
                                  className={cn(
                                    "rounded-full border border-gray-200 bg-white px-2.5 py-0.5 text-xs font-medium text-gray-700 hover:border-brand-300 hover:bg-brand-50",
                                    focusedSkill === skill && "border-brand-300 bg-brand-50 text-brand-700"
                                  )}
                                  onClick={() => toggleSkill(skill)}
                                  onFocus={() => setFocusedSkill(skill)}
                                  onBlur={() => setFocusedSkill(null)}
                                >
                                  {skill}
                                </button>
                              ))}
                            </div>
                          )}
                        </li>
                      ))}
                    </ul>
                  </div>
                ))}
                <p className="text-xs text-gray-400">Paths are illustrative and based on market demand patterns.</p>
              </div>
            )}
          </div>
        </div>
      </AnimatedSection>

      <AnimatedSection variant="card-grid" className="rounded-2xl border border-gray-200 bg-gray-50/50 px-6 py-8 text-center sm:text-left transition-all duration-500" style={{ opacity: visible ? 1 : 0, transform: visible ? "translateY(0)" : "translateY(8px)" }}>
        <h2 className="text-xl font-semibold text-gray-900">What to learn next</h2>
        <p className="mt-2 text-gray-600">
          Focus on the gaps that matter most for your target role, then revisit your profile as you grow.
        </p>
        <div className="mt-4 flex flex-wrap gap-3 justify-center sm:justify-start">
          <a
            href="#skill-gap"
            className="inline-flex items-center justify-center rounded-xl border border-brand-300 bg-brand-50 px-5 py-2.5 text-sm font-semibold text-brand-700 transition hover:bg-brand-100 hover:text-brand-800"
          >
            Review gaps
          </a>
          <Link
            href="/skills"
            className="inline-flex items-center justify-center rounded-xl border border-gray-300 bg-white px-5 py-2.5 text-sm font-semibold text-gray-700 shadow-sm transition hover:bg-gray-50"
          >
            See all skills
          </Link>
        </div>
      </AnimatedSection>
    </>
  );
}
