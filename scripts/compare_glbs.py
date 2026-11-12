import trimesh
import numpy as np

# Load original model.glb
scene = trimesh.load('stone-chariot-in-hampi/source/model.glb')
geom = list(scene.geometry.values())[0] if isinstance(scene, trimesh.Scene) else scene
v = geom.vertices

# Let's inspect the bounding box of original model.glb
print("Original model.glb:")
print(f"X: [{v[:,0].min():.3f}, {v[:,0].max():.3f}]")
print(f"Y: [{v[:,1].min():.3f}, {v[:,1].max():.3f}]")
print(f"Z: [{v[:,2].min():.3f}, {v[:,2].max():.3f}]")

# In the current upright model that the user is seeing right now:
cur_scene = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
cur_geom = list(cur_scene.geometry.values())[0] if isinstance(cur_scene, trimesh.Scene) else cur_scene
v_cur = cur_geom.vertices
print("\nExported hampi_stone_chariot_upright.glb vertices in geom:")
print(f"X: [{v_cur[:,0].min():.3f}, {v_cur[:,0].max():.3f}]")
print(f"Y: [{v_cur[:,1].min():.3f}, {v_cur[:,1].max():.3f}]")
print(f"Z: [{v_cur[:,2].min():.3f}, {v_cur[:,2].max():.3f}]")

