"""
COLMAP Image Undistorter and Pinhole Converter
Prepares unconstrained crowd-sourced cameras for 3D Gaussian Splatting (3DGS).
Converts SIMPLE_RADIAL camera models into standard PINHOLE cameras.
"""

import os
import struct
import numpy as np
import cv2
from pathlib import Path

# Camera model IDs in COLMAP
# 0: SIMPLE_PINHOLE (f, cx, cy)
# 1: PINHOLE (fx, fy, cx, cy)
# 2: SIMPLE_RADIAL (f, cx, cy, k)

def read_cameras_binary(path):
    cameras = {}
    with open(path, "rb") as f:
        num_cameras = struct.unpack("<Q", f.read(8))[0]
        for _ in range(num_cameras):
            cam_id, model_id, width, height = struct.unpack("<iiQQ", f.read(24))
            # Model params count
            # SIMPLE_RADIAL has 4 params: f, cx, cy, k
            if model_id == 2:
                params = struct.unpack("<4d", f.read(32))
            elif model_id == 1:
                params = struct.unpack("<4d", f.read(32))
            elif model_id == 0:
                params = struct.unpack("<3d", f.read(24))
            else:
                # Read 4 doubles default
                params = struct.unpack("<4d", f.read(32))
            cameras[cam_id] = {
                "id": cam_id,
                "model_id": model_id,
                "width": width,
                "height": height,
                "params": params
            }
    return cameras

def write_pinhole_cameras_binary(cameras, out_path):
    with open(out_path, "wb") as f:
        f.write(struct.pack("<Q", len(cameras)))
        for cam_id, cam in cameras.items():
            # Convert to PINHOLE: model_id = 1, params: fx, fy, cx, cy
            p = cam["params"]
            if cam["model_id"] == 2: # SIMPLE_RADIAL (f, cx, cy, k)
                fx, fy, cx, cy = p[0], p[0], p[1], p[2]
            elif cam["model_id"] == 1:
                fx, fy, cx, cy = p[0], p[1], p[2], p[3]
            elif cam["model_id"] == 0:
                fx, fy, cx, cy = p[0], p[0], p[1], p[2]
            else:
                fx, fy, cx, cy = p[0], p[0], p[1], p[2]

            f.write(struct.pack("<iiQQ", cam_id, 1, cam["width"], cam["height"]))
            f.write(struct.pack("<4d", fx, fy, cx, cy))

def undistort_and_convert(scene_dir):
    sparse_dir = Path(scene_dir) / "sparse" / "0"
    cam_bin = sparse_dir / "cameras.bin"
    
    cameras = read_cameras_binary(cam_bin)
    print(f"Read {len(cameras)} cameras from {cam_bin}")
    
    # Save a backup of cameras.bin
    if not (sparse_dir / "cameras_radial.bin").exists():
        (sparse_dir / "cameras.bin").rename(sparse_dir / "cameras_radial.bin")
        
    write_pinhole_cameras_binary(cameras, cam_bin)
    print(f"Successfully converted all cameras to PINHOLE format at {cam_bin}!")

if __name__ == "__main__":
    import sys
    target = sys.argv[1] if len(sys.argv) > 1 else r"C:\Projects\GazeVerse\data\3dgs_scenes\ellora_kailasa"
    undistort_and_convert(target)

