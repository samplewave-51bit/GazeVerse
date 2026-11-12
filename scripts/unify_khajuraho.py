import open3d as o3d
import numpy as np
from plyfile import PlyData, PlyElement

p1 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/kandariya_1_reoriented.ply")
p2 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/kandariya_2_reoriented.ply")

pts1 = np.asarray(p1.points)
cols1 = np.asarray(p1.colors)
pts2 = np.asarray(p2.points)
cols2 = np.asarray(p2.colors)

# Combined points
all_pts = np.vstack([pts1, pts2])
all_cols = np.vstack([cols1, cols2])

pcd = o3d.geometry.PointCloud()
pcd.points = o3d.utility.Vector3dVector(all_pts)
pcd.colors = o3d.utility.Vector3dVector(all_cols)

print(f"Combined points: {len(all_pts)}")

# Densify with KDTree
kdtree = o3d.geometry.KDTreeFlann(pcd)
factor = 15 # densify to ~60,000 points

gen_pts = []
gen_colors = []
for i in range(len(all_pts)):
    k, idx, dists = kdtree.search_knn_vector_3d(pcd.points[i], 10)
    if k > 3:
        for _ in range(factor):
            n1, n2 = np.random.choice(idx[1:k], size=2, replace=False) if k > 2 else (idx[0], idx[0])
            u, v = np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9)
            w = u + v
            if w > 1.0:
                u, v = 1.0 - u, 1.0 - v
            w0 = 1.0 - u - v
            interp_pt = w0 * all_pts[i] + u * all_pts[n1] + v * all_pts[n2]
            interp_col = w0 * all_cols[i] + u * all_cols[n1] + v * all_cols[n2]
            gen_pts.append(interp_pt)
            gen_colors.append(interp_col)

dense_pts = np.vstack([all_pts, np.array(gen_pts)])
dense_cols = np.vstack([all_cols, np.array(gen_colors)])

dense_pcd = o3d.geometry.PointCloud()
dense_pcd.points = o3d.utility.Vector3dVector(dense_pts)
dense_pcd.colors = o3d.utility.Vector3dVector(dense_cols)

cl, ind = dense_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.5)
clean_pcd = dense_pcd.select_by_index(ind)

final_pts = np.asarray(clean_pcd.points)
final_colors = (np.asarray(clean_pcd.colors) * 255).astype(np.uint8)

print(f"Final combined & densified points: {len(final_pts)}")
print(f"Dimensions: X=[{final_pts[:,0].min():.2f}, {final_pts[:,0].max():.2f}], Y=[{final_pts[:,1].min():.2f}, {final_pts[:,1].max():.2f}], Z=[{final_pts[:,2].min():.2f}, {final_pts[:,2].max():.2f}]")

vertex_dtype = [
    ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
    ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
]
vertices = np.empty(len(final_pts), dtype=vertex_dtype)
vertices['x'] = final_pts[:, 0]
vertices['y'] = final_pts[:, 1]
vertices['z'] = final_pts[:, 2]
vertices['red'] = final_colors[:, 0]
vertices['green'] = final_colors[:, 1]
vertices['blue'] = final_colors[:, 2]

el = PlyElement.describe(vertices, 'vertex')
out_path = "static/models/khajuraho_kandariya_dense.ply"
PlyData([el], text=False).write(out_path)
print(f"Saved complete unified Khajuraho model to {out_path}")

