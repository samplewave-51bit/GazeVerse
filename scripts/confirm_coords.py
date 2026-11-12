import trimesh
import numpy as np

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices.copy()

# x = -v0[:, 0]
# y = v0[:, 1]
# z = v0[:, 2]

# Let's inspect the two Z extremes:
# min Z vs max Z:
# Where do the stairs / elephants stick out?
# In check_front1, let's see which Z has the stairs extending:
z_pos = v0[v0[:, 2] > 0.4]
z_neg = v0[v0[:, 2] < -0.4]

print(f"Points with v0[:, 2] > 0.4: {len(z_pos)}, X span={z_pos[:,0].max()-z_pos[:,0].min():.2f}, Y span={z_pos[:,1].max()-z_pos[:,1].min():.2f}")
print(f"Points with v0[:, 2] < -0.4: {len(z_neg)}, X span={z_neg[:,0].max()-z_neg[:,0].min():.2f}, Y span={z_neg[:,1].max()-z_neg[:,1].min():.2f}")

# Remember earlier in check_opt0 we saw:
# The elephants and stairs stick out horizontally at the base!
# In render_vt_g_front.png earlier:
# The elephants and stairs were at the right!
# And in vt_g, X was v0[:, 2]!
# That means:
# HIGH v0[:, 2] (positive Z) is the FRONT (elephants and stairs)!
# LOW v0[:, 2] (negative Z) is the REAR!
print(f"Positive Z (v0[:, 2] > 0) is the FRONT with the elephants and stairs!")
print(f"Negative Z (v0[:, 2] < 0) is the REAR!")
print(f"Y (v0[:, 1]) is the HEIGHT from ground (wheels at bottom) to spire (top)!")
print(f"X (-v0[:, 0]) is the WIDTH from left wheel to right wheel!")

