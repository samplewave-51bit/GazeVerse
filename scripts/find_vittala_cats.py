import urllib.request
import urllib.parse
import json

USER_AGENT = "GazeVerseResearchBot/1.0 (ISMAR 2027 Academic Research; contact: research-gazeverse@gmail.com)"
BASE_API = "https://commons.wikimedia.org/w/api.php"

def count_files(cat):
    params = {
        "action": "query",
        "list": "categorymembers",
        "cmtitle": cat,
        "cmtype": "file",
        "cmlimit": "500",
        "format": "json"
    }
    url = f"{BASE_API}?{urllib.parse.urlencode(params)}"
    req = urllib.request.Request(url, headers={"User-Agent": USER_AGENT})
    with urllib.request.urlopen(req) as resp:
        data = json.loads(resp.read().decode())
        members = data.get("query", {}).get("categorymembers", [])
        print(f"{cat}: {len(members)} files")
        return [m["title"] for m in members]

count_files("Category:Mahamandapa of the Vittala temple")
count_files("Category:Kalyana Mandapa of the Vittala Temple")
count_files("Category:Mandapas of the Vittala Temple")
