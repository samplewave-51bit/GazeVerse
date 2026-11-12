import trimesh
import numpy as np

scene = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
baked = scene.to_geometry()
v = baked.vertices

print(f"Total vertices: {len(v)}")
print(f"World bounds:")
print(f"  X: [{v[:,0].min():.4f}, {v[:,0].max():.4f}]")
print(f"  Y: [{v[:,1].min():.4f}, {v[:,1].max():.4f}]")
print(f"  Z: [{v[:,2].min():.4f}, {v[:,2].max():.4f}]")

# Let's inspect along Y (height slices):
print("\n--- Height profile (Y axis slices from ground Y=0 to top Y=1.83) ---")
for y_low in np.arange(0.0, 1.8, 0.15):
    y_high = y_low + 0.15
    slice_v = v[(v[:,1] >= y_low) & (v[:,1] < y_high)]
    if len(slice_v) > 0:
        print(f"Y [{y_low:.2f} - {y_high:.2f}m]: {len(slice_v):6d} pts | X: [{slice_v[:,0].min():.2f}, {slice_v[:,0].max():.2f}] | Z: [{slice_v[:,2].min():.2f}, {slice_v[:,2].max():.2f}]")

# Let's inspect Z (front-to-back profile):
print("\n--- Depth profile (Z axis slices from back to front) ---")
for z_low in np.arange(v[:,2].min(), v[:,2].max(), 0.15):
    z_high = z_low + 0.15
    slice_v = v[(v[:,2] >= z_low) & (v[:,2] < z_high)]
    if len(slice_v) > 0:
        print(f"Z [{z_low:.2f} - {z_high:.2f}m]: {len(slice_v):6d} pts | Y: [{slice_v[:,1].min():.2f}, {slice_v[:,1].max():.2f}] | X: [{slice_v[:,0].min():.2f}, {slice_v[:,0].max():.2f}]")

# Let's inspect X (left-to-right profile):
print("\n--- Width profile (X axis slices) ---")
for x_low in np.arange(v[:,0].min(), v[:,0].max(), 0.15):
    x_high = x_low + 0.15
    slice_v = v[(v[:,0] >= x_low) & (v[:,0] < x_high)]
    if len(slice_v) > 0:
        print(f"X [{x_low:.2f} - {x_high:.2f}m]: {len(slice_v):6d} pts | Y: [{slice_v[:,1].min():.2f}, {slice_v[:,1].max():.2f}] | Z: [{slice_v[:,2].min():.2f}, {slice_v[:,2].max():.2f}]")
