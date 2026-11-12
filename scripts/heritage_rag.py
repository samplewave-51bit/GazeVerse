"""
GazeVerse Grounded Part-Level Heritage RAG Engine
Links real-time 3D gaze raycasted architectural parts to official ASI (Archaeological Survey of India)
and UNESCO World Heritage dossiers.
"""

import os
import json
import re

KNOWLEDGE_DIR = os.path.join(os.path.dirname(__file__), "..", "data", "knowledge")

class HeritageRAG:
    def __init__(self):
        self.kb = {}
        self.load_all()

    def load_all(self):
        for monument in ["hampi_stone_chariot", "konark_sun_temple"]:
            path = os.path.join(KNOWLEDGE_DIR, f"{monument}_kb.json")
            if os.path.exists(path):
                with open(path, "r", encoding="utf-8") as f:
                    self.kb[monument] = json.load(f)
            else:
                self.kb[monument] = {"parts": {}}

    def get_part_dossier(self, monument_id, part_id):
        m_data = self.kb.get(monument_id, {})
        parts = m_data.get("parts", {})
        return parts.get(part_id, None)

    def query(self, monument_id, part_id, user_query):
        """
        Answers a user query strictly grounded in the ASI & UNESCO knowledge dossier for part_id.
        """
        dossier = self.get_part_dossier(monument_id, part_id)
        if not dossier:
            return {
                "success": False,
                "answer": "This architectural component does not yet have an indexed ASI/UNESCO dossier.",
                "citations": []
            }

        q_lower = user_query.lower()
        
        # 1. Check curated QA for high-similarity matches
        best_qa = None
        best_score = 0
        q_words = set(re.findall(r'\w+', q_lower))

        for qa in dossier.get("curated_qa", []):
            qa_words = set(re.findall(r'\w+', qa["question"].lower()))
            overlap = len(q_words.intersection(qa_words))
            score = overlap / max(1, len(qa_words))
            if score > best_score and overlap >= 2:
                best_score = score
                best_qa = qa

        # If a direct high-confidence match is found:
        if best_qa and best_score >= 0.25:
            body = best_qa["answer"]
        else:
            # Synthesize grounded answer from canonical context
            # Detect thematic focus:
            if any(w in q_lower for w in ["who", "built", "king", "ruler", "patron", "dynasty", "date", "when", "century", "year"]):
                body = f"According to historical and epigraphical records, this feature is attributed to: {dossier.get('epigraphy', 'historical documentation')}. {dossier.get('historical_context', '')}"
            elif any(w in q_lower for w in ["meaning", "symbol", "represent", "why", "theology", "god", "deity"]):
                body = f"Theological and iconographical significance: {dossier.get('theological_significance', '')}. {dossier.get('historical_context', '')}"
            elif any(w in q_lower for w in ["term", "name", "sanskrit", "style", "architecture"]):
                body = f"In classical temple architecture manuals, this component is termed '{dossier.get('canonical_term', '')}'. {dossier.get('historical_context', '')}"
            else:
                body = f"{dossier.get('historical_context', '')} {dossier.get('theological_significance', '')}"

        # Construct authoritative cited response
        citations = [
            f"ASI: {dossier.get('asi_citation', 'Archaeological Survey of India Records')}",
            f"UNESCO: {dossier.get('unesco_reference', 'World Heritage Dossier')}",
            f"Epigraphy: {dossier.get('epigraphy', 'Temple Inscriptions')}"
        ]

        formatted_answer = (
            f"**{dossier.get('canonical_term', 'Architectural Component')}**\n\n"
            f"{body}\n\n"
            f"**Grounding & Archaeological Citations:**\n"
            f"- **ASI Authority:** {dossier.get('asi_citation', 'ASI Memoir Archive')}\n"
            f"- **UNESCO Record:** {dossier.get('unesco_reference', 'UNESCO World Heritage Dossier')}\n"
            f"- **Epigraphical Source:** {dossier.get('epigraphy', 'Historical Inscription')}"
        )

        return {
            "success": True,
            "part_id": part_id,
            "canonical_term": dossier.get("canonical_term", ""),
            "answer": formatted_answer,
            "citations": citations,
            "suggested_questions": [qa["question"] for qa in dossier.get("curated_qa", [])]
        }

rag_engine = HeritageRAG()

if __name__ == "__main__":
    # Test query
    res = rag_engine.query("konark_sun_temple", "konark_chariot_plinth_wheels", "How do these wheels tell time?")
    print(res["answer"])
