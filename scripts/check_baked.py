import trimesh

scene = trimesh.load('static/models/hampi_stone_chariot_upright.glb')
print("Scene type:", type(scene))
if isinstance(scene, trimesh.Scene):
    print("Scene bounds:", scene.bounds)
    print("Scene extents:", scene.extents)
    # Concatenate all geometries with their scene transforms baked in
    baked = scene.to_geometry()
    print("Baked bounds:", baked.bounds)

