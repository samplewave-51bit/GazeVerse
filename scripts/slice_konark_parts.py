import trimesh
import numpy as np
from PIL import Image, ImageDraw, ImageFont

scene = trimesh.load('konark-sun-temple/source/model.glb')
geom = list(scene.geometry.values())[0] if isinstance(scene, trimesh.Scene) else scene
v = geom.vertices.copy()

# Center X and Z, set min Y to 0
cx = (v[:, 0].min() + v[:, 0].max()) / 2.0
cz = (v[:, 2].min() + v[:, 2].max()) / 2.0
min_y = v[:, 1].min()

v[:, 0] -= cx
v[:, 1] -= min_y
v[:, 2] -= cz

# Slices along Z:
# Rear: Vimana / Rekha Deula Sanctum (Z < -0.20)
# Middle: Jagamohana (Audience Hall) (-0.20 <= Z <= 0.35)
# Front: Natya Mandapa / Entrance Porch (Z > 0.35)

print("--- Z Profile Max Heights ---")
for z_val in np.linspace(-0.9, 0.9, 19):
    mask = (v[:, 2] >= z_val - 0.05) & (v[:, 2] < z_val + 0.05)
    if np.sum(mask) > 0:
        print(f"Z ~ {z_val:+.2f}: Count = {np.sum(mask):5d}, Max Y = {v[mask, 1].max():.3f}, Min Y = {v[mask, 1].min():.3f}")

# Let's inspect the distinct architectural elements:
# 1. Base Chariot Plinth & Wheels: Y from 0.00 to ~0.20
# 2. Natya Mandapa / Front Entrance: Z >= 0.35, Y from 0.05 to ~0.40
# 3. Jagamohana Bada (Walls): Z in [-0.22, 0.35], Y from 0.18 to ~0.45
# 4. Jagamohana Pidha Pyramid: Z in [-0.22, 0.35], Y from 0.45 to ~0.82
# 5. Jagamohana Mastaka (Crown / Amalaka / Kalasa): Z in [-0.15, 0.25], Y from 0.82 to ~0.96
# 6. Vimana / Rekha Deula Spire (Sanctuary Shikhara): Z in [-0.95, -0.22], Y from 0.18 to ~1.05
# 7. Sanctum Mastaka & Crown Finial: Z in [-0.75, -0.35], Y from 1.05 to 1.21

