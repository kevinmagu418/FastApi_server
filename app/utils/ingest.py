import os
from app.services.recommendation import SimpleVectorStore
from app.core.config import KNOWLEDGE_DIR

def ingest_knowledge():
    if not os.path.exists(KNOWLEDGE_DIR):
        os.makedirs(KNOWLEDGE_DIR)
        print(f"Created {KNOWLEDGE_DIR}. Please add your .txt files there.")
        return

    store = SimpleVectorStore()
    files = [f for f in os.listdir(KNOWLEDGE_DIR) if f.endswith('.txt')]
    
    if not files:
        print("No knowledge files found to ingest.")
        return

    for file_name in files:
        print(f"Ingesting {file_name}...")
        with open(os.path.join(KNOWLEDGE_DIR, file_name), 'r', encoding='utf-8') as f:
            content = f.read()
            chunks = [c.strip() for c in content.split('\n\n') if c.strip()]
            
            store.add_documents(
                documents=chunks,
                metadatas=[{"source": file_name} for _ in chunks]
            )
    
    print("Ingestion complete!")

if __name__ == "__main__":
    ingest_knowledge()
