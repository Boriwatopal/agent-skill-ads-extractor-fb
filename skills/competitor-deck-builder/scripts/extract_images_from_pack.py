#!/usr/bin/env python3
"""
Extract individual JPEG images from a <brand>_ads_pack.json
downloaded via the browser image extraction workflow.

Usage:
  python extract_images_from_pack.py <path/to/ads_pack.json> <output_dir>

Example:
  python extract_images_from_pack.py ~/Downloads/brand_ads_pack.json ./ad-images/
"""

import json, base64, os, sys

def extract(json_path, output_dir):
    os.makedirs(output_dir, exist_ok=True)

    with open(json_path, "r") as f:
        data = json.load(f)

    count = 0
    for name, b64 in data.items():
        if not isinstance(b64, str) or b64.startswith("ERROR"):
            print(f"SKIP {name}: {b64}")
            continue
        try:
            img_bytes = base64.b64decode(b64)
        except Exception as e:
            print(f"SKIP {name}: base64 decode error — {e}")
            continue

        out_path = os.path.join(output_dir, name + ".jpg")
        with open(out_path, "wb") as f:
            f.write(img_bytes)
        print(f"✅  {name}.jpg  ({len(img_bytes):,} bytes)")
        count += 1

    print(f"\n✅  Extracted {count}/{len(data)} images to: {output_dir}")
    return count


if __name__ == "__main__":
    if len(sys.argv) < 3:
        print(__doc__)
        sys.exit(1)
    extract(sys.argv[1], sys.argv[2])
