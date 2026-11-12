import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices

# In opt3:
# x_opt3 = v0[:, 1]
# y_opt3 = v0[:, 2]
# z_opt3 = v0[:, 0]

# Now, rotating 90 deg clockwise to the right:
# The top (which was -x_opt3, left) goes to +Y (up)!
# So:
# Y_final = -x_opt3 = -v0[:, 1]  (or +x_opt3?)
# Let's check: in opt3, the top was at high y_opt3? No, in opt3 image:
# The top was on the LEFT side of the image (min X of opt3).
# So min x_opt3 was the TOP!
# Therefore:
# If min x_opt3 is the TOP, we want -x_opt3 to be +Y_final!
# And the wheels were at max x_opt3 (right side of the image).
# So max x_opt3 becomes -Y_final (ground/bottom)!
# And what about the vertical axis of opt3 (y_opt3)?
# In the opt3 image, the elephants were on the left side, facing out.
# Let's test the 2 orientations:

def test_upright(vx, vy, vz, name):
    x = vx
    y = vy
    z = vz
    cx = (x.max() + x.min()) / 2.0
    cz = (z.max() + z.min()) / 2.0
    min_y = y.min()
    x_c = x - cx
    y_c = y - min_y
    z_c = z - cz
    
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), f"{name}: X horiz, Y vert", fill=(0, 255, 204))
    img.save(f"static/test_{name}.png")
    print(f"{name} saved: X span={x_c.max()-x_c.min():.2f}, Y span={y_c.max()-y_c.min():.2f}, Z span={z_c.max()-z_c.min():.2f}")

# Test A:
# Y = -v0[:, 1]
# X = v0[:, 2]
# Z = v0[:, 0]
test_upright(v0[:, 2], -v0[:, 1], v0[:, 0], "A_z_negy_x")

# Test B:
# Y = v0[:, 1]
# X = -v0[:, 2]
# Z = v0[:, 0]
test_upright(-v0[:, 2], v0[:, 1], v0[:, 0], "B_negz_y_x")

# Test C:
# What about rotating around Z in Three.js?
# In Three.js, currentMesh was loaded directly from static/models/hampi_stone_chariot_upright.glb.
# Earlier, static/models/hampi_stone_chariot_upright.glb was:
# x' = x, y' = z, z' = -y
# In that model, let's see which way the top was pointing!

