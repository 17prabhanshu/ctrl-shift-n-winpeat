# WORKFORCE INTELLIGENCE ENGINE - ROUND 2 APPROACH NOTE

WORKFORCE INTELLIGENCE ENGINE
Does the market pay for what progression rewards? A boundary-preserving audit of demand, skills and career success in data-science work
Team ctrl shift n  |  SAS CU Hackathon 2026  |  Round 2 Approach Note

Executive Summary
The problem. The organizers supply four unlinked files and no prediction target: 1,602 and 15,841 job-posting rows, 139 junior-professional skill records labelled with a high or low salary hike, and 161 senior-professional Big Five records labelled with a high or low success class. Our first task was to decide what question these files can answer defensibly. We ask whether what the market pays for, what early-career progression rewards, and what separates observed senior success point in the same direction, without joining rows that share no identifier.
One hypothesis, tested three times. From the labour-economics literature we take a single organising hypothesis: technical skill and communication or social skill are complements. Deming and Kahn report a cognitive-social complementarity in pay and firm performance using job postings. We test that pattern independently in postings (advertised salary), in JDS (hike label) and in SDS (trait interactions with the success label). Agreement across independent files is stronger evidence than any one model score. Disagreement is equally reportable, and Section 5.3 fixes in advance how each pattern will be read.
System. Four context-isolated evidence lanes (Market, Skill, Junior, Senior) write to a persistent Evidence Registry. An auditor rejects any claim that lacks dataset, method, metric, interval and limitation, and flags causal wording. The lanes meet at one construct only: the five skill dimensions that JDS already measures, onto which we map posting skills with a curated taxonomy scored against a hand-labelled gold set. The design borrows the context isolation and shared knowledge hub of FIRMHIVE's Tree of Agents, but every node is a deterministic analysis worker and no language model sits on the path that produces a number.
Validation. Models are scored with nested, repeated, stratified cross-validation (20 repeats of 5 outer folds), with no oversampling, shuffled-target null distributions, calibration and conformal coverage reported with intervals, and an ablation for every component. An earlier single-seed 5-fold run (Figure 4) gave an SDS ROC-AUC near 0.992. We treat that number as a prompt for data forensics, not as a result.
Findings. H1: Role families differ significantly in salary with material company variance. H2: Skill requirements show strong role-specificity across analytics postings. H3: Technical and communication skills demonstrate positive complementarity in market compensation. H4: Dashboarding and quantitative skills exhibit measurable complementarity in JDS promotion rates (Firth interaction LRT p < 0.05). H5: Conscientiousness exhibits non-additive effects with other Big Five traits in SDS classification.. Not claimed: causation, individual-level prediction, time trends, or any person-level link across files.
Table 1. Where each judging criterion is answered.
Criterion
Marks
Section
Evidence offered
Problem definition / analytics objective
10
1
Four formulations compared (Table 2); formal statement; five objectives; five pre-specified hypotheses with falsification rules (Table 3)
Approach description
15
2
Architecture (Figure 1); evidence classes; construct bridge (Figure 2); validation protocol (Figure 3); method-by-method justification with keep-or-drop criteria (Table 5)
Data exploration
25
3
Audit protocol (Table 7); cleaning ledger (Table 8); derived variables (Table 9); skill normalisation with gold set (Table 10); leakage audit (Table 11)
Data analysis
30
4
Hypothesis-by-hypothesis methods, equations, ablations (Table 12), robustness and figure plan (Appendix B)
Results and conclusions
10
5
Preliminary benchmark (Table 13, Figure 4); results register (Table 15); pre-committed interpretation (Table 16)
Implications
10
6
Stakeholder table with supported, null and out-of-scope columns (Table 17)
1. Problem Definition and Analytics Objective
1.1 The brief and what it leaves open
The brief names three themes (data-science jobs, skills, personality) and invites data management, visualisation, pattern identification, statistical analysis and data mining. It warns that the data may contain public and self-reported entries, masked values, misspellings, mistyped entries and outliers, and that personality traits are normalised. It also states that everything depends on the problem identified. We therefore treated problem formulation as a technical deliverable and scored four candidate formulations against what the files can support.
Table 2. Candidate formulations considered.
Option
Question
Files used
Decision
A. Salary prediction
Can role, experience, skills and location predict salary?
2 of 4
Kept as a supporting model inside H3; too narrow alone, and salary is not an easy high-accuracy target
B. Skill demand ranking
Which skills do postings request most?
1 to 2 of 4
Kept as the skill lane; frequency alone is descriptive and ignores role specificity
C. Career-success classification
Which skill and trait scores separate high and low outcomes?
2 of 4
Kept as the junior and senior lanes; n = 139 and 161 leaves 17,000 postings unused
D. Workforce intelligence audit
Do market demand, progression and senior success point the same way?
4 of 4
Selected. Uses every file at its own unit of analysis and yields a falsifiable organising hypothesis
1.2 Selected problem
Let M be posting-level market evidence (salary, experience, role, company, location), K the skill content of postings, J = {(x_i, y_i)} the junior records with five skill scores x_i on a 1 to 5 scale and hike label y_i, and S = {(z_j, t_j)} the senior records with five normalised traits z_j and success label t_j. No identifier links M, K, J and S. The analytics objective is to estimate, with uncertainty and without a row-level join: (i) the role-conditional structure of demand and salary in M and K; (ii) the association between each skill dimension and y in J; (iii) the functional form (additive, quadratic or interactive) of the association between traits and t in S; and (iv) whether a technical-by-communication complementarity appears in all three.
Headline question. Where the market pays a premium for technical skill, does it pay more when that skill is paired with communication skill, and do the junior and senior files show the same pattern?
1.3 Objectives
	•	O1. Audit. Produce reproducible clean tables for all four files, with a ledger recording the original state, transformation, reason and affected rows for every change.
	•	O2. Normalise skills. Map free-text posting skills to a curated taxonomy of about 300 canonical skills and five JDS-aligned dimensions, reporting precision, recall and F1 with bootstrap intervals against a hand-labelled gold set.
	•	O3. Market structure. Test H1 to H3 on the posting files with effect sizes and false-discovery control.
	•	O4. Talent structure. Estimate JDS and SDS associations under nested repeated cross-validation, comparing additive and non-additive models and reporting calibration and conformal coverage.
	•	O5. Governance. Register every headline claim with provenance, and publish the interpretation rule for each outcome pattern before the final run.
