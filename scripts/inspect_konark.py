import open3d as o3d
import numpy as np

for name in ['sparse_0', 'sparse_1']:
    p = o3d.io.read_point_cloud(f"data/sfm/konark_sun_temple/{name}.ply")
    pts = np.asarray(p.points)
    print(f"{name}: {len(pts)} pts | min: {pts.min(axis=0)} | max: {pts.max(axis=0)}")

