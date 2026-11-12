"""
Targeted Ingestion Pipeline for Complete Monument Reconstruction
Strictly adheres to Wikimedia Commons etiquette:
- Polite delay (1.1s)
- Custom academic User-Agent
- Directly targets subcategories for the main temple structures
- Filters out sketches, night photos, documents, and non-architectural noise
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
DELAY_SECONDS = 1.1

CONFIG = {
    "ellora_kailasa": {
        "categories": [
            "Category:Shiva Shikhara and Mandapa, Kailash temple (Ellora)",
            "Category:Nandi Mandapa, Kailash temple (Ellora)",
            "Category:Front external views of Kailash temple (Ellora)",
            "Category:External views of Kailash temple (Ellora) from the edge of the cliff",
            "Category:External views of Kailash temple (Ellora) from the northern front terrace",
            "Category:External views of Kailash temple (Ellora) from the southern front terrace"
        ],
        "exclude_keywords": [
            ".djvu", ".pdf", "daniell", "wales", "sketch", "drawing", "engraving", 
            "costume antico", "oriental scenery", "plan", "map", "postcard", "ticket"
        ],
        "target_limit": 140
    },
    "modhera_sun_temple": {
        "categories": [
            "Category:Sabha Mandap",
            "Category:Guda Mandap",
            "Category:Sun Temple, Modhera"
        ],
        "exclude_keywords": [
            ".djvu", ".pdf", "night", "illuminat", "stereoscopic", "plan", "drawing", 
            "map", "ticket", "notice", "plaque", "stamp", "coin", "diagram"
        ],
        "target_limit": 110
    },
    "hampi_vittala": {
        "categories": [
            "Category:Mahamandapa of the Vittala temple",
            "Category:Kalyana Mandapa of the Vittala Temple",
            "Category:Mandapas of the Vittala Temple"
        ],
        "exclude_keywords": [
            ".djvu", ".pdf", "sketch", "drawing", "engraving", "plan", "map", 
            "ticket", "notice", "stamp", "coin", "diagram", "chariot", "ratha"
        ],
        "target_limit": 75
    }
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

def get_category_files(cat_title):
    files = []
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
            if m.get("ns") == 6:
                files.append(m["title"])
        cmcontinue = data.get("continue", {}).get("cmcontinue")
        if not cmcontinue:
            break
    return files

def get_file_metadata(file_titles):
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
                    "mime": info.get("mime")
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

def ingest(monument_key):
    if monument_key not in CONFIG:
        print(f"Unknown monument {monument_key}")
        return

    cfg = CONFIG[monument_key]
    target_limit = cfg["target_limit"]
    raw_dir = Path("data") / "raw" / monument_key / "images"
    raw_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n=======================================================")
    print(f"TARGETED INGESTION: {monument_key.upper()} (Target: {target_limit})")
    print(f"=======================================================")

    all_files = []
    for cat in cfg["categories"]:
        print(f"Querying subcategory: {cat}")
        files = get_category_files(cat)
        print(f"  Found {len(files)} files.")
        all_files.extend(files)

    all_files = list(dict.fromkeys(all_files))
    print(f"Total unique files collected: {len(all_files)}")

    # Keyword filtering
    filtered_titles = []
    for f in all_files:
        low = f.lower()
        if any(bad in low for bad in cfg["exclude_keywords"]):
            continue
        filtered_titles.append(f)

    print(f"Files after keyword exclusion: {len(filtered_titles)}")

    # Fetch metadata in chunks
    print("Fetching image metadata (resolution, mime, URLs)...")
    meta = get_file_metadata(filtered_titles)

    selected = []
    for m in meta:
        mime = m.get("mime", "")
        w = m.get("width", 0)
        h = m.get("height", 0)
        if mime in ["image/jpeg", "image/png"] and w >= 1000 and h >= 700:
            selected.append(m)
            if len(selected) >= target_limit:
                break

    print(f"Selected {len(selected)} high-resolution, qualified photos.")

    # Save manifest
    manifest_path = Path("data") / "raw" / monument_key / "targeted_manifest.json"
    with open(manifest_path, "w", encoding="utf-8") as f:
        json.dump(selected, f, indent=2)

    # Download
    print(f"\nDownloading {len(selected)} images sequentially...")
    downloaded = 0
    for idx, item in enumerate(selected, start=1):
        clean_name = item["title"].replace("File:", "").replace(" ", "_")
        safe_name = "".join(c for c in clean_name if c.isalnum() or c in "._-")
        target_path = raw_dir / safe_name
        print(f"  [{idx}/{len(selected)}] {safe_name} ({item['width']}x{item['height']})")
        if download_file(item["url"], target_path):
            downloaded += 1

    print(f"\nTargeted Ingestion Complete for {monument_key}: {downloaded} images saved to {raw_dir}")

if __name__ == "__main__":
    if len(sys.argv) > 1:
        ingest(sys.argv[1])
    else:
        for m in ["ellora_kailasa", "modhera_sun_temple"]:
            ingest(m)

