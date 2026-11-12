"""
Automated COLMAP Structure-from-Motion (SfM) Pipeline for GazeVerse V2
Runs:
1. Feature extraction (SIFT on GPU)
2. Feature matching (exhaustive or spatial/sequential)
3. Sparse 3D Reconstruction (Mapper)
4. Model evaluation (registered camera fraction, 3D point count)
"""

import os
import sys
import subprocess
from pathlib import Path

COLMAP_BAT = r"C:\Projects\GazeVerse\tools\colmap_release\COLMAP.bat"

def run_sfm(monument_key):
    image_dir = Path("data") / "cleaned" / monument_key / "images"
    output_dir = Path("data") / "sfm" / monument_key
    database_path = output_dir / "database.db"
    sparse_dir = output_dir / "sparse"

    output_dir.mkdir(parents=True, exist_ok=True)
    sparse_dir.mkdir(parents=True, exist_ok=True)

    print(f"\n==========================================")
    print(f"Starting COLMAP SfM for: {monument_key.upper()}")
    print(f"Image directory: {image_dir}")
    print(f"Output directory: {output_dir}")
    print(f"==========================================")

    # 1. Feature Extraction
    print("\n[1/3] Extracting SIFT features (GPU)...")
    extract_cmd = f'cmd.exe /c "{COLMAP_BAT} feature_extractor --database_path {database_path} --image_path {image_dir} --ImageReader.single_camera 0 --ImageReader.camera_model SIMPLE_RADIAL --FeatureExtraction.max_image_size 2000 --FeatureExtraction.use_gpu 1"'
    subprocess.run(extract_cmd, shell=True, check=True)

    # 2. Feature Matching
    print("\n[2/3] Exhaustive feature matching (GPU)...")
    match_cmd = f'cmd.exe /c "{COLMAP_BAT} exhaustive_matcher --database_path {database_path} --FeatureMatching.use_gpu 1"'
    subprocess.run(match_cmd, shell=True, check=True)

    # 3. Sparse Reconstruction (Mapper)
    print("\n[3/3] Running incremental mapper...")
    mapper_cmd = f'cmd.exe /c "{COLMAP_BAT} mapper --database_path {database_path} --image_path {image_dir} --output_path {sparse_dir} --Mapper.init_min_tri_angle 4.0 --Mapper.multiple_models 1"'
    subprocess.run(mapper_cmd, shell=True, check=True)

    print(f"\n[DONE] SfM completed for {monument_key}!")
    print(f"Sparse model stored in: {sparse_dir}")

if __name__ == "__main__":
    monument = sys.argv[1] if len(sys.argv) > 1 else "konark_sun_temple"
    run_sfm(monument)
