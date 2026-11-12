import numpy as np
from plyfile import PlyData, PlyElement
from pathlib import Path

for name in ['model_1', 'model_2', 'sparse_0', 'sparse_1', 'sparse_2', 'sparse_merged']:
    p_path = Path(f'data/sfm/khajuraho_kandariya/{name}.ply')
    if p_path.exists():
        p = PlyData.read(str(p_path))
        v = p['vertex']
        x, y, z = np.array(v['x']), np.array(v['y']), np.array(v['z'])
        r = np.array(v['red']) if 'red' in v else []
        g = np.array(v['green']) if 'green' in v else []
        b = np.array(v['blue']) if 'blue' in v else []
        avg_rgb = f"R:{r.mean():.1f} G:{g.mean():.1f} B:{b.mean():.1f}" if len(r) else "no rgb"
        print(f"{name:15}: {len(x):5} pts | X:[{x.min():6.2f}, {x.max():6.2f}] Y:[{y.min():6.2f}, {y.max():6.2f}] Z:[{z.min():6.2f}, {z.max():6.2f}] | {avg_rgb}")

