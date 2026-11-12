import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices.copy()

# In cam_v_right:
# x was v0[:, 1]
# y was v0[:, 2]
# z was v0[:, 0]
#
# To turn cam_v_right to the right (90 deg clockwise in screen plane X-Y):
# New screen horizontal X_new = y = v0[:, 2]
# New screen vertical Y_new = -x = -v0[:, 1] (or +v0[:, 1])
# And Z_new = -z = -v0[:, 0] (or +v0[:, 0])

# Let's test both signs:
v_turn1 = np.column_stack([v0[:, 2], -v0[:, 1], v0[:, 0]])
v_turn2 = np.column_stack([-v0[:, 2], v0[:, 1], v0[:, 0]])
v_turn3 = np.column_stack([v0[:, 0], -v0[:, 2], v0[:, 1]])
v_turn4 = np.column_stack([-v0[:, 1], v0[:, 0], v0[:, 2]])

# Also test:
# What if the spire in the original model is along Y, and wheels along -Y?
v_turn5 = np.column_stack([v0[:, 0], v0[:, 1], v0[:, 2]])
v_turn6 = np.column_stack([v0[:, 2], v0[:, 0], v0[:, 1]])
v_turn7 = np.column_stack([v0[:, 1], v0[:, 0], -v0[:, 2]])

for idx, vt in enumerate([v_turn1, v_turn2, v_turn3, v_turn4, v_turn6, v_turn7], start=1):
    x = vt[:, 0]
    y = vt[:, 1]
    z = vt[:, 2]
    x_c = x - (x.max() + x.min()) / 2.0
    y_c = y - y.min()
    z_c = z - (z.max() + z.min()) / 2.0
    
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), f"Turn {idx}", fill=(0, 255, 204))
    img.save(f"static/turn_{idx}.png")
    print(f"Turn {idx} saved: X={x_c.max()-x_c.min():.2f}, Y={y_c.max()-y_c.min():.2f}, Z={z_c.max()-z_c.min():.2f}")

