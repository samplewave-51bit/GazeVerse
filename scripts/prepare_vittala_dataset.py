import os
import shutil
import glob
from pathlib import Path
from PIL import Image

def prepare_vittala():
    raw_dir = Path("data/raw/hampi_vittala/images")
    clean_dir = Path("data/cleaned/hampi_vittala/images")
    
    # Backup/clear old clean_dir
    if clean_dir.exists():
        shutil.rmtree(clean_dir)
    clean_dir.mkdir(parents=True, exist_ok=True)

    manifest_path = Path("data/raw/hampi_vittala/targeted_manifest.json")
    import json
    with open(manifest_path, "r", encoding="utf-8") as f:
        manifest = json.load(f)

    print(f"Processing {len(manifest)} targeted images for Hampi Vittala Mandapa...")
    count = 0
    for idx, item in enumerate(manifest, start=1):
        clean_name = item["title"].replace("File:", "").replace(" ", "_")
        safe_name = "".join(c for c in clean_name if c.isalnum() or c in "._-")
        src_path = raw_dir / safe_name
        
        if not src_path.exists():
            continue

        dest_name = f"vittala_mandapa_{idx:03d}.jpg"
        dest_path = clean_dir / dest_name

        try:
            with Image.open(src_path) as img:
                img = img.convert("RGB")
                w, h = img.size
                max_dim = max(w, h)
                if max_dim > 1600:
                    scale = 1600.0 / max_dim
                    new_w = int(w * scale)
                    new_h = int(h * scale)
                    img = img.resize((new_w, new_h), Image.Resampling.LANCZOS)
                img.save(dest_path, "JPEG", quality=92)
                count += 1
        except Exception as e:
            print(f"Error processing {src_path.name}: {e}")

    print(f"Successfully prepared {count} sanitized, normalized images in {clean_dir}")

if __name__ == "__main__":
    prepare_vittala()