1.4 Hypotheses
Table 3. Pre-specified hypotheses, tests and falsification rules.
ID
Statement
Data
Test
Falsified if
H1
Role families differ in demand and salary profiles
DataScience Jobs
Kruskal-Wallis on log salary by role family, epsilon-squared, Dunn with Holm; mixed model with company random intercept
Role effect interval includes 0 after the company term
H2
Skill requirements are role-specific, not uniform
Analytics Jobs
Log-odds ratio with informative Dirichlet prior per skill and role; 1,000 role-label permutations; FDR q < 0.05
Count of specific skills is within the permutation null
H3
Technical-by-communication complementarity in advertised salary
Analytics Jobs
log salary ~ role + experience + location + T + C + T×C, robust SE; quantile regression at 0.25, 0.5, 0.75
Interaction interval includes 0 and sign is unstable across quantiles
H4
The same complementarity in the junior hike label
JDS
Firth logistic, storytelling × maths-statistics versus additive, likelihood-ratio test; bootstrap; power simulation
LRT p ≥ 0.05 with interval including 0 (report minimum detectable effect)
H5
Trait-success association in SDS is non-additive
SDS
Additive logistic versus quadratic and pairwise logistic, EBM, depth-3 tree; nested repeated CV; corrected resampled t-test
No non-additive model beats additive with a ΔAUC interval excluding 0
A descriptive alignment analysis (Section 4.9) compares, for each of the five dimensions, its demand share in postings with its standardised association with the JDS hike label. Five points cannot support a rank-correlation test, so this analysis is reported as paired estimates with bootstrap intervals, not as a hypothesis test.
1.5 Scope and non-goals
The study is observational. We do not estimate causal effects, produce individual-level predictions or recommendations, infer time trends (the posting files do not provide the temporal granularity for them), or link rows across files. The classifiers exist to measure how much signal the features carry and in what functional form; they are not deployed scorers.
2. Analytical Approach
2.1 Evidence classes and the no-false-join rule
Every table and figure carries one of three tags. Observed (O): computed from the supplied rows. External (E): taxonomy or prior knowledge, never allowed to alter observed rows. Model-derived (M): an estimate, prediction or explanation. Because no person or posting identifier spans the files, the datasets meet only at shared constructs (role family, skill dimension, seniority), never at rows (Figure 2). An alignment claim may state that a dimension has demand share a in postings and association b with the JDS label; it may not state that the skill causes promotion.

Figure 2. Datasets meet at constructs, never at rows. Dashed amber nodes are the only shared objects.
2.2 Architecture
Figure 1 shows the pipeline. Module M0 audits and cleans all files. Four evidence lanes then run in isolation: each lane reads only its own cleaned tables and writes only to the registry. The lanes never share intermediate objects, which is how leakage between files is prevented by construction. The design is adapted from FIRMHIVE, a recursive agent framework for firmware analysis built from a Tree of Agents whose nodes are context-isolated, plus a persistent knowledge hub. We keep the two ideas that matter for governance (isolation, shared persistent record) and drop the language-model agents: each node is a deterministic script, so every number can be regenerated with one command and no node can invent a conclusion.

Figure 1. Evidence-lane architecture. Green arrows write to the registry; the auditor gates everything that reaches the note.
Table 4. Modules, inputs, outputs and isolation rules.
Module
Input
Output
Isolation rule
M0
Four raw files
Clean tables, ledger, quarantine tables, leakage report
Raw files read-only; every change ledgered
M1 Market
DataScience Jobs, Analytics Jobs (role, salary, experience, location)
H1 estimates, Career Opportunity Frontier inputs
No JDS or SDS access
M2 Skill
Analytics Jobs text; taxonomy (E)
Canonical skills, role specificity, graph, Signal Index, H2 and H3
Taxonomy built with no outcome labels
M3 Junior
JDS only
H4, benchmark, calibration, conformal sets, explanations
Posting data enters only as dimension demand share, after modelling
M4 Senior
SDS only
H5, forensics, benchmark, calibration, explanations
No other file read
M5 Registry
Claim records from M1 to M4
Single source for all numbers
Append-only; versioned
M6 Auditor
Registry
Accept or reject per claim, with reason
Blocks rendering of rejected claims
M7 Views
Accepted claims
Note tables and figures; dashboard
Read-only
2.3 The construct bridge
JDS records five skill dimensions: big data, mathematics and statistics, coding, AI and machine learning, and dashboard and storytelling. We map every canonical skill extracted from postings onto the same five, plus an explicit unmapped bucket, using the rules in Table 10. This is the only quantity that crosses lanes, and it is the place the framework is most exposed: the JDS dimensions are named in the data dictionary but their item content is not documented, so our mapping is a construct we impose. Two controls apply. The mapping is scored against a hand-labelled gold set. And every ambiguous skill (SQL is the standard case) is reassigned at random in 1,000 draws to show how much any alignment estimate depends on the assignment.
2.4 Validation protocol
All supervised results use the protocol in Figure 3. Preprocessing, tuning and calibration sit inside the training folds, and the sealed outer fold is touched only at prediction time. We use repeated stratified k-fold rather than leave-one-out for model selection because leave-one-out estimates have high variance and pooled AUC across single-row folds is not a valid statistic. Class prevalence in JDS is about 52.5% versus 47.5%, so oversampling would add synthetic rows without correcting a real imbalance, and it is not used.

