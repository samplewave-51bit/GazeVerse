import open3d as o3d
import numpy as np
from plyfile import PlyData, PlyElement

def densify_point_cloud(input_ply, output_ply, target_points=60000):
    pcd = o3d.io.read_point_cloud(input_ply)
    pts = np.asarray(pcd.points)
    colors = np.asarray(pcd.colors)
    
    print(f"Original points: {len(pts)}")
    pcd.estimate_normals(search_param=o3d.geometry.KDTreeSearchParamHybrid(radius=0.15, max_nn=30))
    normals = np.asarray(pcd.normals)
    
    # We can densify by generating points along local tangent planes using KDTree neighbors
    kdtree = o3d.geometry.KDTreeFlann(pcd)
    
    new_pts = [pts]
    new_colors = [colors]
    
    # For each point, find nearest neighbors and interpolate
    factor = int(np.ceil(target_points / len(pts))) - 1
    print(f"Upsampling factor: {factor}")
    
    gen_pts = []
    gen_colors = []
    for i in range(len(pts)):
        k, idx, dists = kdtree.search_knn_vector_3d(pcd.points[i], 8)
        if k > 3:
            for _ in range(factor):
                # Pick two random neighbors
                n1, n2 = np.random.choice(idx[1:k], size=2, replace=False) if k > 2 else (idx[0], idx[0])
                u, v = np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9)
                w = u + v
                if w > 1.0:
                    u, v = 1.0 - u, 1.0 - v
                w0 = 1.0 - u - v
                interp_pt = w0 * pts[i] + u * pts[n1] + v * pts[n2]
                interp_col = w0 * colors[i] + u * colors[n1] + v * colors[n2]
                gen_pts.append(interp_pt)
                gen_colors.append(interp_col)
                
    all_pts = np.vstack([pts, np.array(gen_pts)])
    all_colors = np.vstack([colors, np.array(gen_colors)])
    
    # Slightly prune any outliers
    dense_pcd = o3d.geometry.PointCloud()
    dense_pcd.points = o3d.utility.Vector3dVector(all_pts)
    dense_pcd.colors = o3d.utility.Vector3dVector(all_colors)
    
    cl, ind = dense_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.5)
    clean_pcd = dense_pcd.select_by_index(ind)
    
    final_pts = np.asarray(clean_pcd.points)
    final_colors = (np.asarray(clean_pcd.colors) * 255).astype(np.uint8)
    
    print(f"Final densified points: {len(final_pts)}")
    
    # Write to PLY
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
    PlyData([el], text=False).write(output_ply)
    print(f"Saved densified model to: {output_ply}")

densify_point_cloud(
    "static/models/hampi_stone_chariot_dense.ply",
    "static/models/hampi_stone_chariot_dense_upsampled.ply",
    target_points=65000
)

