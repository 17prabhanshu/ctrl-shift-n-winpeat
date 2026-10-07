"""
Evidence Registry for the Workforce Intelligence Engine.

Every analytical claim is tracked with full provenance:
CLAIM → DATASET → METHOD → METRIC → EVIDENCE → LIMITATION

SAS CU Hackathon 2026 - Team ctrl shift n
"""

import json
import hashlib
from datetime import datetime
from pathlib import Path
from typing import Optional
from dataclasses import dataclass, field, asdict


@dataclass
class EvidenceRecord:
    """A single traceable evidence record."""
    claim_id: str
    statement: str
    dataset: str  # Which dataset: "JDS", "SDS", "DataScience Jobs", "Analytics Jobs"
    evidence_tag: str  # "O" = Observed, "E" = External, "M" = Model-derived
    method: str
    metric: str
    value: Optional[float] = None
    ci95_lower: Optional[float] = None
    ci95_upper: Optional[float] = None
    n: Optional[int] = None
    limitation: str = ""
    code_ref: str = ""
    status: str = "pending_audit"  # pending_audit, accepted, rejected
    rejection_reason: str = ""
    created_at: str = field(default_factory=lambda: datetime.now().isoformat())
    
    def to_dict(self) -> dict:
        return asdict(self)
    
    @classmethod
    def from_dict(cls, d: dict) -> "EvidenceRecord":
        return cls(**{k: v for k, v in d.items() if k in cls.__dataclass_fields__})


