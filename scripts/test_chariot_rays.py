import urllib.request
import json
import numpy as np

base_url = "http://127.0.0.1:5000"

with open("data/semantics/hampi_stone_chariot_regions.json", "r", encoding="utf-8") as f:
    regions = json.load(f)

print(f"Testing 3D gaze raycasting against all 9 components with new upright model:\n")

success = 0
for idx, reg in enumerate(regions, start=1):
    bmin = np.array(reg["bounds_min"])
    bmax = np.array(reg["bounds_max"])
    center = (bmin + bmax) / 2.0
    
    offset = np.array([0.0, 0.1, 0.0])
    if "steps" in reg["id"]:
        offset[2] = 1.2
    elif "front" in reg["id"]:
        offset[2] = 0.8
        offset[0] = 0.8 if center[0] > 0 else -0.8
    elif "rear" in reg["id"]:
        offset[2] = -0.8
        offset[0] = 0.8 if center[0] > 0 else -0.8
    elif "plinth" in reg["id"]:
        offset[0] = 1.0 # side
    elif "sanctum" in reg["id"]:
        offset[2] = 1.0
    elif "cornice" in reg["id"]:
        offset[2] = -1.0
        offset[1] = 0.2
    elif "vimana" in reg["id"]:
        offset[1] = 0.8
        offset[2] = -0.6

    cam_pos = center + offset
    ray_dir = center - cam_pos
    ray_dir /= np.linalg.norm(ray_dir)

    req_data = json.dumps({
        "monument_id": "hampi_stone_chariot",
        "ray_origin": cam_pos.tolist(),
        "ray_dir": ray_dir.tolist()
    }).encode("utf-8")

    req = urllib.request.Request(
        f"{base_url}/api/raycast",
        data=req_data,
        headers={"Content-Type": "application/json"}
    )
    with urllib.request.urlopen(req) as r:
        res = json.loads(r.read().decode())
        hit_id = res.get("region", {}).get("id")
        dist = res.get("distance")
        is_correct = (hit_id == reg["id"])
        if is_correct:
            success += 1
            print(f"[{idx}/9] PASS: {reg['label'][:42]:42s} -> Locked at {dist:.2f}m")
        else:
            print(f"[{idx}/9] FAIL: Expected {reg['id']}, got {hit_id}")

print(f"\nResult: {success}/9 components passed!")
