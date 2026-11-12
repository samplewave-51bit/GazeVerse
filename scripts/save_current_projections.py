import trimesh
import numpy as np
from PIL import Image, ImageDraw

upright = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
mesh = upright.to_geometry() if isinstance(upright, trimesh.Scene) else upright
v = mesh.vertices

def save_projection(x, y, filename, title=""):
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    sub_idx = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x[sub_idx] - x_min) / (x_max - x_min + 1e-8) * 500 + 50
    ys = 550 - (y[sub_idx] - y_min) / (y_max - y_min + 1e-8) * 500
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
    draw.text((20, 20), title, fill=(0, 255, 204))
    img.save(filename)
    print(f"Saved {filename}")

save_projection(v[:, 0], v[:, 1], "static/proj_cur_xy.png", "Current XY: X (screen horiz) vs Y (screen vert)")
save_projection(v[:, 2], v[:, 1], "static/proj_cur_zy.png", "Current ZY: Z (depth) vs Y (screen vert)")
save_projection(v[:, 0], v[:, 2], "static/proj_cur_xz.png", "Current XZ: X (horiz) vs Z (depth)")