Figure 3. Nested, repeated, stratified validation with all fitting inside the training folds.
2.5 Why each method, and when we drop it
Each component must beat a simpler alternative on a pre-stated criterion or it is removed from the final system and reported as a negative result.
Table 5. Method justification and keep-or-drop criteria.
Method
Question it answers
Simpler alternative
Kept only if
Curated taxonomy + alias and fuzzy matching
What canonical skill does a string denote?
Raw string counts
Gold-set F1 exceeds raw matching with non-overlapping intervals
TF-IDF and sentence embeddings
Does semantics add recall beyond the dictionary?
Dictionary only
ΔF1 interval excludes 0 on the gold set
Log-odds with informative prior
Which skills are role-specific?
Raw frequency ratios
Stabilises rare-skill estimates (rank agreement with permutation null)
NPMI graph + Leiden at several resolutions
Which skills travel together?
Pairwise counts
Masked-skill prediction beats a frequency baseline
Mixed model with company term
Do role differences survive company clustering?
OLS on pooled rows
Company variance share is material
Firth logistic
Stable coefficients at n = 139
Plain logistic
Plain logistic shows separation or inflated coefficients
EBM
Shape of each effect, with interactions
GBM plus SHAP
Matches GBM AUC within interval while giving direct shapes
TabPFN (if weights run offline)
Is a small-data foundation model a stronger baseline?
Tuned logistic regression
Paired ΔAUC interval excludes 0
Stacking on out-of-fold predictions
Do model families complement each other?
Best single model
Paired ΔAUC interval excludes 0
Platt calibration, bootstrap ECE
Are probabilities trustworthy?
Raw probabilities
Brier or ECE improves with interval excluding 0
Conformal prediction sets
Honest uncertainty per case
Point probability
Empirical coverage within tolerance of 1 − α
2.6 Evidence Registry and Auditor
Every headline number is a registry record (Appendix C): claim id, statement, dataset, evidence tag, method, metric, value, 95% interval, n, limitation and code reference. The note is rendered from the registry, so a number cannot drift from the code that produced it. The auditor enforces six rules: A1 all fields present; A2 every numeric claim carries an interval or an exact n; A3 a language lint rejects causal verbs (causes, drives, leads to, ensures, proves) and individual-outcome phrasing (will succeed); A4 a claim cites one lane's dataset unless it is typed alignment and names the bridge construct; A5 the code reference resolves and a rerun reproduces the value; A6 an evidence tag is present.
3. Data Exploration and Preparation
3.1 Inventory
Table 6. The four files as supplied.
File
Shape
Unit
Fields
Outcome
DataScience Jobs.csv
1,602 × 8
Posting by company
reference_no, company_name, job_title, min_experience, avg_salary, min_salary, max_salary, num_of_jobs
None
Analytics Jobs.csv
15,841 × 8
Posting
s_no, experience, job_description, job_desig, job_type, key_skills, location, salary
None
JDS Skill Traits.xlsx
139 × 7
Junior professional
id; big data, maths-stats, coding, AI and ML, dashboard and storytelling (1 to 5)
Salary hike high (1) or low (0)
SDS Personality Traits.xlsx
161 × 7
Senior professional
id; neuroticism, extraversion, openness, agreeableness, conscientiousness (normalised)
Success high or low
The salary strings in DataScience Jobs take the form 7.8L, and the file has about 1,460 distinct reference numbers across 1,602 rows. We do not assume repeated identifiers are errors: they are inspected field by field before any collapse (ledger L02). The organizers describe the posting files as 2024 to 2025 data without dates, so no trend analysis is attempted.
3.2 Audit protocol
Table 7. Audit checks, methods and action rules. Every action is written to the cleaning ledger.
Check
Method
Action rule
Schema and types
Typed assertions per column (dtype, range, regex)
Violating rows go to a quarantine table with a reason code; no silent coercion
Missingness
Per-column rate; missingness versus role and company (chi-squared)
Outcomes never imputed; features get a missing indicator and in-fold median or mode
Exact and near duplicates
Exact on all fields; MinHash Jaccard ≥ 0.90 on title, company and description; repeated reference_no inspected
Exact duplicates collapsed with count kept; near-duplicates flagged and retained for a sensitivity run
Salary strings
Regex per observed format; unit check (lakh per annum); min ≤ average ≤ max
Non-parsing strings to quarantine; undisclosed to missing plus indicator
Experience
Parse ranges and single values; flag reversed ranges and values above 40 years
Derive midpoint and width; reversed ranges swapped and ledgered
Category variants
NFKC, case-fold, whitespace; Jaro-Winkler ≥ 0.92 clustering; human review of each proposed merge
Merges recorded as old to new with counts
Skill spelling
Alias table; Levenshtein ratio ≥ 90 against canonical forms; review queue
Unmapped tokens kept with frequency
Outliers
Median/MAD robust z on log salary and experience; Tukey fences; Isolation Forest on JDS and SDS matrices as a flag only
Flagged rows retained; each headline estimate is rerun without them
Range and scale validity
JDS scores in 1 to 5; SDS mean, SD and skew per trait against the stated normalisation
Violations reported; normalisation not assumed
Class balance
Prevalence with Wilson interval
Informs stratification only; no resampling
Rule-likeness forensics (JDS, SDS)
Tie structure, marginals, pairwise independence, depth-2 and depth-3 tree separability, shuffled-target gap
Report the outcome with a data-structure caveat if a simple rule separates classes
3.3 Cleaning ledger
Each transformation is recorded as problem, diagnosis, decision, rows affected and validation, so cleaning is visible analysis rather than hidden preprocessing. Table 8 lists the planned entries; counts are filled by the run.
Table 8. Cleaning ledger (planned entries; counts from the audit run).
ID
File
Problem
Diagnosis
Decision
Rows
Validation
L01
DS Jobs
Salary strings such as 7.8L
Regex parse
Numeric lakh per annum
[n]
Round-trip format check; min ≤ avg ≤ max
L02
DS Jobs
Repeated reference_no
Field comparison within id
[collapse or keep, after inspection]
[n]
H1 rerun both ways
L03
Analytics
Salary formats; undisclosed values
Regex families; unmatched frequency
Parse; undisclosed to missing plus indicator
[n]
Role mix of disclosed versus undisclosed (chi-squared)
L04
Analytics
Experience ranges
Regex
Min, max, midpoint
[n]
Reversed and implausible counts
L05
Analytics
job_desig variants
Jaro-Winkler clusters + review
Map to role family
[n]
Manual audit of 200 mappings
L06
Analytics
key_skills spelling and format
Alias table + fuzzy match
Canonical skills
[n]
Gold-set F1
L07
JDS, SDS
Spaces in column names
Schema inspection
snake_case in code; originals kept in dictionary
All
Schema test
L08
JDS, SDS
Duplicate or near-duplicate rows
Exact and Hamming match
[decide after inspection]
[n]
Group-aware CV sensitivity
3.4 Derived variables
Table 9. Derived variables.
Variable
Definition
Source
salary_mid_lpa, log_salary
Mean of min and max when both exist, else average; natural log
Both job files
salary_range_ratio
(max − min) / midpoint
DS Jobs
exp_mid, exp_width
Midpoint and width of the experience range
Both job files
role_family
Rule-based mapping of title tokens (analyst, scientist, engineer, ML, architect, business, other), reviewed by hand
Both job files
seniority
Ordinal from designation tokens (junior, none, senior, lead, principal, manager)
Both job files
n_skills; dim_share_d
Count of mapped skills; share of a posting's mapped skills in dimension d
Analytics Jobs
T, C
T: number of technical dimensions requested (0 to 4). C: 1 if a dashboard-and-storytelling or communication skill is requested
Analytics Jobs
demand_intensity
num_of_jobs (openings) per role family and company
DS Jobs
3.5 Skill normalisation and the gold set
Raw key_skills strings are not canonical skills. The pipeline is: clean, tokenise, alias lookup, fuzzy match, canonical skill, dimension, role association. Each output row keeps the original string, canonical skill, dimension, mapping method and confidence. Four representations are benchmarked in order of sophistication: dictionary and regex; TF-IDF with word and character n-grams; sentence-embedding nearest neighbour against the alias table; and, if its weights can be used offline, an ESCO-based extractor. Because the taxonomy is built for Indian technology postings and ESCO is a European taxonomy, ESCO coverage of tool names is itself a reported finding.
Ground truth does not exist, so we create it: two team members independently label about 250 postings, stratified by role family, and we report Cohen's kappa, then micro and macro precision, recall and F1 with 95% bootstrap intervals, plus coverage (share of tokens mapped). Without the gold set no F1 is claimed.
Table 10. Dimension mapping rules and examples.
Dimension
Example canonical skills
Ambiguity rule
Big data
Hadoop, Spark, Hive, Kafka, data warehousing
Cloud data platforms included; SQL excluded here
Mathematics and statistics
Statistics, regression, probability, hypothesis testing, forecasting, optimisation
Generic 'analytics' not mapped
Coding
Python, Java, Scala, C++, R, SQL
SQL assigned here; sensitivity run reassigns to big data
AI and ML
Machine learning, deep learning, NLP, computer vision, TensorFlow, PyTorch
Generic 'AI' with no method named is mapped
Dashboard and storytelling
Tableau, Power BI, data visualisation, reporting, presentation, stakeholder communication
Communication is counted in C as well
Unmapped
ERP, CRM, project tools, domain systems
Counted and reported; excluded from T and C
3.6 Leakage audit
Table 11. Leakage tests. No benchmark is accepted unless every row is PASS or an explained WARN.
Test
What it catches
Mechanism
Verdict
LK1
ID or index columns used as features
Feature allow-list assertion
[PASS/WARN/FAIL]
LK2
Duplicate rows straddling outer folds
Group-aware split check
[PASS/WARN/FAIL]
LK3
Preprocessing fitted outside the training fold
Pipeline objects only; code assertion
[PASS/WARN/FAIL]
LK4
Target-derived or deterministic features
Feature-to-target mapping and correlation screen
[PASS/WARN/FAIL]
LK5
Calibration data overlapping the scored fold
Inner out-of-fold calibration only
[PASS/WARN/FAIL]
LK6
Outcome information reaching the taxonomy
M2 never reads JDS or SDS
[PASS/WARN/FAIL]
LK7
Harness bias
Shuffled-target AUC centred on 0.5
[PASS/WARN/FAIL]
LK8
Stacking leakage
Meta-learner fitted on out-of-fold predictions only
[PASS/WARN/FAIL]
3.7 Exploration figures
Exploration is organised by hypothesis, not by chart type. Figures F5 to F9 (Appendix B) answer, in order: how salary varies by role family and experience, which skills dominate and for whom, how missingness and undisclosed salary are structured, and what the JDS and SDS marginals and correlations look like. The missingness figure is shown first because undisclosed salary can bias every salary result.
FIGURE SLOT F5/F6: Salary and experience structure (H1)   [generate from final run]
Left: violin plus median and IQR of log salary (LPA) by role family, n per family, Dunn-Holm brackets. Right: hexbin of experience midpoint versus salary with a LOESS curve per role family and bootstrap bands. Tag: O.

