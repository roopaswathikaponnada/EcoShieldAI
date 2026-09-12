"""
EcoShield AI
RAG Document Loader

This module loads and validates Markdown documents from the
EcoShield knowledge base.

Responsibilities:
- Discover knowledge-base Markdown files
- Read files using UTF-8
- Validate document content
- Extract basic metadata
- Return structured document objects
- Keep loading logic separate from vector storage and retrieval

This module does NOT:
- create embeddings
- build a vector store
- perform retrieval
- call an LLM
"""

from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from typing import Iterable

from config.config import (
    CYBERSECURITY_KB_DIR,
    SUSTAINABILITY_KB_DIR,
)


# ============================================================
# SUPPORTED KNOWLEDGE CATEGORIES
# ============================================================

CATEGORY_CYBERSECURITY = "cybersecurity"

CATEGORY_SUSTAINABILITY = "sustainability"


SUPPORTED_CATEGORIES = {
    CATEGORY_CYBERSECURITY: CYBERSECURITY_KB_DIR,
    CATEGORY_SUSTAINABILITY: SUSTAINABILITY_KB_DIR,
}


# ============================================================
# DOCUMENT SETTINGS
# ============================================================

SUPPORTED_EXTENSIONS = {
    ".md",
}

MIN_DOCUMENT_CHARACTERS = 100

EXPECTED_DOCUMENT_COUNT = 14


# ============================================================
# DOCUMENT MODEL
# ============================================================

@dataclass(frozen=True)
class KnowledgeDocument:
    """
    Structured representation of a knowledge-base document.

    Attributes
    ----------
    document_id:
        Stable identifier derived from category and filename.

    title:
        Human-readable document title.

    category:
        Knowledge category such as cybersecurity or sustainability.

    source_name:
        Original filename.

    source_path:
        Absolute path to the document.

    content:
        Full Markdown content.

    character_count:
        Number of characters in the document.
    """

    document_id: str

    title: str

    category: str

    source_name: str

    source_path: Path

    content: str

    character_count: int


# ============================================================
# TITLE EXTRACTION
# ============================================================

def _extract_title(
    content: str,
    fallback_name: str,
) -> str:
    """
    Extract the first Markdown H1 heading.

    If no H1 heading exists, derive a readable title from
    the filename.

    Example
    -------
    secure_data_erasure.md
        ->
    Secure Data Erasure
    """

    for line in content.splitlines():

        stripped = (
            line.strip()
        )

        if stripped.startswith(
            "# "
        ):

            title = (
                stripped[2:]
                .strip()
            )

            if title:
                return title

    return (
        Path(
            fallback_name
        )
        .stem
        .replace(
            "_",
            " ",
        )
        .replace(
            "-",
            " ",
        )
        .title()
    )


# ============================================================
# DOCUMENT ID
# ============================================================

def _build_document_id(
    category: str,
    file_path: Path,
) -> str:
    """
    Create a stable document identifier.

    Example
    -------
    cybersecurity_secure_data_erasure
    """

    return (
        f"{category}_"
        f"{file_path.stem.lower()}"
    )


# ============================================================
# FILE VALIDATION
# ============================================================

def _validate_file(
    file_path: Path,
) -> None:
    """
    Validate a knowledge-base file before loading.
    """

    if not file_path.exists():

        raise FileNotFoundError(
            f"Knowledge-base file does not exist: "
            f"{file_path}"
        )

    if not file_path.is_file():

        raise ValueError(
            f"Knowledge-base path is not a file: "
            f"{file_path}"
        )

    if (
        file_path.suffix.lower()
        not in SUPPORTED_EXTENSIONS
    ):

        raise ValueError(
            f"Unsupported knowledge-base file type: "
            f"{file_path.suffix}"
        )


# ============================================================
# CONTENT VALIDATION
# ============================================================

def _validate_content(
    *,
    content: str,
    file_path: Path,
) -> None:
    """
    Validate document content.
    """

    if not content.strip():

        raise ValueError(
            f"Knowledge-base document is empty: "
            f"{file_path.name}"
        )

    if (
        len(
            content.strip()
        )
        < MIN_DOCUMENT_CHARACTERS
    ):

        raise ValueError(
            f"Knowledge-base document is too short: "
            f"{file_path.name}"
        )

    has_h1 = any(
        line.strip().startswith(
            "# "
        )
        for line in content.splitlines()
    )

    if not has_h1:

        raise ValueError(
            f"Knowledge-base document does not contain "
            f"a Markdown H1 title: "
            f"{file_path.name}"
        )


# ============================================================
# SINGLE DOCUMENT LOADER
# ============================================================

def load_document(
    file_path: Path,
    *,
    category: str,
) -> KnowledgeDocument:
    """
    Load one validated knowledge-base document.
    """

    if category not in SUPPORTED_CATEGORIES:

        raise ValueError(
            f"Unsupported knowledge category: "
            f"{category}"
        )

    file_path = (
        Path(
            file_path
        )
        .resolve()
    )

    _validate_file(
        file_path
    )

    try:

        content = (
            file_path.read_text(
                encoding="utf-8"
            )
        )

    except UnicodeDecodeError as exc:

        raise ValueError(
            f"Knowledge-base document is not valid UTF-8: "
            f"{file_path.name}"
        ) from exc

    except OSError as exc:

        raise OSError(
            f"Unable to read knowledge-base document: "
            f"{file_path}"
        ) from exc

    _validate_content(
        content=content,
        file_path=file_path,
    )

    title = (
        _extract_title(
            content,
            file_path.name,
        )
    )

    document_id = (
        _build_document_id(
            category,
            file_path,
        )
    )

    return KnowledgeDocument(
        document_id=document_id,
        title=title,
        category=category,
        source_name=file_path.name,
        source_path=file_path,
        content=content,
        character_count=len(
            content
        ),
    )


