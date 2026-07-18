import json
import os

import chromadb
from sentence_transformers import SentenceTransformer
from tqdm import tqdm


# ==============================
# CONFIGURATION
# ==============================

INPUT_FILE = "processed/legal_chunks.json"

CHROMA_PATH = "vectorstore"


COLLECTION_NAME = "uae_legal_documents"



# ==============================
# LOAD CHUNKS
# ==============================

def load_chunks():

    with open(
        INPUT_FILE,
        "r",
        encoding="utf-8"
    ) as f:

        data = json.load(f)


    print(
        "Total chunks loaded:",
        len(data)
    )

    return data



# ==============================
# CREATE VECTOR DATABASE
# ==============================

def create_vector_database(chunks):


    print("\nLoading embedding model...")


    model = SentenceTransformer(
        "all-MiniLM-L6-v2"
    )


    print("Creating Chroma database...")


    client = chromadb.PersistentClient(
        path=CHROMA_PATH
    )


    collection = client.get_or_create_collection(
        name=COLLECTION_NAME
    )


    documents=[]
    embeddings=[]
    metadatas=[]
    ids=[]



    print("\nGenerating embeddings...")


    for index,item in tqdm(
        enumerate(chunks),
        total=len(chunks)
    ):


        text=item["text"]


        embedding = model.encode(
            text
        ).tolist()


        documents.append(text)

        embeddings.append(
            embedding
        )


        metadatas.append(
            item["metadata"]
        )


        ids.append(
            str(index)
        )



    collection.add(

        documents=documents,

        embeddings=embeddings,

        metadatas=metadatas,

        ids=ids

    )


    print(
        "\nVector database created successfully!"
    )

    print(
        "Total vectors:",
        collection.count()
    )



# ==============================
# MAIN
# ==============================


if __name__=="__main__":


    chunks = load_chunks()


    create_vector_database(
        chunks
    )