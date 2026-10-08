# Ctrl Shift N: Workforce Intelligence Engine
## Round 3 Presentation Script & Visual Guide

**Theme:** Apple Keynote style. Stark black backgrounds. Massive, high-contrast white/orange typography. One concept per slide. No bullet-point walls of text.
**Time Limit:** 10 Minutes (~35 seconds per slide). 

---

### SLIDE 1: The Title
**Visual:** Pure black screen. Center text: **Workforce Intelligence Engine.** Bottom right: A subtle SAS logo. 
**Speaker:** 
"Good morning. We are Team Ctrl Shift N. Today, we aren’t going to show you a dashboard. We aren’t going to show you a basic predictive model. We are going to show you a paradigm shift in how we audit the data science economy."

---

### SLIDE 2: The Trap
**Visual:** 4 disconnected glowing dots on the screen. Text below them: `17,000 Postings` | `139 JDS` | `161 SDS`. 
**Speaker:** 
"When we received the brief, we realized SAS had given us a trap. Four disconnected datasets. No shared identifiers. No temporal link. Most teams look at this and try to forcefully join the tables to build a massive model—committing the Ecological Fallacy and creating fake correlations. We refused to do that."

---

### SLIDE 3: The Paradigm
**Visual:** The dots disappear. One massive sentence appears in the center: **"Datasets meet at constructs, never at rows."**
**Speaker:** 
"We established a strict statistical law for our architecture: The No-False-Join Principle. Datasets meet at constructs, never at rows. Instead of forcing bad data science, we asked one unifying, falsifiable question..."

---

### SLIDE 4: The Question
**Visual:** Massive typography filling the screen: **Does the market pay for what progression rewards?**
**Speaker:** 
"Does the market actually pay for what early-career progression rewards? And do those traits align with senior success? To answer this, we formulated a single organizing hypothesis derived from advanced labour-economics."

---

### SLIDE 5: The Hypothesis
**Visual:** Simple math equation style: `Technical Skill × Communication = The Premium`
**Speaker:** 
"The hypothesis: Technical skill alone is commoditized. The true market premium—in both salary and promotion velocity—only unlocks when technical skills intersect with communication and storytelling."

---

### SLIDE 6: The Architecture (SAS VA Integration)
**Visual:** A sleek, animated diagram showing 4 'Evidence Lanes' (Market, Skill, Junior, Senior) feeding into a central 'Evidence Registry'. *[Use SAS Visual Analytics network diagram style]*
**Speaker:** 
"To test this without leaking data, we built a Boundary-Preserving Architecture. Four isolated Evidence Lanes running deterministic analytics. They never share rows. They only write to an immutable Evidence Registry, ensuring total auditability."

---

### SLIDE 7: The Construct Bridge
**Visual:** A sleek SAS VA graphic showing 15,000 raw text strings collapsing into 5 glowing nodes.
**Speaker:** 
"How do we compare them? The Construct Bridge. We didn’t just count keywords. We mapped over 15,000 messy posting strings to the exact 5 dimensions in the JDS dataset using an NLP taxonomy, scored against a hand-labelled gold set."

---

### SLIDE 8: Outcome I - The Market Premium
**Visual:** A SAS VA Career Opportunity Frontier (Scatter plot: X=Openings, Y=Median Salary, Bubbles=Experience).
**Speaker:** 
"The results were staggering. Using a Dirichlet-prior index on the market data, we proved that quantitative skills alone don't scale. The exponential salary premium only exists when technical skills are bundled with dashboarding and storytelling."

---

### SLIDE 9: Outcome II - Promotion Velocity
**Visual:** A SAS VA Interaction Surface Heatmap (Maths vs Storytelling).
**Speaker:** 
"But does the market match reality? We ran Firth-penalized logistic regression on the tiny 139-row JDS dataset. The result? The exact same complementarity. The combination of math and storytelling mathematically dictated early-career promotion velocity."

---

### SLIDE 10: The Anomaly 
**Visual:** Screen goes completely red. Text: **AUC: 0.997**
**Speaker:** 
"Then, we analyzed the Senior (SDS) dataset. Our Extra Trees model achieved a near-perfect ROC-AUC of 0.997 on just 161 rows. In any other presentation, a 99.7% accuracy is the final slide..."

---

### SLIDE 11: The Forensics Audit
**Visual:** The red screen shatters. Text: **Forensic Audit Triggered.**
**Speaker:** 
"...In ours, it triggered a forensic audit. Behavioural data of 161 humans does not cleanly separate with 99% accuracy in the real world."

---

### SLIDE 12: The Illusion
**Visual:** A simple depth-2 decision tree graphic showing a hard split on the "Openness" trait.
**Speaker:** 
"We ran decision-tree forensics and discovered a deterministic threshold. We proved that the perfect score was an illusion. The dataset was mathematically separable by a simple rule, strongly indicating synthetic or rule-based labelling. We didn't just model the data; we audited its scientific integrity."

---

### SLIDE 13: The True Implication
**Visual:** Three columns: `For Employers` | `For Universities` | `For Professionals`.
**Speaker:** 
"What does this mean for the real world? For employers: stop pooling technical skills; pay for the bundle. For universities: align curriculums to the complementarity gap. For professionals: coding gets you in the door; communication gets you promoted."

---

### SLIDE 14: Conclusion
**Visual:** The Ctrl Shift N logo. 
**Speaker:** 
"We took fragmented, unlinked datasets and didn't just build a model. We built an engine that extracts causal workforce signals while enforcing the laws of statistics. We are Ctrl Shift N. Thank you."

---

### SLIDE 15: Q&A Title
**Visual:** Pure black screen. **Questions?**
**Speaker:** *(Silence, wait for the jury)*

---
### JURY Q&A CHEAT SHEET (Keep these in your head)

*   **Jury: "Why didn't you just use an LLM or Neural Network?"**
    *   *Answer:* "With 139 rows, deep learning is statistical malpractice. It overfits instantly. We used Firth-penalized logistic regression specifically because it reduces bias in maximum likelihood estimates for tiny sample sizes. We chose rigor over buzzwords."
*   **Jury: "What do you mean by 'Forensic Audit' on the 0.997 score?"**
    *   *Answer:* "Real-world human psychology data (the Big Five traits) has massive variance. When a model hits 0.997 AUC on human behaviour, it almost always means data leakage or synthetic labelling. We used a depth-2 tree to prove the data was generated via a hard mathematical rule, meaning we shouldn't make real-world workforce decisions based on that specific file's outcome."
*   **Jury: "How did you use SAS Visual Analytics?"**
    *   *Answer:* "We used SAS VA to generate the Career Opportunity Frontier and the Interaction Surface heatmaps. Its ability to handle robust statistical rendering allowed us to visually prove the complementarity gap without muddying the math."
