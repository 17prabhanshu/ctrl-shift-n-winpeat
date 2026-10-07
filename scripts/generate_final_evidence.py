import json
import os
from src.agents.evidence_registry import EvidenceRegistry, EvidenceRecord

def generate():
    registry = EvidenceRegistry("reports/evidence/evidence_registry.json")
    
    # Read from reports/evidence/evidence_registry.json to see what claims already exist
    existing_claims = {r.claim_id for r in registry.records}
    
    # Load JDS benchmark
    with open("reports/benchmarks/jds_benchmark.json", "r") as f:
        jds_data = json.load(f)
        
    lr_acc = jds_data["LogisticRegression"]["accuracy"]["mean"]
    rf_auc = jds_data["RandomForest"]["roc_auc"]["mean"]
    
    registry.register(EvidenceRecord(
        claim_id="JDS-ACC-001",
        statement="JDS Full Model Logistic Regression accuracy",
        dataset="JDS Skill Traits",
        evidence_tag="M",
        method="Logistic Regression",
        metric="accuracy",
        value=lr_acc,
        limitation="Small sample size (n=139); repeated CV folds overlap and are not independent experiments"
    ))
    
    registry.register(EvidenceRecord(
        claim_id="JDS-AUC-001",
        statement="JDS Random Forest AUC",
        dataset="JDS Skill Traits",
        evidence_tag="M",
        method="Random Forest",
        metric="roc_auc",
        value=rf_auc,
        limitation="Small sample size (n=139); repeated CV folds overlap and are not independent experiments"
    ))

    # Load SDS benchmark
    with open("reports/benchmarks/sds_benchmark.json", "r") as f:
        sds_data = json.load(f)
        
    rf_acc = sds_data["RandomForest"]["accuracy"]["mean"]
    rf_auc = sds_data["RandomForest"]["roc_auc"]["mean"]
    
    registry.register(EvidenceRecord(
        claim_id="SDS-ACC-001",
        statement="SDS Full Model Random Forest accuracy",
        dataset="SDS Personality Traits",
        evidence_tag="M",
        method="Random Forest",
        metric="accuracy",
        value=rf_acc,
        limitation="Labels may be deterministically derived from personality thresholds (see forensic analysis)"
    ))
    
    registry.register(EvidenceRecord(
        claim_id="SDS-AUC-001",
        statement="SDS Multiple Seeds ROC-AUC mean",
        dataset="SDS Personality Traits",
        evidence_tag="M",
        method="Random Forest",
        metric="roc_auc",
        value=rf_auc,
        limitation="Labels may be deterministically derived from personality thresholds (see forensic analysis)"
    ))

    if "SSI-001" not in existing_claims:
        with open("reports/evidence/skill_signal_index.json", "r") as f:
            ssi_data = json.load(f)
            
        top_skill = max(ssi_data.items(), key=lambda x: x[1]["ssi_mean"])
        
        registry.register(EvidenceRecord(
            claim_id="SSI-001",
            statement=f"Skill '{top_skill[0]}' has the highest skill signal index.",
            dataset="Analytics Jobs",
            evidence_tag="M",
            method="Skill Signal Index",
            metric="ssi_mean",
            value=top_skill[1]["ssi_mean"],
            limitation="Based on observational data; cross-dataset taxonomy mapping may have inconsistencies."
        ))

    registry.auto_audit()
    report = registry.generate_report()
    
    os.makedirs("reports/evidence", exist_ok=True)
    with open("reports/evidence/evidence_audit_report.md", "w") as f:
        f.write(report)
        
    print("Final evidence registry and report generated.")

if __name__ == "__main__":
    generate()
