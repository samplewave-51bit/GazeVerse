import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices.copy()

# vt_g was:
# x_g = v0[:, 2]
# y_g = v0[:, 1]
# z_g = -v0[:, 0]

# Now, we want:
# Y_final = y_g = v0[:, 1] (Vertical height, wheels at bottom, spire at top)
# We want the elephants to face +Z (towards camera):
# In vt_g, the elephants were at +x_g (i.e. +v0[:, 2]).
# So Z_final = x_g = v0[:, 2]!
# And X_final = -z_g = v0[:, 0]!
# Let's check determinant:
# X = v0[:, 0]
# Y = v0[:, 1]
# Z = v0[:, 2]
# Wait! In raw v0:
# X was v0[:, 0], Y was v0[:, 1], Z was v0[:, 2]!
# But in vt_g:
# Height was v0[:, 1]!
# And in raw v0, what were the bounds?
# X: [-0.646, 0.645]
# Y: [-0.683, 0.683]
# Z: [-0.933, 0.893]
# Look at vt_g_side.png and vt_g_front.png:
# In vt_g:
# Height (Y) was v0[:, 1] (from -0.683 to +0.683)!
# That was width 1.37m.
# But wait! Why did vt_g_side look like the temple?
# Let's check what the height was in vt_g:
# Let's inspect the dimensions of vt_g:

x = v0[:, 2]
y = v0[:, 1]
z = -v0[:, 0]

# Let's test rotating around Y by -90 deg:
# x_final = -z = v0[:, 0]
# y_final = y = v0[:, 1]
# z_final = x = v0[:, 2]

# Let's render this view:
v_final = np.column_stack([v0[:, 0], v0[:, 1], v0[:, 2]])

# Let's test all 4 rotations around Y of vt_g:
for rot_k in [0, 1, 2, 3]:
    angle = rot_k * np.pi / 2
    cos_a, sin_a = np.cos(angle), np.sin(angle)
    # Rotate around Y:
    # x' = x*cos + z*sin
    # z' = -x*sin + z*cos
    x_rot = x * cos_a + z * sin_a
    y_rot = y
    z_rot = -x * sin_a + z * cos_a
    
    x_c = x_rot - (x_rot.max() + x_rot.min()) / 2.0
    y_c = y_rot - y_rot.min()
    z_c = z_rot - (z_rot.max() + z_rot.min()) / 2.0
    
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), f"Rot {rot_k * 90} deg", fill=(0, 255, 204))
    img.save(f"static/perfect_rot_{rot_k*90}.png")
    print(f"Saved static/perfect_rot_{rot_k*90}.png")

