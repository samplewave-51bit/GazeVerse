"""
Process, Clean, Reorient (Upright), and Export Reconstructed Heritage Models
- Inverts COLMAP Y-axis (+Y is down in COLMAP -> flip to Three.js +Y is up)
- Centers coordinates at (0, 0, 0)
- Filters statistical outliers and sky floaters
- Saves clean upright models for the interactive 3D viewer
"""

import numpy as np
from plyfile import PlyData, PlyElement
from pathlib import Path

def process_and_reorient_ply(input_ply_path, output_ply_path, remove_sky=True):
    print(f"\nProcessing {input_ply_path} -> {output_ply_path}...")
    ply = PlyData.read(input_ply_path)
    v = ply['vertex']
    
    x = np.array(v['x'], dtype=np.float32)
    y = np.array(v['y'], dtype=np.float32)
    z = np.array(v['z'], dtype=np.float32)
    
    r = np.array(v['red'], dtype=np.uint8) if 'red' in v else np.full(len(x), 200, dtype=np.uint8)
    g = np.array(v['green'], dtype=np.uint8) if 'green' in v else np.full(len(x), 180, dtype=np.uint8)
    b = np.array(v['blue'], dtype=np.uint8) if 'blue' in v else np.full(len(x), 160, dtype=np.uint8)
    
    # 1. Flip Y and Z axes to convert from COLMAP camera coordinates (Y down, Z forward)
    # to Three.js world coordinates (Y up, Z out/back)
    # R_x(180 deg): y' = -y, z' = -z
    y_up = -y
    z_up = -z
    x_up = x

    # 2. Statistical outlier removal (3 sigma)
    mask = np.ones(len(x), dtype=bool)
    for coord in [x_up, y_up, z_up]:
        med = np.median(coord)
        mad = np.median(np.abs(coord - med))
        if mad > 1e-4:
            mask &= (np.abs(coord - med) <= 4.0 * mad * 1.4826)

    # 3. Filter sky floaters (light-blue/pure-white high altitude points)
    if remove_sky:
        # Sky points are high Y with blue > red + 25 and high brightness
        is_sky = (b > (r.astype(int) + 30)) & (b > 160) & (y_up > np.percentile(y_up[mask], 70))
        mask &= ~is_sky

    x_filt = x_up[mask]
    y_filt = y_up[mask]
    z_filt = z_up[mask]
    r_filt = r[mask]
    g_filt = g[mask]
    b_filt = b[mask]

    # 4. Center coordinates at ground level (center of X/Z, min of Y at 0)
    cx = (x_filt.max() + x_filt.min()) / 2.0
    cz = (z_filt.max() + z_filt.min()) / 2.0
    min_y = y_filt.min()

    x_centered = x_filt - cx
    y_centered = y_filt - min_y  # Ground sits at Y=0
    z_centered = z_filt - cz

    print(f"  Retained {len(x_centered)}/{len(x)} points ({len(x_centered)/len(x)*100:.1f}%)")
    print(f"  Dimensions: Width(X)={x_centered.max()-x_centered.min():.2f}m, Height(Y)={y_centered.max():.2f}m, Depth(Z)={z_centered.max()-z_centered.min():.2f}m")

    # Create new PLY
    vertex_dtype = [
        ('x', 'f4'), ('y', 'f4'), ('z', 'f4'),
        ('red', 'u1'), ('green', 'u1'), ('blue', 'u1')
    ]
    vertices = np.empty(len(x_centered), dtype=vertex_dtype)
    vertices['x'] = x_centered
    vertices['y'] = y_centered
    vertices['z'] = z_centered
    vertices['red'] = r_filt
    vertices['green'] = g_filt
    vertices['blue'] = b_filt

    el = PlyElement.describe(vertices, 'vertex')
    Path(output_ply_path).parent.mkdir(parents=True, exist_ok=True)
    PlyData([el], text=False).write(output_ply_path)
    print(f"  Successfully wrote upright model to: {output_ply_path}")

if __name__ == "__main__":
    # 1. Modhera Sun Temple (from newly reconstructed 27-camera Sabha Mandapa model)
    process_and_reorient_ply(
        "data/sfm/modhera_sun_temple/modhera_full_sparse.ply",
        "static/models/modhera_sun_temple_dense.ply",
        remove_sky=True
    )

    # 2. Ellora Kailasa Temple (from newly reconstructed 22-camera, 15k point full complex model)
    process_and_reorient_ply(
        "data/sfm/ellora_kailasa/ellora_full_sparse.ply",
        "static/models/ellora_kailasa_dense.ply",
        remove_sky=True
    )

    # 3. Hampi Stone Chariot (orient upright and clean sky floaters from 76-camera reconstruction)
    process_and_reorient_ply(
        "output/3dgs/hampi_stone_chariot/input.ply",
        "static/models/hampi_stone_chariot_dense.ply",
        remove_sky=True
    )

