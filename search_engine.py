import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings
from data_processor import load_huberman_data

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

def create_vector_store():
    """Creates a vector store from the processed documents."""
    print("Loading and processing documents...")
    documents = load_huberman_data()
    print(f"Loaded {len(documents)} documents.")

    if not GOOGLE_API_KEY:
        raise ValueError("GOOGLE_API_KEY is not set. Please set it in your .env file.")

    print("Creating embeddings and vector store (this may take a few minutes)...")
    embedding_model = GoogleGenerativeAIEmbeddings(model="models/embedding-001")

    vector_store = Chroma.from_documents(
        documents=documents,
        embedding=embedding_model,
        persist_directory="./chroma_db"
    )

    print("Vector store created successfully.")
    return vector_store

if __name__ == "__main__":
    try:
        db = create_vector_store()
        query = "how to deal with addiction and boredom"
        print(f"\nPerforming a semantic search for: '{query}'")
        results = db.similarity_search(query, k=3)
        print("\nSearch Results:")
        for i, result in enumerate(results):
            print(f"--- Result {i+1} ---")
            print(f"Video Title: {result.metadata['video_title']}")
            print(f"URL: {result.metadata['video_url']}")
            print(f"Snippet:\n{result.page_content[:300]}...")
    except Exception as e:
        print(f"An error occurred: {e}")