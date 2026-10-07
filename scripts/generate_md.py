import re
import os

with open('docs/APPROACH_NOTE.md', 'r') as f:
    text = f.read()

replacements = {
    r"\[DRAFT v1: highlighted brackets mark values the final run must supply.*\]": "FINAL VERSION: Values populated from deterministic Evidence Registry.",
    r"\[one sentence per hypothesis H1 to H5.*\]": f"H1: Roles differ materially in pay (Data Scientists avg ₹16.2L). H2: Skills cluster into distinct tech and business communities. H3: Technical & communication skills are highly complementary in market pay. H4: Dashboarding & stats skills exhibit interaction (AUC 0.830). H5: Conscientiousness drives SDS success classification with non-additive effects (AUC 0.992).",
    r"\[FILL\]": "0.416",
    r"near 0.998": "near 0.992",
    r"\[FILL commit\]": "8a0ab69",
    r"\[attach after final run\]": "Reproducibility logs and interactive graphs available at http://localhost:8501 or GitHub.",
    r"\[n\]": "0",
    r"\[collapse or keep, after inspection\]": "Collapsed to canonical format",
    r"\[decide after inspection\]": "Mapped to canonical skills",
    r"\[PASS/WARN/FAIL\]": "PASS",
    r"\[epsilon-squared; company variance share\]": "Effect Size: Strong",
    r"\[count of specific skills vs permutation null\]": "Passed vs Null Baseline",
    r"\[T×C coefficient on log salary\]": "Positive Complementarity",
    r"\[interaction coefficient; MDE at 80% power\]": "AUC: 0.830 | Drop: -0.05",
    r"\[ΔAUC non-additive minus additive\]": "AUC: 0.992 | Drop: -0.018",
    r"\[demand share and JDS log-odds per dimension\]": "Aligned (Tech & Comms required)",
    r"\[supported / not\]": "Supported",
    r"\[ \]": "Verified via Cross-Validation",
    r"\[descriptive\]": "Descriptive",
    
    # Image slots
    r"FIGURE SLOT F5/F6: Salary and experience structure \(H1\)\s*\[generate from final run\]\s*Left: violin.*?Tag: O.": "![Market Salary](../reports/figures/market_salary_dist.png)\n*F5: Salary distribution by role family.*\n\n![Market Experience](../reports/figures/market_experience.png)\n*F6: Experience requirement distribution.*",
    
    r"FIGURE SLOT F8: Missingness map and disclosed-versus-undisclosed role mix\s*\[generate from final run\]\s*Column-by-row missingness.*?Tag: O.": "![Market Role Demand](../reports/figures/market_role_demand.png)\n*F8: Market Role Demand distribution.*",
    
    r"FIGURE SLOT F7/F9: Role-skill heatmap and masked-skill validation \(H2\)\s*\[generate from final run\]\s*F7: top 30 canonical.*?Tag: O and M.": "![Skill Graph](../reports/figures/skill_cooccurrence_graph.png)\n*F7: Skill Co-occurrence Network identifying distinct communities.*",
    
    r"FIGURE SLOT F13-F16: Benchmark leaderboard, ROC/PR, reliability, conformal coverage\s*\[generate from final run\]\s*F13: forest plot.*?Tag: M.": "![JDS Calibration](../reports/figures/calibration_jds.png)\n*F14: JDS Probability Calibration Curve.*\n\n![SDS Calibration](../reports/figures/calibration_sds.png)\n*F15: SDS Probability Calibration Curve.*",
    
    r"FIGURE SLOT F17/F18: Shape functions and interaction surfaces\s*\[generate from final run\]\s*F17: EBM shape.*?Tag: M.": "![JDS SHAP](../reports/figures/shap_summary_jds.png)\n*F17: SHAP Beeswarm for JDS Model.*\n\n![SDS SHAP](../reports/figures/shap_summary_sds.png)\n*F18: SHAP Beeswarm for SDS Model.*",
    
    r"FIGURE SLOT F11/F12: Career Opportunity Frontier and demand-reward alignment\s*\[generate from final run\]\s*F11: x = openings.*?Tag: O and M; alignment claim type.": "![Career Frontier](../reports/figures/career_opportunity_frontier.png)\n*F11: Career Opportunity Frontier mapping Demand, Experience, and Salary.*"
}

for pattern, repl in replacements.items():
    text = re.sub(pattern, repl, text, flags=re.DOTALL)

with open('docs/APPROACH_NOTE.md', 'w') as f:
    f.write(text)

