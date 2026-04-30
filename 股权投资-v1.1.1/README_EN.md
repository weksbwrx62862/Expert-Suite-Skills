# Private Equity

End-to-end PE/VC toolkit covering deal screening, due diligence checklists, term sheet review, investment committee memos, return modeling, and exit analysis.

> **Disclaimer:** This plugin supports professional workflows and does not replace professional advice. All outputs should be reviewed by qualified professionals before being used for decision-making.

## Target Users

- **Investment Managers** -- Core tool for deal screening and due diligence
- **Managing Directors** -- IC material preparation and risk oversight
- **Partners** -- Rapid evaluation of investment opportunities
- **Portfolio Management** -- Exit analysis and return tracking

## Quick Commands

| Command | Description | Typical Input |
|---------|-------------|---------------|
| `/deal-screening` | Rapid BP/CIM screening with a one-page six-dimension scoring memo | Upload a BP or describe the deal |
| `/due-diligence-checklist` | Generate a structured DD checklist (financial / legal / commercial / technical + sector-specific) | Project name + industry + corporate structure |
| `/term-sheet-review` | Clause-by-clause TS/SPA review with PRC compliance checks and negotiation guidance | Upload a Term Sheet or SPA |
| `/investment-memo` | Generate an IC Memo with investment thesis, valuation analysis, and term summary | Project details + DD findings |
| `/return-modeling` | IRR / MOIC / DPI modeling with a 25-cell sensitivity table | Deal terms + exit assumptions |
| `/exit-analysis` | Compare five exit pathways (IPO / M&A / secondary / buyback) with time and cost estimates | Portfolio company status + fund timeline |

## Typical Workflow

```
Source deal -> /deal-screening (quick filter) -> /due-diligence-checklist (launch DD) -> /term-sheet-review (review deal docs)
                                                                                              |
                      /exit-analysis (post-investment) <- /return-modeling (model returns) <- /investment-memo (go to IC)
```

## Connectors (Optional Enhancement)

This plugin works independently and requires no MCP connectors. All features operate on text and files without external dependencies.
