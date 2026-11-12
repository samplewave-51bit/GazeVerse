import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices

# In raw model:
# Top is +Z, Base is -Z
# Front (elephants) is +Y, Rear is -Y
# Left is -X, Right is +X

# We want:
# Up (vertical) = +Z -> Y_new = Z
# Front (towards camera) = +Y -> Z_new = -Y (facing camera at +Z looking towards -Z) or Z_new = Y
# Let's test standard transform:
# Rotation around X by -90 deg:
# x_new = x
# y_new = z
# z_new = -y

# Wait, why was it rotated to the left previously?
# Let's check how the GLB was actually exported in static/models/hampi_stone_chariot_upright.glb!
# In save_current_projections.py earlier:
# We saw that static/models/hampi_stone_chariot_upright.glb in trimesh had:
# v[:, 0] = x
# v[:, 1] = y (where elephants were at +y)
# v[:, 2] = z (where spire was at +z)
# In Three.js:
# Three.js camera is at (0, 1.3, 2.5), looking at (0, 0.9, 0).
# The camera looks along -Z!
# So on the screen:
# Horizontal is X.
# Vertical is Y.
# When the camera looked along -Z, it saw X as horizontal, Y as vertical!
# But in the model, Y is the FRONT (elephants), and Z is the SPIRE (top)!
# So on the screen:
# The top (Z) was pointing along Z (depth)!
# And X was horizontal, Y was vertical!
# That means the temple was lying on its side facing UP (elephants pointing UP along Y)!

# Now: what does "Turn it to the right. the top is to the left side now" mean?
# Let's test a rotation where:
# Y_new is UP (Spire)
# Z_new is FRONT (Elephants)
# X_new is RIGHT
# Let's test:
# 1. R_x(-90): x'=x, y'=z, z'=-y
# 2. R_x(+90): x'=x, y'=-z, z'=y
# 3. R_y(-90): x'=-z, y'=y, z'=x
# 4. R_y(+90): x'=z, y'=y, z'=-x
# 5. R_z(-90): x'=y, y'=-x, z'=z
# 6. R_z(+90): x'=-y, y'=x, z'=z

def test_transform(v_in, name):
    x, y, z = v_in[:,0], v_in[:,1], v_in[:,2]
    # Center X and Z, set min Y to 0
    cx = (x.max() + x.min()) / 2.0
    cz = (z.max() + z.min()) / 2.0
    min_y = y.min()
    
    x_c = x - cx
    y_c = y - min_y
    z_c = z - cz
    
    # Save Front View (X vs Y): looking from front (+Z looking towards -Z)
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), f"{name}: Front View (X horiz, Y vert)", fill=(0, 255, 204))
    img.save(f"static/test_{name}_front.png")

    # Save Side View (Z vs Y): looking from right (+X looking towards -X)
    img_side = Image.new("RGB", (600, 600), (20, 24, 30))
    draw_s = ImageDraw.Draw(img_side)
    zs = (z_c[sub] - z_c.min()) / (z_c.max() - z_c.min() + 1e-8) * 500 + 50
    ys_s = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    for px, py in zip(zs, ys_s):
        img_side.putpixel((int(px), int(py)), (220, 190, 150))
    draw_s.text((20, 20), f"{name}: Side View (Z horiz, Y vert)", fill=(0, 255, 204))
    img_side.save(f"static/test_{name}_side.png")
    print(f"Generated {name} views: X span={x_c.max()-x_c.min():.2f}, Y span={y_c.max()-y_c.min():.2f}, Z span={z_c.max()-z_c.min():.2f}")

# Transform 1: x'=x, y'=z, z'=-y (Spire is +Y, Front is -Z)
v1 = np.column_stack([v0[:,0], v0[:,2], -v0[:,1]])
test_transform(v1, "opt1_x_z_negy")

# Transform 2: x'=-x, y'=z, z'=y (Spire is +Y, Front is +Z)
v2 = np.column_stack([-v0[:,0], v0[:,2], v0[:,1]])
test_transform(v2, "opt2_negx_z_y")

# Transform 3: x'=y, y'=z, z'=x (Spire is +Y, Front is +X)
v3 = np.column_stack([v0[:,1], v0[:,2], v0[:,0]])
test_transform(v3, "opt3_y_z_x")

# Transform 4: x'=-y, y'=z, z'=-x
v4 = np.column_stack([-v0[:,1], v0[:,2], -v0[:,0]])
test_transform(v4, "opt4_negy_z_negx")