# ============================================================
# CATEGORY FILE DISCOVERY
# ============================================================

def discover_category_files(
    directory: Path,
) -> tuple[Path, ...]:
    """
    Discover supported Markdown files in one category folder.

    Files are returned in deterministic alphabetical order.
    """

    directory = (
        Path(
            directory
        )
        .resolve()
    )

    if not directory.exists():

        raise FileNotFoundError(
            f"Knowledge-base directory does not exist: "
            f"{directory}"
        )

    if not directory.is_dir():

        raise ValueError(
            f"Knowledge-base path is not a directory: "
            f"{directory}"
        )

    files = tuple(
        sorted(
            (
                path
                for path in directory.iterdir()
                if (
                    path.is_file()
                    and path.suffix.lower()
                    in SUPPORTED_EXTENSIONS
                )
            ),
            key=lambda path: (
                path.name.lower()
            ),
        )
    )

    return files


# ============================================================
# CATEGORY LOADER
# ============================================================

def load_category_documents(
    category: str,
) -> tuple[KnowledgeDocument, ...]:
    """
    Load all documents belonging to one category.
    """

    if category not in SUPPORTED_CATEGORIES:

        raise ValueError(
            f"Unsupported knowledge category: "
            f"{category}"
        )

    directory = (
        SUPPORTED_CATEGORIES[
            category
        ]
    )

    files = (
        discover_category_files(
            directory
        )
    )

    documents = tuple(
        load_document(
            file_path,
            category=category,
        )
        for file_path in files
    )

    return documents


# ============================================================
# COMPLETE KNOWLEDGE-BASE LOADER
# ============================================================

def load_knowledge_base(
    *,
    validate_expected_count: bool = True,
) -> tuple[KnowledgeDocument, ...]:
    """
    Load the complete EcoShield knowledge base.

    Parameters
    ----------
    validate_expected_count:
        When True, require exactly EXPECTED_DOCUMENT_COUNT
        documents.

    Returns
    -------
    tuple[KnowledgeDocument, ...]
        All validated knowledge documents.
    """

    documents: list[
        KnowledgeDocument
    ] = []

    for category in (
        CATEGORY_CYBERSECURITY,
        CATEGORY_SUSTAINABILITY,
    ):

        documents.extend(
            load_category_documents(
                category
            )
        )

    # --------------------------------------------------------
    # Ensure unique document identifiers
    # --------------------------------------------------------

    document_ids = [
        document.document_id
        for document in documents
    ]

    if (
        len(
            document_ids
        )
        != len(
            set(
                document_ids
            )
        )
    ):

        raise ValueError(
            "Duplicate knowledge-base document IDs detected."
        )

    # --------------------------------------------------------
    # Optional expected-count validation
    # --------------------------------------------------------

    if (
        validate_expected_count
        and len(
            documents
        )
        != EXPECTED_DOCUMENT_COUNT
    ):

        raise ValueError(
            "Unexpected number of knowledge-base documents. "
            f"Expected {EXPECTED_DOCUMENT_COUNT}, "
            f"found {len(documents)}."
        )

    return tuple(
        documents
    )


# ============================================================
# DOCUMENT LOOKUP
# ============================================================

def get_document_by_id(
    document_id: str,
    documents: Iterable[
        KnowledgeDocument
    ] | None = None,
) -> KnowledgeDocument | None:
    """
    Find a document by its stable document ID.

    Returns None if no matching document exists.
    """

    normalized_id = (
        str(
            document_id
        )
        .strip()
        .lower()
    )

    if not normalized_id:
        return None

    source_documents = (
        tuple(
            documents
        )
        if documents is not None
        else load_knowledge_base()
    )

    for document in (
        source_documents
    ):

        if (
            document.document_id.lower()
            == normalized_id
        ):

            return document

    return None


# ============================================================
# CATEGORY FILTER
# ============================================================

def filter_documents_by_category(
    documents: Iterable[
        KnowledgeDocument
    ],
    category: str,
) -> tuple[KnowledgeDocument, ...]:
    """
    Return only documents belonging to a category.
    """

    if category not in SUPPORTED_CATEGORIES:

        raise ValueError(
            f"Unsupported knowledge category: "
            f"{category}"
        )

    return tuple(
        document
        for document in documents
        if document.category
        == category
    )


# ============================================================
# KNOWLEDGE-BASE SUMMARY
# ============================================================

def get_knowledge_base_summary(
    documents: Iterable[
        KnowledgeDocument
    ] | None = None,
) -> dict[str, int]:
    """
    Return simple knowledge-base statistics.
    """

    source_documents = (
        tuple(
            documents
        )
        if documents is not None
        else load_knowledge_base()
    )

    cybersecurity_count = sum(
        1
        for document
        in source_documents
        if document.category
        == CATEGORY_CYBERSECURITY
    )

    sustainability_count = sum(
        1
        for document
        in source_documents
        if document.category
        == CATEGORY_SUSTAINABILITY
    )

    total_characters = sum(
        document.character_count
        for document
        in source_documents
    )

    return {
        "total_documents": len(
            source_documents
        ),
        "cybersecurity_documents": (
            cybersecurity_count
        ),
        "sustainability_documents": (
            sustainability_count
        ),
        "total_characters": (
            total_characters
        ),
    }