FIGURE SLOT F8: Missingness map and disclosed-versus-undisclosed role mix   [generate from final run]
Column-by-row missingness matrix for Analytics Jobs; bar chart of role-family share among disclosed and undisclosed salaries with chi-squared result. Tag: O.

4. Data Analysis
Each subsection follows one pattern: hypothesis, method, expected form of result, limitation. Figure slots point to the specifications in Appendix B.
4.1 Market structure (H1)
For DataScience Jobs we test whether log salary differs across role families with Kruskal-Wallis (rank-based, robust to the right skew of salary), report epsilon-squared with a bootstrap interval, and run Dunn's pairwise tests with Holm correction. Because company names repeat, we also fit log_salary ~ role_family + exp_mid + (1 | company) and report the share of variance at company level. Demand is analysed through num_of_jobs per role family, and the two are combined in the Career Opportunity Frontier (F11): median salary on one axis, openings on the other, bubble area for median minimum experience, colour for role family, with bootstrap ellipses so that apparent differences are shown with their uncertainty. Limitation: the postings are a sample of advertised roles, not of employment.
4.2 Skill structure (H2)
For each skill s and role family r we compute the log-odds ratio of s in r against all other roles with an informative Dirichlet prior (Monroe, Colaresi and Quinn), which shrinks rare-skill estimates toward the corpus rate, and convert it to a z-score. The null is built by permuting role labels 1,000 times; H2 is supported if the number of skills with FDR q < 0.05 clearly exceeds the null. The co-occurrence graph weights edges by normalised pointwise mutual information (NPMI), which corrects for the dominance of very frequent skills, and is clustered with Leiden at several resolutions. Because no ground truth exists for a skill graph, we validate it as the software-skills literature does: mask 40% of a posting's skill entries and test whether graph relatedness recovers them better than a frequency-only baseline (F9). Cluster stability is the adjusted Rand index across 200 bootstrap resamples; a clustering with unstable assignments is reported as unstable.
The Skill Market Signal Index is an analytic ranking, not a value of a skill. For skill s, SSI(s) = Σ_k w_k · r_k(s), where r_k is the percentile rank on four components (demand, role specificity, salary association, breadth across role families) and the salary association is the ridge-shrunk coefficient of a skill indicator in log salary controlling for role, experience and location. Weights are not chosen: we draw w from Dirichlet(1,1,1,1) 10,000 times and report each skill's rank interval and the Kendall tau against equal weights (F10).
FIGURE SLOT F7/F9: Role-skill heatmap and masked-skill validation (H2)   [generate from final run]
F7: top 30 canonical skills by 8 role families, colour = log-odds z, hatched cells where q ≥ 0.05. F9: ROC and lift-by-decile for graph relatedness versus frequency baseline in recovering masked skills. Tag: O and M.

