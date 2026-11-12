import trimesh
import numpy as np

scene = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
baked = scene.to_geometry()
v = baked.vertices

regions = [
    {
        "id": "hampi_elephant_guardians_steps",
        "name": "Entrance Sopana (Stairs) & Flanking Elephant Guardians",
        "box": ([-0.38, 0.00, 0.36], [0.38, 0.62, 0.72])
    },
    {
        "id": "hampi_wheels_front_left",
        "name": "Front Left Monolithic Concentric Wheel & Axle",
        "box": ([-0.65, 0.05, 0.18], [-0.32, 0.72, 0.66])
    },
    {
        "id": "hampi_wheels_front_right",
        "name": "Front Right Monolithic Concentric Wheel & Axle",
        "box": ([0.32, 0.05, 0.18], [0.65, 0.72, 0.66])
    },
    {
        "id": "hampi_wheels_rear_left",
        "name": "Rear Left Monolithic Concentric Wheel & Axle",
        "box": ([-0.65, 0.05, -0.62], [-0.32, 0.72, -0.16])
    },
    {
        "id": "hampi_wheels_rear_right",
        "name": "Rear Right Monolithic Concentric Wheel & Axle",
        "box": ([0.32, 0.05, -0.62], [0.65, 0.72, -0.16])
    },
    {
        "id": "hampi_chariot_plinth_adhisthana",
        "name": "Carved Chariot Platform & Adhisthana Friezes",
        "box": ([-0.48, 0.18, -0.58], [0.48, 0.65, 0.38])
    },
    {
        "id": "hampi_garuda_sanctum_pillars",
        "name": "Pillared Mandapa & Garuda Sanctum Chamber",
        "box": ([-0.46, 0.62, -0.48], [0.46, 1.25, 0.35])
    },
    {
        "id": "hampi_kapota_cornice",
        "name": "Overhanging Carved Cornice (Kapota) & Parapet",
        "box": ([-0.56, 1.18, -0.56], [0.56, 1.38, 0.42])
    },
    {
        "id": "hampi_vimana_superstructure",
        "name": "Stepped Dravidian Vimana Superstructure (Shikhara)",
        "box": ([-0.38, 1.35, 0.18], [0.38, 1.83, 0.70])
    }
]

print("Verifying architectural bounding boxes against mesh vertices:\n")
for reg in regions:
    bmin, bmax = reg["box"]
    mask = (
        (v[:,0] >= bmin[0]) & (v[:,0] <= bmax[0]) &
        (v[:,1] >= bmin[1]) & (v[:,1] <= bmax[1]) &
        (v[:,2] >= bmin[2]) & (v[:,2] <= bmax[2])
    )
    in_pts = v[mask]
    pct = len(in_pts) / len(v) * 100
    print(f"[{reg['id']}] {reg['name']}")
    print(f"   Vertices captured: {len(in_pts):6d} ({pct:4.1f}%)")
    print(f"   Box: X:[{bmin[0]:.2f}, {bmax[0]:.2f}] Y:[{bmin[1]:.2f}, {bmax[1]:.2f}] Z:[{bmin[2]:.2f}, {bmax[2]:.2f}]\n")

