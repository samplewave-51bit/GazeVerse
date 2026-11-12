import struct
from pathlib import Path

def read_images_binary(path_to_model_file):
    images = {}
    with open(path_to_model_file, "rb") as fid:
        num_reg_images = struct.unpack("<Q", fid.read(8))[0]
        for _ in range(num_reg_images):
            binary_image_properties = fid.read(64)
            image_id, qw, qx, qy, qz, tx, ty, tz, camera_id = struct.unpack(
                "<idddddddi", binary_image_properties
            )
            image_name = ""
            current_char = struct.unpack("<c", fid.read(1))[0]
            while current_char != b"\x00":
                image_name += current_char.decode("utf-8")
                current_char = struct.unpack("<c", fid.read(1))[0]
            num_points2D = struct.unpack("<Q", fid.read(8))[0]
            fid.read(num_points2D * 24)
            images[image_id] = image_name
    return images

for model_id in ['1', '2']:
    p = Path(f'data/sfm/khajuraho_kandariya/sparse/{model_id}/images.bin')
    if p.exists():
        imgs = read_images_binary(p)
        print(f"\nModel {model_id} has {len(imgs)} images:")
        for k, name in sorted(imgs.items())[:10]:
            print(f"  {k}: {name}")

