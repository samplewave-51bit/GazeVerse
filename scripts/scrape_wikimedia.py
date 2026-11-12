"""
Wikimedia Commons Ingestion Script for GazeVerse V2
Strictly complies with Wikimedia User-Agent and Rate Limiting policies:
- One request at a time (sequential)
- Polite interval delay between calls (1.0 - 1.5s)
- Custom informative User-Agent
- Organized folder structure preserving metadata and licenses
"""

import os
import sys
import time
import json
import urllib.request
import urllib.parse
from pathlib import Path

USER_AGENT = "GazeVerseResearchBot/1.0 (ISMAR 2027 Academic Research; contact: research-gazeverse@gmail.com)"
BASE_API = "https://commons.wikimedia.org/w/api.php"
DELAY_SECONDS = 1.2  # Sequential etiquette

MONUMENT_CATEGORIES = {
    "konark_sun_temple": [
        "Category:Konark Sun Temple"
    ],
    "hampi_vittala": [
        "Category:Vittala Temple"
    ],
    "hampi_stone_chariot": [
        "Category:Kallina Ratha"
    ],
    "khajuraho_kandariya": [
        "Category:Kandariya Mahadeva Temple"
    ],
    "modhera_sun_temple": [
        "Category:Sun Temple, Modhera"
    ],
    "khajuraho_group": [
        "Category:Khajuraho group of monuments"
    ],
    "ellora_kailasa": [
        "Category:Kailasa Temple, Ellora"
    ]
}

def api_get(params):
    params["format"] = "json"
    url = f"{BASE_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            data = json.loads(resp.read().decode("utf-8"))
            time.sleep(DELAY_SECONDS)
            return data
    except Exception as e:
        print(f"API Error ({url[:80]}...): {e}")
        time.sleep(DELAY_SECONDS * 2)
        return None

def get_category_files_and_subcats(cat_title):
    """Fetch files and immediate subcategories in a category."""
    files = []
    subcats = []
    cmcontinue = None

    while True:
        params = {
            "action": "query",
            "list": "categorymembers",
            "cmtitle": cat_title,
            "cmlimit": "100"
        }
        if cmcontinue:
            params["cmcontinue"] = cmcontinue

        data = api_get(params)
        if not data:
            break

        members = data.get("query", {}).get("categorymembers", [])
        for m in members:
            ns = m.get("ns")
            if ns == 6:  # File
                files.append(m["title"])
            elif ns == 14:  # Subcategory
                subcats.append(m["title"])

        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break

    return files, subcats

def get_file_metadata(file_titles):
    """Retrieve direct image URLs, dimensions, MIME, and license info for files (up to 40 at once)."""
    meta_results = []
    chunk_size = 40
    for i in range(0, len(file_titles), chunk_size):
        chunk = file_titles[i:i + chunk_size]
        params = {
            "action": "query",
            "titles": "|".join(chunk),
            "prop": "imageinfo",
            "iiprop": "url|size|mime|extmetadata",
            "formatversion": "2"
        }
        data = api_get(params)
        if not data:
            continue

        pages = data.get("query", {}).get("pages", [])
        for p in pages:
            if "imageinfo" in p and len(p["imageinfo"]) > 0:
                info = p["imageinfo"][0]
                meta_results.append({
                    "title": p.get("title"),
                    "url": info.get("url"),
                    "descriptionurl": info.get("descriptionurl"),
                    "width": info.get("width"),
                    "height": info.get("height"),
                    "size_bytes": info.get("size"),
                    "mime": info.get("mime"),
                    "extmetadata": info.get("extmetadata", {})
                })
    return meta_results

def download_file(url, out_path):
    if os.path.exists(out_path) and os.path.getsize(out_path) > 0:
        return True
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    try:
        with urllib.request.urlopen(req, timeout=45) as resp:
            content = resp.read()
            with open(out_path, "wb") as f:
                f.write(content)
        time.sleep(DELAY_SECONDS)
        return True
    except Exception as e:
        print(f"Failed to download {url}: {e}")
        time.sleep(DELAY_SECONDS)
        return False

def scrape_monument(monument_key, categories, target_limit=50):
    """Scrapes candidate images for a given monument pilot."""
    base_dir = Path("data") / "raw" / monument_key
    images_dir = base_dir / "images"
    meta_dir = base_dir / "metadata"
    images_dir.mkdir(parents=True, exist_ok=True)
    meta_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n[{monument_key.upper()}] Starting scraping up to {target_limit} images...")
    
    all_files = []
    for cat in categories:
        print(f"  Listing files in: {cat}")
        files, subcats = get_category_files_and_subcats(cat)
        print(f"    Found {len(files)} direct files, {len(subcats)} subcategories.")
        all_files.extend(files)
        
        # If we need more files and direct files are few, check immediate top subcategories
        if len(all_files) < target_limit and subcats:
            for sc in subcats[:3]:
                print(f"    Checking subcategory: {sc}")
                sc_files, _ = get_category_files_and_subcats(sc)
                all_files.extend(sc_files)
                if len(all_files) >= target_limit * 2:
                    break

    # De-duplicate
    all_files = list(dict.fromkeys(all_files))
    print(f"  Total unique candidate files found: {len(all_files)}")

    # Fetch metadata for candidates in chunks until we reach target_limit valid photos
    selected = []
    chunk_size = 40
    for i in range(0, len(all_files), chunk_size):
        if len(selected) >= target_limit:
            break
        chunk = all_files[i:i + chunk_size]
        meta = get_file_metadata(chunk)
        for m in meta:
            mime = m.get("mime", "")
            w = m.get("width", 0)
            h = m.get("height", 0)
            title = m.get("title", "").lower()
            
            # Simple keyword rejection for obvious non-reconstruction elements
            if any(bad in title for bad in ["notice", "ticket", "board", "plaque", "map", "plan"]):
                continue

            if mime in ["image/jpeg", "image/png", "image/webp"] and w >= 800 and h >= 600:
                selected.append(m)
                if len(selected) >= target_limit:
                    break

    print(f"  Valid photo candidates selected: {len(selected)}")

    # Save manifest
    manifest_path = meta_dir / "manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(selected, f, indent=2)
    print(f"  Saved metadata manifest ({len(selected)} entries) to {manifest_path}")

    # Download images sequentially
    downloaded = 0
    for idx, item in enumerate(selected, start=1):
        clean_name = item["title"].replace("File:", "").replace(" ", "_")
        # Keep filename safe on Windows
        safe_name = "".join(c for c in clean_name if c.isalnum() or c in "._-")
        target_path = images_dir / safe_name
        print(f"  [{idx}/{len(selected)}] Downloading: {safe_name}")
        if download_file(item["url"], target_path):
            downloaded += 1

    print(f"[{monument_key.upper()}] Ingestion complete: {downloaded} images saved to {images_dir}\n")

if __name__ == "__main__":
    monument = sys.argv[1] if len(sys.argv) > 1 else "konark_sun_temple"
    limit = int(sys.argv[2]) if len(sys.argv) > 2 else 30
    if monument in MONUMENT_CATEGORIES:
        scrape_monument(monument, MONUMENT_CATEGORIES[monument], target_limit=limit)
    else:
        print(f"Unknown monument {monument}. Choose from: {list(MONUMENT_CATEGORIES.keys())}")

