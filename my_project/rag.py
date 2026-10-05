from pathlib import Path
from sentence_transformers import SentenceTransformer
import numpy as np

from google import genai
from dotenv import load_dotenv
import os
import time
# ---------------------------------
# Load Environment Variables
# ---------------------------------

load_dotenv()

api_key = os.getenv("GEMINI_API_KEY")

client = genai.Client(api_key=api_key)

# ---------------------------------
# Load Career Knowledge
# ---------------------------------

BASE_DIR = Path(__file__).resolve().parent
KNOWLEDGE_FILE = BASE_DIR / "knowledge_base" / "career_data.txt"


def load_knowledge():
    """Read the career knowledge file."""

    with open(KNOWLEDGE_FILE, "r", encoding="utf-8") as file:
        return file.read()


# ---------------------------------
# Split Knowledge into Sections
# ---------------------------------

def create_chunks(text):
    """Split knowledge into career sections."""

    sections = text.split("CAREER: ")

    chunks = []

    for section in sections:
        section = section.strip()

        if section:
            chunks.append("CAREER: " + section)

    return chunks


# ---------------------------------
# Create Embeddings
# ---------------------------------

model = SentenceTransformer("all-MiniLM-L6-v2")


def create_embeddings(chunks):
    """Convert knowledge chunks into numerical vectors."""

    embeddings = model.encode(
        chunks,
        convert_to_numpy=True
    )

    return embeddings


# ---------------------------------
# RAG Search
# ---------------------------------

def search_career(query, top_k=2):
    """
    Find the most relevant career information
    for the user's query.
    """

    knowledge = load_knowledge()

    chunks = create_chunks(knowledge)

    embeddings = create_embeddings(chunks)

    query_embedding = model.encode(
        [query],
        convert_to_numpy=True
    )[0]

    # Normalize vectors
    embeddings_norm = embeddings / np.linalg.norm(
        embeddings,
        axis=1,
        keepdims=True
    )

    query_norm = query_embedding / np.linalg.norm(
        query_embedding
    )

    # Calculate similarity
    scores = embeddings_norm @ query_norm

    # Get best matching sections
    top_indices = np.argsort(scores)[::-1][:top_k]

    results = []

    for index in top_indices:
        results.append({
            "content": chunks[index],
            "score": float(scores[index])
        })

    return results


# ---------------------------------
# Gemini Career Recommendation
# ---------------------------------

def generate_career_response(user_query):
    """Generate a personalized career response using RAG + Gemini."""

    # Search relevant career knowledge
    results = search_career(user_query, top_k=2)

    # Combine retrieved knowledge
    context = "\n\n".join(
        result["content"] for result in results
    )

    # Create AI prompt
    prompt = f"""
You are CareerBridge, an AI-powered career guidance assistant.

Use ONLY the career information provided in the context below.

CAREER KNOWLEDGE:
{context}

STUDENT QUESTION:
{user_query}

Give a clear and beginner-friendly answer.

Include:
1. Recommended career
2. Required skills
3. Learning roadmap
4. Suggested projects

Do not invent career information that is not supported by the provided context.
"""

    # Try Gemini 3.8 Flash first
    try:
        response = client.models.generate_content(
            model="gemini-3.8-flash",
            contents=prompt
        )
        return response.text

    except Exception:
        # Fallback model if Gemini 3.8 Flash is temporarily unavailable
        response = client.models.generate_content(
            model="gemini-3.5-flash-lite",
            contents=prompt
        )
        return response.text

# ---------------------------------
# Test RAG + Gemini
# ---------------------------------

if __name__ == "__main__":

    query = "I want to become a data analyst"

    answer = generate_career_response(query)

    print("\n==============================")
    print("CAREERBRIDGE AI RESPONSE")
    print("==============================\n")

    print(answer)