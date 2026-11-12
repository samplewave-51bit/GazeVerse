import trimesh
import numpy as np

scene = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
baked = scene.to_geometry()
v = baked.vertices

center_steps = v[(np.abs(v[:, 0]) < 0.25) & (v[:, 1] < 0.40)]
print("Centerline base points (|X| < 0.25, Y < 0.40):", len(center_steps))
print(f"  Z min: {center_steps[:,2].min():.3f}, Z max: {center_steps[:,2].max():.3f}")

# Check ground level Y < 0.10:
ground_pts = v[v[:, 1] < 0.10]
print("Points touching ground (Y < 0.10m):", len(ground_pts))
print(f"  X: [{ground_pts[:,0].min():.3f}, {ground_pts[:,0].max():.3f}]")
print(f"  Z: [{ground_pts[:,2].min():.3f}, {ground_pts[:,2].max():.3f}]")
neg_ground = ground_pts[ground_pts[:, 2] < 0]
pos_ground = ground_pts[ground_pts[:, 2] > 0]
print(f"  Touching ground at Z < 0: {len(neg_ground)} pts (min Z={neg_ground[:,2].min() if len(neg_ground) else 'none'})")
print(f"  Touching ground at Z > 0: {len(pos_ground)} pts (max Z={pos_ground[:,2].max() if len(pos_ground) else 'none'})")

# Let's inspect the two front elephants:
# The two elephants are located at the front, flanking the entrance staircase.
# Let's see what is at Z < -0.45 vs Z > 0.45 at Y between 0.10 and 0.50:
for z_side, z_label in [(-1, "Z < -0.45 (negative)"), (1, "Z > 0.45 (positive)")]:
    cond = (v[:, 1] > 0.10) & (v[:, 1] < 0.60) & (z_side * v[:, 2] > 0.45) & (np.abs(v[:, 0]) < 0.35)
    pts = v[cond]
    print(f"\nCentral structures at {z_label}: {len(pts)} pts")
    if len(pts) > 0:
        print(f"  X range: [{pts[:,0].min():.3f}, {pts[:,0].max():.3f}]")
        print(f"  Y range: [{pts[:,1].min():.3f}, {pts[:,1].max():.3f}]")
        print(f"  Z range: [{pts[:,2].min():.3f}, {pts[:,2].max():.3f}]")

