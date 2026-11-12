import trimesh

scene = trimesh.load('stone-chariot-in-hampi/source/model.glb')
print("Geometries in scene:")
for name, geom in scene.geometry.items():
    print(f"  {name}: {len(geom.vertices)} vertices, {len(geom.faces)} faces")
    print(f"    Bounds min: {geom.bounds[0]}")
    print(f"    Bounds max: {geom.bounds[1]}")

