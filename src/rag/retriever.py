"""
EcoShield AI
RAG Retriever

This module performs intelligent retrieval over the EcoShield
knowledge base.

Responsibilities:
- Normalize user queries
- Detect cybersecurity / sustainability / hybrid intent
- Detect topic signals from the query
- Enrich retrieval using device-assessment context
- Retrieve a larger candidate pool from the vector store
- Re-rank candidates using domain and topic relevance
- Deduplicate sources
- Return structured evidence for the LLM layer

This module does NOT:
- load Markdown files directly
- build the vector store implementation
- perform deterministic risk scoring
- generate final LLM responses
"""

from __future__ import annotations

from dataclasses import dataclass

from typing import Any, Mapping

from src.rag.vector_store import (
    DEFAULT_TOP_K,
    VectorSearchResult,
    VectorStore,
    build_vector_store,
    search_vector_store,
)


# ============================================================
# RETRIEVAL INTENTS
# ============================================================

INTENT_CYBERSECURITY = "cybersecurity"

INTENT_SUSTAINABILITY = "sustainability"

INTENT_HYBRID = "hybrid"


SUPPORTED_INTENTS = {
    INTENT_CYBERSECURITY,
    INTENT_SUSTAINABILITY,
    INTENT_HYBRID,
}


# ============================================================
# RETRIEVAL TOPICS
# ============================================================

TOPIC_SANITIZATION = "sanitization"

TOPIC_STORAGE = "storage"

TOPIC_ENCRYPTION = "encryption"

TOPIC_ACCOUNTS = "accounts"

TOPIC_REMOVABLE_MEDIA = "removable_media"

TOPIC_TRANSFER = "transfer"

TOPIC_PLATFORM = "platform"

TOPIC_REPAIR = "repair"

TOPIC_REUSE = "reuse"

TOPIC_DONATION_RESALE = "donation_resale"

TOPIC_EWASTE = "ewaste"

TOPIC_RECYCLING = "recycling"

TOPIC_LIFECYCLE = "lifecycle"


SUPPORTED_TOPICS = {
    TOPIC_SANITIZATION,
    TOPIC_STORAGE,
    TOPIC_ENCRYPTION,
    TOPIC_ACCOUNTS,
    TOPIC_REMOVABLE_MEDIA,
    TOPIC_TRANSFER,
    TOPIC_PLATFORM,
    TOPIC_REPAIR,
    TOPIC_REUSE,
    TOPIC_DONATION_RESALE,
    TOPIC_EWASTE,
    TOPIC_RECYCLING,
    TOPIC_LIFECYCLE,
}


# ============================================================
# RETRIEVAL SETTINGS
# ============================================================

DEFAULT_FINAL_TOP_K = 5

DEFAULT_CANDIDATE_TOP_K = 50

DEFAULT_MIN_VECTOR_SCORE = 0.0


# ============================================================
# RERANKING WEIGHTS
# ============================================================

INTENT_MATCH_BOOST = 0.10

INTENT_MISMATCH_PENALTY = 0.05

TOPIC_MATCH_BOOST = 0.08

PRIMARY_TOPIC_BOOST = 0.06

ASSESSMENT_CONTEXT_BOOST = 0.03

SOURCE_SPECIALIZATION_BOOST = 0.04


# ============================================================
# RETRIEVAL RESULT MODEL
# ============================================================

@dataclass(frozen=True)
class RetrievedEvidence:
    """
    Final reranked evidence returned by the EcoShield retriever.

    Attributes
    ----------
    chunk_id:
        Stable knowledge chunk identifier.

    document_id:
        Stable source document identifier.

    title:
        Human-readable source title.

    category:
        cybersecurity or sustainability.

    source_name:
        Original Markdown filename.

    text:
        Retrieved evidence text.

    vector_score:
        Raw vector similarity score.

    rerank_score:
        Final score after EcoShield reranking.

    matched_topics:
        Topics responsible for relevance boosts.
    """

    chunk_id: str

    document_id: str

    title: str

    category: str

    source_name: str

    text: str

    vector_score: float

    rerank_score: float

    matched_topics: tuple[str, ...]


