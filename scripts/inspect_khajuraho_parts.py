import open3d as o3d
import numpy as np

p1 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/kandariya_1_reoriented.ply")
p2 = o3d.io.read_point_cloud("data/sfm/khajuraho_kandariya/kandariya_2_reoriented.ply")

pts1 = np.asarray(p1.points)
pts2 = np.asarray(p2.points)

print(f"P1 (Mandapa & Base): {len(pts1)} pts")
print(f"   X: [{pts1[:,0].min():.2f}, {pts1[:,0].max():.2f}]")
print(f"   Y: [{pts1[:,1].min():.2f}, {pts1[:,1].max():.2f}]")
print(f"   Z: [{pts1[:,2].min():.2f}, {pts1[:,2].max():.2f}]")

print(f"P2 (Shikhara Spire): {len(pts2)} pts")
print(f"   X: [{pts2[:,0].min():.2f}, {pts2[:,0].max():.2f}]")
print(f"   Y: [{pts2[:,1].min():.2f}, {pts2[:,1].max():.2f}]")
print(f"   Z: [{pts2[:,2].min():.2f}, {pts2[:,2].max():.2f}]")

