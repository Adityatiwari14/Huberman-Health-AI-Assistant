import json
from langchain.schema import Document

def load_huberman_data(file_path="dataset_youtube-scraper_2025-09-05_09-56-34-887.json"):
    """Loads data from the JSON file and processes it into LangChain Documents."""
    with open(file_path, 'r', encoding='utf-8') as f:
        data = json.load(f)

    documents = []
    for video in data:
        # Extract relevant information
        video_url = video.get('url')
        video_title = video.get('title')
        video_text = video.get('text', '')

        # We will process the subtitles for more detailed context
        subtitles_content = ""
        if 'subtitles' in video:
            for subtitle_entry in video['subtitles']:
                if 'srt' in subtitle_entry:
                    lines = subtitle_entry['srt'].split('\n')
                    text_lines = [line for line in lines if '-->' not in line and not line.strip().isdigit() and line.strip() != '']
                    subtitles_content = " ".join(text_lines)
                    break

        # Extract timestamps and join them into a single string
        timestamps = video_text.split("Timestamps\n")[-1].split("\n") if "Timestamps\n" in video_text else []
        timestamps_str = " | ".join(timestamps)

        if video_title and subtitles_content:
            # Combine all text for embedding
            full_text = f"Title: {video_title}\nDescription: {video_text}\nTranscript: {subtitles_content}"
            metadata = {
                "source": "hubermanlab",
                "video_title": video_title,
                "video_url": video_url,
                "timestamps": timestamps_str
            }
            documents.append(Document(page_content=full_text, metadata=metadata))

    return documents

if __name__ == "__main__":
    docs = load_huberman_data()
    print(f"Loaded {len(docs)} documents.")
    if docs:
        print("\nExample Document:")
        print(docs[0].metadata)
        print("--- Content Snippet ---")
        print(docs[0].page_content[:500])