# Ad Analysis PPTX — Generation Guide

This guide documents the exact patterns for building a professional competitor ad analysis deck using **pptxgenjs** (Node.js). These patterns were battle-tested in production and encode important hard-won lessons.

---

## Setup

```bash
cd /your-workspace && npm install pptxgenjs
```

```javascript
const PptxGenJS = require("pptxgenjs");
const fs = require("fs");
const pres = new PptxGenJS();
pres.layout = "LAYOUT_WIDE"; // 13.33 × 7.5 inches
```

---

## Critical: How to Embed Images Correctly

**ALWAYS use base64 `data:` URIs, never file paths.**

File paths (like `/sessions/.../image.png`) work on Linux but break when the PPTX is opened on Windows. The `data:` approach makes the deck self-contained.

```javascript
function imgData(filePath) {
  const ext = filePath.split('.').pop().toLowerCase();
  const mime = (ext === 'jpg' || ext === 'jpeg') ? 'image/jpeg' : 'image/png';
  const data = fs.readFileSync(filePath).toString('base64');
  return `data:${mime};base64,${data}`;
}

// Usage:
slide.addImage({ data: imgData('/path/to/ad.jpg'), x: 0.5, y: 1.2, w: 3.8, h: 3.8 });
```

---

## Critical: How to Add Clickable Hyperlinks on Ad Cards

**NEVER add `hyperlink` directly to `addImage()` — it makes the image go blank.**

Also **NEVER use a transparent overlay shape on top of the image** — even at 100% transparency, it blocks the image from rendering in PowerPoint and LibreOffice.

**The working pattern:** add a visible colored bar ABOVE the image (not on top of it):

```javascript
function adCard(slide, imgPath, x, y, w, h, label, sublabel, labelColor, linkUrl) {
  // Drop shadow
  slide.addShape(pres.shapes.RECTANGLE, {
    x: x + 0.04, y: y + 0.04, w, h,
    fill: { color: "000000", transparency: 88 },
    line: { color: "000000", transparency: 88 }
  });

  // The image — embedded as base64
  slide.addImage({ data: imgData(imgPath), x, y, w, h });

  // Clickable blue bar ABOVE the image (not covering it)
  if (linkUrl) {
    slide.addShape(pres.shapes.RECTANGLE, {
      x, y: y - 0.22, w, h: 0.22,
      fill: { color: "1A56DB" },
      line: { color: "1A56DB" },
      hyperlink: { url: linkUrl, tooltip: "Click to open Facebook Ad Library" }
    });
    slide.addText("🔗  Click to view live ads on Meta Ad Library", {
      x, y: y - 0.22, w, h: 0.22,
      fontSize: 7.5, color: "FFFFFF", align: "center", valign: "middle", margin: 0,
      hyperlink: { url: linkUrl }
    });
  }

  // Label below
  if (label) {
    slide.addText(label, {
      x, y: y + h + 0.06, w, h: 0.22,
      fontSize: 8.5, bold: true, color: labelColor || "333333", align: "center", margin: 0
    });
  }
  if (sublabel) {
    slide.addText(sublabel, {
      x, y: y + h + 0.28, w, h: 0.18,
      fontSize: 7.5, color: "888888", align: "center", margin: 0
    });
  }
  // Text link below card (also clickable)
  if (linkUrl) {
    slide.addText("🔗  View Live Ads on Meta Ad Library  →", {
      x, y: y + h + 0.46, w, h: 0.2,
      fontSize: 7.5, color: "1A56DB", align: "center", underline: true, margin: 0,
      hyperlink: { url: linkUrl, tooltip: "Open in browser" }
    });
  }
}
```

**Why this works:** By positioning the bar at `y - 0.22` (above the image start), it never overlaps the image area, so there is no z-order conflict.

---

## Recommended Slide Structure (15 slides)

