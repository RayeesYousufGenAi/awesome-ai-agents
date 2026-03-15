"""
YouTube Video Summarizer — Generate AI summaries from YouTube video transcripts.
Extracts transcripts using youtube-transcript-api and generates summaries using GPT-4.
Author: Rayees Yousuf (@RayeesYousufGenAi)
"""

import os
import re
from typing import Optional

import streamlit as st
from dotenv import load_dotenv
from openai import OpenAI
from youtube_transcript_api import YouTubeTranscriptApi
from youtube_transcript_api._errors import TranscriptsDisabled, NoTranscriptFound, VideoUnavailable

load_dotenv()

# Validate OpenAI API key early for clearer error messages
openai_api_key = os.environ.get("OPENAI_API_KEY")
if not openai_api_key:
    raise ValueError(
        "OPENAI_API_KEY environment variable is not set. "
        "Please set it in your .env file or environment variables."
    )

st.set_page_config(
    page_title="📺 YouTube Video Summarizer",
    page_icon="📺",
    layout="wide"
)
st.title("📺 YouTube Video Summarizer")
st.caption("Paste a YouTube URL and get an AI-generated summary with key points from the transcript")

client = OpenAI(api_key=openai_api_key)

MAX_CHUNK_SIZE = 4000  # Characters per chunk to stay within token limits
MAX_TOTAL_CHARS = 50000  # Maximum characters to process for very long videos


def extract_video_id(url: str) -> Optional[str]:
    """Extract YouTube video ID from various URL formats.

    Supports:
    - https://www.youtube.com/watch?v=VIDEO_ID
    - https://youtu.be/VIDEO_ID
    - https://youtube.com/embed/VIDEO_ID
    - https://www.youtube.com/v/VIDEO_ID

    Args:
        url: The YouTube URL to parse.

    Returns:
        The video ID string or None if not found.
    """
    patterns = [
        r'(?:youtube\.com/watch\?v=|youtu\.be/|youtube\.com/embed/|youtube\.com/v/|youtube\.com/shorts/)([a-zA-Z0-9_-]{11})',
        r'youtube\.com/watch\?.*v=([a-zA-Z0-9_-]{11})',
    ]

    for pattern in patterns:
        match = re.search(pattern, url)
        if match:
            return match.group(1)
    return None


def get_transcript(video_id: str) -> str:
    """Fetch transcript for a YouTube video.

    Args:
        video_id: The YouTube video ID.

    Returns:
        The full transcript text.

    Raises:
        ValueError: If transcript is disabled, not found, or video is unavailable.
        Exception: For other API errors.
    """
    try:
        transcript_list = YouTubeTranscriptApi.get_transcript(video_id, proxies={"timeout": 30})
        transcript_text = " ".join([segment["text"] for segment in transcript_list])
        return transcript_text
    except TranscriptsDisabled:
        raise ValueError("Transcripts are disabled for this video.")
    except NoTranscriptFound:
        raise ValueError("No transcript found for this video. It may not have captions available.")
    except VideoUnavailable:
        raise ValueError("This video is unavailable. It may be private, deleted, or region-restricted.")
    except Exception as e:
        raise ValueError(f"Error fetching transcript: {str(e)}")


def split_transcript(transcript: str, chunk_size: int = MAX_CHUNK_SIZE) -> list[str]:
    """Split transcript into chunks for processing long videos.

    Args:
        transcript: The full transcript text.
        chunk_size: Maximum characters per chunk.

    Returns:
        List of transcript chunks.
    """
    # Limit total transcript length to avoid excessive API costs
    if len(transcript) > MAX_TOTAL_CHARS:
        transcript = transcript[:MAX_TOTAL_CHARS]
        st.info(f"Transcript truncated to {MAX_TOTAL_CHARS:,} characters for processing.")

    chunks = []
    sentences = transcript.split(". ")
    current_chunk = ""

    for sentence in sentences:
        if len(current_chunk) + len(sentence) + 2 <= chunk_size:
            current_chunk += sentence + ". "
        else:
            if current_chunk:
                chunks.append(current_chunk.strip())
            current_chunk = sentence + ". "

    if current_chunk:
        chunks.append(current_chunk.strip())

    return chunks


