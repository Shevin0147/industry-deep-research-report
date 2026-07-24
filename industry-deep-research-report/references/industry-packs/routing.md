# Industry Evidence Pack Routing

Use the universal evidence core for every report. Load one primary pack and at most one secondary pack. Packs change evidence requirements only; they never change the 10-section report format.

## Pack IDs

| Pack | Use when the research object is mainly about |
|---|---|
| `consumer-retail` | consumer products, brands, retail categories, packaged goods |
| `saas-ai` | SaaS, software, AI products, developer tools, digital services |
| `manufacturing` | factories, equipment, industrial supply chains, components, robotics hardware |
| `ecommerce-platform` | marketplaces, cross-border ecommerce, platform commerce, merchant ecosystems |
| `healthcare` | medical devices, drugs, clinical services, digital health, regulated health products |
| `restaurant-local-service` | restaurants, stores, hospitality, local and labor-intensive services |

## Routing Rules

1. Select the pack that best represents the paying customer, operating model, and decisive evidence.
2. Add a secondary pack only when another industry's evidence requirements materially change the decision.
3. Never load more than two packs.
4. If classification is uncertain, use `core` only and add a routing warning.
5. When two packs overlap, take the union of requirements. For the same claim type, use the stricter minimum source count and category coverage.

Examples:

- AI medical software: `saas-ai` + `healthcare`
- cross-border pet supplies: `consumer-retail` + `ecommerce-platform`
- industrial robot: `manufacturing` + `saas-ai`

## Brief Schema 1.1

```json
{
  "schema_version": "1.1",
  "mode": "standard",
  "industry_family": "saas-ai",
  "secondary_industry_family": "healthcare",
  "evidence_packs": ["saas-ai", "healthcare"],
  "decision_level": "L2",
  "routing_confidence": "high|medium|low",
  "routing_notes": []
}
```

Research depth and decision level are independent. A deep research run can still support only L1 when commercial evidence is absent.

## Evidence Schema 1.1 Additions

```json
{
  "evidence_categories": ["official_statistics"],
  "supports_claim_types": ["market_size"],
  "cannot_support_claim_types": ["commercialization"],
  "verifiability": "high|medium|low",
  "conflict_of_interest": "none|low|medium|high",
  "retrieved_at": "YYYY-MM-DD",
  "original_source_url": "https://...",
  "evidence_excerpt": "Decision-relevant excerpt or structured data note",
  "content_hash": "optional"
}
```

## Claim Schema 1.1 Additions

Each claim must include `claim_type`. Core claims must use only evidence whose `supports_claim_types` contains that type and whose `cannot_support_claim_types` does not contain it.