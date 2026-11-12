import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices.copy()

# Turn 3:
# x' = v0[:, 0]
# y' = -v0[:, 2]
# z' = v0[:, 1]
# Let's also test:
# What if y' = +v0[:, 2]? (inverted Y of turn 3)
vt_a = np.column_stack([v0[:, 0], -v0[:, 2], v0[:, 1]])
vt_b = np.column_stack([v0[:, 0], v0[:, 2], -v0[:, 1]])

# What if x' and z' are swapped?
vt_c = np.column_stack([v0[:, 1], v0[:, 2], v0[:, 0]])
vt_d = np.column_stack([-v0[:, 1], v0[:, 2], v0[:, 0]])
vt_e = np.column_stack([v0[:, 1], -v0[:, 2], v0[:, 0]])

# And what if Y in original model was height?
# (e.g. y' = v0[:, 1], z' = v0[:, 2], x' = v0[:, 0])
vt_f = np.column_stack([v0[:, 0], v0[:, 1], v0[:, 2]])
vt_g = np.column_stack([v0[:, 2], v0[:, 1], -v0[:, 0]])
vt_h = np.column_stack([-v0[:, 2], v0[:, 1], v0[:, 0]])

def render_both(vt, name):
    x = vt[:, 0]
    y = vt[:, 1]
    z = vt[:, 2]
    x_c = x - (x.max() + x.min()) / 2.0
    y_c = y - y.min()
    z_c = z - (z.max() + z.min()) / 2.0
    
    # 1. Front (X horiz, Y vert)
    img_f = Image.new("RGB", (600, 600), (20, 24, 30))
    draw_f = ImageDraw.Draw(img_f)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(xs, ys):
        img_f.putpixel((int(px), int(py)), (220, 190, 150))
    draw_f.text((20, 20), f"{name}: Front View (X, Y)", fill=(0, 255, 204))
    img_f.save(f"static/render_{name}_front.png")

    # 2. Side (Z horiz, Y vert)
    img_s = Image.new("RGB", (600, 600), (20, 24, 30))
    draw_s = ImageDraw.Draw(img_s)
    zs = (z_c[sub] - z_c.min()) / (z_c.max() - z_c.min() + 1e-8) * 500 + 50
    ys_s = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(zs, ys_s):
        img_s.putpixel((int(px), int(py)), (220, 190, 150))
    draw_s.text((20, 20), f"{name}: Side View (Z, Y)", fill=(0, 255, 204))
    img_s.save(f"static/render_{name}_side.png")

for vt, name in [(vt_a, "vt_a"), (vt_b, "vt_b"), (vt_g, "vt_g"), (vt_h, "vt_h")]:
    render_both(vt, name)
    print(f"Rendered {name}")