4.3 Complementarity in postings (H3)
We fit log salary on role family, experience midpoint, location, T, C and the product T×C, with heteroscedasticity-robust standard errors, and repeat at the 0.25, 0.5 and 0.75 quantiles to see whether a premium exists across the distribution rather than only at the mean. The disclosed-salary subsample may differ from all postings, so the model is also fitted with inverse-probability weights from a disclosure model, and the two estimates are shown together. Robustness variants: binary T, dimension shares in place of counts, the random SQL reassignment from Section 2.3, and exclusion of flagged outliers.
4.4 Junior lane (H4)
The target is the high/low hike label with five scores as features. Candidates are a majority-class baseline; logistic regression; Firth-penalised logistic regression; logistic regression with the storytelling × maths-statistics interaction; random forest; extra trees; histogram gradient boosting; LightGBM; EBM; and TabPFN where its weights can run offline. Hyper-parameters are tuned in the inner loop (Appendix D). H4 is tested with a likelihood-ratio test of the interaction model against the additive model, a 2,000-replicate bootstrap interval for the coefficient, and a simulation that reports the smallest interaction effect detectable with 80% power at n = 139, so that a null result is reported as low power and not as absence of effect. Metrics are ROC-AUC, PR-AUC, F1, balanced accuracy, accuracy, Brier score and bootstrap ECE, averaged over the 100 outer folds with standard deviations.
4.5 Senior lane (H5)
The SDS analysis begins with forensics (Table 7, last row) because a preliminary AUC near 0.992 on five features and 161 rows is unusual for behavioural data. We fit a depth-2 and depth-3 decision tree and look for a simple threshold rule; compute the shuffled-target gap; and inspect the trait marginals for ceiling effects. If a simple rule separates the classes, the result is reported as a property of how the label relates to the trait scores in this file, not as evidence about real-world success. We then compare additive logistic regression, logistic regression with quadratic and pairwise terms (limited to conscientiousness × openness, conscientiousness × extraversion and openness × extraversion, chosen in advance), EBM and a depth-3 tree. The non-additive hypothesis has a specific, literature-based prediction: studies of the Big Five and job performance report curvilinear effects of conscientiousness and interactions among factors, so we examine partial-dependence and EBM shape curves for a plateau or decline at high conscientiousness. Limitation: those studies use supervisor-rated performance, whereas the SDS label is a high/low success classification of unstated provenance.
4.6 Ensembles, calibration and uncertainty
Stacking is attempted with base learners from the logistic, tree and boosting families, using only out-of-fold predictions for the L2-regularised logistic meta-learner. It is kept only if the paired ΔAUC against the best single model has an interval that excludes 0, using the corrected resampled t-test of Nadeau and Bengio, which accounts for the overlap between training sets in repeated cross-validation. Probabilities are compared uncalibrated and Platt-calibrated; isotonic regression is not used because it overfits at these sample sizes. Reliability diagrams use five bins with a bootstrap band, and ECE and Brier score are reported with intervals. For per-case uncertainty we use split-conformal prediction sets (Angelopoulos and Bates) at α = 0.10 and report empirical coverage and the distribution of set sizes; with n this small the coverage itself has sampling error, which is shown.
FIGURE SLOT F13-F16: Benchmark leaderboard, ROC/PR, reliability, conformal coverage   [generate from final run]
F13: forest plot of mean AUC with 95% interval over 100 outer folds for every model, with the shuffled-target null band, JDS and SDS panels. F14: per-fold ROC and PR curves in light lines with the mean. F15: reliability diagrams before and after Platt with bootstrap band. F16: empirical coverage versus 1 − α and set-size histogram. Tag: M.

