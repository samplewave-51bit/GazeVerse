import trimesh
import numpy as np
from PIL import Image, ImageDraw

raw = trimesh.load('stone-chariot-in-hampi/source/model.glb')
raw_mesh = list(raw.geometry.values())[0] if isinstance(raw, trimesh.Scene) else raw
v = raw_mesh.vertices

# Function to render a 2D projection scatter plot
def save_projection(x, y, filename, title=""):
    img = Image.new("RGB", (600, 600), (20, 24, 30))
    draw = ImageDraw.Draw(img)
    
    # Normalize coordinates to 50..550
    x_min, x_max = x.min(), x.max()
    y_min, y_max = y.min(), y.max()
    
    # Subsample 15000 points
    sub_idx = np.random.choice(len(x), size=min(15000, len(x)), replace=False)
    xs = (x[sub_idx] - x_min) / (x_max - x_min + 1e-8) * 500 + 50
    # Invert Y for image
    ys = 550 - (y[sub_idx] - y_min) / (y_max - y_min + 1e-8) * 500
    
    for px, py in zip(xs, ys):
        img.putpixel((int(px), int(py)), (220, 190, 150))
        
    draw.text((20, 20), title, fill=(0, 255, 204))
    img.save(filename)
    print(f"Saved {filename}")

# Save projections of raw model.glb
save_projection(v[:, 0], v[:, 1], "static/proj_raw_xy.png", "Raw XY: X (horizontal) vs Y (vertical)")
save_projection(v[:, 0], v[:, 2], "static/proj_raw_xz.png", "Raw XZ: X (horizontal) vs Z (vertical)")
save_projection(v[:, 1], v[:, 2], "static/proj_raw_yz.png", "Raw YZ: Y (horizontal) vs Z (vertical)")

