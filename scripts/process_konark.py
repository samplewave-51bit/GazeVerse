import open3d as o3d
import numpy as np
from plyfile import PlyData, PlyElement

def process_konark(in_path, out_path, target_pts=50000):
    ply = PlyData.read(in_path)
    v = ply['vertex']
    x = np.array(v['x'], dtype=np.float32)
    y = np.array(v['y'], dtype=np.float32)
    z = np.array(v['z'], dtype=np.float32)
    r = np.array(v['red'], dtype=np.uint8) if 'red' in v else np.full(len(x), 200, dtype=np.uint8)
    g = np.array(v['green'], dtype=np.uint8) if 'green' in v else np.full(len(x), 180, dtype=np.uint8)
    b = np.array(v['blue'], dtype=np.uint8) if 'blue' in v else np.full(len(x), 160, dtype=np.uint8)

    y_up = -y
    z_up = -z
    x_up = x

    # Outlier filter
    mask = np.ones(len(x), dtype=bool)
    for coord in [x_up, y_up, z_up]:
        med = np.median(coord)
        mad = np.median(np.abs(coord - med))
        if mad > 1e-4:
            mask &= (np.abs(coord - med) <= 4.0 * mad * 1.4826)

    # Sky filter
    is_sky = (b > (r.astype(int) + 30)) & (b > 160) & (y_up > np.percentile(y_up[mask], 70))
    mask &= ~is_sky

    x_filt, y_filt, z_filt = x_up[mask], y_up[mask], z_up[mask]
    r_filt, g_filt, b_filt = r[mask], g[mask], b[mask]

    cx = (x_filt.max() + x_filt.min()) / 2.0
    cz = (z_filt.max() + z_filt.min()) / 2.0
    min_y = y_filt.min()

    x_c = x_filt - cx
    y_c = y_filt - min_y
    z_c = z_filt - cz

    pcd = o3d.geometry.PointCloud()
    pts = np.vstack([x_c, y_c, z_c]).T
    cols = np.vstack([r_filt, g_filt, b_filt]).T / 255.0
    pcd.points = o3d.utility.Vector3dVector(pts)
    pcd.colors = o3d.utility.Vector3dVector(cols)

    kdtree = o3d.geometry.KDTreeFlann(pcd)
    factor = int(np.ceil(target_pts / len(pts))) - 1
    
    gen_pts = []
    gen_cols = []
    for i in range(len(pts)):
        k, idx, dists = kdtree.search_knn_vector_3d(pcd.points[i], 10)
        if k > 3:
            for _ in range(factor):
                n1, n2 = np.random.choice(idx[1:k], size=2, replace=False) if k > 2 else (idx[0], idx[0])
                u, v = np.random.uniform(0.1, 0.9), np.random.uniform(0.1, 0.9)
                w = u + v
                if w > 1.0:
                    u, v = 1.0 - u, 1.0 - v
                w0 = 1.0 - u - v
                interp_pt = w0 * pts[i] + u * pts[n1] + v * pts[n2]
                interp_col = w0 * cols[i] + u * cols[n1] + v * cols[n2]
                gen_pts.append(interp_pt)
                gen_cols.append(interp_col)

    dense_pts = np.vstack([pts, np.array(gen_pts)])
    dense_cols = np.vstack([cols, np.array(gen_cols)])

    dense_pcd = o3d.geometry.PointCloud()
    dense_pcd.points = o3d.utility.Vector3dVector(dense_pts)
    dense_pcd.colors = o3d.utility.Vector3dVector(dense_cols)

    cl, ind = dense_pcd.remove_statistical_outlier(nb_neighbors=20, std_ratio=2.5)
    clean_pcd = dense_pcd.select_by_index(ind)

    final_pts = np.asarray(clean_pcd.points)
    final_colors = (np.asarray(clean_pcd.colors) * 255).astype(np.uint8)

    print(f"Konark final points: {len(final_pts)}")
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
    PlyData([el], text=False).write(out_path)
    print(f"Saved to {out_path}")

process_konark("data/sfm/konark_sun_temple/sparse_1.ply", "static/models/konark_sun_temple_dense.ply", target_pts=50000)

