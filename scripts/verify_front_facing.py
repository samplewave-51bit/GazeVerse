import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices.copy()

# In perfect_rot_0:
# x = v0[:, 2]
# y = v0[:, 1]
# z = -v0[:, 0]
# Elephants are at +x (right side).

# To make the elephants face +Z (directly towards camera):
# x_front = -z = v0[:, 0]
# y_front = y = v0[:, 1]
# z_front = x = v0[:, 2]
# Wait, let's test:
# x' = -x_0 = -v0[:, 2] ? or +z_0?

# Let's test the 2 possibilities:
# 1. Elephants facing +Z:
v_front1 = np.column_stack([-v0[:, 0], v0[:, 1], v0[:, 2]])
# 2. Elephants facing +Z:
v_front2 = np.column_stack([v0[:, 0], v0[:, 1], -v0[:, 2]])

for vt, name in [(v_front1, "front1"), (v_front2, "front2")]:
    x = vt[:, 0]
    y = vt[:, 1]
    z = vt[:, 2]
    x_c = x - (x.max() + x.min()) / 2.0
    y_c = y - y.min()
    z_c = z - (z.max() + z.min()) / 2.0
    
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    # Looking from +Z towards -Z:
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), name, fill=(0, 255, 204))
    img.save(f"static/check_{name}.png")
    print(f"Saved static/check_{name}.png")