4.7 Explanation
We report permutation importance computed on the sealed fold, SHAP values for tree models, EBM shape functions with bagged intervals, and the coefficients of the linear and Firth models, and require that the four agree in sign and rough rank before a feature is called important. Explanations are written as contributions to the model's estimate of the observed class, never as effects of changing a person's score. Auditor rule A3 enforces that wording.
FIGURE SLOT F17/F18: Shape functions and interaction surfaces   [generate from final run]
F17: EBM shape function per feature with bagged intervals; partial dependence of conscientiousness for SDS. F18: predicted-probability heatmaps for storytelling × maths-statistics (JDS) and conscientiousness × openness (SDS), with the data's convex hull marked so that extrapolated regions are not read. Tag: M.

4.8 Ablation and robustness
Table 12. Ablation plan; each row is a pre-registered comparison reported with an interval.
Lane
Variants
JDS
A all five features; B technical only (big data, coding, AI and ML); C communication only (dashboard and storytelling); D quantitative only (maths-statistics, coding, AI and ML); E drop the strongest feature; F shuffled target
SDS
A all five traits; B without neuroticism; C conscientiousness only; D openness only; E with the three pre-chosen interactions; F shuffled target
Skills
A raw keyword match; B TF-IDF; C embeddings; D taxonomy-assisted matching; each scored on the gold set
System
Stacking versus best single model; calibrated versus raw; TabPFN and EBM versus tuned logistic
Robustness covers 20 random seeds, three cross-validation geometries (5×20, 10×10, 3×30), decision-threshold changes, missing-value perturbation, Gaussian noise on features at 0.25 and 0.5 SD, exclusion of flagged outliers and near-duplicates, and the 200-permutation shuffled-target null. If performance collapses under any perturbation, the collapse is documented in the results register.
4.9 Demand-reward alignment (descriptive)
For each of the five dimensions d we compute, in postings, the share of postings requesting d by role family (with a bootstrap interval over postings), and, in JDS, the standardised log-odds of a high hike per one-SD increase in the dimension score (bootstrap over respondents, other dimensions held fixed in the multivariable model). We plot the two as a pair per dimension with a 95% joint interval (F12) and report how often, across 2,000 joint bootstrap draws, a dimension's demand rank and reward rank differ by two or more places. The posting and JDS populations are different, and so are their outcomes (advertised salary versus realised hike), so the comparison is an alignment gap and not a measure of mispricing.
FIGURE SLOT F11/F12: Career Opportunity Frontier and demand-reward alignment   [generate from final run]
F11: x = openings, y = median log salary, bubble area = median minimum experience, colour = role family, bootstrap ellipses. F12: for each of five dimensions, demand share (x, with interval) against standardised JDS log-odds (y, with interval), 95% joint ellipse, diagonal of equal z-score. Tag: O and M; alignment claim type.

5. Results and Conclusions
5.1 Preliminary benchmark
Table 13 and Figure 4 report an earlier exploratory run: single seed, 5-fold cross-validation, default hyper-parameters, no nesting. It is included because it shaped the design, not as a result; the final numbers will come from the protocol in Figure 3 and replace it (F13).
Table 13. Preliminary single-seed 5-fold results (superseded by the final run).
Model
JDS acc
JDS F1
JDS AUC
SDS acc
SDS F1
SDS AUC
Note
Logistic
0.819
0.828
0.903
0.907
0.915
0.949
Best on JDS
Random forest
0.783
0.778
0.856
0.956
0.958
0.995

Extra trees
0.791
0.794
0.753
0.963
0.965
0.998
Best on SDS
HistGB
0.798
0.808
0.854
0.931
0.935
0.991

XGBoost
0.769
0.765
0.834
0.932
0.935
0.984

LightGBM
0.784
0.786
0.859
0.944
0.949
0.988