# ============================================================
# RETRIEVAL CONTEXT MODEL
# ============================================================

@dataclass(frozen=True)
class RetrievalContext:
    """
    Complete output of the EcoShield retrieval pipeline.

    Attributes
    ----------
    original_query:
        User's original query.

    enriched_query:
        Query after assessment-aware enrichment.

    intent:
        cybersecurity, sustainability, or hybrid.

    topics:
        Detected EcoShield topics.

    evidence:
        Final deduplicated and reranked evidence.
    """

    original_query: str

    enriched_query: str

    intent: str

    topics: tuple[str, ...]

    evidence: tuple[RetrievedEvidence, ...]


# ============================================================
# RETRIEVER MODEL
# ============================================================

@dataclass
class EcoShieldRetriever:
    """
    Reusable EcoShield retrieval service.

    The vector store should normally be built once and reused
    instead of being rebuilt for every user query.
    """

    vector_store: VectorStore


# ============================================================
# RETRIEVER FACTORY
# ============================================================

def build_retriever(
    vector_store: VectorStore | None = None,
) -> EcoShieldRetriever:
    """
    Build an EcoShield retriever.

    Parameters
    ----------
    vector_store:
        Optional prebuilt vector store.

        When omitted, the complete EcoShield knowledge base
        is loaded and indexed automatically.
    """

    store = (
        vector_store
        if vector_store is not None
        else build_vector_store()
    )

    return EcoShieldRetriever(
        vector_store=store
    )

    # ============================================================
# QUERY NORMALIZATION
# ============================================================

def normalize_query(
    query: str,
) -> str:
    """
    Normalize a user query for retrieval.

    Removes unnecessary surrounding whitespace and collapses
    repeated internal whitespace while preserving the original
    wording and punctuation.
    """

    normalized = (
        " ".join(
            str(query)
            .strip()
            .split()
        )
    )

    if not normalized:

        raise ValueError(
            "Retrieval query cannot be empty."
        )

    return normalized


# ============================================================
# INTENT KEYWORDS
# ============================================================

CYBERSECURITY_INTENT_KEYWORDS = {
    "secure",
    "security",
    "cybersecurity",
    "privacy",
    "erase",
    "erasure",
    "sanitize",
    "sanitization",
    "wipe",
    "delete",
    "deletion",
    "encrypt",
    "encryption",
    "password",
    "account",
    "accounts",
    "sign out",
    "logout",
    "factory reset",
    "reset",
    "sensitive data",
    "personal data",
    "storage",
    "ssd",
    "hdd",
    "emmc",
    "flash storage",
    "sim",
    "memory card",
    "sd card",
    "data protection",
    "data exposure",
    "transfer security",
}


SUSTAINABILITY_INTENT_KEYWORDS = {
    "sustainability",
    "sustainable",
    "repair",
    "reuse",
    "reusable",
    "recycle",
    "recycling",
    "e-waste",
    "ewaste",
    "electronic waste",
    "donate",
    "donation",
    "resell",
    "resale",
    "second life",
    "device lifecycle",
    "lifecycle",
    "end of life",
    "end-of-life",
    "responsible disposal",
    "responsible recycling",
    "circular",
    "circular economy",
    "extend device life",
    "extend lifespan",
    "old device",
    "old laptop",
    "old phone",
}


# ============================================================
# KEYWORD MATCHING
# ============================================================

def _count_keyword_matches(
    query: str,
    keywords: set[str],
) -> int:
    """
    Count unique keyword or phrase matches in a query.

    Matching is case-insensitive.
    """

    normalized_query = (
        query.casefold()
    )

    matches = {
        keyword
        for keyword in keywords
        if keyword.casefold()
        in normalized_query
    }

    return len(
        matches
    )


# ============================================================
# INTENT DETECTION
# ============================================================

