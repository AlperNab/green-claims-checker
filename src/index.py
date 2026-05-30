#!/usr/bin/env python3
"""
green-claims-checker — marketing copy → greenwashing risk score
Detects vague claims, unsubstantiated statistics, misleading certifications,
hidden trade-offs, FTC Green Guides violations, EU Green Claims Directive issues
"""
import anthropic, json, re, sys, urllib.request
from pathlib import Path

SYSTEM = """You are a sustainability marketing compliance specialist and environmental lawyer.
Analyze this marketing copy for greenwashing — misleading or unsubstantiated environmental claims.

Reference frameworks:
- FTC Green Guides (US) — 16 CFR Part 260
- EU Green Claims Directive (2024)
- UK CMA Green Claims Code
- ASA (UK Advertising Standards) guidelines

Return ONLY valid JSON — no markdown, no explanation.

{
  "brand": "company/product name if detectable",
  "greenwashing_risk_score": number_0_to_100,
  "risk_level": "low|medium|high|critical",
  "verdict": "credible|needs_improvement|misleading|deceptive",
  "claims_analyzed": [
    {
      "claim": "exact quote from the copy",
      "claim_type": "vague|unqualified|misleading|comparative|certification|carbon|biodegradable|recyclable|natural|sustainable|other",
      "greenwashing_risk": "low|medium|high|critical",
      "issue": "what's wrong with this claim",
      "legal_risk": {
        "ftc_issue": "string or null",
        "eu_directive_issue": "string or null",
        "uk_cma_issue": "string or null"
      },
      "evidence_required": "what substantiation would be needed",
      "improved_version": "how to rewrite this claim honestly"
    }
  ],
  "positive_practices": ["things done right in the copy"],
  "most_problematic_claims": ["top 3 highest-risk claims"],
  "missing_disclosures": ["important context the consumer needs that's absent"],
  "hidden_trade_offs": ["environmental costs downplayed or omitted"],
  "certification_analysis": [
    {
      "certification": "name",
      "legitimate": true_or_false,
      "scope": "what it actually certifies",
      "misused": true_or_false
    }
  ],
  "regulatory_exposure": {
    "ftc_action_risk": "low|medium|high",
    "eu_action_risk": "low|medium|high",
    "uk_action_risk": "low|medium|high",
    "class_action_risk": "low|medium|high"
  },
  "recommendations": [
    {
      "priority": "immediate|soon|optional",
      "action": "specific change to make",
      "rationale": "why this reduces risk"
    }
  ],
  "honest_rewrite_summary": "2-3 sentence honest version of the core environmental message",
  "confidence": 0.0
}"""

def check(source: str) -> dict:
    client = anthropic.Anthropic()
    if source.startswith("http"):
        try:
            req = urllib.request.Request(source, headers={"User-Agent":"green-claims-checker/1.0"})
            html = urllib.request.urlopen(req, timeout=12).read().decode("utf-8",errors="replace")
            text = re.sub(r'<[^>]+>',' ',re.sub(r'<script[^>]*>[\s\S]*?</script>','',html,flags=re.I))
            text = re.sub(r'\s+',' ',text).strip()[:20000]
            prompt = f"URL: {source}\n\nContent:\n{text}"
        except Exception as e:
            prompt = f"URL: {source}\n[Could not fetch: {e}]\nAnalyze the URL itself for green claims."
    elif Path(source).exists():
        prompt = Path(source).read_text(encoding="utf-8",errors="replace")[:20000]
    else:
        prompt = source[:20000]

    resp = client.messages.create(
        model="claude-sonnet-4-20250514", max_tokens=3000, system=SYSTEM,
        messages=[{"role":"user","content":f"Check for greenwashing:\n\n{prompt}"}]
    )
    raw = re.sub(r'^```(?:json)?\s*','',resp.content[0].text.strip(),flags=re.MULTILINE)
    raw = re.sub(r'\s*```$','',raw,flags=re.MULTILINE)
    return json.loads(raw)

RISK_C = {"low":"\033[92m","medium":"\033[93m","high":"\033[91m","critical":"\033[91m"}
RISK_ICON = {"low":"🟢","medium":"🟡","high":"🔴","critical":"💀"}
R = "\033[0m"

def print_report(r: dict):
    score = r.get("greenwashing_risk_score",0)
    risk = r.get("risk_level","medium")
    verdict = r.get("verdict","needs_improvement")
    print(f"\n{'═'*60}")
    print(f"  GREEN CLAIMS CHECKER — {r.get('brand','?')}")
    print(f"  Risk: {RISK_ICON.get(risk,'')} {RISK_C.get(risk,'')}{risk.upper()}{R} ({score}/100)")
    print(f"  Verdict: {verdict.upper().replace('_',' ')}")
    print(f"{'═'*60}")

    claims = r.get("claims_analyzed",[])
    if claims:
        sorted_claims = sorted(claims, key=lambda x: ["critical","high","medium","low"].index(x.get("greenwashing_risk","low")))
        print(f"\n  CLAIMS ANALYZED ({len(claims)})")
        for c in sorted_claims:
            cr = c.get("greenwashing_risk","low")
            print(f"\n  {RISK_ICON.get(cr,'')} \"{c.get('claim','')[:70]}\"")
            print(f"     Issue: {c.get('issue','')}")
            legal = c.get("legal_risk",{})
            for framework, issue in [("FTC",legal.get("ftc_issue")),("EU",legal.get("eu_directive_issue")),("UK",legal.get("uk_cma_issue"))]:
                if issue: print(f"     {framework}: {issue}")
            if c.get("improved_version"): print(f"     Better: \"{c['improved_version'][:80]}\"")

    hidden = r.get("hidden_trade_offs",[])
    if hidden:
        print(f"\n  HIDDEN TRADE-OFFS")
        for h in hidden: print(f"  ⚠ {h}")

    missing = r.get("missing_disclosures",[])
    if missing:
        print(f"\n  MISSING DISCLOSURES")
        for m in missing: print(f"  ○ {m}")

    reg = r.get("regulatory_exposure",{})
    print(f"\n  REGULATORY RISK")
    print(f"  FTC: {reg.get('ftc_action_risk','?')} | EU: {reg.get('eu_action_risk','?')} | UK: {reg.get('uk_action_risk','?')} | Class action: {reg.get('class_action_risk','?')}")

    recs = r.get("recommendations",[])
    immediate = [rc for rc in recs if rc.get("priority")=="immediate"]
    if immediate:
        print(f"\n  IMMEDIATE ACTIONS")
        for rc in immediate: print(f"  ⚡ {rc.get('action','')}")

    if r.get("honest_rewrite_summary"):
        print(f"\n  HONEST VERSION\n  \"{r['honest_rewrite_summary']}\"")

    positive = r.get("positive_practices",[])
    if positive: print(f"\n  ✅ Done right: {', '.join(positive[:3])}")
    print(f"\n  Confidence: {int(r.get('confidence',0)*100)}%")
    print(f"{'═'*60}\n")

if __name__ == "__main__":
    if len(sys.argv)<2: print("Usage: python -m green_claims_checker <url|file|text> [--json]"); sys.exit(0)
    src = sys.argv[1] if sys.argv[1]!="-" else sys.stdin.read()
    r = check(src if not Path(src).exists() or src.startswith("http") else Path(src).read_text())
    if "--json" in sys.argv: print(json.dumps(r,indent=2,ensure_ascii=False))
    else: print_report(r)
