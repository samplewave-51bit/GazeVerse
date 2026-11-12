import numpy as np
from plyfile import PlyData, PlyElement

def reorient(in_ply, out_ply):
    ply = PlyData.read(in_ply)
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

    print(f"Retained {len(x_c)}/{len(x)} points | Dimensions: X={x_c.max()-x_c.min():.2f}m, Y={y_c.max():.2f}m, Z={z_c.max()-z_c.min():.2f}m")

    vertex_dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
    ]
    vertices = np.empty(len(x_c), dtype=vertex_dtype)
    vertices['x'] = x_c
    vertices['y'] = y_c
    vertices['z'] = z_c
    vertices['red'] = r_filt
    vertices['green'] = g_filt
    vertices['blue'] = b_filt

    el = PlyElement.describe(vertices, 'vertex')
    PlyData([el], text=False).write(out_ply)

reorient("data/sfm/hampi_vittala/sparse_0.ply", "data/sfm/hampi_vittala/vittala_reoriented.ply")

