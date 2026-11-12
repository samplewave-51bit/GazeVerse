import open3d as o3d
import numpy as np

p1 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/model_1.ply")
p2 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/model_2.ply")

print("Model 1:")
print("  Points:", len(p1.points))
print("  Bounds min:", p1.get_min_bound())
print("  Bounds max:", p1.get_max_bound())

print("Model 2:")
print("  Points:", len(p2.points))
print("  Bounds min:", p2.get_min_bound())
print("  Bounds max:", p2.get_max_bound())

