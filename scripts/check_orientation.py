import trimesh
import numpy as np

scene = trimesh.load('stone-chariot-in-hampi/source/model.glb')
geom = list(scene.geometry.values())[0]
v = geom.vertices

print("Vertices shape:", v.shape)
print("X percentiles [1, 50, 99]:", np.percentile(v[:, 0], [1, 50, 99]))
print("Y percentiles [1, 50, 99]:", np.percentile(v[:, 1], [1, 50, 99]))
print("Z percentiles [1, 50, 99]:", np.percentile(v[:, 2], [1, 50, 99]))

# Check cross-sectional area at both ends of each axis to find which end tapers (spire) vs wide (base)
for axis, name in enumerate(['X', 'Y', 'Z']):
    min_val, max_val = v[:, axis].min(), v[:, axis].max()
    low_pts = v[v[:, axis] < (min_val + 0.15 * (max_val - min_val))]
    high_pts = v[v[:, axis] > (max_val - 0.15 * (max_val - min_val))]
    
    other_axes = [i for i in range(3) if i != axis]
    low_spread = np.std(low_pts[:, other_axes], axis=0).prod()
    high_spread = np.std(high_pts[:, other_axes], axis=0).prod()
    print(f"Axis {name}: Low end spread={low_spread:.4f}, High end spread={high_spread:.4f}")

