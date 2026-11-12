import trimesh
import numpy as np
import os

os.makedirs('static/models', exist_ok=True)

# Load original model.glb
print("Loading konark-sun-temple/source/model.glb...")
raw = trimesh.load('konark-sun-temple/source/model.glb')
mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v = mesh.vertices.copy()

print("Original bounds:")
print("X:", v[:,0].min(), v[:,0].max())
print("Y:", v[:,1].min(), v[:,1].max())
print("Z:", v[:,2].min(), v[:,2].max())

# Center X and Z, set min Y to 0
cx = (v[:,0].max() + v[:,0].min()) / 2.0
min_y = v[:,1].min()
cz = (v[:,2].max() + v[:,2].min()) / 2.0

v_new = v.copy()
v_new[:, 0] = v[:, 0] - cx
v_new[:, 1] = v[:, 1] - min_y
v_new[:, 2] = v[:, 2] - cz

print("\nBaked upright bounds:")
print(f"X: [{v_new[:,0].min():.4f}, {v_new[:,0].max():.4f}] (width: {v_new[:,0].max()-v_new[:,0].min():.3f}m)")
print(f"Y: [{v_new[:,1].min():.4f}, {v_new[:,1].max():.4f}] (height: {v_new[:,1].max()-v_new[:,1].min():.3f}m)")
print(f"Z: [{v_new[:,2].min():.4f}, {v_new[:,2].max():.4f}] (depth: {v_new[:,2].max()-v_new[:,2].min():.3f}m)")

# Apply this directly to the mesh
mesh.vertices = v_new

# Export directly as GLB
export_path = "static/models/konark_sun_temple_upright.glb"
print(f"Exporting to {export_path}...")
mesh.export(export_path)
print(f"Successfully exported baked upright mesh to: {export_path}")

file_size_mb = os.path.getsize(export_path) / (1024 * 1024)
print(f"File size: {file_size_mb:.2f} MB")

