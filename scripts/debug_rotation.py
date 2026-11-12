import trimesh
import numpy as np

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_geom = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v_raw = raw_geom.vertices

print("RAW model.glb:")
print("X bounds:", v_raw[:, 0].min(), v_raw[:, 0].max())
print("Y bounds:", v_raw[:, 1].min(), v_raw[:, 1].max())
print("Z bounds:", v_raw[:, 2].min(), v_raw[:, 2].max())

# In export_upright_glb.py, we rotated by -90 around X:
# x' = x, y' = z, z' = -y
# And the user sees: "the top is to the left side now"
# If in the viewer (Three.js world):
# The top is currently to the LEFT (-X),
# that means the top has negative X!
# Let's check which end has the top in the current static/models/hampi_stone_chariot_upright.glb!
upright = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
baked = upright.to_geometry() if isinstance(upright, trimesh.Scene) else upright
v_cur = baked.vertices

print("\nCURRENT upright model:")
print("X bounds:", v_cur[:, 0].min(), v_cur[:, 0].max())
print("Y bounds:", v_cur[:, 1].min(), v_cur[:, 1].max())
print("Z bounds:", v_cur[:, 2].min(), v_cur[:, 2].max())

# Where is the narrowest, pointy part of the model (the spire/top)?
# Let's find the point with the highest density of vertices that has the smallest radius:
# In the current model, let's check slices along X, Y, and Z:
print("\nChecking which axis actually has the SPIRE (narrowest cross-section):")
for axis, name in enumerate(['X', 'Y', 'Z']):
    # Check extremes of this axis
    min_val, max_val = v_cur[:, axis].min(), v_cur[:, axis].max()
    low_10 = v_cur[v_cur[:, axis] < (min_val + 0.10 * (max_val - min_val))]
    high_10 = v_cur[v_cur[:, axis] > (max_val - 0.10 * (max_val - min_val))]
    
    other_axes = [i for i in range(3) if i != axis]
    low_area = (low_10[:, other_axes[0]].max() - low_10[:, other_axes[0]].min()) * (low_10[:, other_axes[1]].max() - low_10[:, other_axes[1]].min())
    high_area = (high_10[:, other_axes[0]].max() - high_10[:, other_axes[0]].min()) * (high_10[:, other_axes[1]].max() - high_10[:, other_axes[1]].min())
    print(f"Axis {name}: min={min_val:.3f}, max={max_val:.3f} | Low 10% cross-section={low_area:.4f}, High 10% cross-section={high_area:.4f}")

