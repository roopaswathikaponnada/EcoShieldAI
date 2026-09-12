"""
EcoShield AI
RAG Vector Store

This module converts loaded knowledge-base documents into
searchable text chunks using TF-IDF vectorization.

Responsibilities:
- Split knowledge documents into retrieval-friendly chunks
- Preserve source/document metadata for every chunk
- Build a TF-IDF vector index
- Provide similarity search over knowledge chunks
- Keep vector indexing separate from retrieval orchestration

This module does NOT:
- load Markdown files directly
- call an LLM
- generate final user recommendations
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Iterable

import numpy as np

from sklearn.feature_extraction.text import (
    TfidfVectorizer,
)

from sklearn.metrics.pairwise import (
    cosine_similarity,
)

from src.rag.document_loader import (
    KnowledgeDocument,
    load_knowledge_base,
)


# ============================================================
# VECTOR STORE SETTINGS
# ============================================================

DEFAULT_CHUNK_SIZE = 1200

DEFAULT_CHUNK_OVERLAP = 200

DEFAULT_TOP_K = 5

MIN_CHUNK_CHARACTERS = 80


# ============================================================
# KNOWLEDGE CHUNK MODEL
# ============================================================

@dataclass(frozen=True)
class KnowledgeChunk:
    """
    Retrieval-ready knowledge chunk.

    Attributes
    ----------
    chunk_id:
        Stable chunk identifier.

    document_id:
        Source document identifier.

    title:
        Source document title.

    category:
        cybersecurity or sustainability.

    source_name:
        Original Markdown filename.

    text:
        Chunk content.

    chunk_index:
        Zero-based chunk position inside the source document.

    character_count:
        Number of characters in the chunk.
    """

    chunk_id: str

    document_id: str

    title: str

    category: str

    source_name: str

    text: str

    chunk_index: int

    character_count: int


# ============================================================
# SEARCH RESULT MODEL
# ============================================================

@dataclass(frozen=True)
class VectorSearchResult:
    """
    Similarity-search result.
    """

    chunk: KnowledgeChunk

    score: float


# ============================================================
# VECTOR STORE MODEL
# ============================================================

@dataclass
class VectorStore:
    """
    In-memory TF-IDF vector store.
    """

    chunks: tuple[KnowledgeChunk, ...]

    vectorizer: TfidfVectorizer

    matrix: object


# ============================================================
# TEXT NORMALIZATION
# ============================================================

def _normalize_text(
    text: str,
) -> str:
    """
    Normalize whitespace while preserving paragraph boundaries
    reasonably well for retrieval.
    """

    if not text:
        return ""

    lines = [
        line.strip()
        for line in text.splitlines()
    ]

    cleaned_lines: list[str] = []

    previous_blank = False

    for line in lines:

        if not line:

            if not previous_blank:

                cleaned_lines.append(
                    ""
                )

            previous_blank = True

            continue

        cleaned_lines.append(
            line
        )

        previous_blank = False

    return "\n".join(
        cleaned_lines
    ).strip()


# ============================================================
# PARAGRAPH SPLITTING
# ============================================================

def _split_into_blocks(
    text: str,
) -> list[str]:
    """
    Split Markdown into paragraph/section blocks.

    Keeps headings attached as independent retrieval signals.
    """

    normalized = (
        _normalize_text(
            text
        )
    )

    if not normalized:
        return []

    blocks = [
        block.strip()
        for block in normalized.split(
            "\n\n"
        )
        if block.strip()
    ]

    return blocks


# ============================================================
# CHUNKING
# ============================================================

def chunk_document(
    document: KnowledgeDocument,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> tuple[KnowledgeChunk, ...]:
    """
    Split one knowledge document into retrieval-friendly chunks.

    Chunking prefers paragraph boundaries while still enforcing
    an approximate character limit.
    """

    if chunk_size <= 0:

        raise ValueError(
            "chunk_size must be greater than zero."
        )

    if chunk_overlap < 0:

        raise ValueError(
            "chunk_overlap cannot be negative."
        )

    if chunk_overlap >= chunk_size:

        raise ValueError(
            "chunk_overlap must be smaller than chunk_size."
        )

    blocks = (
        _split_into_blocks(
            document.content
        )
    )

    if not blocks:
        return tuple()

    chunk_texts: list[str] = []

    current_parts: list[str] = []

    current_length = 0

    for block in blocks:

        block_length = len(
            block
        )

        # ----------------------------------------------------
        # Large block fallback
        # ----------------------------------------------------

        if (
            block_length
            > chunk_size
        ):

            if current_parts:

                chunk_texts.append(
                    "\n\n".join(
                        current_parts
                    )
                )

                current_parts = []

                current_length = 0

            start = 0

            while start < block_length:

                end = min(
                    start + chunk_size,
                    block_length,
                )

                piece = (
                    block[
                        start:end
                    ]
                    .strip()
                )

                if (
                    len(piece)
                    >= MIN_CHUNK_CHARACTERS
                ):

                    chunk_texts.append(
                        piece
                    )

                if end >= block_length:
                    break

                start = (
                    end
                    - chunk_overlap
                )

            continue

        separator_length = (
            2
            if current_parts
            else 0
        )

        projected_length = (
            current_length
            + separator_length
            + block_length
        )

        # ----------------------------------------------------
        # Append block when it fits
        # ----------------------------------------------------

        if (
            projected_length
            <= chunk_size
        ):

            current_parts.append(
                block
            )

            current_length = (
                projected_length
            )

            continue

        # ----------------------------------------------------
        # Finalize current chunk
        # ----------------------------------------------------

        if current_parts:

            finished_chunk = (
                "\n\n".join(
                    current_parts
                )
            )

            if (
                len(
                    finished_chunk
                )
                >= MIN_CHUNK_CHARACTERS
            ):

                chunk_texts.append(
                    finished_chunk
                )

        # ----------------------------------------------------
        # Build overlap context
        # ----------------------------------------------------

        overlap_parts: list[str] = []

        overlap_length = 0

        for previous_block in reversed(
            current_parts
        ):

            candidate_length = (
                len(
                    previous_block
                )
                + (
                    2
                    if overlap_parts
                    else 0
                )
            )

            if (
                overlap_length
                + candidate_length
                > chunk_overlap
            ):

                break

            overlap_parts.insert(
                0,
                previous_block,
            )

            overlap_length += (
                candidate_length
            )

        current_parts = (
            overlap_parts
            + [
                block
            ]
        )

        current_length = len(
            "\n\n".join(
                current_parts
            )
        )

    # --------------------------------------------------------
    # Final chunk
    # --------------------------------------------------------

    if current_parts:

        final_chunk = (
            "\n\n".join(
                current_parts
            )
        )

        if (
            len(
                final_chunk
            )
            >= MIN_CHUNK_CHARACTERS
        ):

            chunk_texts.append(
                final_chunk
            )

    # --------------------------------------------------------
    # Build structured chunk objects
    # --------------------------------------------------------

    chunks = tuple(
        KnowledgeChunk(
            chunk_id=(
                f"{document.document_id}"
                f"_chunk_{index}"
            ),
            document_id=(
                document.document_id
            ),
            title=document.title,
            category=document.category,
            source_name=document.source_name,
            text=chunk_text,
            chunk_index=index,
            character_count=len(
                chunk_text
            ),
        )
        for index, chunk_text
        in enumerate(
            chunk_texts
        )
    )

    return chunks


# ============================================================
# COMPLETE KNOWLEDGE-BASE CHUNKING
# ============================================================

def chunk_documents(
    documents: Iterable[
        KnowledgeDocument
    ],
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> tuple[KnowledgeChunk, ...]:
    """
    Chunk multiple knowledge documents.
    """

    all_chunks: list[
        KnowledgeChunk
    ] = []

    for document in documents:

        all_chunks.extend(
            chunk_document(
                document,
                chunk_size=chunk_size,
                chunk_overlap=chunk_overlap,
            )
        )

    chunk_ids = [
        chunk.chunk_id
        for chunk in all_chunks
    ]

    if (
        len(
            chunk_ids
        )
        != len(
            set(
                chunk_ids
            )
        )
    ):

        raise ValueError(
            "Duplicate knowledge chunk IDs detected."
        )

    return tuple(
        all_chunks
    )

# ============================================================
# SEARCHABLE CHUNK TEXT
# ============================================================

def _build_searchable_text(
    chunk: KnowledgeChunk,
) -> str:
    """
    Build weighted searchable text for a knowledge chunk.

    Document metadata is intentionally repeated so that
    specialized sources rank more strongly for matching
    technical queries.

    Example:
        title: Storage Media Sanitization
        category: cybersecurity
        source: storage_media_sanitization
        chunk text...
    """

    source_label = (
        chunk.source_name
        .replace(".md", "")
        .replace("_", " ")
        .replace("-", " ")
    )

    metadata = " ".join(
        [
            chunk.title,
            chunk.title,
            source_label,
            source_label,
            chunk.category,
        ]
    )

    return (
        f"{metadata}\n\n"
        f"{chunk.text}"
    )

# ============================================================
# VECTOR STORE BUILDER
# ============================================================

def build_vector_store(
    documents: Iterable[
        KnowledgeDocument
    ] | None = None,
    *,
    chunk_size: int = DEFAULT_CHUNK_SIZE,
    chunk_overlap: int = DEFAULT_CHUNK_OVERLAP,
) -> VectorStore:
    """
    Build an in-memory TF-IDF vector store.
    """

    source_documents = (
        tuple(
            documents
        )
        if documents is not None
        else load_knowledge_base()
    )

    if not source_documents:

        raise ValueError(
            "Cannot build vector store from an empty "
            "document collection."
        )

    chunks = (
        chunk_documents(
            source_documents,
            chunk_size=chunk_size,
            chunk_overlap=chunk_overlap,
        )
    )

    if not chunks:

        raise ValueError(
            "No valid knowledge chunks were generated."
        )

    texts = [
    _build_searchable_text(
        chunk
    )
    for chunk in chunks
]

    vectorizer = (
    TfidfVectorizer(
        lowercase=True,
        strip_accents="unicode",
        stop_words="english",
        ngram_range=(
            1,
            3,
        ),
        sublinear_tf=True,
        max_df=0.98,
        min_df=1,
        norm="l2",
    )
)

    matrix = (
        vectorizer.fit_transform(
            texts
        )
    )

    return VectorStore(
        chunks=chunks,
        vectorizer=vectorizer,
        matrix=matrix,
    )


# ============================================================
# QUERY VALIDATION
# ============================================================

def _validate_query(
    query: str,
) -> str:
    """
    Validate and normalize search query.
    """

    normalized = (
        str(
            query
        )
        .strip()
    )

    if not normalized:

        raise ValueError(
            "Search query cannot be empty."
        )

    return normalized


# ============================================================
# VECTOR SEARCH
# ============================================================

def search_vector_store(
    vector_store: VectorStore,
    query: str,
    *,
    top_k: int = DEFAULT_TOP_K,
    category: str | None = None,
    min_score: float = 0.0,
    unique_documents: bool = False,
) -> tuple[VectorSearchResult, ...]:
    
    """
    Search the vector store using cosine similarity.

    Parameters
    ----------
    vector_store:
        Built EcoShield VectorStore.

    query:
        Natural-language search query.

    top_k:
        Maximum number of results.

    category:
        Optional category filter:
        cybersecurity or sustainability.

    min_score:
        Minimum cosine similarity score.
    """

    normalized_query = (
        _validate_query(
            query
        )
    )

    if top_k <= 0:

        raise ValueError(
            "top_k must be greater than zero."
        )

    if not (
        0.0
        <= min_score
        <= 1.0
    ):

        raise ValueError(
            "min_score must be between 0 and 1."
        )

    query_vector = (
        vector_store
        .vectorizer
        .transform(
            [
                normalized_query
            ]
        )
    )

    similarities = (
        cosine_similarity(
            query_vector,
            vector_store.matrix,
        )[0]
    )

    candidate_indices = (
        np.argsort(
            similarities
        )[::-1]
    )

    results: list[
        VectorSearchResult
    ] = []

    seen_documents: set[str] = set()

    for index in (
        candidate_indices
    ):

        chunk = (
            vector_store
            .chunks[
                int(index)
            ]
        )

        score = float(
            similarities[
                int(index)
            ]
        )

        if (
            category is not None
            and chunk.category
            != category
        ):

            continue

        if score < min_score:
            continue

        if (
           unique_documents
           and chunk.document_id
           in seen_documents
           ):
           continue

        results.append(
            VectorSearchResult(
                chunk=chunk,
                score=score,
            )
        )

        seen_documents.add(
    chunk.document_id
)
        if len(results) >= top_k:
            break

    return tuple(
        results
    )


# ============================================================
# VECTOR STORE SUMMARY
# ============================================================

def get_vector_store_summary(
    vector_store: VectorStore,
) -> dict[str, int]:
    """
    Return vector-store statistics.
    """

    cybersecurity_chunks = sum(
        1
        for chunk
        in vector_store.chunks
        if chunk.category
        == "cybersecurity"
    )

    sustainability_chunks = sum(
        1
        for chunk
        in vector_store.chunks
        if chunk.category
        == "sustainability"
    )

    vocabulary_size = len(
        vector_store
        .vectorizer
        .vocabulary_
    )

    return {
        "total_chunks": len(
            vector_store.chunks
        ),
        "cybersecurity_chunks": (
            cybersecurity_chunks
        ),
        "sustainability_chunks": (
            sustainability_chunks
        ),
        "vocabulary_size": (
            vocabulary_size
        ),
    }


# ============================================================
# CONVENIENCE SEARCH
# ============================================================

def search_knowledge_base(
    query: str,
    *,
    top_k: int = DEFAULT_TOP_K,
    category: str | None = None,
    min_score: float = 0.0,
    unique_documents: bool = False,
) -> tuple[VectorSearchResult, ...]:
    
    """
    Build the EcoShield vector store and search it.

    Useful for testing and lightweight direct usage.

    Production flows should normally build the store once
    and reuse it through retriever.py.
    """

    vector_store = (
        build_vector_store()
    )

    return search_vector_store(
    vector_store,
    query,
    top_k=top_k,
    category=category,
    min_score=min_score,
    unique_documents=unique_documents,
)