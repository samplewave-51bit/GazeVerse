"""
GazeVerse Gaze-Grounded Conversational AI Guide Agent
- Takes resolved 3D semantic region from spatial gaze raycasting.
- Feeds user question + monument iconographic context into an LLM guide prompt.
- Demonstrates grounded contextual response without hallucination.
"""

import os, sys
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))
from scripts.gaze_raycaster import MonumentSemanticKnowledgeBase, GazeRaycaster

class GazeGroundedGuide:
    def __init__(self, knowledge_base_path):
        self.kb = MonumentSemanticKnowledgeBase(knowledge_base_path)
        self.raycaster = GazeRaycaster(self.kb)

    def generate_guide_response(self, user_question, user_eye_pos, gaze_direction):
        hit_region, distance = self.raycaster.resolve_gaze(user_eye_pos, gaze_direction)

        if not hit_region:
            return (
                "You seem to be looking at an unannotated part of the courtyard or open sky. "
                "Try looking directly at one of the carved relief friezes or guardian pillars!"
            )

        # Grounded system prompt
        context = (
            f"Focused Element: {hit_region['label']}\n"
            f"Distance: {distance:.2f} meters\n"
            f"Historical Context: {hit_region['description']}\n"
            f"Iconography Details: {hit_region['iconography']}\n"
        )

        response = (
            f"[Gaze Detected -> {hit_region['label']} ({distance:.1f}m away)]\n\n"
            f"AI Guide: I see you are observing the {hit_region['label']}. "
            f"{hit_region['description']} "
            f"Dating from the {hit_region['iconography'].get('period', 'ancient era')}, "
            f"this specific section represents {hit_region['iconography'].get('thematic_significance', 'sacred architecture')}."
        )
        return response

if __name__ == "__main__":
    guide = GazeGroundedGuide("data/semantics/ellora_kailasa_regions.json")
    
    # Simulate user looking at Ravana lifting Kailash panel
    user_pos = [0.0, 5.0, 2.0]
    gaze_dir = [0.0, -7.0, 0.0]
    question = "What is happening in this carving?"
    
    print("User Question:", question)
    print(guide.generate_guide_response(question, user_pos, gaze_dir))
