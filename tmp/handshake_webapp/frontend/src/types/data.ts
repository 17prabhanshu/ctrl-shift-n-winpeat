export interface RoleSalaryStats {
  role: string;
  demand: number;
  avgSalary: number;
  avgExperience: number;
  medianSalary?: number;
  n: number;
}

export interface SkillStat {
  skill: string;
  demand: number;
  salaryAssociation?: "high" | "moderate" | "low" | "variable";
  dimension: string;
}

export interface JobPosting {
  id: string;
  title: string;
  slug: string;
  company: string;
  roleFamily: string;
  location: string;
  salaryMin: number;
  salaryMax: number;
  experienceMin: number;
  experienceMax: number;
  skills: string[];
  postedAt?: string;
}

export interface SalaryEstimate {
  role: string;
  estimatedMin: number;
  estimatedMax: number;
  confidenceLevel: "high" | "moderate" | "low";
  sourceNote: string;
}

export interface SkillGap {
  skill: string;
  owned: boolean;
  priority: "critical" | "high" | "optional";
  salaryImpact: string;
}
