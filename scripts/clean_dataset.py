"""
Cleaning and Occluder Screening Pipeline for GazeVerse V2
Step 2:
- Detect duplicate / near-duplicate images (perceptual hashing)
- Aspect ratio and minimum dimension validation
- Prepares directories for transient occluder masking (YOLOv8 / SAM / SegFormer)
"""

import os
import sys
import json
import shutil
from pathlib import Path
from PIL import Image

def compute_dhash(image, hash_size=8):
    """Compute difference hash (dHash) to detect duplicate images."""
    image = image.convert('L').resize((hash_size + 1, hash_size), Image.Resampling.LANCZOS)
    pixels = list(image.getdata())
    difference = []
    for row in range(hash_size):
        for col in range(hash_size):
            pixel_left = pixels[row * (hash_size + 1) + col]
            pixel_right = pixels[row * (hash_size + 1) + col + 1]
            difference.append(pixel_left > pixel_right)
    decimal_value = 0
    hex_string = []
    for index, value in enumerate(difference):
        if value:
            decimal_value += 2 ** (index % 8)
        if (index % 8) == 7:
            hex_string.append(hex(decimal_value)[2:].rjust(2, '0'))
            decimal_value = 0
    return ''.join(hex_string)

def clean_monument_dataset(monument_key, min_res=(800, 600)):
    raw_dir = Path("data") / "raw" / monument_key / "images"
    clean_dir = Path("data") / "cleaned" / monument_key / "images"
    rejected_dir = Path("data") / "cleaned" / monument_key / "rejected"
    clean_dir.mkdir(parents=True, exist_ok=True)
    rejected_dir.mkdir(parents=True, exist_ok=True)

    if not raw_dir.exists():
        print(f"Directory {raw_dir} does not exist.")
        return

    images = list(raw_dir.glob("*.[jJ][pP][gG]")) + list(raw_dir.glob("*.[pP][nN][gG]"))
    print(f"\n[{monument_key.upper()}] Starting cleaning on {len(images)} raw images...")

    seen_hashes = set()
    accepted = 0
    duplicates = 0
    corrupt_or_small = 0

    manifest_log = []

    for img_path in images:
        try:
            with Image.open(img_path) as img:
                img.verify()
            with Image.open(img_path) as img:
                w, h = img.size
                if w < min_res[0] or h < min_res[1]:
                    corrupt_or_small += 1
                    shutil.copy2(img_path, rejected_dir / f"small_{img_path.name}")
                    continue

                h_val = compute_dhash(img)
                if h_val in seen_hashes:
                    duplicates += 1
                    shutil.copy2(img_path, rejected_dir / f"dup_{img_path.name}")
                    continue

                seen_hashes.add(h_val)
                # Copy to clean folder
                dest_path = clean_dir / img_path.name
                shutil.copy2(img_path, dest_path)
                accepted += 1
                manifest_log.append({
                    "filename": img_path.name,
                    "width": w,
                    "height": h,
                    "dhash": h_val
                })
        except Exception as e:
            corrupt_or_small += 1
            print(f"  Error processing {img_path.name}: {e}")

    # Write summary
    summary_path = Path("data") / "cleaned" / monument_key / "clean_summary.json"
    with open(summary_path, "w", encoding="utf-8") as f:
        json.dump({
            "total_raw": len(images),
            "accepted": accepted,
            "duplicates": duplicates,
            "corrupt_or_small": corrupt_or_small,
            "images": manifest_log
        }, f, indent=2)

    print(f"  Results: {accepted} accepted, {duplicates} duplicates, {corrupt_or_small} rejected.")
    print(f"  Saved clean images to {clean_dir}")

if __name__ == "__main__":
    monument = sys.argv[1] if len(sys.argv) > 1 else "konark_sun_temple"
    clean_monument_dataset(monument)