def detect_intent(
    query: str,
) -> str:
    """
    Detect the primary EcoShield retrieval intent.

    Returns
    -------
    str
        One of:
        - cybersecurity
        - sustainability
        - hybrid

    Notes
    -----
    Hybrid intent is used when both cybersecurity and
    sustainability signals are meaningfully present.
    """

    normalized_query = (
        normalize_query(
            query
        )
    )

    cybersecurity_score = (
        _count_keyword_matches(
            normalized_query,
            CYBERSECURITY_INTENT_KEYWORDS,
        )
    )

    sustainability_score = (
        _count_keyword_matches(
            normalized_query,
            SUSTAINABILITY_INTENT_KEYWORDS,
        )
    )

    # --------------------------------------------------------
    # Strong mixed intent
    # --------------------------------------------------------

    if (
        cybersecurity_score > 0
        and sustainability_score > 0
    ):

        return INTENT_HYBRID

    # --------------------------------------------------------
    # Cybersecurity intent
    # --------------------------------------------------------

    if (
        cybersecurity_score
        > sustainability_score
    ):

        return INTENT_CYBERSECURITY

    # --------------------------------------------------------
    # Sustainability intent
    # --------------------------------------------------------

    if (
        sustainability_score
        > cybersecurity_score
    ):

        return INTENT_SUSTAINABILITY

    # --------------------------------------------------------
    # No clear signal
    #
    # EcoShield spans both domains, so defaulting to hybrid
    # is safer than forcing an unsupported domain assumption.
    # --------------------------------------------------------

    return INTENT_HYBRID

    # ============================================================
# TOPIC KEYWORDS
# ============================================================

TOPIC_KEYWORDS: dict[str, set[str]] = {

    TOPIC_SANITIZATION: {
        "secure erase",
        "erase",
        "erasure",
        "sanitize",
        "sanitization",
        "wipe",
        "wiping",
        "factory reset",
        "reset",
        "delete data",
        "remove data",
    },

    TOPIC_STORAGE: {
        "storage",
        "ssd",
        "hdd",
        "hard drive",
        "hard disk",
        "solid state drive",
        "emmc",
        "flash storage",
        "internal storage",
        "storage media",
    },

    TOPIC_ENCRYPTION: {
        "encrypt",
        "encrypted",
        "encryption",
        "data protection",
        "bitlocker",
        "filevault",
        "device encryption",
    },

    TOPIC_ACCOUNTS: {
        "account",
        "accounts",
        "sign out",
        "signed out",
        "logout",
        "log out",
        "remove account",
        "unlink account",
        "credentials",
    },

    TOPIC_REMOVABLE_MEDIA: {
        "sim",
        "sim card",
        "memory card",
        "sd card",
        "microsd",
        "removable media",
        "external storage",
    },

    TOPIC_TRANSFER: {
    "sell",
    "selling",
    "resell",
    "resale",
    "donate",
    "donation",
    "give away",
    "giving away",
    "transfer",
    "transferring",
    "new owner",
    "ownership transfer",
    "trade in",
    "trade-in",
},

    TOPIC_PLATFORM: {
        "windows",
        "macos",
        "linux",
        "android",
        "ios",
        "chromeos",
        "laptop",
        "desktop",
        "computer",
        "phone",
        "smartphone",
        "tablet",
    },

    TOPIC_REPAIR: {
        "repair",
        "repairing",
        "fix",
        "fixing",
        "upgrade",
        "refurbish",
        "refurbishment",
    },

    TOPIC_REUSE: {
        "reuse",
        "reusing",
        "reusable",
        "second life",
        "repurpose",
        "repurposing",
        "continue using",
    },

    TOPIC_DONATION_RESALE: {
    "donate",
    "donation",
    "sell",
    "selling",
    "resell",
    "resale",
    "second hand",
    "second-hand",
    "give away",
    "giving away",
},

    TOPIC_EWASTE: {
        "e-waste",
        "ewaste",
        "electronic waste",
        "electronic disposal",
        "environmental impact",
    },

    TOPIC_RECYCLING: {
        "recycle",
        "recycling",
        "recycler",
        "recycling center",
        "recycling centre",
        "responsible recycling",
    },

    TOPIC_LIFECYCLE: {
        "lifecycle",
        "life cycle",
        "device life",
        "device lifespan",
        "extend lifespan",
        "extend device life",
        "end of life",
        "end-of-life",
        "circular economy",
    },
}


