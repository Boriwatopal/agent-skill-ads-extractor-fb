# Competitor Deck Builder - Agent Skill

Full end-to-end competitive intelligence skill: navigates Facebook Ad Library, extracts real ad copy and images, builds a professional PowerPoint deck with embedded creatives, clickable Meta Ad Library links, and strategic analysis.

## Folder Structure

```
skills/competitor-deck-builder/
  SKILL.md                          # Full 11-step workflow
  scripts/
    extract_images_from_pack.py     # Extracts JPEGs from JSON pack
  references/
    pptx_deck_guide.md              # pptxgenjs API reference & gotchas
README.md
```

## Trigger Phrases

- "Build a competitor deck for [brand]"
- "Analyze competitor ads and make a PPTX"
- "What ads is [brand] running?"
- "Pull Facebook ads and create slides"

## Key Features

- Real ad creatives (fetched from Facebook CDN via browser, btoa-encoded, packed into JSON)
- Clickable blue link bars on each ad card (link above image, never overlapping)
- 12-15 slide deck: exec summary, brand architecture, ad examples by tier, messaging themes, CTA patterns, pricing ladder, competitive gaps, recommendations
- Self-contained PPTX (all images embedded as base64 data: URIs - works on Windows)

## Critical Gotchas

1. Use `data:` URIs not file paths - file paths break on Windows
2. Never `hyperlink` on `addImage()` - images render as black rectangles
3. Never overlay shapes on images - even transparent shapes block rendering
4. Single JSON pack only - Chrome drops multiple rapid downloads silently

## Example Output

See `/examples/` - Thailand Real Estate Ad Intelligence 2026: 13 brands, ~200 ads analyzed, 12-slide deck with real embedded creatives.

## Requirements

- Python 3.6+, Node.js 14+, pptxgenjs
- Chrome with MCP support
- Meta Ad Library access (public)

---
**Version:** 1.0 | **Updated:** March 2026 | **Status:** Production-Ready
