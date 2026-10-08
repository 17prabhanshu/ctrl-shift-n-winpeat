import type { RoleSalaryStats, SkillStat, JobPosting, SalaryEstimate, SkillGap } from "../types/data";

export const roleSalaryStats: RoleSalaryStats[] = [
  { role: "Data Scientist", demand: 470, avgSalary: 1620000, medianSalary: 1620000, avgExperience: 4.2, n: 470 },
  { role: "Data Engineer", demand: 408, avgSalary: 1520000, medianSalary: 1500000, avgExperience: 4.6, n: 408 },
  { role: "ML Engineer", demand: 210, avgSalary: 1710000, medianSalary: 1700000, avgExperience: 5.1, n: 210 },
  { role: "Data Analyst", demand: 1840, avgSalary: 890000, medianSalary: 850000, avgExperience: 2.6, n: 1840 },
  { role: "Business Analyst", demand: 1208, avgSalary: 790000, medianSalary: 760000, avgExperience: 3.1, n: 1208 },
  { role: "Software Engineer", demand: 1208, avgSalary: 1090000, medianSalary: 1080000, avgExperience: 3.8, n: 1208 },
];

export const topSkills: SkillStat[] = [
  { skill: "SQL", demand: 3210, salaryAssociation: "moderate", dimension: "Coding" },
  { skill: "Python", demand: 2980, salaryAssociation: "high", dimension: "Coding" },
  { skill: "Java", demand: 1640, salaryAssociation: "moderate", dimension: "Coding" },
  { skill: "Machine Learning", demand: 770, salaryAssociation: "high", dimension: "AI/ML" },
  { skill: "Excel", demand: 693, salaryAssociation: "low", dimension: "Dashboard/Storytelling" },
  { skill: "Tableau", demand: 420, salaryAssociation: "moderate", dimension: "Dashboard/Storytelling" },
  { skill: "Statistics", demand: 380, salaryAssociation: "moderate", dimension: "Maths/Stats" },
  { skill: "SAS", demand: 320, salaryAssociation: "moderate", dimension: "Maths/Stats" },
  { skill: "R", demand: 280, salaryAssociation: "moderate", dimension: "Maths/Stats" },
  { skill: "Big Data", demand: 260, salaryAssociation: "high", dimension: "Big Data" },
];

export const sampleJobPostings: JobPosting[] = [
  {
    id: "job-1",
    title: "Data Scientist",
    slug: "data-scientist-1",
    company: "AnalyticsCorp",
    roleFamily: "Data Scientist",
    location: "Bangalore",
    salaryMin: 1200000,
    salaryMax: 2200000,
    experienceMin: 2,
    experienceMax: 5,
    skills: ["Python", "SQL", "Machine Learning", "Statistics"],
  },
  {
    id: "job-2",
    title: "Senior Data Engineer",
    slug: "senior-data-engineer-1",
    company: "DataInfra Pvt Ltd",
    roleFamily: "Data Engineer",
    location: "Hyderabad",
    salaryMin: 1600000,
    salaryMax: 2500000,
    experienceMin: 5,
    experienceMax: 9,
    skills: ["Python", "SQL", "Spark", "Hadoop", "Java"],
  },
  {
    id: "job-3",
    title: "ML Engineer",
    slug: "ml-engineer-1",
    company: "AIFirst Labs",
    roleFamily: "ML Engineer",
    location: "Bangalore",
    salaryMin: 1500000,
    salaryMax: 2400000,
    experienceMin: 3,
    experienceMax: 7,
    skills: ["Python", "Machine Learning", "Deep Learning", "SQL", "Java"],
  },
  {
    id: "job-4",
    title: "Data Analyst",
    slug: "data-analyst-1",
    company: "InsightWorks",
    roleFamily: "Data Analyst",
    location: "Pune",
    salaryMin: 500000,
    salaryMax: 900000,
    experienceMin: 0,
    experienceMax: 3,
    skills: ["SQL", "Excel", "Python", "Tableau"],
  },
  {
    id: "job-5",
    title: "Business Analyst",
    slug: "business-analyst-1",
    company: "StrategyBridge",
    roleFamily: "Business Analyst",
    location: "Mumbai",
    salaryMin: 600000,
    salaryMax: 1100000,
    experienceMin: 1,
    experienceMax: 4,
    skills: ["SQL", "Excel", "Communication", "Project Management"],
  },
];

