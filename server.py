"""
GazeVerse Interactive 3D Spatial Gaze Raycasting Server
- Serves interactive 3D WebXR/Three.js viewer for the 3 heritage scenes.
- Performs real-time Ray-AABB intersection on user gaze vectors.
- Dynamically responds with AI Guide iconography and context.
"""

import os
import json
import numpy as np
from flask import Flask, request, jsonify, send_from_directory
from scripts.heritage_rag import rag_engine

app = Flask(__name__, static_folder="static")

SEMANTICS_MAP = {
    "khajuraho_kandariya": "data/semantics/khajuraho_kandariya_regions.json",
    "hampi_stone_chariot": "data/semantics/hampi_stone_chariot_regions.json",
    "konark_sun_temple": "data/semantics/konark_sun_temple_regions.json",
    "hampi_vittala": "data/semantics/hampi_vittala_regions.json",
    "ellora_kailasa": "data/semantics/ellora_kailasa_regions.json",
    "modhera_sun_temple": "data/semantics/modhera_sun_temple_regions.json"
}

def load_semantic_regions(monument_key):
    path = SEMANTICS_MAP.get(monument_key)
    if not path or not os.path.exists(path):
        return []
    with open(path, "r", encoding="utf-8") as f:
        data = json.load(f)
        if isinstance(data, dict):
            return list(data.values())
        return data

def ray_aabb_intersect(ray_origin, ray_dir, box_min, box_max):
    """3D Slab method for Ray-AABB intersection."""
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

@app.route("/")
def index():
    return send_from_directory("static", "index.html")

@app.route("/api/monuments")
def get_monuments():
    return jsonify([
        {"id": "hampi_stone_chariot", "name": "Hampi Stone Chariot (Textured 3D Mesh)", "model": "/static/models/hampi_stone_chariot_upright.glb", "format": "glb"},
        {"id": "konark_sun_temple", "name": "Konark Sun Temple (Textured 3D Mesh)", "model": "/static/models/konark_sun_temple_upright.glb", "format": "glb"}
    ])

@app.route("/api/regions/<monument_id>")
def get_regions(monument_id):
    regions = load_semantic_regions(monument_id)
    return jsonify(regions)

@app.route("/api/raycast", methods=["POST"])
def raycast_gaze():
    data = request.json or {}
    monument_id = data.get("monument_id", "ellora_kailasa")
    ray_origin = np.array(data.get("ray_origin", [0, 0, 0]), dtype=np.float32)
    ray_dir = np.array(data.get("ray_dir", [0, 0, 1]), dtype=np.float32)
    user_query = data.get("query", "Tell me about what I am looking at.")

    norm = np.linalg.norm(ray_dir)
    if norm > 1e-8:
        ray_dir /= norm

    regions = load_semantic_regions(monument_id)
    closest_region = None
    min_dist = float('inf')

    for reg in regions:
        b_min = np.array(reg["bounds_min"], dtype=np.float32)
        b_max = np.array(reg["bounds_max"], dtype=np.float32)
        hit, t = ray_aabb_intersect(ray_origin, ray_dir, b_min, b_max)
        if hit and t < min_dist:
            min_dist = t
            closest_region = reg

    if closest_region:
        hit_pos = (ray_origin + ray_dir * min_dist).tolist()
        part_id = closest_region.get("id")
        
        # Grounded RAG query from ASI & UNESCO records
        rag_res = rag_engine.query(monument_id, part_id, user_query)
        guide_reply = rag_res["answer"]
        suggested_questions = rag_res.get("suggested_questions", [])

        return jsonify({
            "hit": True,
            "region": closest_region,
            "distance": round(float(min_dist), 2),
            "hit_point": hit_pos,
            "guide_response": guide_reply,
            "suggested_questions": suggested_questions,
            "citations": rag_res.get("citations", [])
        })
    else:
        return jsonify({
            "hit": False,
            "guide_response": "Your gaze is currently directed toward unannotated space or open perimeter. Pan your gaze toward the architectural reliefs or pillars!"
        })

@app.route("/api/ask_part", methods=["POST"])
def ask_part():
    data = request.json or {}
    monument_id = data.get("monument_id", "hampi_stone_chariot")
    part_id = data.get("part_id", "")
    query = data.get("query", "Tell me about this architectural part.")
    
    rag_res = rag_engine.query(monument_id, part_id, query)
    return jsonify(rag_res)

if __name__ == "__main__":
    app.run(host="127.0.0.1", port=5000, debug=False)

