import trimesh
import numpy as np
from PIL import Image, ImageDraw

# 1. Load model
scene = trimesh.load('konark-sun-temple/source/model.glb')
print("Scene loaded:", type(scene))
geom = list(scene.geometry.values())[0] if isinstance(scene, trimesh.Scene) else scene
v = geom.vertices.copy()

print(f"Total vertices: {len(v)}, faces: {len(geom.faces)}")
print(f"Raw X bounds: [{v[:,0].min():.4f}, {v[:,0].max():.4f}] (span: {v[:,0].max()-v[:,0].min():.3f}m)")
print(f"Raw Y bounds: [{v[:,1].min():.4f}, {v[:,1].max():.4f}] (span: {v[:,1].max()-v[:,1].min():.3f}m)")
print(f"Raw Z bounds: [{v[:,2].min():.4f}, {v[:,2].max():.4f}] (span: {v[:,2].max()-v[:,2].min():.3f}m)")

# 2. Render 2D projections of Raw model
def save_proj(x, y, filename, title):
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

save_proj(v[:, 0], v[:, 1], "static/konark_raw_xy.png", "Raw XY: X (horiz) vs Y (vert)")
save_proj(v[:, 0], v[:, 2], "static/konark_raw_xz.png", "Raw XZ: X (horiz) vs Z (vert)")
save_proj(v[:, 2], v[:, 1], "static/konark_raw_zy.png", "Raw ZY: Z (horiz) vs Y (vert)")

