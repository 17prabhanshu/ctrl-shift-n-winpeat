"""Tests for the Evidence Registry and Agent Architecture."""

import json
import tempfile
from pathlib import Path
import sys

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from src.evidence.evidence_registry import EvidenceRecord, EvidenceRegistry
from src.evidence.agent_architecture import (
    AgentInput, AgentOutput, DataAuditor, EvidenceAuditorAgent,
    AGENT_REGISTRY, run_agent,
)


class TestEvidenceRecord:
    def test_create_record(self):
        r = EvidenceRecord(
            claim_id="test-001",
            statement="Test claim",
            dataset="JDS",
            evidence_tag="O",
            method="test method",
            metric="accuracy",
            value=0.85,
            limitation="test limitation",
        )
        assert r.claim_id == "test-001"
        assert r.evidence_tag == "O"
    
    def test_to_dict(self):
        r = EvidenceRecord(
            claim_id="test-002",
            statement="Test",
            dataset="SDS",
            evidence_tag="M",
            method="test",
            metric="roc_auc",
            value=0.95,
            limitation="observational",
        )
        d = r.to_dict()
        assert isinstance(d, dict)
        assert d["claim_id"] == "test-002"
        assert d["value"] == 0.95
    
    def test_roundtrip(self):
        r = EvidenceRecord(
            claim_id="test-003",
            statement="Roundtrip",
            dataset="JDS",
            evidence_tag="O",
            method="test",
            metric="f1",
            value=0.88,
            limitation="small sample",
        )
        d = r.to_dict()
        r2 = EvidenceRecord.from_dict(d)
        assert r2.claim_id == r.claim_id
        assert r2.value == r.value


class TestEvidenceRegistry:
    def _make_registry(self):
        with tempfile.TemporaryDirectory() as tmpdir:
            path = Path(tmpdir) / "test_registry.json"
            return EvidenceRegistry(registry_path=path), path
    
    def test_register_and_retrieve(self):
        registry, _ = self._make_registry()
        r = EvidenceRecord(
            claim_id="reg-001",
            statement="Test registration",
            dataset="JDS",
            evidence_tag="O",
            method="test",
            metric="accuracy",
            value=0.80,
            limitation="test",
        )
        registry.register(r)
        assert len(registry.records) == 1
        assert registry.get_by_id("reg-001") is not None
    
    def test_auto_audit_rejects_causal(self):
        registry, _ = self._make_registry()
        r = EvidenceRecord(
            claim_id="causal-001",
            statement="Storytelling causes salary increase",
            dataset="JDS",
            evidence_tag="M",
            method="logistic regression",
            metric="coefficient",
            value=0.55,
            limitation="observational",
        )
        registry.register(r)
        results = registry.auto_audit()
        assert results["rejected"] == 1
        assert registry.get_by_id("causal-001").status == "rejected"
    
    def test_auto_audit_rejects_no_value(self):
        registry, _ = self._make_registry()
        r = EvidenceRecord(
            claim_id="noval-001",
            statement="Skills are associated with hike",
            dataset="JDS",
            evidence_tag="M",
            method="logistic regression",
            metric="coefficient",
            value=None,
            limitation="observational",
        )
        registry.register(r)
        results = registry.auto_audit()
        assert results["rejected"] == 1
    
    def test_auto_audit_accepts_valid(self):
        registry, _ = self._make_registry()
        r = EvidenceRecord(
            claim_id="valid-001",
            statement="Dashboard skill exhibits stronger observed association with hike classification",
            dataset="JDS",
            evidence_tag="M",
            method="logistic regression",
            metric="coefficient",
            value=0.55,
            ci95_lower=0.32,
            ci95_upper=0.78,
            n=139,
            limitation="Observational; n=139; no causal inference",
        )
        registry.register(r)
        results = registry.auto_audit()
        assert results["accepted"] == 1
    
    def test_generate_report(self):
        registry, _ = self._make_registry()
        r = EvidenceRecord(
            claim_id="rpt-001",
            statement="Test report",
            dataset="JDS",
            evidence_tag="O",
            method="test",
            metric="accuracy",
            value=0.80,
            limitation="test",
        )
        registry.register(r)
        registry.auto_audit()
        report = registry.generate_report()
        assert "Evidence Registry Report" in report
        assert "JDS" in report


class TestAgentArchitecture:
    def test_agent_input(self):
        inp = AgentInput(
            agent_name="test",
            dataset_paths=["/tmp/test.csv"],
        )
        assert inp.agent_name == "test"
    
    def test_agent_output(self):
        out = AgentOutput(
            agent_name="test",
            status="success",
            results={"key": "value"},
        )
        d = out.to_dict()
        assert d["status"] == "success"
    
    def test_agent_registry_complete(self):
        expected = {
            "data_auditor",
            "market_intelligence",
            "skill_intelligence",
            "junior_talent",
            "senior_talent",
            "validation",
            "evidence_auditor",
            "synthesis",
        }
        assert set(AGENT_REGISTRY.keys()) == expected
    
    def test_data_auditor_validation(self):
        agent = DataAuditor()
        inp = AgentInput(agent_name="data_auditor", dataset_paths=[])
        assert not agent.validate_input(inp)
        
        inp2 = AgentInput(agent_name="data_auditor", dataset_paths=["/tmp/test.csv"])
        assert agent.validate_input(inp2)


if __name__ == "__main__":
    import pytest
    pytest.main([__file__, "-v"])