# ============================================================
# TOPIC DETECTION
# ============================================================

def detect_topics(
    query: str,
) -> tuple[str, ...]:
    """
    Detect EcoShield knowledge topics present in a query.

    Multiple topics may be returned because a single device
    decision can involve cybersecurity and sustainability
    concerns simultaneously.

    Example
    -------
    Query:
        "How should I securely erase an SSD before
        selling my laptop?"

    Possible topics:
        sanitization
        storage
        transfer
        donation_resale
        platform
    """

    normalized_query = (
        normalize_query(
            query
        ).casefold()
    )

    detected_topics: list[str] = []

    for topic, keywords in (
        TOPIC_KEYWORDS.items()
    ):

        if any(
            keyword.casefold()
            in normalized_query
            for keyword in keywords
        ):

            detected_topics.append(
                topic
            )

    return tuple(
        detected_topics
    )

    # ============================================================
# ASSESSMENT FIELD LABELS
# ============================================================

ASSESSMENT_FIELD_LABELS = {
    "device_type": "Device type",
    "operating_system": "Operating system",
    "device_age": "Device age",
    "device_condition": "Device condition",
    "storage_type": "Storage type",
    "storage_capacity": "Storage capacity",
    "contains_personal_data": "Personal data",
    "contains_sensitive_data": "Sensitive data",
    "device_accessible": "Device accessible",
    "can_power_on": "Can power on",
    "data_backed_up": "Data backed up",
    "factory_reset_performed": "Factory reset performed",
    "secure_erase_performed": "Secure erase performed",
    "encryption_enabled": "Encryption enabled",
    "accounts_signed_out": "Accounts signed out",
    "sim_memory_card_removed": "SIM / memory card removed",
    "intended_disposal_method": "Intended action",
}


# ============================================================
# ASSESSMENT VALUE NORMALIZATION
# ============================================================

def _normalize_assessment_value(
    value: Any,
) -> str:
    """
    Convert an assessment value into clean retrieval text.
    """

    if value is None:
        return ""

    return (
        " ".join(
            str(value)
            .strip()
            .split()
        )
    )


# ============================================================
# BUILD ASSESSMENT CONTEXT
# ============================================================

def build_assessment_context(
    assessment: Mapping[str, Any] | None,
) -> tuple[str, ...]:
    """
    Convert known EcoShield assessment values into concise
    retrieval-friendly context lines.

    Unknown additional fields are deliberately ignored.
    """

    if assessment is None:
        return tuple()

    if not isinstance(
        assessment,
        Mapping,
    ):
        raise TypeError(
            "assessment must be a dictionary-like mapping."
        )

    context_lines: list[str] = []

    for (
        field_name,
        label,
    ) in ASSESSMENT_FIELD_LABELS.items():

        if field_name not in assessment:
            continue

        value = (
            _normalize_assessment_value(
                assessment.get(
                    field_name
                )
            )
        )

        if not value:
            continue

        context_lines.append(
            f"{label}: {value}"
        )

    return tuple(
        context_lines
    )


# ============================================================
# QUERY ENRICHMENT
# ============================================================

def enrich_query(
    query: str,
    *,
    assessment: Mapping[str, Any] | None = None,
) -> str:
    """
    Enrich a natural-language retrieval query with known
    EcoShield assessment context.

    The user's original query remains the primary text.
    Device context is appended when available.
    """

    normalized_query = (
        normalize_query(
            query
        )
    )

    context_lines = (
        build_assessment_context(
            assessment
        )
    )

    if not context_lines:
        return normalized_query

    context_text = "\n".join(
        context_lines
    )

    return (
        f"{normalized_query}\n\n"
        f"Device assessment context:\n"
        f"{context_text}"
    )

    # ============================================================