const requiredSkillsByRole: Record<string, string[]> = {
  "Data Scientist": ["Python", "SQL", "Machine Learning", "Statistics", "Data Visualization"],
  "Data Engineer": ["Python", "SQL", "Big Data", "Spark", "Hadoop", "Java"],
  "ML Engineer": ["Python", "Machine Learning", "Deep Learning", "SQL", "Java"],
  "Data Analyst": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"],
  "Business Analyst": ["SQL", "Excel", "Communication", "Project Management", "Statistics"],
  "Software Engineer": ["Java", "Python", "JavaScript", "SQL", "Project Management"],
};

const priorityForRole: Record<string, string[]> = {
  "Data Scientist": ["Python", "SQL", "Statistics", "Machine Learning", "Data Visualization"],
  "Data Engineer": ["SQL", "Python", "Big Data", "Spark", "Hadoop"],
  "ML Engineer": ["Python", "SQL", "Machine Learning", "Deep Learning", "Java"],
  "Data Analyst": ["SQL", "Excel", "Python", "Data Visualization", "Statistics"],
  "Business Analyst": ["SQL", "Excel", "Communication", "Project Management"],
  "Software Engineer": ["Java", "Python", "SQL", "JavaScript", "Project Management"],
};

const salaryImpactBySkill: Record<string, string> = {
  "Machine Learning": "High positive impact",
  "Python": "High positive impact",
  "SQL": "Moderate positive impact",
  "Big Data": "High positive impact (for Data Engineers)",
  "Spark": "High positive impact (for Data Engineers)",
  "Statistics": "Moderate positive impact",
  "Deep Learning": "High positive impact (for ML Engineers)",
  "Tableau": "Moderate positive impact (for Analysts)",
  "R": "Moderate positive impact",
  "Java": "Moderate positive impact (for Engineers)",
  "Excel": "Low positive impact (basic requirement)",
  "Communication": "Variable impact (context-dependent)",
};

export function estimateSalaryForRole(role: string): SalaryEstimate {
  const match = roleSalaryStats.find((r) => r.role === role);
  if (!match) {
    return {
      role,
      estimatedMin: 0,
      estimatedMax: 0,
      confidenceLevel: "low",
      sourceNote: "No postings found in current extract",
    };
  }
  return {
    role,
    estimatedMin: Math.round(match.medianSalary * 0.85),
    estimatedMax: Math.round(match.medianSalary * 1.25),
    confidenceLevel: match.n > 200 ? "high" : "moderate",
    sourceNote: `Based on ${match.n} postings in current extract`,
  };
}

export function analyzeSkillGap(profile: { targetRole: string; currentSkills: string[] }): { requiredSkills: string[]; ownedSkills: string[]; gaps: SkillGap[] } {
  const required = requiredSkillsByRole[profile.targetRole] ?? [];
  const owned = required.filter((s) => profile.currentSkills.includes(s));
  const gaps = required
    .filter((s) => !profile.currentSkills.includes(s))
    .map((skill) => ({
      skill,
      owned: false,
      priority: priorityForRole[profile.targetRole]?.includes(skill) ? "critical" : "high",
      salaryImpact: salaryImpactBySkill[skill] ?? "Not estimated",
    }));
  return {
    requiredSkills: required,
    ownedSkills: owned,
    gaps,
  };
}

export function expandCareerPaths(profile: { currentRole?: string }): { from: string; paths: { to: string; keySkills: string[]; demand: number }[] }[] {
  const base = profile.currentRole ?? "Data Analyst";
  const maps: Record<string, { to: string; keySkills: string[]; demand: number }[]> = {
    "Data Analyst": [
      { to: "Data Scientist", keySkills: ["Machine Learning", "Python", "Statistics"], demand: 470 },
      { to: "Business Analyst", keySkills: ["Communication", "Project Management"], demand: 1208 },
      { to: "Data Engineer", keySkills: ["Python", "Big Data", "SQL"], demand: 408 },
    ],
    "Business Analyst": [
      { to: "Data Analyst", keySkills: ["SQL", "Python", "Data Visualization"], demand: 1840 },
      { to: "Product Manager", keySkills: ["Communication", "Project Management"], demand: 300 },
      { to: "Data Scientist", keySkills: ["Python", "Machine Learning", "Statistics"], demand: 470 },
    ],
  };
  return Object.entries(maps).map(([from, paths]) => ({ from, paths }));
}
