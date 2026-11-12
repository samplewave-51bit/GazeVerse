import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v0 = raw_mesh.vertices

# In v0:
# The 4 wheels are located at:
# 1. (-0.47, 0.46, -0.42)
# 2. (0.47, 0.46, -0.42)
# 3. (-0.45, -0.41, -0.47)
# 4. (0.45, -0.41, -0.47)
# Notice that in v0, all 4 wheels have:
# |X| ~ 0.46 (two negative X, two positive X!)
# Y has two at +0.46, two at -0.41!
# And Z is at -0.42 to -0.47 (low Z)!
# And the Spire peak is at Z ~ +0.89!
# And the ground/base is at Z ~ -0.93!
# This means:
# IN RAW v0:
# +Z is ALREADY the vertical axis (from ground Z=-0.93 to spire Z=+0.89)!
# X is the LEFT-RIGHT axis (wheels at X = -0.46 and X = +0.46)!
# Y is the FRONT-BACK axis (elephants at +Y ~ 0.68, rear at -Y ~ -0.68)!

print("RAW v0 structure:")
print("  Left-Right (Width): X axis in [-0.65, +0.65]")
print("  Front-Back (Depth): Y axis in [-0.68, +0.68] (Front/Elephants at +Y)")
print("  Bottom-Top (Height): Z axis in [-0.93, +0.89] (Wheels at -Z, Spire at +Z)")

# NOW: In Three.js:
# Three.js uses:
# X = Left-Right (Width)
# Y = Bottom-Top (Height) -> must be +Z of v0!
# Z = Back-Front (Depth) -> must be +Y of v0!

# So in Three.js:
# Y_three = Z_raw (so height Y is from 0 to 1.83)
# Z_three = Y_raw (so front is towards +Z, facing camera!)
# X_three = -X_raw (to keep right-handed system: det([ -1 0 0; 0 0 1; 0 1 0 ]) = +1)
# OR:
# X_three = X_raw, Y_three = Z_raw, Z_three = -Y_raw (front faces -Z, camera at -Z sees front)

# Let's test both and render Front View:
def render_front_view(v_trans, filename, label):
    x = v_trans[:, 0]
    y = v_trans[:, 1]
    z = v_trans[:, 2]
    
    # Center X and Z, place ground at Y=0
    x_c = x - (x.max() + x.min()) / 2.0
    y_c = y - y.min()
    z_c = z - (z.max() + z.min()) / 2.0
    
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    
    # Front View: looking from camera at (+Z) towards (0, 0, 0)
    # Screen horizontal is X, screen vertical is Y
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), label, fill=(0, 255, 204))
    img.save(filename)
    print(f"Saved {filename}")

# Configuration 1:
# x' = -x, y' = z, z' = y (det = +1)
v_cfg1 = np.column_stack([-v0[:, 0], v0[:, 2], v0[:, 1]])
render_front_view(v_cfg1, "static/cfg1_front_view.png", "Cfg 1: Front View (X, Y)")

# Configuration 2:
# x' = x, y' = z, z' = -y (det = +1)
v_cfg2 = np.column_stack([v0[:, 0], v0[:, 2], -v0[:, 1]])
render_front_view(v_cfg2, "static/cfg2_front_view.png", "Cfg 2: Front View (X, Y)")

