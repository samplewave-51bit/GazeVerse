import numpy as np
from plyfile import PlyData, PlyElement

ply = PlyData.read("output/3dgs/hampi_stone_chariot/point_cloud/iteration_1000/point_cloud.ply")
v = ply['vertex']
print("Fields in 3dgs ply:", [p.name for p in v.properties])

x = np.array(v['x'])
y = np.array(v['y'])
z = np.array(v['z'])
opacity = 1.0 / (1.0 + np.exp(-np.array(v['opacity'])))
print(f"Total Gaussians: {len(x)}, Opacity > 0.2: {(opacity > 0.2).sum()}")

# Compute RGB from DC spherical harmonic
SH_C0 = 0.28209479177387814
r = np.clip(np.floor((0.5 + SH_C0 * np.array(v['f_dc_0'])) * 255), 0, 255).astype(np.uint8)
g = np.clip(np.floor((0.5 + SH_C0 * np.array(v['f_dc_1'])) * 255), 0, 255).astype(np.uint8)
b = np.clip(np.floor((0.5 + SH_C0 * np.array(v['f_dc_2'])) * 255), 0, 255).astype(np.uint8)

print(f"RGB means: R={r.mean():.1f}, G={g.mean():.1f}, B={b.mean():.1f}")

