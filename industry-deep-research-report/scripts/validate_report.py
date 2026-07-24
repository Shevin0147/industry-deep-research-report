#!/usr/bin/env python3
"""Validate industry research artifacts with core and conditional evidence packs."""
from __future__ import annotations
import argparse,json,math,re,sys
from datetime import date,datetime
from pathlib import Path

FILES=("brief.json","hypotheses.json","evidence.json","claims.json","model.json")
TARGET={"quick":1,"standard":2,"deep":3}; GOOD={"A","B","C"}; LEVELS=("L1","L2","L3","L4")
PACKS={"consumer-retail","saas-ai","manufacturing","ecommerce-platform","healthcare","restaurant-local-service"}
CLAIMS={"policy_regulation","market_size","demand","product_effectiveness","commercialization","competition","business_model","unit_economics","technical_feasibility","operational_feasibility","risk"}
URL_RE=re.compile(r"https?://[^\s)>\]}]+")
class Results:
 def __init__(self): self.errors=[]; self.warnings=[]
 def error(self,c,m): self.errors.append({"code":c,"message":m})
 def warn(self,c,m): self.warnings.append({"code":c,"message":m})
def filled(v): return v not in (None,"",[],{})
def norm(u): return u.rstrip(".,;:，。；：")
def load(p,r):
 try: d=json.loads(p.read_text(encoding="utf-8-sig"))
 except FileNotFoundError: r.error("missing_artifact",f"Missing {p.name}"); return {}
 except (OSError,json.JSONDecodeError) as e: r.error("invalid_json",f"Cannot read {p.name}: {e}"); return {}
 if not isinstance(d,dict): r.error("invalid_shape",f"{p.name} must be an object"); return {}
 return d
def check_brief(d,mode,r):
 for f in ("topic","scope","geography","time_range","research_goal","decision_questions"):
  if not filled(d.get(f)): r.error("brief_missing_field",f"brief.json missing {f}")
 if d.get("mode") and d["mode"]!=mode: r.warn("mode_mismatch",f"Brief mode {d['mode']} differs from {mode}")
 if isinstance(d.get("decision_questions"),list) and len(d["decision_questions"])<5: r.warn("decision_question_coverage","Fewer than five decision questions")
def route(d,pack_dir,r):
 legacy=str(d.get("schema_version","1.0"))!="1.1"; warnings=[]
 if legacy:
  msg="Legacy schema 1.0: defaulting to L1 and core-only gates"; r.warn("legacy_schema",msg); return "L1",[],[],[msg],True
 requested=str(d.get("decision_level","L1")).upper()
 if requested not in LEVELS: r.error("invalid_decision_level",f"Unknown decision level {requested}"); requested="L1"
 raw=d.get("evidence_packs",[])
 if not isinstance(raw,list): r.error("invalid_evidence_packs","evidence_packs must be an array"); raw=[]
 ids=[str(x) for x in raw]
 if len(ids)>2: r.error("too_many_evidence_packs","At most two evidence packs are allowed")
 if len(set(ids))!=len(ids): r.error("duplicate_evidence_pack","Evidence pack IDs must be unique")
 bad=[x for x in ids if x not in PACKS]
 if bad: r.error("invalid_evidence_pack",f"Unknown evidence packs: {bad}")
 ids=[x for x in ids[:2] if x in PACKS]
 if ids and d.get("industry_family") and d["industry_family"]!=ids[0]: r.error("primary_pack_mismatch","industry_family must match first pack")
 if len(ids)>1 and d.get("secondary_industry_family") and d["secondary_industry_family"]!=ids[1]: r.error("secondary_pack_mismatch","secondary_industry_family must match second pack")
 if not ids: msg="Industry uncertain: universal core only"; warnings.append(msg); r.warn("core_only_routing",msg)
 configs=[]
 for pid in ids:
  try: cfg=json.loads((pack_dir/f"{pid}.json").read_text(encoding="utf-8-sig"))
  except (OSError,json.JSONDecodeError) as e: r.error("pack_load_failure",f"Cannot load {pid}: {e}"); continue
  if cfg.get("id")!=pid: r.error("pack_id_mismatch",f"Pack {pid} has mismatched id")
  else: configs.append(cfg)
 return requested,ids,configs,warnings,False
