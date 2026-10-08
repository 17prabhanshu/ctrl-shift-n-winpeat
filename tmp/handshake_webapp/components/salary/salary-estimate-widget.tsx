"use client";

import { useState } from "react";
import { estimateSalaryForRole, roleSalaryStats } from "@/lib/data";
import { formatCurrency } from "@/lib/utils";
import { AnimatedSection } from "@/components/ui/animated-section";
import { cn } from "@/lib/utils";

const roleOptions = roleSalaryStats.map((r) => r.role);

export function SalaryEstimateWidget({ initialRole, initialEstimate }: { initialRole: string; initialEstimate: NonNullable<ReturnType<typeof estimateSalaryForRole>> }) {
  const [selectedRole, setSelectedRole] = useState(initialRole);
  const estimate = estimateSalaryForRole(selectedRole);

  return (
    <div id="salary-widget" className="card-interactive p-6">
      <h2 className="text-lg font-semibold text-gray-900">Estimate salary for a role</h2>
      <p className="mt-1 text-sm text-gray-500">Select a role to see the estimated range.</p>

      <div className="mt-5">
        <label htmlFor="role-select" className="block text-sm font-medium text-gray-700">Role</label>
        <select
          id="role-select"
          className="select mt-1 w-full"
          value={selectedRole}
          onChange={(e) => setSelectedRole(e.target.value)}
        >
          {roleOptions.map((role) => (
            <option key={role} value={role}>{role}</option>
          ))}
        </select>
      </div>

      <div className="mt-6 grid gap-4 sm:grid-cols-2">
        <div className="rounded-xl bg-gray-50 p-4">
          <div className="text-sm text-gray-500">Estimated range</div>
          <div className="mt-1 text-2xl font-bold text-gray-900">{formatCurrency(estimate.estimatedMin)}</div>
          <div className="mt-0.5 text-base font-medium text-gray-600">to</div>
          <div className="mt-0.5 text-2xl font-bold text-brand-600">{formatCurrency(estimate.estimatedMax)}</div>
        </div>
        <div className="rounded-xl bg-gray-50 p-4">
          <div className="text-sm text-gray-500">Confidence</div>
          <div className="mt-1">
            <span className={cn(
              "inline-flex items-center rounded-full px-2.5 py-1 text-sm font-semibold",
              estimate.confidenceLevel === "high" ? "bg-green-50 text-green-700" : "bg-amber-50 text-amber-700"
            )}>
              {estimate.confidenceLevel === "high" ? "High" : "Moderate"}
            </span>
          </div>
          <p className="mt-2 text-sm text-gray-600">{estimate.sourceNote}</p>
        </div>
      </div>

      <p className="mt-4 text-xs text-gray-400">Estimates are illustrative and based on the current market extract. Not financial advice.</p>
    </div>
  );
}