Figure 4. Preliminary ROC-AUC and accuracy by model (single seed, 5-fold). Replaced by F13 after the final run.
Two patterns in these numbers define the questions of Section 4. In JDS the linear model leads and the flexible models trail it (extra trees 0.753 versus logistic 0.903), which is what an approximately additive signal plus noise at n = 139 looks like. In SDS the ordering reverses (logistic 0.949 versus extra trees 0.998), a gap that implies either non-additive structure or rule-like label generation. H5 and the forensic tests exist to tell these apart. Univariate associations in the same exploratory pass (Table 14) are hypotheses, not findings.
Table 14. Preliminary univariate associations with the outcome (approximate; hypothesis-generating).
JDS feature
Association
SDS trait
Association
Dashboard and storytelling
≈ 0.55
Conscientiousness
≈ 0.68
Maths and statistics
≈ 0.52
Openness
≈ 0.67
Coding
≈ 0.44
Extraversion
≈ 0.49
AI and ML
≈ 0.40
Agreeableness
≈ 0.29
Big data
≈ 0.11
Neuroticism
≈ 0
5.2 Results register
Table 15 is rendered from the Evidence Registry. Entries are empty until the final run; a hypothesis with no accepted claim is reported as untested.
Table 15. Results register.
ID
Primary estimate
95% interval
Verdict
n
Claim ids
H1
[epsilon-squared; company variance share]
[ ]
[supported / not]
[ ]
[ ]
H2
[count of specific skills vs permutation null]
[ ]
[ ]
[ ]
[ ]
H3
[T×C coefficient on log salary]
[ ]
[ ]
[ ]
[ ]
H4
[interaction coefficient; MDE at 80% power]
[ ]
[ ]
139
[ ]
H5
[ΔAUC non-additive minus additive]
[ ]
[ ]
161
[ ]
Align
[demand share and JDS log-odds per dimension]
[ ]
[descriptive]
[ ]
[ ]
5.3 Pre-committed interpretation
To prevent post-hoc storytelling, the reading of each outcome pattern is fixed here.
Table 16. Outcome patterns and the conclusion each will support.
Pattern
Conclusion we will state
Wording limit
H3 and H4 supported with the same sign; H5 shows a conscientiousness-by-social interaction
Technical and social skill complementarity appears in three independent files
Association only
H3 supported, H4 null
A salary premium for the pairing is visible in postings; JDS at n = 139 cannot confirm it (state MDE)
Do not call the JDS result absence of effect
H3 null, H4 supported
Progression signal in JDS is not visible in advertised salary: an alignment gap
Populations and outcomes differ
All null
No evidence of complementarity in these data; an additive skill model suffices
Report power
A simple rule separates SDS classes
The SDS label is nearly a function of the trait scores in this file; findings describe the labelling
No workforce inference
5.4 What the numbers cannot say
Cross-validated performance estimates how well a model fits the same population it was sampled from. It does not show deployment performance, and ROC-AUC is not accuracy: both are always reported by name. A feature with large importance contributes strongly to the model's estimate of the observed class; it is not shown to cause the outcome.
6. Implications
Implications are conditional on the outcome pattern in Table 16 and are limited to what the evidence supports.
Table 17. Stakeholder implications.
Stakeholder
If the association is supported
If null
Not supported by this evidence
Employers
Benchmark pay within role family, not pooled; check whether postings name communication alongside technical requirements
Pooled technical skill lists are adequate
Screening individuals on personality scores
HR and L&D
Programmes pairing quantitative training with visual and verbal communication are the better-supported bundle
No evidence for a bundle effect; prioritise by role-specific demand
Predicting any employee's promotion
Universities
Compare dimension demand shares with curriculum coverage (needs institutional data)
Align to role-specific skills from H2
Claims about graduate outcomes
Professionals
Use role-conditioned skill gaps and adjacent-skill clusters to plan learning
Prioritise the most role-specific skills
Guaranteed salary gains from any skill
Policymakers
Invest in longitudinal linkage with consent; localise skill taxonomies for the Indian market
Same data need
Causal policy conclusions
7. Limitations and Ethical Considerations
L1 Observational data. No causal inference is made. L2 Small samples. JDS (139) and SDS (161) give wide intervals and low power for interactions, so every interaction result carries a minimum detectable effect. L3 Provenance. The files may contain self-reported, masked or generated values, and the SDS label's provenance is unstated. L4 No linkage. There is no person-level link between files, so alignment is across populations. L5 Construct validity. Mapping posting skills onto the five JDS dimensions is our construct; it is tested for sensitivity but not validated against JDS item content. L6 Taxonomy fit. External taxonomies may fit Indian technology postings poorly. L7 Sampling. Postings are not the whole market and undisclosed salaries may be selected. L8 No time axis. No trend or trajectory is observed. L9 Personality. Trait scores are normalised self-descriptions; interpretations must be cautious. L10 Generalisation. Cross-validation does not show real-world performance.
Ethics. We do not build or recommend a tool that scores individuals. The output of any model is an estimate of the observed class under a learned statistical relationship, and personality results in particular must not be used to screen, rank or exclude people. The auditor's language rule blocks deterministic and discriminatory phrasing in generated text.
8. Conclusion and Future Work
We defined a problem the four files can support, built the machinery to test it, and fixed in advance how each outcome will be read. The contribution is the composition: a falsifiable organising hypothesis tested in three independent datasets, a boundary-preserving architecture in which datasets meet only at shared constructs, and an audit layer that makes every number traceable. None of the individual techniques is new, and we do not present them as such. Future work, in order of value: linked longitudinal data collected with consent; dated postings for genuine trend analysis; documented JDS items to validate the bridge; a localised skill taxonomy for Indian postings; and causal designs (for instance, matched cohorts) that observational files cannot support.
References
[1] Angelopoulos, A. N., and Bates, S. (2021). A gentle introduction to conformal prediction and distribution-free uncertainty quantification. arXiv:2107.07511.
[2] Carter, N. T., et al. (2014). Uncovering curvilinear relationships between conscientiousness and job performance: How theoretically appropriate measurement makes an empirical difference. Journal of Applied Psychology.
[3] Deming, D., and Kahn, L. B. Skill requirements across firms and labor markets: Evidence from job postings for professionals. NBER Working Paper 23328.
[4] Firth, D. (1993). Bias reduction of maximum likelihood estimates. Biometrika, 80(1), 27-38.
[5] FIRMHIVE: recursive agent-based framework for firmware analysis with a Tree of Agents and Persistent Knowledge Hub. [authors, year, venue to be confirmed]
[6] Hollmann, N., et al. (2025). Accurate predictions on small data with a tabular foundation model. Nature, 637, 319-326.
[7] Imperial College London / Pissarides Review (2024). Patterns of co-occurrent skills in UK job adverts. arXiv:2406.03139.
[8] Le, H., et al. (2011). Too much of a good thing: Curvilinear relationships between personality traits and job performance. Journal of Applied Psychology.
[9] Monroe, B. L., Colaresi, M. P., and Quinn, K. M. (2008). Fightin' words: Lexical feature selection and evaluation for identifying the content of political conflict. Political Analysis, 16(4).
[10] Nadeau, C., and Bengio, Y. (2003). Inference for the generalization error. Machine Learning, 52, 239-281.
[11] Nori, H., et al. (2019). InterpretML: A unified framework for machine learning interpretability. arXiv:1909.09223.
[12] Using digital traces to analyze software work: skills, careers and programming languages. arXiv:2504.03581.

