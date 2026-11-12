import open3d as o3d
import numpy as np

p1 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/kandariya_1_reoriented.ply")
p2 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/kandariya_2_reoriented.ply")

print("P1 points:", len(p1.points))
print("P2 points:", len(p2.points))

# Let's inspect the point distributions
b1 = p1.get_axis_aligned_bounding_box()
b2 = p2.get_axis_aligned_bounding_box()
print("P1 bounds min:", b1.min_bound, "max:", b1.max_bound)
print("P2 bounds min:", b2.min_bound, "max:", b2.max_bound)

