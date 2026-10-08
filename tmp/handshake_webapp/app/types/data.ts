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
