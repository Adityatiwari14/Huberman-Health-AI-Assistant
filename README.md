Huberman Health AI Assistant
A Streamlit-based semantic search application that allows users to find relevant videos and specific timestamps from the Huberman Lab podcast transcripts. The app uses Google's Generative AI Embeddings and ChromaDB for efficient and accurate search.

Features 
Semantic Search: Search for content using natural language queries (e.g., "how to improve sleep hygiene" or "benefits of cold exposure").

Video & Timestamp Retrieval: The app returns the most relevant videos, along with clickable timestamps that link directly to the exact moment in the YouTube video.

Persistent Vector Store: The application creates a local, persistent vector store using ChromaDB, so the embedding process only needs to be run once.

Intuitive UI: A simple and clean user interface built with Streamlit for a great user experience.

<br>

Getting Started 🚀
Follow these steps to set up and run the project locally.

Prerequisites
Make sure you have Python 3.8 or higher installed on your system.

1. Setup
Clone the repository and navigate into the project directory:

git clone <repository_url>
cd huberman-assistant

2. Install Dependencies
Install the required Python packages from the requirements.txt file.

pip install -r requirements.txt

3. Configure API Key
Create a file named .env in the root of the project and add your Google Generative AI API key.

GOOGLE_API_KEY="your_api_key_here"

4. Build the Vector Store
Run the search_engine.py script. This is a one-time process that loads the podcast transcripts, creates embeddings, and builds the vector store in a local folder called chroma_db.

python search_engine.py

How to Use the App
After the vector store has been created, run the Streamlit application.

streamlit run app.py

This will open the app in your web browser. You can now enter your queries and start finding relevant Huberman Lab content!

File Structure 
app.py: The main Streamlit application script.

data_processor.py: Handles loading and cleaning the raw JSON data into a format suitable for embedding.

search_engine.py: The script used to create the vector store from the processed data.

requirements.txt: Lists all the necessary Python libraries.

.env: Your API key. (Not included in the repository for security)

chroma_db/: The folder containing the persistent vector store. (Created after running search_engine.py)

License
