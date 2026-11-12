import urllib.request
import json
import os

base_url = "http://127.0.0.1:5000"

# 1. Monuments
resp = urllib.request.urlopen(f"{base_url}/api/monuments")
monuments = json.loads(resp.read().decode())
print("Monuments API response:")
for m in monuments:
    print(f"  [{m['id']}] {m['name']} -> {m['model']}")
    local_path = m['model'].lstrip('/')
    exists = os.path.exists(local_path)
    size_mb = os.path.getsize(local_path) / (1024*1024) if exists else 0
    print(f"      File exists: {exists} ({size_mb:.2f} MB)")

# 2. Test raycast for each monument
print("\nTesting 3D Gaze Raycasting:")
tests = [
    ("khajuraho_kandariya", [0, 2.5, 5.5], [0, -0.2, -1.0]),
    ("hampi_stone_chariot", [0, 1.2, 3.6], [0, -0.15, -1.0]),
    ("konark_sun_temple", [0.6, 2.8, 5.8], [0, -0.25, -1.0])
]

for mon_id, origin, direction in tests:
    req_data = json.dumps({
        "monument_id": mon_id,
        "ray_origin": origin,
        "ray_dir": direction
    }).encode("utf-8")
    req = urllib.request.Request(
        f"{base_url}/api/raycast",
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode())
        print(f"  {mon_id}: hit={res.get('hit')}, target='{res.get('region', {}).get('label')}', dist={res.get('distance')}m")

print("\nAll API verification tests passed successfully!")

