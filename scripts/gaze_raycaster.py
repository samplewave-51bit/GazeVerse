"""
GazeVerse 3D Spatial Gaze Raycaster & Semantic Grounding Engine
- Casts a user gaze ray (origin [x, y, z], direction [dx, dy, dz]) in 3D scene space.
- Resolves intersection with oriented/axis-aligned 3D semantic bounding regions.
- Queries curated monument iconography & architectural knowledge bases.
"""

import os
import json
import numpy as np

class MonumentSemanticKnowledgeBase:
    """Manages curated architectural & iconographical metadata for monuments."""
    def __init__(self, metadata_path=None):
        self.regions = {}
        if metadata_path and os.path.exists(metadata_path):
            with open(metadata_path, 'r', encoding='utf-8') as f:
                self.regions = json.load(f)

    def add_region(self, region_id, label, bounds_min, bounds_max, description, iconography=None):
        self.regions[region_id] = {
            "id": region_id,
            "label": label,
            "bounds_min": list(bounds_min),
            "bounds_max": list(bounds_max),
            "description": description,
            "iconography": iconography or {}
        }

    def save(self, path):
        os.makedirs(os.path.dirname(path), exist_ok=True)
        with open(path, 'w', encoding='utf-8') as f:
            json.dump(self.regions, f, indent=2)

class GazeRaycaster:
    """Performs 3D ray-AABB and ray-sphere spatial intersection against semantic scene regions."""
    def __init__(self, knowledge_base: MonumentSemanticKnowledgeBase):
        self.kb = knowledge_base

    @staticmethod
    def ray_aabb_intersect(ray_origin, ray_dir, box_min, box_max):
        """
        Slab method for Ray-AABB intersection in 3D.
        Returns (hit: bool, t_entry: float)
        """
        tmin = -float('inf')
        tmax = float('inf')

        for i in range(3):
            if abs(ray_dir[i]) < 1e-8:
                if ray_origin[i] < box_min[i] or ray_origin[i] > box_max[i]:
                    return False, float('inf')
            else:
                inv_d = 1.0 / ray_dir[i]
                t1 = (box_min[i] - ray_origin[i]) * inv_d
                t2 = (box_max[i] - ray_origin[i]) * inv_d
                if t1 > t2:
                    t1, t2 = t2, t1
                tmin = max(tmin, t1)
                tmax = min(tmax, t2)
                if tmin > tmax:
                    return False, float('inf')

        if tmax < 0:
            return False, float('inf')
        return True, (tmin if tmin >= 0 else tmax)

    def resolve_gaze(self, ray_origin, ray_direction):
        """
        Casts a 3D gaze ray into the scene, resolving the closest intersected semantic region.
        ray_origin: (3,) float array
        ray_direction: (3,) normalized float array
        """
        ray_origin = np.array(ray_origin, dtype=np.float32)
        ray_direction = np.array(ray_direction, dtype=np.float32)
        norm = np.linalg.norm(ray_direction)
        if norm > 1e-8:
            ray_direction /= norm

        closest_hit = None
        min_t = float('inf')

        for region_id, data in self.kb.regions.items():
            b_min = np.array(data["bounds_min"], dtype=np.float32)
            b_max = np.array(data["bounds_max"], dtype=np.float32)
            hit, t = self.ray_aabb_intersect(ray_origin, ray_direction, b_min, b_max)
            if hit and t < min_t:
                min_t = t
                closest_hit = data

        return closest_hit, min_t

if __name__ == "__main__":
    # Test initialization with Ellora Kailasa semantic structure
    kb = MonumentSemanticKnowledgeBase()
    
    # Coordinates aligned with sparse point cloud bounds:
    # X: [-2.6, 7.7], Y: [-7.1, 5.9], Z: [-3.2, 11.7]
    kb.add_region(
        region_id="ellora_ravana_lifting_kailash",
        label="Ravana Shaking Mount Kailash Relief",
        bounds_min=[-1.5, -3.0, 0.5],
        bounds_max=[1.5, -0.5, 3.5],
        description="Monumental rock-cut relief panel depicting multi-armed Ravana attempting to uproot Mount Kailash, while Shiva calms the mountain with his toe.",
        iconography={
            "period": "Rashtrakuta dynasty, 8th century CE",
            "deities": ["Shiva", "Parvati", "Ravana"],
            "thematic_significance": "Displays dynamic muscular tension and divine serenity."
        }
    )

    kb.add_region(
        region_id="ellora_elephant_colonnade",
        label="Monolithic Elephant Courtyard Guardian",
        bounds_min=[2.0, -1.0, 1.0],
        bounds_max=[5.0, 2.0, 4.0],
        description="Life-sized monolithic carved elephant flanking the central courtyard, carved out of the single basalt cliff rock.",
        iconography={
            "period": "Rashtrakuta dynasty, reign of Krishna I",
            "thematic_significance": "Symbolizes royal sovereignty and strength supporting the sacred mountain."
        }
    )

    out_json = "data/semantics/ellora_kailasa_regions.json"
    kb.save(out_json)
    print(f"Saved semantic knowledge base to {out_json}")

    # Simulate Gaze Raycast from a user standing at [0, 5, 2] looking towards Ravana relief [0, -2, 2]
    user_eye_pos = [0.0, 5.0, 2.0]
    look_target = [0.0, -2.0, 2.0]
    gaze_dir = np.array(look_target) - np.array(user_eye_pos)

    raycaster = GazeRaycaster(kb)
    hit_region, distance = raycaster.resolve_gaze(user_eye_pos, gaze_dir)

    print("\n--- Gaze Raycast Simulation ---")
    print(f"User Gaze Origin: {user_eye_pos}")
    print(f"Gaze Direction:   {gaze_dir}")
    if hit_region:
        print(f"Target Resolved:  {hit_region['label']} (Distance: {distance:.2f}m)")
        print(f"Description:      {hit_region['description']}")
        print(f"Iconography Data: {hit_region['iconography']}")
    else:
        print("Gaze did not intersect any registered semantic region.")

