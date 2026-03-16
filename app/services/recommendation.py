import os
import json
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq
from typing import Dict, Any, List

from app.core.config import GROQ_API_KEY, GROQ_MODEL, EMBEDDING_MODEL_NAME

class SimpleVectorStore:
    def __init__(self, storage_path: str = "app/db/knowledge_store.json"):
        self.storage_path = storage_path
        self.embedding_model = SentenceTransformer(EMBEDDING_MODEL_NAME)
        self.data = self._load()

    def _load(self):
        if os.path.exists(self.storage_path):
            with open(self.storage_path, 'r') as f:
                return json.load(f)
        return []

    def save(self):
        os.makedirs(os.path.dirname(self.storage_path), exist_ok=True)
        with open(self.storage_path, 'w') as f:
            json.dump(self.data, f)

    def add_documents(self, documents: List[str], metadatas: List[Dict] = None):
        embeddings = self.embedding_model.encode(documents)
        for i, doc in enumerate(documents):
            self.data.append({
                "text": doc,
                "embedding": embeddings[i].tolist(),
                "metadata": metadatas[i] if metadatas else {}
            })
        self.save()

    def query(self, query_text: str, n_results: int = 3) -> str:
        if not self.data:
            return ""
        
        query_embedding = self.embedding_model.encode([query_text])[0]
        
        # Calculate cosine similarity
        similarities = []
        for item in self.data:
            doc_emb = np.array(item["embedding"])
            sim = np.dot(query_embedding, doc_emb) / (np.linalg.norm(query_embedding) * np.linalg.norm(doc_emb))
            similarities.append(sim)
        
        # Get top indices
        top_indices = np.argsort(similarities)[-n_results:][::-1]
        results = [self.data[i]["text"] for i in top_indices if similarities[i] > 0.3]
        
        return "\n---\n".join(results)

class RecommendationEngine:
    def __init__(self):
        self.client = Groq(api_key=GROQ_API_KEY)
        self.vector_store = SimpleVectorStore()

    def generate_recommendation(self, disease_data: Dict[str, Any]) -> Dict[str, Any]:
        disease_name = disease_data.get("display_label", "Unknown Disease")
        crop = disease_data.get("crop", "Unknown Crop")
        severity = disease_data.get("severity", "Unknown Severity")
        
        # 1. Retrieval
        query = f"treatment and prevention for {disease_name} in {crop}"
        context = self.vector_store.query(query)
        
        # 2. Prompt
        prompt = f"""
        You are an expert agricultural consultant. Using the provided disease detection results and context, generate a professional and farmer-friendly recommendation.

        DISEASE DETECTION RESULTS:
        - Crop: {crop}
        - Detected Condition: {disease_name}
        - Severity Level: {severity}

        RELEVANT AGRICULTURAL KNOWLEDGE (CONTEXT):
        {context if context else "No specific context found. Use your internal knowledge to provide safe, general guidance."}

        TASK:
        Generate a recommendation in STRICT JSON format.

        JSON STRUCTURE:
        {{
            "disease": "{disease_name}",
            "severity": "{severity}",
            "chemical_treatment": "Detail fungicides/pesticides.",
            "organic_treatment": "Detail natural remedies.",
            "prevention": "List preventive measures."
        }}
        """

        try:
            chat_completion = self.client.chat.completions.create(
                messages=[
                    {"role": "system", "content": "You are an AI assistant that provides agricultural recommendations in JSON format."},
                    {"role": "user", "content": prompt},
                ],
                model=GROQ_MODEL,
                temperature=0.2,
                response_format={"type": "json_object"}
            )
            return json.loads(chat_completion.choices[0].message.content)
        except Exception as e:
            return {"error": str(e), "disease": disease_name, "severity": severity}

engine = RecommendationEngine()
