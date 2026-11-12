import trimesh
import numpy as np

scene = trimesh.load('static/models/hampi_stone_chariot.glb')
geom = list(scene.geometry.values())[0]
v = geom.vertices

# Rotate: x' = x, y' = z, z' = -y
x_prime = v[:, 0]
y_prime = v[:, 2]
z_prime = -v[:, 1]

# Center on X and Z, set min Y to 0
cx = (x_prime.max() + x_prime.min()) / 2.0
cz = (z_prime.max() + z_prime.min()) / 2.0
min_y = y_prime.min()

x_final = x_prime - cx
y_final = y_prime - min_y
z_final = z_prime - cz

print(f"Upright bounds:")
print(f"  X: [{x_final.min():.3f}, {x_final.max():.3f}] (width: {x_final.max()-x_final.min():.3f}m)")
print(f"  Y: [{y_final.min():.3f}, {y_final.max():.3f}] (height: {y_final.max()-y_final.min():.3f}m)")
print(f"  Z: [{z_final.min():.3f}, {z_final.max():.3f}] (depth: {z_final.max()-z_final.min():.3f}m)")