class EvidenceRegistry:
    """
    Append-only evidence registry.
    
    All analytical claims must be registered here before they can
    appear in the Approach Note or application.
    """
    
    def __init__(self, registry_path: Optional[Path] = None):
        if registry_path is None:
            from src.utils.config import EVIDENCE_DIR
            registry_path = EVIDENCE_DIR / "evidence_registry.json"
        self.registry_path = Path(registry_path)
        self.records: list[EvidenceRecord] = []
        self._load()
    
    def _load(self):
        """Load existing registry from disk."""
        if self.registry_path.exists():
            with open(self.registry_path, 'r') as f:
                data = json.load(f)
            self.records = [EvidenceRecord.from_dict(r) for r in data]
    
    def _save(self):
        """Persist registry to disk."""
        self.registry_path.parent.mkdir(parents=True, exist_ok=True)
        with open(self.registry_path, 'w') as f:
            json.dump([r.to_dict() for r in self.records], f, indent=2, default=str)
    
    def register(self, record: EvidenceRecord) -> str:
        """Register a new evidence record. Returns the claim_id."""
        # Validate required fields
        assert record.claim_id, "claim_id is required"
        assert record.statement, "statement is required"
        assert record.dataset, "dataset is required"
        assert record.evidence_tag in ("O", "E", "M"), \
            f"evidence_tag must be O, E, or M, got {record.evidence_tag}"
        assert record.method, "method is required"
        assert record.metric, "metric is required"
        
        # Check for duplicate claim_id
        existing_ids = {r.claim_id for r in self.records}
        if record.claim_id in existing_ids:
            # Update existing record
            for i, r in enumerate(self.records):
                if r.claim_id == record.claim_id:
                    self.records[i] = record
                    break
        else:
            self.records.append(record)
        
        self._save()
        return record.claim_id
    
    def audit(self, claim_id: str, accept: bool, reason: str = "") -> None:
        """Accept or reject a claim."""
        for r in self.records:
            if r.claim_id == claim_id:
                r.status = "accepted" if accept else "rejected"
                r.rejection_reason = reason if not accept else ""
                break
        self._save()
    
    def get_accepted(self) -> list[EvidenceRecord]:
        """Return only accepted claims."""
        return [r for r in self.records if r.status == "accepted"]
    
    def get_by_dataset(self, dataset: str) -> list[EvidenceRecord]:
        """Return all claims for a given dataset."""
        return [r for r in self.records if r.dataset == dataset]
    
    def get_by_id(self, claim_id: str) -> Optional[EvidenceRecord]:
        """Retrieve a specific claim."""
        for r in self.records:
            if r.claim_id == claim_id:
                return r
        return None
    
    def auto_audit(self) -> dict:
        """
        Automated audit: reject claims that violate rules.
        
        Rules:
        1. No causal language without experimental design
        2. No claim without a value
        3. No claim without a limitation
        """
        causal_words = ["causes", "caused by", "leads to", "results in", 
                        "determines", "proves", "proven"]
        
        audit_results = {"accepted": 0, "rejected": 0, "reasons": []}
        
        for r in self.records:
            if r.status != "pending_audit":
                continue
            
            reject = False
            reason = ""
            
            # Check for causal language
            stmt_lower = r.statement.lower()
            for word in causal_words:
                if word in stmt_lower:
                    reject = True
                    reason = f"Causal language detected: '{word}'. Use associational language."
                    break
            
            # Check for missing value
            if not reject and r.value is None:
                reject = True
                reason = "No metric value provided."
            
            # Check for missing limitation
            if not reject and not r.limitation:
                reject = True
                reason = "No limitation statement provided."
            
            if reject:
                r.status = "rejected"
                r.rejection_reason = reason
                audit_results["rejected"] += 1
                audit_results["reasons"].append({"claim_id": r.claim_id, "reason": reason})
            else:
                r.status = "accepted"
                audit_results["accepted"] += 1
        
        self._save()
        return audit_results
    
    def generate_report(self) -> str:
        """Generate a markdown report of the evidence registry."""
        lines = [
            "# Evidence Registry Report",
            "",
            f"Generated: {datetime.now().isoformat()}",
            f"Total claims: {len(self.records)}",
            f"Accepted: {sum(1 for r in self.records if r.status == 'accepted')}",
            f"Rejected: {sum(1 for r in self.records if r.status == 'rejected')}",
            f"Pending: {sum(1 for r in self.records if r.status == 'pending_audit')}",
            "",
            "## Claims by Dataset",
            "",
        ]
        
        datasets = sorted(set(r.dataset for r in self.records))
        for ds in datasets:
            records = self.get_by_dataset(ds)
            lines.append(f"### {ds}")
            lines.append("")
            lines.append("| Claim ID | Statement | Method | Metric | Value | CI 95% | Status |")
            lines.append("|----------|-----------|--------|--------|-------|--------|--------|")
            for r in records:
                ci = f"[{r.ci95_lower:.3f}, {r.ci95_upper:.3f}]" if r.ci95_lower is not None else "—"
                val = f"{r.value:.4f}" if r.value is not None else "—"
                lines.append(f"| {r.claim_id} | {r.statement[:60]}... | {r.method} | {r.metric} | {val} | {ci} | {r.status} |")
            lines.append("")
        
        return "\n".join(lines)
    
    def summary_stats(self) -> dict:
        """Return summary statistics for the registry."""
        return {
            "total": len(self.records),
            "accepted": sum(1 for r in self.records if r.status == "accepted"),
            "rejected": sum(1 for r in self.records if r.status == "rejected"),
            "pending": sum(1 for r in self.records if r.status == "pending_audit"),
            "by_dataset": {
                ds: len(self.get_by_dataset(ds))
                for ds in set(r.dataset for r in self.records)
            },
            "by_tag": {
                tag: sum(1 for r in self.records if r.evidence_tag == tag)
                for tag in ("O", "E", "M")
            },
        }


if __name__ == "__main__":
    # Example usage
    registry = EvidenceRegistry()
    
    # Register a sample claim
    record = EvidenceRecord(
        claim_id="H1-salary-001",
        statement="Role families differ in median salary (Kruskal-Wallis test)",
        dataset="DataScience Jobs",
        evidence_tag="O",
        method="Kruskal-Wallis H-test on log salary by role family",
        metric="epsilon_squared",
        limitation="Observational data; roles are classified by our taxonomy, not by employers",
    )
    registry.register(record)
    print(f"Registered {len(registry.records)} claims")
