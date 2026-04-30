# Investment Banking

AI-powered investment banking assistant covering six core workflows: IPO prospectus drafting, M&A advisory reports, bond offering memoranda, regulatory response to exchange inquiries, roadshow materials, and financial modeling.

> **Disclaimer:** This plugin assists professional workflows and does not replace professional judgment. All outputs should be reviewed by qualified professionals before being used in decision-making.

## Target Users

- **IB Deal Manager** -- End-to-end execution and coordination of IPO / M&A / bond deals
- **Sponsor Representative** -- Registration-based review material oversight and disclosure quality control
- **IB Analyst** -- Working paper preparation, financial modeling, and data analysis
- **Bond Underwriter** -- Offering memorandum drafting and roadshow preparation

## Typical Workflow

```
Financial Modeling --> Prospectus / Bond Offering / M&A Advisory --> Regulatory Response --> Roadshow Materials
  (valuation basis)      (filing documents)                        (review feedback)       (marketing)
```

## Skills

| Skill | Description | Typical Input |
|-------|-------------|---------------|
| prospectus | Generate IPO prospectus chapter drafts per registration-based disclosure rules; adapts to STAR Market / ChiNext / Main Board / BSE | Company info + target board |
| ma-advisory | Generate M&A restructuring report drafts per the Major Asset Restructuring Rules; includes pricing analysis and earnout design | Deal background + target info |
| bond-offering | Generate offering memorandum drafts per exchange / interbank market rules; includes debt-service capacity analysis | Issuer info + bond type |
| regulatory-response | Respond to exchange inquiry letters item-by-item: factual statement + reasonableness analysis + peer comparison + verification opinion | Inquiry letter PDF / Word |
| roadshow-materials | Generate IPO / bond / M&A / follow-on roadshow slide outlines, page-by-page scripts, and Q&A playbooks | Deal info + roadshow type |
| financial-modeling | Build a CAS three-statement linked forecast model with DCF valuation, comps analysis, and sensitivity testing | Historical financial data |

## Quick Commands

| Command | Description |
|---------|-------------|
| `/prospectus` | Provide company info and target board to generate prospectus chapter drafts |
| `/ma-advisory` | Provide deal background and target info to generate an M&A restructuring report draft |
| `/bond-offering` | Provide issuer info and bond type to generate an offering memorandum draft |
| `/regulatory-response` | Upload an inquiry letter to generate item-by-item responses in regulatory format |
| `/roadshow-materials` | Provide deal info and roadshow type to generate a slide outline and script |
| `/financial-modeling` | Upload financials or enter a company name to build a three-statement + DCF model |

## MCP Enhancement

This plugin works standalone and does not require any MCP connectors.
