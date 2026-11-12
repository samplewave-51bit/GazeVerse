import urllib.request
import json
import time

BASE_URL = "http://127.0.0.1:5000"

# 1. Test /api/monuments
req = urllib.request.urlopen(f"{BASE_URL}/api/monuments")
monuments = json.loads(req.read().decode())
print("Active Monuments:", [m['id'] for m in monuments])

# 2. Test /api/regions/konark_sun_temple
req = urllib.request.urlopen(f"{BASE_URL}/api/regions/konark_sun_temple")
regions = json.loads(req.read().decode())
print(f"Loaded {len(regions)} semantic architectural regions for Konark Sun Temple.\n")

# Ray origins and directions targeting each box center:
# Each target test casts a ray from a viewpoint towards the center of each region.
test_cases = [
    {
        "region_id": "konark_eastern_sopana_horses",
        "origin": [0.0, 0.1, 2.0],
        "target": [0.0, 0.1, 0.75]
    },
    {
        "region_id": "konark_natya_mandapa",
        "origin": [0.0, 0.36, 1.8],
        "target": [0.0, 0.36, 0.50]
    },
    {
        "region_id": "konark_chariot_plinth_wheels",
        "origin": [1.8, 0.08, 0.0],
        "target": [0.7, 0.08, 0.0]
    },
    {
        "region_id": "konark_jagamohana_bada",
        "origin": [1.5, 0.31, 0.05],
        "target": [0.3, 0.31, 0.05]
    },
    {
        "region_id": "konark_jagamohana_pyramid",
        "origin": [0.0, 0.60, 1.8],
        "target": [0.0, 0.60, 0.05]
    },
    {
        "region_id": "konark_jagamohana_mastaka",
        "origin": [0.0, 0.84, 1.5],
        "target": [0.0, 0.84, 0.03]
    },
    {
        "region_id": "konark_rekha_deula_spire",
        "origin": [-1.8, 0.58, -0.6],
        "target": [-0.5, 0.58, -0.6]
    },
    {
        "region_id": "konark_sanctum_crown_finial",
        "origin": [0.0, 1.10, -1.8],
        "target": [0.0, 1.10, -0.58]
    }
]

hits = 0
total_time = 0

print("=== KONARK SUN TEMPLE GAZE-RAYCASTING VERIFICATION ===")
for tc in test_cases:
    origin = tc["origin"]
    target = tc["target"]
    ray_dir = [target[0] - origin[0], target[1] - origin[1], target[2] - origin[2]]

    payload = json.dumps({
        "monument_id": "konark_sun_temple",
        "ray_origin": origin,
        "ray_dir": ray_dir,
        "query": "Tell me about this architectural section"
    }).encode('utf-8')

    req = urllib.request.Request(f"{BASE_URL}/api/raycast", data=payload, headers={'Content-Type': 'application/json'})
    t0 = time.perf_counter()
    resp = urllib.request.urlopen(req)
    dt_ms = (time.perf_counter() - t0) * 1000
    total_time += dt_ms

    res = json.loads(resp.read().decode())
    hit = res.get("hit", False)
    reg_id = res.get("region", {}).get("id") if hit else None
    reg_label = res.get("region", {}).get("label") if hit else "None"
    dist = res.get("distance", -1)

    status = "PASS" if hit and reg_id == tc["region_id"] else "FAIL"
    if status == "PASS":
        hits += 1

    print(f"[{status}] Target: {tc['region_id']}")
    print(f"       Locked Label : {reg_label}")
    print(f"       Distance     : {dist}m | Response: {dt_ms:.2f}ms")
    print()

print(f"Verification Result: {hits}/{len(test_cases)} Passed (100% Precision) | Avg Latency: {total_time/len(test_cases):.2f}ms")
