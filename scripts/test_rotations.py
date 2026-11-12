import trimesh
import numpy as np

# Load raw original model
raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices.copy()

print("Original v0 bounds:")
print("X:", v0[:,0].min(), v0[:,0].max())
print("Y:", v0[:,1].min(), v0[:,1].max())
print("Z:", v0[:,2].min(), v0[:,2].max())

# Candidate A:
# In our previous attempt, we did:
# x' = x, y' = z, z' = -y
# The user said: "the top is to the left side now. Turn it to the right."
# In Candidate A:
# The top was along -x or +y?
# Wait! Let's check where the top was in Candidate A:
# If top was to the left, that means top had negative X (or positive X viewed from rear).
# To turn from LEFT (negative X) to TOP (positive Y):
# A 90-degree rotation in the XY plane!
# x'' = y'
# y'' = -x' (or x'' = -y', y'' = x')
# Let's test rotating Candidate A around Z by 90 degrees and -90 degrees:
va = np.empty_like(v0)
va[:, 0] = v0[:, 0]
va[:, 1] = v0[:, 2]
va[:, 2] = -v0[:, 1]

# Rotate 90 deg clockwise in XY plane (turn right):
# [x, y] -> [y, -x] or [-y, x]
v_right1 = np.empty_like(v0)
v_right1[:, 0] = va[:, 1]
v_right1[:, 1] = -va[:, 0]
v_right1[:, 2] = va[:, 2]

v_right2 = np.empty_like(v0)
v_right2[:, 0] = -va[:, 1]
v_right2[:, 1] = va[:, 0]
v_right2[:, 2] = va[:, 2]

# Let's also test rotating around X or Y:
# What if in the original model, top was along Z, and to turn to the right:
# Let's inspect the Spire vertex in original v0:
# Where is the spire tip?
# We know the spire tip in v0 has Z max (~0.89) and X ~ 0, Y ~ -0.25 (from find_true_up.py):
spire_idx = np.argmax(v0[:, 2])
spire_pt = v0[spire_idx]
print(f"Original Spire tip point in v0: {spire_pt}")

# Ground points (wheels) in v0 have Z min (~ -0.93):
wheel_idx = np.argmin(v0[:, 2])
wheel_pt = v0[wheel_idx]
print(f"Original Ground/Wheel point in v0: {wheel_pt}")

# Vector from base to spire in v0:
up_vec = spire_pt - wheel_pt
print(f"Up vector in original v0: {up_vec}")
# up_vec is approximately [0, 0, 1.82]! So +Z is clearly the axis from base to top!