def summarize_chunk(chunk: str, chunk_index: int, total_chunks: int) -> str:
    """Generate summary for a single transcript chunk.

    Args:
        chunk: The transcript chunk text.
        chunk_index: Index of this chunk (0-based).
        total_chunks: Total number of chunks.

    Returns:
        The generated summary for this chunk.
    """
    context = ""
    if total_chunks > 1:
        context = f"This is part {chunk_index + 1} of {total_chunks} of the video transcript. "

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert video summarizer. Summarize YouTube video transcripts "
                    "by extracting the key points, main ideas, and important details. "
                    "Be concise but comprehensive. Use bullet points for clarity."
                ),
            },
            {
                "role": "user",
                "content": f"{context}Summarize this video transcript section:\n\n{chunk}"
            },
        ],
        temperature=0.3,
        max_tokens=500,
        timeout=60,
    )
    return response.choices[0].message.content


def combine_summaries(summaries: list[str], video_url: str) -> str:
    """Combine chunk summaries into final structured summary.

    Args:
        summaries: List of summaries from each chunk.
        video_url: Original YouTube URL for reference.

    Returns:
        Final formatted summary with all key points.
    """
    if len(summaries) == 1:
        return summaries[0]

    combined_text = "\n\n".join([
        f"Section {i + 1}:\n{summary}" for i, summary in enumerate(summaries)
    ])

    response = client.chat.completions.create(
        model="gpt-4",
        messages=[
            {
                "role": "system",
                "content": (
                    "You are an expert at creating comprehensive video summaries. "
                    "Combine multiple section summaries into a clear, well-structured summary "
                    "with the following sections:\n"
                    "1. **Overview** — Brief description of what the video is about\n"
                    "2. **Key Points** — Main takeaways and important information\n"
                    "3. **Notable Details** — Specific facts, figures, or insights mentioned\n"
                    "Use markdown formatting with headers and bullet points."
                ),
            },
            {
                "role": "user",
                "content": f"Create a final summary from these sections:\n\n{combined_text}"
            },
        ],
        temperature=0.3,
        max_tokens=800,
        timeout=60,
    )

    final_summary = response.choices[0].message.content
    return final_summary


def summarize_video(url: str) -> str:
    """Main function to summarize a YouTube video from its URL.

    Args:
        url: The YouTube URL.

    Returns:
        The generated summary.

    Raises:
        ValueError: If URL is invalid or transcript cannot be fetched.
    """
    video_id = extract_video_id(url)
    if not video_id:
        raise ValueError("Invalid YouTube URL. Please provide a valid YouTube URL.")

    transcript = get_transcript(video_id)

    if not transcript.strip():
        raise ValueError("Transcript is empty. This video may not have captions.")

    chunks = split_transcript(transcript)
    chunk_summaries = []

    # Summarize each chunk
    for i, chunk in enumerate(chunks):
        chunk_summary = summarize_chunk(chunk, i, len(chunks))
        chunk_summaries.append(chunk_summary)

    # Combine summaries
    final_summary = combine_summaries(chunk_summaries, url)

    return final_summary


# UI
col1, col2 = st.columns([3, 1])

with col1:
    url = st.text_input(
        "🔗 Enter YouTube URL:",
        placeholder="https://www.youtube.com/watch?v=..."
    )

with col2:
    st.markdown("&nbsp;  ")
    summarize_button = st.button("📝 Summarize", type="primary", use_container_width=True)

# Error message placeholder
error_placeholder = st.empty()

if summarize_button:
    if not url:
        error_placeholder.warning("Please enter a YouTube URL!")
    else:
        try:
            with st.spinner("📺 Extracting transcript and generating summary..."):
                summary = summarize_video(url)

            st.markdown("---")
            st.subheader("📝 Video Summary")
            st.markdown(summary)

        except ValueError as e:
            error_placeholder.error(f"⚠️ {str(e)}")
        except Exception as e:
            error_placeholder.error(f"⚠️ An unexpected error occurred: {str(e)}")

# Footer
st.markdown("---")
st.caption("💡 Tip: Works best with videos that have English captions. Very long videos are automatically chunked for processing.")
