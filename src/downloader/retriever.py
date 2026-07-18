import chromadb
from sentence_transformers import SentenceTransformer


# IMPORTANT: Use your actual vectorstore location
CHROMA_PATH = "vectorstore"

COLLECTION_NAME = "uae_legal_documents"


# Load embedding model
model = SentenceTransformer(
    "all-MiniLM-L6-v2"
)


# Connect to existing ChromaDB
client = chromadb.PersistentClient(
    path=CHROMA_PATH
)


collection = client.get_collection(
    name=COLLECTION_NAME
)


def retrieve_documents(query, top_k=3):

    query_embedding = model.encode(
        query
    ).tolist()


    results = collection.query(
        query_embeddings=[
            query_embedding
        ],
        n_results=top_k
    )


    documents = results["documents"][0]

    metadata = results["metadatas"][0]


    return documents, metadata



# Test only
if __name__ == "__main__":

    docs, meta = retrieve_documents(
        "What is data protection law?"
    )


    for i, doc in enumerate(docs):

        print("\n========== RESULT", i+1, "==========")

        print("TITLE:")
        print(meta[i].get("title"))

        print("\nTEXT:")
        print(doc[:500])