def check_hypotheses(d,r):
 items=d.get("hypotheses")
 if not isinstance(items,list): r.error("invalid_hypotheses","hypotheses must be an array"); return
 if len(items)<3: r.error("too_few_hypotheses","At least three hypotheses are required")
 selected=0
 for i,x in enumerate(items,1):
  if not isinstance(x,dict): r.error("invalid_hypothesis",f"Hypothesis #{i} must be an object"); continue
  hid=x.get("id",f"#{i}")
  for f in ("statement","expected_evidence","falsifier","status"):
   if not filled(x.get(f)): r.error("hypothesis_missing_field",f"Hypothesis {hid} missing {f}")
  selected+=x.get("status")=="selected"
  if not x.get("counterevidence_ids"): r.warn("hypothesis_no_counterevidence",f"Hypothesis {hid} has no counterevidence")
 if selected!=1: r.error("selected_hypothesis_count",f"Exactly one selected hypothesis required; found {selected}")
def check_evidence(d,r,strict):
 items=d.get("evidence")
 if not isinstance(items,list): r.error("invalid_evidence","evidence must be an array"); return {},set()
 by={}; urls=set(); year=date.today().year
 required=("evidence_categories","supports_claim_types","cannot_support_claim_types","verifiability","conflict_of_interest","retrieved_at","original_source_url","evidence_excerpt")
 for i,x in enumerate(items,1):
  if not isinstance(x,dict): r.error("invalid_evidence_item",f"Evidence #{i} must be object"); continue
  eid=str(x.get("id") or "")
  if not eid: r.error("evidence_missing_id",f"Evidence #{i} missing id"); continue
  if eid in by: r.error("duplicate_evidence_id",f"Duplicate evidence id {eid}")
  by[eid]=x
  if x.get("source_level") not in {"A","B","C","D"}: r.error("invalid_source_level",f"Evidence {eid} invalid source level")
  if x.get("url"): urls.add(norm(str(x["url"])))
  if x.get("is_external_fact",True):
   for f in ("source_title","url","period","scope"):
    if not filled(x.get(f)): r.error("external_fact_missing_metadata",f"Evidence {eid} missing {f}")
  scores=x.get("scores")
  if not isinstance(scores,dict): r.error("missing_evidence_scores",f"Evidence {eid} missing scores")
  else:
   for f in ("authority","originality","recency","scope_fit","independence"):
    v=scores.get(f)
    if not isinstance(v,int) or not 0<=v<=4: r.error("invalid_evidence_score",f"Evidence {eid} score {f} must be 0-4")
  if strict:
   for f in required:
    if f not in x or x[f] in (None,""): r.error("evidence_11_missing_metadata",f"Evidence {eid} missing {f}")
   if x.get("verifiability") not in {"high","medium","low"}: r.error("invalid_verifiability",f"Evidence {eid} invalid verifiability")
   if x.get("conflict_of_interest") not in {"none","low","medium","high"}: r.error("invalid_conflict_of_interest",f"Evidence {eid} invalid conflict_of_interest")
   sup=x.get("supports_claim_types",[]); ban=x.get("cannot_support_claim_types",[]); cats=set(x.get("evidence_categories",[]))
   if not isinstance(sup,list) or any(t not in CLAIMS for t in sup): r.error("invalid_supported_claim_types",f"Evidence {eid} invalid supports_claim_types")
   if not isinstance(ban,list) or any(t not in CLAIMS for t in ban): r.error("invalid_prohibited_claim_types",f"Evidence {eid} invalid cannot_support_claim_types")
   if "official_policy" in cats and {"demand","commercialization"}&set(sup): r.error("policy_source_misuse",f"Policy evidence {eid} cannot establish demand or commercialization")
   if "population_context" in cats and "market_size" in sup: r.error("population_not_market_size",f"Population evidence {eid} cannot establish market size")
   if "trial_registration" in cats and "product_effectiveness" in sup: r.error("trial_registration_not_outcome",f"Trial registration {eid} cannot establish effect")
  m=re.search(r"(19|20)\d{2}",str(x.get("published_at",x.get("period",""))))
  if m and year-int(m.group())>5: r.warn("old_evidence",f"Evidence {eid} is over five years old")
  if not x.get("original_source_id"): r.warn("missing_lineage",f"Evidence {eid} missing original_source_id")
 return by,urls