# TOPIC → PREFERRED SOURCES
# ============================================================

TOPIC_SOURCE_MAP: dict[str, tuple[str, ...]] = {

    TOPIC_SANITIZATION: (
        "secure_data_erasure.md",
        "factory_reset_and_sanitization.md",
        "storage_media_sanitization.md",
    ),

    TOPIC_STORAGE: (
        "storage_media_sanitization.md",
        "secure_data_erasure.md",
    ),

    TOPIC_ENCRYPTION: (
        "encryption_and_data_protection.md",
    ),

    TOPIC_ACCOUNTS: (
        "account_and_identity_security.md",
    ),

    TOPIC_REMOVABLE_MEDIA: (
        "removable_media_security.md",
    ),

    TOPIC_TRANSFER: (
        "secure_device_transfer.md",
        "donation_and_resale.md",
    ),

    TOPIC_PLATFORM: (
        "platform_security_guidance.md",
    ),

    TOPIC_REPAIR: (
        "device_repair.md",
    ),

    TOPIC_REUSE: (
        "device_reuse.md",
        "sustainable_device_lifecycle.md",
    ),

    TOPIC_DONATION_RESALE: (
        "donation_and_resale.md",
        "secure_device_transfer.md",
        "device_reuse.md",
    ),

    TOPIC_EWASTE: (
        "ewaste_awareness.md",
        "responsible_recycling.md",
    ),

    TOPIC_RECYCLING: (
        "responsible_recycling.md",
        "ewaste_awareness.md",
        "sustainable_device_lifecycle.md",
    ),

    TOPIC_LIFECYCLE: (
        "sustainable_device_lifecycle.md",
        "device_reuse.md",
        "device_repair.md",
    ),
}

    # ============================================================
# SOURCE SPECIALIZATION MAP
# ============================================================

SOURCE_PRIMARY_TOPICS: dict[str, tuple[str, ...]] = {

    "account_and_identity_security.md": (
        TOPIC_ACCOUNTS,
    ),

    "encryption_and_data_protection.md": (
        TOPIC_ENCRYPTION,
    ),

    "factory_reset_and_sanitization.md": (
        TOPIC_SANITIZATION,
    ),

    "platform_security_guidance.md": (
        TOPIC_PLATFORM,
    ),

    "removable_media_security.md": (
        TOPIC_REMOVABLE_MEDIA,
    ),

    "secure_data_erasure.md": (
        TOPIC_SANITIZATION,
    ),

    "secure_device_transfer.md": (
        TOPIC_TRANSFER,
    ),

    "storage_media_sanitization.md": (
        TOPIC_STORAGE,
        TOPIC_SANITIZATION,
    ),

    "device_repair.md": (
        TOPIC_REPAIR,
    ),

    "device_reuse.md": (
        TOPIC_REUSE,
    ),

    "donation_and_resale.md": (
        TOPIC_DONATION_RESALE,
        TOPIC_TRANSFER,
    ),

    "ewaste_awareness.md": (
        TOPIC_EWASTE,
    ),

    "responsible_recycling.md": (
        TOPIC_RECYCLING,
    ),

    "sustainable_device_lifecycle.md": (
        TOPIC_LIFECYCLE,
        TOPIC_REUSE,
    ),
}

    # ============================================================
# INTENT MATCHING
# ============================================================

def _intent_matches_category(
    intent: str,
    category: str,
) -> bool:
    """
    Return whether the source category matches detected intent.
    """

    if intent == INTENT_HYBRID:
        return True

    return intent == category


# ============================================================
# TOPIC MATCHING
# ============================================================

