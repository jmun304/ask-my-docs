import re
from langchain_text_splitters import RecursiveCharacterTextSplitter

# =========================================================
# TEXT CLEANING
# =========================================================


def clean_text(text: str) -> str:
    """
    Real PDF text cleaning layer:
    - fixes broken line wraps
    - removes hyphenation artifacts
    - normalizes whitespace
    - restores sentence flow
    """

    # 1. Basic trim
    text = text.strip()

    # 2. Fix hyphenated line breaks
    # "well-\nbeing" → "wellbeing"
    text = re.sub(r"-\s*\n\s*", "", text)

    # 3. Replace single newlines between words with space
    # BUT preserve paragraph breaks (2+ newlines)
    text = re.sub(r"(?<!\n)\n(?!\n)", " ", text)

    # 4. Collapse multiple spaces/tabs
    text = re.sub(r"[ \t]+", " ", text)

    # 5. Fix spacing before punctuation
    text = re.sub(r"\s+([.,;:!?])", r"\1", text)

    # 6. Fix weird spacing around apostrophes (common PDF issue)
    text = re.sub(r"\s+’\s+", "’", text)

    # 7. Collapse leftover double spaces again (safe pass)
    text = re.sub(r" {2,}", " ", text)

    return text


# =========================================================
# CHUNKING (RAG-OPTIMIZED)
# =========================================================
def chunk_text(text: str) -> list[str]:
    """
    Splits text into semantically meaningful chunks for embedding + retrieval.

    This version:
    - Uses hierarchical separators (paragraph → sentence → word)
    - Preserves meaning boundaries instead of blindly cutting words
    - Uses overlap to improve retrieval continuity
    """

    text_splitter = RecursiveCharacterTextSplitter(
        # Target chunk size in CHARACTERS (not words)
        # 700–1000 chars is usually a good balance for embeddings
        chunk_size=800,

        # Overlap helps preserve context between adjacent chunks without duplicating full content
        chunk_overlap=100,

        # Character-based length is more stable than word-based
        length_function=len,

        # IMPORTANT: hierarchical splitting strategy
        # This is what makes chunks "smart"
        separators=[
            "\n\n",  # paragraph boundary (best case split)
            "\n",  # line break
            ". ",  # sentence boundary
            " ",  # fallback: word-level split
            ""  # last resort: character split
        ],
    )

    # Returns a list of text chunks
    return text_splitter.split_text(text)


# =========================================================
# DEBUG / UI HELPER
# =========================================================
def get_preview_of_chunk(chunk: str, num_words: int = 10) -> str:
    """
    Returns a short preview of a chunk for debugging or UI display.
    """

    words = chunk.split()
    return " ".join(words[:num_words])
