import trimesh
import numpy as np

scene = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
baked = scene.to_geometry()
v = baked.vertices

# Let's inspect the two ends of Z:
# Negative Z end: Z in [-0.68, -0.40]
neg_z = v[v[:, 2] < -0.40]
# Positive Z end: Z in [0.40, 0.68]
pos_z = v[v[:, 2] > 0.40]

print("Negative Z region (Z < -0.40m):")
print(f"  Count: {len(neg_z)}")
print(f"  X: [{neg_z[:,0].min():.3f}, {neg_z[:,0].max():.3f}]")
print(f"  Y: [{neg_z[:,1].min():.3f}, {neg_z[:,1].max():.3f}]")
print(f"  Z: [{neg_z[:,2].min():.3f}, {neg_z[:,2].max():.3f}]")

print("\nPositive Z region (Z > 0.40m):")
print(f"  Count: {len(pos_z)}")
print(f"  X: [{pos_z[:,0].min():.3f}, {pos_z[:,0].max():.3f}]")
print(f"  Y: [{pos_z[:,1].min():.3f}, {pos_z[:,1].max():.3f}]")
print(f"  Z: [{pos_z[:,2].min():.3f}, {pos_z[:,2].max():.3f}]")

# Where are the four wheels?
# The 4 wheels are located at left (X < -0.40) and right (X > 0.40) at ground/low Y level (Y < 0.70).
# Two wheels at front Z, two wheels at back Z!
# Let's find the centers of the 4 clusters of wheel points:
wheels_v = v[(v[:, 1] < 0.65) & (np.abs(v[:, 0]) > 0.40)]
print(f"\nWheel vertices (Y < 0.65, |X| > 0.40): {len(wheels_v)}")

for x_side, x_label in [(-1, "Left (-X)"), (1, "Right (+X)")]:
    for z_side, z_label in [(-1, "Z-negative"), (1, "Z-positive")]:
        cond = (v[:, 1] < 0.65) & (x_side * v[:, 0] > 0.40) & (z_side * v[:, 2] > 0.10)
        pts = v[cond]
        if len(pts) > 0:
            print(f"  Wheel {x_label} {z_label}: center=({pts[:,0].mean():.2f}, {pts[:,1].mean():.2f}, {pts[:,2].mean():.2f}), points={len(pts)}")

