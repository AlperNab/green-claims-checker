# green-claims-checker

> **Marketing copy or URL → greenwashing risk score.** Flags vague claims, unsubstantiated statistics, FTC Green Guides violations, EU Green Claims Directive issues, hidden trade-offs.

[![PyPI](https://img.shields.io/pypi/v/green-claims-checker?style=flat)](https://pypi.org/project/green-claims-checker/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

## Quickstart

```bash
pip install green-claims-checker
python -m green_claims_checker https://brand.com/sustainability
python -m green_claims_checker marketing_copy.txt --json
echo "Our products are 100% sustainable and eco-friendly" | python -m green_claims_checker -
```

Flags: vague terms (eco-friendly, natural, green, sustainable without definition) ·
Unverifiable statistics · Misleading certifications · Hidden trade-offs ·
FTC/EU/UK regulatory exposure assessment