def check_claims(d,evidence,mode,r,strict):
 items=d.get("claims")
 if not isinstance(items,list) or not items: r.error("invalid_claims","claims must be non-empty array"); return []
 claims=[]
 for i,x in enumerate(items,1):
  if not isinstance(x,dict): r.error("invalid_claim",f"Claim #{i} must be object"); continue
  claims.append(x); cid=x.get("id",f"#{i}"); ids=x.get("support_evidence_ids") or []; ctype=x.get("claim_type")
  if not filled(x.get("statement")): r.error("claim_missing_statement",f"Claim {cid} missing statement")
  missing=[eid for eid in ids if eid not in evidence]
  if missing: r.error("claim_unknown_evidence",f"Claim {cid} references {missing}")
  support=[evidence[eid] for eid in ids if eid in evidence]
  if strict:
   if ctype not in CLAIMS: r.error("invalid_claim_type",f"Claim {cid} invalid claim_type")
   for ev in support:
    if ctype in ev.get("cannot_support_claim_types",[]): r.error("prohibited_evidence_use",f"Evidence {ev.get('id')} prohibited for {ctype}")
    if ctype not in ev.get("supports_claim_types",[]): r.error("unsupported_evidence_use",f"Evidence {ev.get('id')} does not support {ctype}")
  if x.get("core",False):
   if not any(ev.get("source_level") in GOOD for ev in support): r.error("core_claim_no_qualifying_evidence",f"Core claim {cid} lacks A/B/C evidence")
   roots={str(ev.get("original_source_id") or ev.get("id")) for ev in support}
   if len(roots)<TARGET[mode]: r.warn("independent_source_target",f"Claim {cid} has {len(roots)} independent sources; target {TARGET[mode]}")
   for f in ("valid_if","falsified_if"):
    if not x.get(f): r.error("claim_missing_conditions",f"Core claim {cid} missing {f}")
   if not x.get("counterevidence_ids"): r.warn("claim_no_counterevidence",f"Core claim {cid} has no counterevidence")
  if x.get("confidence") not in {"high","medium","low"}: r.error("invalid_claim_confidence",f"Claim {cid} invalid confidence")
 return claims
def gaps(req,claims,evidence):
 relevant=[c for c in claims if c.get("core",False) and c.get("claim_type")==req.get("claim_type")]; support=[]
 for c in relevant: support += [evidence[e] for e in c.get("support_evidence_ids",[]) if e in evidence]
 roots={str(e.get("original_source_id") or e.get("id")) for e in support}; cats={c for e in support for c in e.get("evidence_categories",[])}; out=[]
 if not relevant: out.append(f"no core {req.get('claim_type')} claim")
 minimum=int(req.get("min_independent_sources",1))
 if len(roots)<minimum: out.append(f"{len(roots)}/{minimum} independent sources")
 for group in req.get("required_category_groups",[]):
  if not cats.intersection(group): out.append(f"category group {group}")
 if req.get("disallow_company_only") and support and not any("company_disclosure" not in e.get("evidence_categories",[]) for e in support): out.append("independent non-company evidence")
 return out
def decision_gate(requested,configs,claims,evidence,r):
 if not configs: return "L1",[]
 missing={}
 for level in LEVELS:
  arr=[]
  for cfg in configs:
   for req in cfg.get("requirements_by_level",{}).get(level,[]):
    gs=gaps(req,claims,evidence)
    if gs: arr.append({"pack":cfg["id"],"level":level,"requirement_id":req.get("id"),"claim_type":req.get("claim_type"),"description":req.get("description"),"gaps":gs})
  missing[level]=arr
 supported="L1"
 for level in LEVELS[1:]:
  if missing[level]: break
  supported=level
 if requested=="L1":
  for x in missing["L1"]: r.warn("industry_evidence_gap",f"{x['pack']}/{x['requirement_id']}: {x['gaps']}")
 elif LEVELS.index(supported)<LEVELS.index(requested): r.error("decision_level_not_supported",f"Requested {requested}, current evidence supports at most {supported}")
 return supported,missing.get(requested,[])
def calculate(op,vals):
 if not vals: raise ValueError("empty operands")
 if op=="add": return sum(vals)
 if op=="multiply": return math.prod(vals)
 result=vals[0]
 for v in vals[1:]: result=result-v if op=="subtract" else result/v if op=="divide" else (_ for _ in ()).throw(ValueError(f"unsupported operation {op}"))
 return result