| # | Slide | Type | Notes |
|---|-------|------|-------|
| 01 | Title | Dark | Brand name, date, tagline |
| 02 | Executive Summary | Dark | 4-stat dashboard |
| 03 | Brand Architecture | Light | Table: sub-brands, price, positioning |
| 04a | Ad Examples — Luxury/Premium | Dark | 3 real ad images, each card with hyperlink |
| 04b | Ad Examples — Family/Mid-tier | Light | 3 real ad images |
| 04c | Ad Examples — Entry Tier | Light | 2 real images + analysis panel |
| 05 | Key Messaging Themes | Light | 6 themes with icons |
| 06 | Emotional Arc by Tier | Dark | Journey diagram |
| 07 | Creative Format Matrix | Light | Format vs tier grid |
| 08 | CTA Pattern Analysis | Dark | Stats + flow diagram |
| 09 | Pricing Ladder | Light | Horizontal bar chart |
| 10 | Hashtag & Keyword Strategy | Light | Tag cloud |
| 11 | Winning Ad Patterns | Dark | 3-column breakdown |
| 12 | Competitive Gaps | Light | Opportunity matrix |
| 13 | Strategic Recommendations | Dark | 5 numbered actions |
| 14 | Methodology | Light | Data sourcing notes |
| 15 | Thank You / Credits | Dark | |

---

## Ad Example Slide Pattern

For each tier slide, position 3 ad cards side by side:

```javascript
const cardW = 3.8, cardH = 3.8; // square cards match real Facebook ad images (600×600)
const startX = 0.5, gap = 0.42;
const cardY = 1.65; // leave room for title + top bar

const BASE_URL = "https://www.facebook.com/ads/library/?active_status=active&ad_type=all&country=TH&sort_data[mode]=total_impressions&sort_data[direction]=desc&search_type=keyword_unordered&q=";

const cards = [
  { img: "path/to/brand_ad_1.jpg", label: "BrandName", sub: "฿12M • Premium", url: BASE_URL + "BrandName" },
  { img: "path/to/brand_ad_2.jpg", label: "BrandName2", sub: "฿8-12M • Nature", url: BASE_URL + "BrandName2" },
  { img: "path/to/brand_ad_3.jpg", label: "BrandName3", sub: "Portfolio", url: BASE_URL + "BrandName3" },
];

cards.forEach((c, i) => {
  adCard(slide, c.img, startX + i * (cardW + gap), cardY, cardW, cardH, c.label, c.sub, "#CC0000", c.url);
});
```

**Why square cards (3.8 × 3.8)?** Real Facebook ad images from the CDN are 600×600 pixels (square). Using a square card prevents stretching.

---

## Color Palette for Dark/Light Slides

```javascript
const C = {
  dark: "0D1B2A",    // near-black navy background
  navy: "1A2E42",    // section label bg
  white: "FFFFFF",
  text: "1F2937",    // body text on light slides
  orange: "F97316",  // accent / CTA
  amber: "D97706",   // luxury tier
  red: "DC2626",     // Sansiri red / urgent
  green: "059669",   // family / nature
  teal: "0D9488",    // retreat / premium
  blue: "1A56DB",    // links
  purple: "7C3AED",  // expat / premium
  muted: "9CA3AF",   // secondary text on dark
  gray: "6B7280",    // secondary text on light
};
```

---

## Generating the File

```javascript
await pres.writeFile({ fileName: "/path/to/output/Brand_Ads_Analysis.pptx" });
console.log("✅ Done");
```

---

## Verify the Output

```bash
# Quick sanity check — convert to PDF and render slides to JPEG
PYTHONPATH=/path/to/pptx-skill/scripts python3 -c "
from office.soffice import run_soffice
run_soffice(['--headless','--convert-to','pdf','--outdir','/tmp/','/path/to/deck.pptx'],
  capture_output=True, text=True, timeout=120)
"
pdftoppm -r 120 -jpeg -f 4 -l 6 /tmp/deck.pdf /tmp/slide
# Then Read each /tmp/slide-04.jpg etc. to confirm images show correctly
```

If images show as blank black rectangles, check:
1. Are you using `data:` URIs (not `path:`)?
2. Are there any shapes with hyperlinks overlapping the image area?
3. Is the image file actually valid? (`python3 -c "from PIL import Image; Image.open('file.jpg').verify()"`)
