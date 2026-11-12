import trimesh
import numpy as np

# Load GLB
scene = trimesh.load('static/models/hampi_stone_chariot.glb')

# 90-degree rotation around X axis (Z -> Y, Y -> -Z)
# Rotation matrix for -90 degrees around X:
# [ 1,  0,  0, 0]
# [ 0,  0,  1, 0]
# [ 0, -1,  0, 0]
# [ 0,  0,  0, 1]
R = trimesh.transformations.rotation_matrix(-np.pi / 2, [1, 0, 0])

# Apply rotation
scene.apply_transform(R)

# Get bounds after rotation
bounds = scene.bounds
min_corner = bounds[0]
max_corner = bounds[1]

cx = (min_corner[0] + max_corner[0]) / 2.0
cz = (min_corner[2] + max_corner[2]) / 2.0
min_y = min_corner[1]

# Translation to center X/Z and place ground at Y=0
T = trimesh.transformations.translation_matrix([-cx, -min_y, -cz])
scene.apply_transform(T)

print("Exporting upright GLB...")
print(f"Final bounds min: {scene.bounds[0]}")
print(f"Final bounds max: {scene.bounds[1]}")

scene.export("static/models/hampi_stone_chariot_upright.glb")
print("Saved static/models/hampi_stone_chariot_upright.glb")

