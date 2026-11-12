import trimesh
import numpy as np

# Load original RAW model.glb
raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_geom = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v = raw_geom.vertices.copy()

print("Original raw vertices shape:", v.shape)

# Let's find:
# 1. Spire tip: In the original model, where is the spire tip?
# We know the spire has the narrowest cross section and smallest radius.
# Let's find which point in the original model is the spire tip!

# Also in the original model:
# The ground points (points that touch the ground):
# In the original model, 4 wheels touch the ground.
# A flat plane of wheels/ground!

# Let's test the 6 possible directions (+X, -X, +Y, -Y, +Z, -Z) for UP:
for axis, name in [(0, "+X"), (0, "-X"), (1, "+Y"), (1, "-Y"), (2, "+Z"), (2, "-Z")]:
    sign = 1 if "+" in name else -1
    # Check top 5% along this direction
    val = sign * v[:, axis]
    top_thresh = np.percentile(val, 95)
    top_pts = v[val > top_thresh]
    
    other_axes = [i for i in range(3) if i != axis]
    spread = np.std(top_pts[:, other_axes], axis=0).prod()
    
    bot_thresh = np.percentile(val, 5)
    bot_pts = v[val < bot_thresh]
    bot_spread = np.std(bot_pts[:, other_axes], axis=0).prod()
    
    print(f"Direction {name:2s} as UP: Top 5% spread={spread:.5f}, Bottom 5% spread={bot_spread:.5f}, Ratio(Bot/Top)={bot_spread/(spread+1e-8):.1f}")