def _get_source_topic_matches(
    source_name: str,
    topics: tuple[str, ...],
) -> tuple[str, ...]:
    """
    Return detected topics directly associated with a source.
    """

    source_topics = (
        SOURCE_PRIMARY_TOPICS.get(
            source_name,
            tuple(),
        )
    )

    return tuple(
        topic
        for topic in topics
        if topic in source_topics
    )


# ============================================================
# SOURCE PREFERENCE CHECK
# ============================================================

def _is_preferred_source(
    source_name: str,
    topics: tuple[str, ...],
) -> bool:
    """
    Return True when a source is preferred for any
    currently detected topic.
    """

    for topic in topics:

        preferred_sources = (
            TOPIC_SOURCE_MAP.get(
                topic,
                tuple(),
            )
        )

        if source_name in preferred_sources:
            return True

    return False


        # ============================================================
# REQUIRED TOPIC SOURCES
# ============================================================

def _get_topic_required_sources(
    topics: tuple[str, ...],
) -> tuple[str, ...]:
    """
    Return all source documents that are explicitly relevant
    to the detected EcoShield topics.

    This protects topic-specific documents from being lost
    simply because raw TF-IDF candidate ranking was weak.
    """

    required_sources: list[str] = []

    for topic in topics:

        for source_name in (
            TOPIC_SOURCE_MAP.get(
                topic,
                tuple(),
            )
        ):

            if (
                source_name
                not in required_sources
            ):

                required_sources.append(
                    source_name
                )

    return tuple(
        required_sources
    )


     # ============================================================
# TOPIC SOURCE RESCUE
# ============================================================

def _rescue_topic_candidates(
    *,
    vector_store: VectorStore,
    candidates: tuple[
        VectorSearchResult,
        ...
    ],
    topics: tuple[str, ...],
) -> tuple[
    VectorSearchResult,
    ...
]:
    """
    Ensure topic-specific source documents are represented in
    the candidate pool whenever possible.

    Raw TF-IDF retrieval can sometimes rank broad documents
    above highly specialized documents.

    This function does not invent evidence or scores.
    It only restores relevant chunks that already exist inside
    the built vector store.
    """

    required_sources = (
        _get_topic_required_sources(
            topics
        )
    )

    if not required_sources:
        return candidates

    candidate_sources = {
        result.chunk.source_name
        for result in candidates
    }

    missing_sources = [
        source_name
        for source_name
        in required_sources
        if source_name
        not in candidate_sources
    ]

    if not missing_sources:
        return candidates

    rescued: list[
        VectorSearchResult
    ] = list(
        candidates
    )

    for source_name in (
        missing_sources
    ):

        best_result: (
            VectorSearchResult
            | None
        ) = None

        for index, chunk in enumerate(
            vector_store.chunks
        ):

            if (
                chunk.source_name
                != source_name
            ):

                continue

            # The raw vector score is unavailable here because
            # the original search did not return this chunk.
            #
            # We use zero as the lexical base score and allow
            # EcoShield topic reranking to determine relevance.
            candidate = (
                VectorSearchResult(
                    chunk=chunk,
                    score=0.0,
                )
            )

            best_result = (
                candidate
            )

            break

        if best_result is not None:

            rescued.append(
                best_result
            )

    return tuple(
        rescued
    )

    # ============================================================
# RERANK SCORE
# ============================================================

