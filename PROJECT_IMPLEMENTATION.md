# Green Claims Checker — Standalone Real GUI Implementation

This folder is now its own runnable project app. It does not depend on the root all-project dashboard at runtime.

## Run

```bash
./run_gui.sh
```

Windows:

```powershell
.\run_gui_windows.ps1
```

Default URL: `http://127.0.0.1:9125`

## What is inside this project folder

- `app/` — FastAPI backend for this project.
- `static/` — elegant browser GUI.
- `plugins/green-claims-checker.json` — this project’s own feature/customization/input schema.
- `project_config.json` — readable copy of the same project-specific configuration.
- `data/` — local SQLite jobs, uploads, exports.
- `tests/` — verifies this project has a registered real local engine.

## Project-specific scope

- Domain: `ESG / Marketing Compliance`
- Target user: `Domain operator, business owner, analyst, or team member who needs this workflow executed reliably.`
- Core job: Marketing claims → greenwashing risk review
- Suite: `Legal & Compliance Suite`

## Deep features applied

- claim taxonomy
- evidence matching
- certification checker
- vague language detector
- regulatory risk
- safer rewrite
- substantiation checklist

## Customization controls

- `execution_mode` — Execution mode (select)
- `market_jurisdiction` — market/jurisdiction (select)
- `claim_type` — claim type (text)
- `industry` — industry (text)
- `strictness` — strictness (slider)
- `brand_tone` — brand tone (text)
- `evidence_standard` — evidence standard (text)
- `rewrite_style` — rewrite style (select)
- `output_format` — output format (select)
- `language` — language (select)
- `privacy_mode` — privacy mode (select)
- `confidence_threshold` — Confidence threshold (slider)

## Input fields

- `marketing_claims` — Marketing claims (text) required
- `work_brief` — Work brief / source text / URL / instructions (textarea) required

## External data policy

The local deterministic core is real and executable. Live external systems are not simulated. If Shopify, ATS, ERP, OCR/STT, maps, SERP, market data, medical databases, tax/customs databases, or other live systems are required, this project reports the missing connector/API requirement instead of inventing data.

---

## Final UX/UI Layer

This project now uses the **Legal Review Desk** pattern.

**UX workflow:** Document intake → clause map → risk heatmap → negotiation/actions

**Domain components:**
- Clause extraction grid
- Risk heatmap
- Obligation timeline
- Redline/position panel
- Negotiation checklist

**Quick actions:**
- Extract clauses
- Build risk matrix
- Create negotiation points
- Prepare redline checklist

**No fake-data policy:** external/live actions require real connectors or API keys. Missing connectors are reported instead of simulated.
