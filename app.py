import streamlit as st
import os
from dotenv import load_dotenv
from langchain_community.vectorstores import Chroma
from langchain_google_genai import GoogleGenerativeAIEmbeddings

# Load environment variables
load_dotenv()
GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")

@st.cache_resource
def load_database():
    """Loads the persistent ChromaDB database."""
    if not GOOGLE_API_KEY:
        st.error("GOOGLE_API_KEY is not set. Please set it in your .env file.")
        return None

    # Use the synchronous 'rest' transport to avoid the event loop error
    embedding_model = GoogleGenerativeAIEmbeddings(
        model="models/embedding-001",
        transport="rest"
    )
    try:
        return Chroma(persist_directory="./chroma_db", embedding_function=embedding_model)
    except Exception as e:
        st.error(f"Error loading database: {e}")
        return None

# --- Streamlit App UI ---
st.title("Huberman Health AI Assistant")
st.markdown("A simple AI assistant to find relevant videos and timestamps from the Huberman Lab podcast.")

# Health Disclaimer
st.warning("""
**Health Disclaimer:** This tool is for informational purposes only. It is not a substitute for professional medical advice, diagnosis, or treatment. Always seek the advice of your physician or other qualified health provider with any questions you may have regarding a medical condition.
""")

# Load the database
db = load_database()
if db:
    query = st.text_input("Enter your health query (e.g., 'I have stomach ache'):")

    if query:
        with st.spinner("Searching for relevant information..."):
            try:
                results = db.similarity_search_with_score(query, k=3)

                st.subheader("Recommended Videos:")
                for doc, score in results:
                    video_title = doc.metadata.get('video_title')
                    video_url = doc.metadata.get('video_url')
                    timestamps_str = doc.metadata.get('timestamps', '')
                    timestamps = timestamps_str.split(" | ") if timestamps_str else []

                    st.markdown(f"**Video:** [{video_title}]({video_url})")
                    st.markdown(f"**Relevance Score:** {score:.4f}")

                    # Display timestamps as clickable links
                    if timestamps:
                        st.markdown("**Relevant Timestamps:**")
                        for ts in timestamps:
                            try:
                                time_part, description = ts.split(' ', 1)
                                # Convert timestamp string to seconds for YouTube URL
                                time_parts = time_part.split(':')
                                seconds = 0
                                if len(time_parts) == 3:
                                    seconds = int(time_parts[0]) * 3600 + int(time_parts[1]) * 60 + int(time_parts[2])
                                elif len(time_parts) == 2:
                                    seconds = int(time_parts[0]) * 60 + int(time_parts[1])

                                st.markdown(f"- [{time_part}]({video_url}&t={seconds}s) {description}")
                            except (ValueError, IndexError):
                                st.markdown(f"- {ts}")

                    st.markdown("---")
            except Exception as e:
                st.error(f"An error occurred during the search: {e}")