def _calculate_rerank_score(
    result: VectorSearchResult,
    *,
    intent: str,
    topics: tuple[str, ...],
    assessment_present: bool,
) -> tuple[float, tuple[str, ...]]:
    """
    Calculate the final EcoShield relevance score.

    Combines:
    - raw vector similarity
    - intent/category match
    - topic/source relevance
    - source specialization
    - assessment-aware context
    """

    score = float(
        result.score
    )

    chunk = (
        result.chunk
    )

    # --------------------------------------------------------
    # Intent match
    # --------------------------------------------------------

    if _intent_matches_category(
        intent,
        chunk.category,
    ):

        score += (
            INTENT_MATCH_BOOST
        )

    elif (
        intent
        != INTENT_HYBRID
    ):

        score -= (
            INTENT_MISMATCH_PENALTY
        )

    # --------------------------------------------------------
    # Direct topic matches
    # --------------------------------------------------------

    matched_topics = (
        _get_source_topic_matches(
            chunk.source_name,
            topics,
        )
    )

    score += (
        len(
            matched_topics
        )
        * TOPIC_MATCH_BOOST
    )

    # --------------------------------------------------------
    # Preferred source boost
    # --------------------------------------------------------

    if _is_preferred_source(
        chunk.source_name,
        topics,
    ):

        score += (
            PRIMARY_TOPIC_BOOST
        )

    # --------------------------------------------------------
    # Specialized source boost
    # --------------------------------------------------------

    if matched_topics:

        score += (
            SOURCE_SPECIALIZATION_BOOST
        )

    # --------------------------------------------------------
    # Assessment-aware context boost
    # --------------------------------------------------------

    if assessment_present:

        score += (
            ASSESSMENT_CONTEXT_BOOST
        )

    return (
        score,
        matched_topics,
    )

    # ============================================================
# CANDIDATE RERANKING
# ============================================================

def _rerank_candidates(
    candidates: tuple[
        VectorSearchResult,
        ...
    ],
    *,
    intent: str,
    topics: tuple[str, ...],
    assessment_present: bool,
) -> tuple[
    RetrievedEvidence,
    ...
]:
    """
    Convert raw vector-search candidates into EcoShield
    reranked evidence objects.
    """

    reranked: list[
        RetrievedEvidence
    ] = []

    for result in candidates:

        rerank_score, matched_topics = (
            _calculate_rerank_score(
                result,
                intent=intent,
                topics=topics,
                assessment_present=assessment_present,
            )
        )

        chunk = result.chunk

        reranked.append(
            RetrievedEvidence(
                chunk_id=chunk.chunk_id,
                document_id=chunk.document_id,
                title=chunk.title,
                category=chunk.category,
                source_name=chunk.source_name,
                text=chunk.text,
                vector_score=float(
                    result.score
                ),
                rerank_score=float(
                    rerank_score
                ),
                matched_topics=(
                    matched_topics
                ),
            )
        )

    return tuple(
        sorted(
            reranked,
            key=lambda item: (
                item.rerank_score
            ),
            reverse=True,
        )
    )


# ============================================================
# DOCUMENT-LEVEL DEDUPLICATION
# ============================================================

def _deduplicate_evidence(
    evidence: tuple[
        RetrievedEvidence,
        ...
    ],
    *,
    top_k: int,
) -> tuple[
    RetrievedEvidence,
    ...
]:
    """
    Keep only the highest-ranked chunk from each source
    document.

    This prevents one long Markdown file from occupying
    several final evidence slots.
    """

    if top_k <= 0:

        raise ValueError(
            "top_k must be greater than zero."
        )

    seen_documents: set[str] = (
        set()
    )

    selected: list[
        RetrievedEvidence
    ] = []

    for item in evidence:

        if (
            item.document_id
            in seen_documents
        ):

            continue

        seen_documents.add(
            item.document_id
        )

        selected.append(
            item
        )

        if (
            len(selected)
            >= top_k
        ):

            break

    return tuple(
        selected
    )


# ============================================================
# PRIMARY RETRIEVAL FUNCTION
# ============================================================

