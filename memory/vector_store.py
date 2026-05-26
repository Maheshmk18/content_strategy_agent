from chromadb import Client
from chromadb.config import Settings as ChromaSettings
from graph.state import DayEntry

# Initialize ChromaDB client
chroma_client = Client()
collection = chroma_client.get_or_create_collection(
    name="content_plans",
    metadata={"hnsw:space": "cosine"},
)


def save_plan_to_memory(calendar: list[DayEntry], month: str, niche: str):
    """Save approved calendar to memory for future reference."""
    for day_entry in calendar:
        text = f"{day_entry['platform']} {day_entry['content_type']} - {day_entry['topic']}"
        doc_id = f"{month}_{day_entry['day']}"

        collection.add(
            ids=[doc_id],
            documents=[text],
            metadatas=[{
                "month": month,
                "day": day_entry["day"],
                "platform": day_entry["platform"],
                "content_type": day_entry["content_type"],
                "niche": niche,
            }],
        )


def query_similar_content(query: str, niche: str, k: int = 5) -> list[dict]:
    """Query for similar past content."""
    try:
        results = collection.query(
            query_texts=[query],
            n_results=k,
            where={"niche": niche},
        )

        if results and results["metadatas"]:
            return [
                {
                    "text": doc,
                    "metadata": meta,
                }
                for doc, meta in zip(results["documents"][0], results["metadatas"][0])
            ]

        return []

    except Exception as e:
        print(f"Error querying memory: {e}")
        return []