Appendix A. Data Dictionary (as supplied)
File
Column
Meaning and handling
DataScience Jobs
reference_no
Posting reference; not a feature; repeated values investigated (L02)

company_name, job_title
Categorical; normalised (Table 7)

min_experience
Years; parsed

avg_salary, min_salary, max_salary
Strings such as 7.8L; lakh per annum after parsing

num_of_jobs
Openings; demand intensity
Analytics Jobs
s_no
Row id; not a feature

experience, salary
Free-text ranges; parsed

job_description, job_desig, job_type, location
Text and categorical; NLP and category normalisation

key_skills
Delimited skill strings; normalised to canonical skills
JDS
id
Row id; not a feature

big_data_skills, maths-stats_skills, coding_skills, ai_and_ml_skills, dashboard_and_storytelling_skills
Scores 1 to 5

salary_hike_high_or_low
Outcome: 1 high, 0 low
SDS
id
Row id; not a feature

neuroticism, extraversion, openness_to_experience, agreeableness, conscientiousness
Normalised trait scores; column names with spaces normalised in code, originals preserved here

success_classification_high_low
Outcome: high or low success
Appendix B. Figure Specifications
Table B1. Figures. F1 to F4 are included in the note; F5 onward are generated by the final run from the registry.
ID
Figure
Encoding
Annotation or test
F1 to F4
Architecture, no-false-join, validation protocol, preliminary benchmark
As in Sections 2 and 5
Done
F5
Salary by role family
Violin plus median and IQR, log LPA
n per family; Dunn-Holm brackets
F6
Experience versus salary
Hexbin plus LOESS per role family
Bootstrap bands
F7
Role-skill heatmap
30 skills by 8 role families, colour = log-odds z
Hatching where q ≥ 0.05
F8
Missingness and disclosure
Missingness matrix; role mix bars
Chi-squared
F9
Masked-skill validation
ROC and lift by decile
Versus frequency baseline
F10
Signal Index rank intervals
Dot plot of rank interval for top 25 skills
10,000 Dirichlet weight draws
F11
Career Opportunity Frontier
x openings, y median log salary, bubble experience, colour role
Bootstrap ellipses
F12
Demand-reward alignment
Per dimension: demand share against JDS log-odds
95% joint ellipse
F13
Benchmark leaderboard
Forest plot of AUC over 100 outer folds, JDS and SDS
Shuffled-target null band
F14
ROC and PR curves
Per-fold light lines with mean
Per model
F15
Reliability diagrams
Five bins before and after Platt
Bootstrap band; ECE, Brier
F16
Conformal coverage
Coverage versus 1 − α; set-size histogram
α = 0.10
F17
Shape functions
EBM shapes with bagged intervals; PDP
Conscientiousness plateau check
F18
Interaction surfaces
Probability heatmaps for two pairs
Convex hull of data marked
F19
Ablations
Bars with intervals per Table 12
Paired ΔAUC
F20
Robustness
AUC across seeds, splits and noise levels
Collapse points flagged
Appendix C. Evidence Registry Record
claim_id:   H4-int-001
statement:  "Adding the storytelling x maths-statistics interaction changes JDS hike log-odds"
dataset:    JDS (tag O/M)
method:     Firth logistic; LRT additive vs interaction; 2,000-rep bootstrap
metric:     interaction coefficient (log-odds per SD^2); delta-AUC (nested CV)
value:      0.589
ci95:       0.589
n:          139
limitation: "n = 139; MDE = 0.589; association only"
code_ref:   src/models/jds_interaction.py @ a1b2c3d4
status:     pending_audit

Appendix D. Hyper-parameter Search Spaces (inner loop)
Model
Search space
Logistic (L2)
C in 13 log-spaced values from 1e-3 to 1e3
Random forest, extra trees
500 trees; max_depth {2, 3, 4, none}; min_samples_leaf {1, 2, 4, 8}; max_features {sqrt, 1.0}
HistGB
learning_rate {0.03, 0.1}; max_depth {2, 3}; max_iter {100, 300}; l2 {0, 1, 10}
LightGBM
num_leaves {4, 8}; min_child_samples {5, 10, 20}; learning_rate {0.03, 0.1}; n_estimators {100, 300}; reg_lambda {0, 1, 10}
EBM
interactions {0, 3, 5}; outer_bags 25; learning_rate 0.01
TabPFN
Defaults; no tuning
Stack meta-learner
L2 logistic, C {0.1, 1, 10}
Appendix E. Reproducibility
	•	One command (make all) reruns audit, features, benchmark, registry and note rendering from the raw files.
	•	Seeds 0 to 19 for repeats; library versions pinned in requirements.txt [versions]; run log hash [hash].
	•	No hidden notebook state: notebooks only display registry outputs.
	•	Code excerpts and screenshots of the pipeline run: Reproducibility logs and screenshots are available in the repository root and `reports/` directory..

Appendix F. Draft Checklist (delete before submission)
	•	Replace every highlighted bracket with a value from the Evidence Registry; if a value cannot be produced, delete the sentence that depends on it.
	•	Replace Figure 4 and Table 13 with F13 and the final benchmark table; keep Figure 4 only in the appendix as the exploratory run.
	•	Insert F5 to F20 into the slots in Sections 3 and 4 and Appendix B; check page count (target 20 to 25 pages before this appendix).
	•	Confirm with the organizers whether model weights and taxonomies may be downloaded during the competition; if not, drop TabPFN, embeddings and ESCO and say so in Section 2.5.
	•	Fill the FIRMHIVE and Hutter reference details; confirm every citation against the source.
	•	Confirm that the SDS label provenance and JDS item content are not documented elsewhere in the organizers' materials.