def retrieve(
    retriever: EcoShieldRetriever,
    query: str,
    *,
    assessment: Mapping[
        str,
        Any,
    ] | None = None,
    top_k: int = DEFAULT_FINAL_TOP_K,
    candidate_top_k: int = DEFAULT_CANDIDATE_TOP_K,
    min_vector_score: float = DEFAULT_MIN_VECTOR_SCORE,
) -> RetrievalContext:
    """
    Execute the complete EcoShield retrieval pipeline.

    Parameters
    ----------
    retriever:
        Reusable EcoShieldRetriever instance.

    query:
        Natural-language user question.

    assessment:
        Optional EcoShield device-assessment context.

    top_k:
        Number of final deduplicated evidence items.

    candidate_top_k:
        Number of raw vector candidates considered before
        reranking.

    min_vector_score:
        Minimum raw vector similarity score.

    Returns
    -------
    RetrievalContext
        Complete retrieval output containing:
        - original query
        - enriched query
        - detected intent
        - detected topics
        - reranked evidence
    """

    if not isinstance(
        retriever,
        EcoShieldRetriever,
    ):

        raise TypeError(
            "retriever must be an EcoShieldRetriever."
        )

    if top_k <= 0:

        raise ValueError(
            "top_k must be greater than zero."
        )

    if candidate_top_k <= 0:

        raise ValueError(
            "candidate_top_k must be greater than zero."
        )

    if (
        candidate_top_k
        < top_k
    ):

        raise ValueError(
            "candidate_top_k must be greater than or equal "
            "to top_k."
        )

    if not (
        0.0
        <= min_vector_score
        <= 1.0
    ):

        raise ValueError(
            "min_vector_score must be between 0 and 1."
        )

    # --------------------------------------------------------
    # Normalize original query
    # --------------------------------------------------------

    original_query = (
        normalize_query(
            query
        )
    )

    # --------------------------------------------------------
    # Detect query intent
    # --------------------------------------------------------

    intent = (
        detect_intent(
            original_query
        )
    )

    # --------------------------------------------------------
    # Detect topics
    # --------------------------------------------------------

    topics = (
        detect_topics(
            original_query
        )
    )

    # --------------------------------------------------------
    # Add device-assessment context
    # --------------------------------------------------------

    enriched_query = (
        enrich_query(
            original_query,
            assessment=assessment,
        )
    )

    # --------------------------------------------------------
    # Raw vector candidate retrieval
    #
    # We intentionally retrieve more candidates than the
    # final result count so EcoShield reranking has enough
    # evidence to work with.
    # --------------------------------------------------------

    candidates = (
        search_vector_store(
            retriever.vector_store,
            enriched_query,
            top_k=candidate_top_k,
            min_score=min_vector_score,
            unique_documents=False,
        )
    )

    # --------------------------------------------------------
    # Rescue strongly topic-relevant sources
    # --------------------------------------------------------

    candidates = (
        _rescue_topic_candidates(
            vector_store=(
                retriever.vector_store
            ),
            candidates=candidates,
            topics=topics,
        )
    )

    # --------------------------------------------------------
    # Rerank candidates
    # --------------------------------------------------------

    reranked = (
        _rerank_candidates(
            candidates,
            intent=intent,
            topics=topics,
            assessment_present=(
                assessment
                is not None
            ),
        )
    )

    # --------------------------------------------------------
    # Deduplicate source documents
    # --------------------------------------------------------

    final_evidence = (
        _deduplicate_evidence(
            reranked,
            top_k=top_k,
        )
    )

    return RetrievalContext(
        original_query=(
            original_query
        ),
        enriched_query=(
            enriched_query
        ),
        intent=intent,
        topics=topics,
        evidence=final_evidence,
    )


# ============================================================
# CONVENIENCE RETRIEVAL FUNCTION
# ============================================================

def retrieve_knowledge(
    query: str,
    *,
    assessment: Mapping[
        str,
        Any,
    ] | None = None,
    top_k: int = DEFAULT_FINAL_TOP_K,
    candidate_top_k: int = DEFAULT_CANDIDATE_TOP_K,
    min_vector_score: float = DEFAULT_MIN_VECTOR_SCORE,
) -> RetrievalContext:
    """
    Convenience wrapper that builds a retriever automatically.

    Useful for terminal testing and lightweight usage.

    Application code should normally build the retriever once
    and reuse it.
    """

    retriever = (
        build_retriever()
    )

    return retrieve(
        retriever,
        query,
        assessment=assessment,
        top_k=top_k,
        candidate_top_k=(
            candidate_top_k
        ),
        min_vector_score=(
            min_vector_score
        ),
    )
