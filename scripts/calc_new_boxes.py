import trimesh
import numpy as np
import json

mesh = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
geom = list(mesh.geometry.values())[0] if isinstance(mesh, trimesh.Scene) else mesh
v = geom.vertices

print("Total vertices:", len(v))
print("Bounds:")
print("  X:", v[:,0].min(), v[:,0].max())
print("  Y:", v[:,1].min(), v[:,1].max())
print("  Z:", v[:,2].min(), v[:,2].max())

# Now let's locate each component:
# 1. Entrance stairs & Elephants:
# In Z: front is positive Z (Z > 0.45)
# In Y: Y is from ground 0 to 0.55
# In X: |X| < 0.38
# Let's inspect:
front_elephants = v[(v[:, 2] > 0.45) & (v[:, 1] < 0.55)]
print(f"\n1. Elephants & Steps: {len(front_elephants)} pts | X: [{front_elephants[:,0].min():.2f}, {front_elephants[:,0].max():.2f}], Y: [{front_elephants[:,1].min():.2f}, {front_elephants[:,1].max():.2f}], Z: [{front_elephants[:,2].min():.2f}, {front_elephants[:,2].max():.2f}]")

# 2. Four Wheels:
# Wheels are on the sides (|X| > 0.35) near the ground (Y < 0.55)
# Two front wheels (Z in [0.0, 0.48]), Two rear wheels (Z in [-0.65, -0.15])
w_fl = v[(v[:, 0] < -0.35) & (v[:, 1] < 0.55) & (v[:, 2] > 0.0) & (v[:, 2] < 0.50)]
w_fr = v[(v[:, 0] > 0.35) & (v[:, 1] < 0.55) & (v[:, 2] > 0.0) & (v[:, 2] < 0.50)]
w_rl = v[(v[:, 0] < -0.35) & (v[:, 1] < 0.55) & (v[:, 2] < -0.10) & (v[:, 2] > -0.65)]
w_rr = v[(v[:, 0] > 0.35) & (v[:, 1] < 0.55) & (v[:, 2] < -0.10) & (v[:, 2] > -0.65)]

print(f"\n2. Front Left Wheel:  {len(w_fl):6d} pts | X: [{w_fl[:,0].min():.2f}, {w_fl[:,0].max():.2f}] Y: [{w_fl[:,1].min():.2f}, {w_fl[:,1].max():.2f}] Z: [{w_fl[:,2].min():.2f}, {w_fl[:,2].max():.2f}]")
print(f"3. Front Right Wheel: {len(w_fr):6d} pts | X: [{w_fr[:,0].min():.2f}, {w_fr[:,0].max():.2f}] Y: [{w_fr[:,1].min():.2f}, {w_fr[:,1].max():.2f}] Z: [{w_fr[:,2].min():.2f}, {w_fr[:,2].max():.2f}]")
print(f"4. Rear Left Wheel:   {len(w_rl):6d} pts | X: [{w_rl[:,0].min():.2f}, {w_rl[:,0].max():.2f}] Y: [{w_rl[:,1].min():.2f}, {w_rl[:,1].max():.2f}] Z: [{w_rl[:,2].min():.2f}, {w_rl[:,2].max():.2f}]")
print(f"5. Rear Right Wheel:  {len(w_rr):6d} pts | X: [{w_rr[:,0].min():.2f}, {w_rr[:,0].max():.2f}] Y: [{w_rr[:,1].min():.2f}, {w_rr[:,1].max():.2f}] Z: [{w_rr[:,2].min():.2f}, {w_rr[:,2].max():.2f}]")

# 6. Carved Plinth & Adhisthana:
# Base platform above wheels: Y in [0.20, 0.55], inside wheels |X| < 0.45, Z in [-0.75, 0.45]
plinth = v[(v[:, 1] >= 0.20) & (v[:, 1] <= 0.55) & (np.abs(v[:, 0]) <= 0.45) & (v[:, 2] <= 0.45)]
print(f"\n6. Adhisthana Plinth: {len(plinth):6d} pts | X: [{plinth[:,0].min():.2f}, {plinth[:,0].max():.2f}] Y: [{plinth[:,1].min():.2f}, {plinth[:,1].max():.2f}] Z: [{plinth[:,2].min():.2f}, {plinth[:,2].max():.2f}]")

# 7. Pillared Mandapa & Garuda Sanctum:
# Middle height: Y in [0.55, 1.00], Z in [-0.70, 0.40]
mandapa = v[(v[:, 1] > 0.55) & (v[:, 1] <= 1.00) & (v[:, 2] <= 0.40)]
print(f"7. Pillared Sanctum:  {len(mandapa):6d} pts | X: [{mandapa[:,0].min():.2f}, {mandapa[:,0].max():.2f}] Y: [{mandapa[:,1].min():.2f}, {mandapa[:,1].max():.2f}] Z: [{mandapa[:,2].min():.2f}, {mandapa[:,2].max():.2f}]")

# 8. Overhanging Cornice (Kapota):
# Upper cornice: Y in [1.00, 1.15]
cornice = v[(v[:, 1] > 1.00) & (v[:, 1] <= 1.15)]
print(f"8. Kapota Cornice:    {len(cornice):6d} pts | X: [{cornice[:,0].min():.2f}, {cornice[:,0].max():.2f}] Y: [{cornice[:,1].min():.2f}, {cornice[:,1].max():.2f}] Z: [{cornice[:,2].min():.2f}, {cornice[:,2].max():.2f}]")

# 9. Vimana Superstructure (Roof & Finial):
# Top tier: Y in [1.15, 1.37]
vimana = v[v[:, 1] > 1.15]
print(f"9. Vimana Tower:      {len(vimana):6d} pts | X: [{vimana[:,0].min():.2f}, {vimana[:,0].max():.2f}] Y: [{vimana[:,1].min():.2f}, {vimana[:,1].max():.2f}] Z: [{vimana[:,2].min():.2f}, {vimana[:,2].max():.2f}]")

