import trimesh
import numpy as np
from PIL import Image, ImageDraw

# 1. Load model
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

# Bounding boxes dictionary:
# Format: [min_x, max_x, min_y, max_y, min_z, max_z]
boxes = {
    "konark_chariot_plinth_wheels": [-0.78, 0.78, 0.00, 0.17, -0.96, 0.55],
    "konark_eastern_sopana_horses": [-0.35, 0.35, 0.00, 0.20, 0.55, 0.96],
    "konark_natya_mandapa": [-0.35, 0.35, 0.17, 0.55, 0.35, 0.65],
    "konark_jagamohana_bada": [-0.43, 0.43, 0.17, 0.45, -0.22, 0.35],
    "konark_jagamohana_pyramid": [-0.43, 0.43, 0.45, 0.76, -0.22, 0.35],
    "konark_jagamohana_mastaka": [-0.25, 0.25, 0.76, 0.92, -0.15, 0.22],
    "konark_rekha_deula_spire": [-0.56, 0.56, 0.17, 0.98, -0.96, -0.22],
    "konark_sanctum_crown_finial": [-0.26, 0.26, 0.98, 1.22, -0.75, -0.40]
}

# Check point counts for each box
print("--- Point Count per Box ---")
for name, b in boxes.items():
    mask = (
        (v[:, 0] >= b[0]) & (v[:, 0] <= b[1]) &
        (v[:, 1] >= b[2]) & (v[:, 1] <= b[3]) &
        (v[:, 2] >= b[4]) & (v[:, 2] <= b[5])
    )
    print(f"{name:32s}: {np.sum(mask):6d} vertices (X:[{b[0]:.2f}, {b[1]:.2f}], Y:[{b[2]:.2f}, {b[3]:.2f}], Z:[{b[4]:.2f}, {b[5]:.2f}])")

# Render boxes overlaid on ZY side projection
img_side = Image.new("RGB", (800, 800), (18, 22, 28))
draw_side = ImageDraw.Draw(img_side)

z_min, z_max = -1.0, 1.0
y_min, y_max = -0.05, 1.25

def to_side_px(z, y):
    px = int((z - z_min) / (z_max - z_min) * 700 + 50)
    py = int(750 - (y - y_min) / (y_max - y_min) * 700)
    return px, py

sub_idx = np.random.choice(len(v), size=min(25000, len(v)), replace=False)
for idx in sub_idx:
    px, py = to_side_px(v[idx, 2], v[idx, 1])
    img_side.putpixel((px, py), (180, 160, 130))

colors = [
    (0, 255, 204), (255, 120, 0), (255, 220, 0), (0, 180, 255),
    (255, 80, 180), (100, 255, 100), (200, 150, 255), (255, 80, 80)
]

for (name, b), col in zip(boxes.items(), colors):
    p1 = to_side_px(b[4], b[3]) # z_min, y_max
    p2 = to_side_px(b[5], b[2]) # z_max, y_min
    draw_side.rectangle([p1[0], p1[1], p2[0], p2[1]], outline=col, width=2)
    draw_side.text((p1[0] + 5, p1[1] + 5), name.replace("konark_", ""), fill=col)

img_side.save("static/konark_boxes_zy.png")
print("Saved static/konark_boxes_zy.png")

