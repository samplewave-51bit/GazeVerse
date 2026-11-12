import trimesh
import numpy as np

# Load original model.glb
raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v = mesh.vertices.copy()

print("Original bounds:")
print("X:", v[:,0].min(), v[:,0].max())
print("Y:", v[:,1].min(), v[:,1].max())
print("Z:", v[:,2].min(), v[:,2].max())

# In check_front1, we saw:
# X was -v[:, 0] (so X is width, left to right)
# Y was v[:, 1] (so Y is height, ground to roof)
# Z was v[:, 2] (so Z is depth, rear to front)

# Let's center X and Z, set min Y to 0:
cx = (v[:,0].max() + v[:,0].min()) / 2.0
min_y = v[:,1].min()
cz = (v[:,2].max() + v[:,2].min()) / 2.0

v_new = v.copy()
v_new[:, 0] = v[:, 0] - cx
v_new[:, 1] = v[:, 1] - min_y
v_new[:, 2] = v[:, 2] - cz

print("\nNew bounds:")
print(f"X: [{v_new[:,0].min():.4f}, {v_new[:,0].max():.4f}] (width: {v_new[:,0].max()-v_new[:,0].min():.3f}m)")
print(f"Y: [{v_new[:,1].min():.4f}, {v_new[:,1].max():.4f}] (height: {v_new[:,1].max()-v_new[:,1].min():.3f}m)")
print(f"Z: [{v_new[:,2].min():.4f}, {v_new[:,2].max():.4f}] (depth: {v_new[:,2].max()-v_new[:,2].min():.3f}m)")

# Apply this directly to the mesh
mesh.vertices = v_new

# Export directly as GLB
export_path = "static/models/hampi_stone_chariot_upright.glb"
mesh.export(export_path)
print(f"Successfully exported baked upright mesh to: {export_path}")

