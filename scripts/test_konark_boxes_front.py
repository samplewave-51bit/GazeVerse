import trimesh
import numpy as np
from PIL import Image, ImageDraw

scene = trimesh.load('konark-sun-temple/source/model.glb')
geom = list(scene.geometry.values())[0] if isinstance(scene, trimesh.Scene) else scene
v = geom.vertices.copy()
cx = (v[:, 0].min() + v[:, 0].max()) / 2.0
cz = (v[:, 2].min() + v[:, 2].max()) / 2.0
min_y = v[:, 1].min()
v[:, 0] -= cx; v[:, 1] -= min_y; v[:, 2] -= cz

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

img_front = Image.new("RGB", (800, 800), (18, 22, 28))
draw_front = ImageDraw.Draw(img_front)

x_min, x_max = -0.9, 0.9
y_min, y_max = -0.05, 1.25

def to_front_px(x, y):
    px = int((x - x_min) / (x_max - x_min) * 700 + 50)
    py = int(750 - (y - y_min) / (y_max - y_min) * 700)
    return px, py

sub_idx = np.random.choice(len(v), size=min(25000, len(v)), replace=False)
for idx in sub_idx:
    px, py = to_front_px(v[idx, 0], v[idx, 1])
    img_front.putpixel((px, py), (180, 160, 130))

colors = [
    (0, 255, 204), (255, 120, 0), (255, 220, 0), (0, 180, 255),
    (255, 80, 180), (100, 255, 100), (200, 150, 255), (255, 80, 80)
]

for (name, b), col in zip(boxes.items(), colors):
    p1 = to_front_px(b[0], b[3]) # x_min, y_max
    p2 = to_front_px(b[1], b[2]) # x_max, y_min
    draw_front.rectangle([p1[0], p1[1], p2[0], p2[1]], outline=col, width=2)
    draw_front.text((p1[0] + 5, p1[1] + 5), name.replace("konark_", ""), fill=col)

img_front.save("static/konark_boxes_xy.png")
print("Saved static/konark_boxes_xy.png")

