import importlib.util
import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "industry-deep-research-report"
SPEC = importlib.util.spec_from_file_location("validator", SKILL / "scripts" / "validate_report.py")
validator = importlib.util.module_from_spec(SPEC)
assert SPEC.loader is not None
SPEC.loader.exec_module(validator)
PACK_DIR = SKILL / "references" / "industry-packs"


def evidence(eid, categories, claim_types):
    return {
        "id": eid,
        "source_level": "A",
        "source_title": "Example source",
        "url": f"https://example.com/{eid}",
        "period": "2026",
        "scope": "Example scope",
        "scores": {"authority": 4, "originality": 4, "recency": 4, "scope_fit": 4, "independence": 4},
        "original_source_id": eid,
        "evidence_categories": categories,
        "supports_claim_types": claim_types,
        "cannot_support_claim_types": [],
        "verifiability": "high",
        "conflict_of_interest": "none",
        "retrieved_at": "2026-07-24",
        "original_source_url": f"https://example.com/{eid}",
        "evidence_excerpt": "Sanitized test evidence",
    }


class EvidencePackTests(unittest.TestCase):
    expected = {"consumer-retail", "saas-ai", "manufacturing", "ecommerce-platform", "healthcare", "restaurant-local-service"}

    def test_all_pack_files_and_levels(self):
        found = set()
        for path in PACK_DIR.glob("*.json"):
            data = json.loads(path.read_text(encoding="utf-8"))
            self.assertEqual(data["id"], path.stem)
            self.assertEqual(set(data["requirements_by_level"]), set(validator.LEVELS))
            found.add(data["id"])
        self.assertEqual(found, self.expected)

    def test_single_and_mixed_routing(self):
        cases = [("saas-ai", None), ("saas-ai", "healthcare"), ("consumer-retail", "ecommerce-platform"), ("manufacturing", "saas-ai")]
        for primary, secondary in cases:
            packs = [primary] + ([secondary] if secondary else [])
            brief = {"schema_version": "1.1", "industry_family": primary, "secondary_industry_family": secondary, "evidence_packs": packs, "decision_level": "L2"}
            results = validator.Results()
            routed = validator.route(brief, PACK_DIR, results)
            self.assertFalse(results.errors)
            self.assertEqual(routed[1], packs)

    def test_third_pack_is_rejected(self):
        results = validator.Results()
        validator.route({"schema_version": "1.1", "evidence_packs": ["saas-ai", "healthcare", "manufacturing"], "decision_level": "L3"}, PACK_DIR, results)
        self.assertIn("too_many_evidence_packs", {item["code"] for item in results.errors})

    def test_source_misuse_is_blocked(self):
        cases = [
            (evidence("policy", ["official_policy"], ["demand"]), "policy_source_misuse"),
            (evidence("population", ["population_context"], ["market_size"]), "population_not_market_size"),
            (evidence("trial", ["trial_registration"], ["product_effectiveness"]), "trial_registration_not_outcome"),
        ]
        for item, expected_code in cases:
            results = validator.Results()
            validator.check_evidence({"evidence": [item]}, results, True)
            self.assertIn(expected_code, {error["code"] for error in results.errors})

    def test_l1_warns_but_l3_blocks(self):
        config = json.loads((PACK_DIR / "saas-ai.json").read_text(encoding="utf-8"))
        l1 = validator.Results()
        validator.decision_gate("L1", [config], [], {}, l1)
        self.assertFalse(l1.errors)
        self.assertIn("industry_evidence_gap", {item["code"] for item in l1.warnings})
        l3 = validator.Results()
        supported, _ = validator.decision_gate("L3", [config], [], {}, l3)
        self.assertEqual(supported, "L1")
        self.assertIn("decision_level_not_supported", {item["code"] for item in l3.errors})


if __name__ == "__main__":
    unittest.main()