def check_model(d,evidence,r):
 sizing=d.get("market_sizing")
 if not isinstance(sizing,dict): r.error("missing_market_sizing","model missing market_sizing")
 else:
  for method in ("top_down","bottom_up"):
   block=sizing.get(method)
   if not isinstance(block,dict): r.warn("missing_sizing_method",f"Missing {method}"); continue
   if not block.get("formula") and not block.get("limitations"): r.error("sizing_formula_missing",f"{method} lacks formula or limitation")
   for x in block.get("inputs",[]):
    if isinstance(x,dict) and x.get("kind")=="external_fact" and x.get("evidence_id") not in evidence: r.error("model_input_missing_evidence",f"Input {x.get('name')} lacks evidence")
    if isinstance(x,dict) and x.get("kind")=="internal_assumption" and x.get("evidence_id"): r.warn("assumption_has_evidence_id",f"Assumption {x.get('name')} has evidence_id")
  if not sizing.get("som_constraints"): r.warn("missing_som_constraints","No SOM constraints recorded")
 names={str(x.get("name")) for x in d.get("scenarios",[]) if isinstance(x,dict)}; miss={"downside","base","upside"}-names
 if miss: r.warn("missing_scenarios",f"Missing scenarios: {sorted(miss)}")
 if len(d.get("sensitivity",[]))<3: r.warn("limited_sensitivity","Fewer than three sensitivity variables")
 if not d.get("break_even"): r.warn("missing_break_even","No break-even analysis")
 for x in d.get("calculations",[]):
  cid=x.get("id","unknown") if isinstance(x,dict) else "unknown"
  try:
   expected=calculate(str(x["operation"]),[float(v) for v in x["operands"]]); reported=float(x["reported_result"]); tol=float(x.get("tolerance",.01))
   if not math.isclose(expected,reported,rel_tol=tol,abs_tol=tol): r.error("calculation_mismatch",f"Calculation {cid}: expected {expected}, reported {reported}")
  except (KeyError,TypeError,ValueError,ZeroDivisionError) as e: r.error("invalid_calculation",f"Calculation {cid}: {e}")
def check_report(text,urls,r):
 low=text.lower(); groups={"entry judgment":("是否建议进入","建议进入","不建议进入","validate first"),"biggest risk":("最大风险","主要风险","biggest risk"),"validation path":("验证路径","第一阶段验证","30 天验证","30天验证","validation path")}
 for label,terms in groups.items():
  if not any(t.lower() in low for t in terms): r.error("report_missing_decision_answer",f"Report missing {label}")
 body=text.split("## 附录",1)[0]; sections=len(re.findall(r"^##\s+",body,re.M))
 if sections>10: r.error("too_many_body_sections",f"Report body has {sections} sections")
 visuals=len(re.findall(r"```(?:mermaid|svg|html)",body,re.I))+len(re.findall(r"^\|.+\|\s*$",body,re.M))//3
 if visuals<4: r.warn("visualization_count",f"Detected about {visuals} visualizations")
 missing=sorted({norm(u) for u in URL_RE.findall(text)}-urls)
 if missing: r.error("unregistered_report_url",f"Report URLs absent from evidence: {missing[:10]}")
def main():
 ap=argparse.ArgumentParser(); ap.add_argument("--report",required=True,type=Path); ap.add_argument("--research-dir",required=True,type=Path); ap.add_argument("--mode",choices=tuple(TARGET),default="standard"); a=ap.parse_args(); r=Results()
 try: text=a.report.read_text(encoding="utf-8-sig")
 except OSError as e: r.error("report_unreadable",str(e)); text=""
 data={f:load(a.research_dir/f,r) for f in FILES}; check_brief(data["brief.json"],a.mode,r)
 requested,packs,configs,routing_warnings,legacy=route(data["brief.json"],Path(__file__).resolve().parent.parent/"references"/"industry-packs",r)
 check_hypotheses(data["hypotheses.json"],r); evidence,urls=check_evidence(data["evidence.json"],r,not legacy); claims=check_claims(data["claims.json"],evidence,a.mode,r,not legacy)
 supported,missing=decision_gate(requested,configs,claims,evidence,r); check_model(data["model.json"],evidence,r)
 if text: check_report(text,urls,r)
 payload={"schema_version":"1.1","validated_at":datetime.now().astimezone().isoformat(timespec="seconds"),"mode":a.mode,"report":str(a.report.resolve()),"requested_decision_level":requested,"supported_decision_level":supported,"loaded_packs":packs,"routing_warnings":routing_warnings,"missing_evidence":missing,"status":"blocked" if r.errors else "passed_with_warnings" if r.warnings else "passed","errors":r.errors,"warnings":r.warnings,"summary":{"blocking_errors":len(r.errors),"warnings":len(r.warnings)}}
 a.research_dir.mkdir(parents=True,exist_ok=True); (a.research_dir/"validation.json").write_text(json.dumps(payload,ensure_ascii=False,indent=2)+"\n",encoding="utf-8"); print(json.dumps(payload,ensure_ascii=False,indent=2)); return 1 if r.errors else 0
if __name__=="__main__": sys.exit(main())