import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v = raw_mesh.vertices.copy()

# We know:
# v[:, 0] is X (width)
# v[:, 1] is Y (front-back, elephants at +Y)
# v[:, 2] is Z (bottom-top, ground at min Z, spire at max Z)

# Let's test the 4 orientations where Z is UP (Y_new = v[:, 2]):
# 1. Front faces +Z (towards Three.js camera):
#    Y_new = v[:, 2] (Height)
#    Z_new = v[:, 1] (Front)
#    X_new = -v[:, 0] (Right)
v_front = np.column_stack([-v[:, 0], v[:, 2], v[:, 1]])

# 2. Front faces -Z (away from camera):
#    Y_new = v[:, 2]
#    Z_new = -v[:, 1]
#    X_new = v[:, 0]
v_back = np.column_stack([v[:, 0], v[:, 2], -v[:, 1]])

# 3. Front faces +X (towards right):
#    Y_new = v[:, 2]
#    X_new = v[:, 1]
#    Z_new = v[:, 0]
v_right = np.column_stack([v[:, 1], v[:, 2], v[:, 0]])

# 4. Front faces -X (towards left):
#    Y_new = v[:, 2]
#    X_new = -v[:, 1]
#    Z_new = -v[:, 0]
v_left = np.column_stack([-v[:, 1], v[:, 2], -v[:, 0]])

# Render front view (as seen by camera in Three.js from +Z looking towards 0)
def render_cam_view(v_in, name, title):
    x = v_in[:, 0]
    y = v_in[:, 1]
    z = v_in[:, 2]
    
    # Center X and Z, ground at Y=0
    x_c = x - (x.max() + x.min()) / 2.0
    y_c = y - y.min()
    z_c = z - (z.max() + z.min()) / 2.0
    
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    sub = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    
    # Looking from +Z towards -Z:
    # Screen X = x_c, Screen Y = y_c
    xs = (x_c[sub] - x_c.min()) / (x_c.max() - x_c.min() + 1e-8) * 500 + 50
    ys = 550 - (y_c[sub] - y_c.min()) / (y_c.max() - y_c.min() + 1e-8) * 500
    
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), title, fill=(0, 255, 204))
    img.save(f"static/cam_{name}.png")
    print(f"Saved static/cam_{name}.png")

render_cam_view(v_front, "v_front", "V_FRONT: Elephants facing camera, Spire UP")
render_cam_view(v_back, "v_back", "V_BACK: Rear facing camera, Spire UP")
render_cam_view(v_right, "v_right", "V_RIGHT: Side facing camera, Spire UP")
render_cam_view(v_left, "v_left", "V_LEFT: Side facing camera, Spire UP")

