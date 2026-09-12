"""
EcoShield AI
AI Advisor Service

This module owns the orchestration contract for EcoShield's
knowledge and question-answering Advisor.

Responsibilities:
- Normalize and validate Advisor questions
- Keep Advisor questions inside EcoShield's supported scope
- Classify questions deterministically
- Decide whether stored assessment context is relevant
- Map Advisor question types to existing LLM response modes
- Define normalized Advisor request/result contracts

The following responsibilities remain in existing frozen layers:
- Knowledge retrieval / reranking -> src.rag.retriever
- LLM generation / Responsible-AI validation -> src.ai.llm_client
- Risk calculation -> src.risk_engine
- Recommendation generation -> src.recommendation

RAG execution, LLM execution, runtime dependency construction,
fallback orchestration, and frontend-state synchronization are
connected in later Phase-10 checkpoints.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from enum import Enum
from pydoc import text
from typing import Any

from config.config import (
    RuntimeConfig,
    load_runtime_config,
)

from src.ai.llm_client import (
    LLMClient,
    LLMConfig,
    LLMGenerationStatus,
    LLMProvider,
    LLMResponse,
    LLMResponseMode,
    build_llm_client,
    build_llm_request_from_retrieval,
    generate_llm_response,
)

from src.rag.retriever import (
    EcoShieldRetriever,
    RetrievalContext,
    build_retriever,
    retrieve,
)
from src.recommendation import RecommendationResult
from src.risk_engine import RiskAssessment


# ============================================================
# CONSTANTS
# ============================================================

MAX_ADVISOR_QUESTION_LENGTH = 2000
DEFAULT_ADVISOR_TOP_K = 5
GENERAL_KNOWLEDGE_ADVISOR_TOP_K = 3
ASSESSMENT_EXPLANATION_ADVISOR_TOP_K = 3

# ============================================================
# ENUMS
# ============================================================

class AdvisorQuestionType(str, Enum):
    """
    Supported EcoShield Advisor question categories.
    """

    GENERAL_KNOWLEDGE = "general_knowledge"
    ASSESSMENT_EXPLANATION = "assessment_explanation"
    SECURITY_GUIDANCE = "security_guidance"
    SUSTAINABILITY_GUIDANCE = "sustainability_guidance"


class AdvisorGenerationStatus(str, Enum):
    """
    Overall processing status for an Advisor request.
    """

    SUCCESS = "success"
    FALLBACK = "fallback"
    UNAVAILABLE = "unavailable"
    ERROR = "error"


# ============================================================
# PUBLIC DATA CONTRACTS
# ============================================================

@dataclass(frozen=True)
class AdvisorRuntimeSettings:
    """
    Runtime behavior derived from EcoShield's centralized
    RuntimeConfig.

    assessment_mode remains the single source of truth.
    """

    assessment_mode: str
    use_rag: bool
    use_ai: bool

@dataclass(frozen=True)
class AdvisorRequest:
    """
    Normalized request passed through the Advisor service.
    """

    question: str
    question_type: AdvisorQuestionType

    assessment: RiskAssessment | None = None
    recommendation: RecommendationResult | None = None

    assessment_context_used: bool = False

    use_rag: bool = True
    use_ai: bool = True


@dataclass(frozen=True)
class AdvisorResult:
    """
    Normalized result returned by the EcoShield Advisor.
    """

    question: str
    question_type: AdvisorQuestionType

    answer: str
    status: AdvisorGenerationStatus

    assessment_context_used: bool = False

    rag_enabled: bool = False
    ai_enabled: bool = False

    rag_attempted: bool = False
    ai_attempted: bool = False

    rag_succeeded: bool = False
    ai_succeeded: bool = False

    used_fallback: bool = False

    retrieval: RetrievalContext | None = None
    llm_response: LLMResponse | None = None

    warnings: tuple[str, ...] = field(default_factory=tuple)
    errors: tuple[str, ...] = field(default_factory=tuple)

    def to_dict(self) -> dict[str, Any]:
        return asdict(self)

# ============================================================
# RUNTIME CONFIGURATION
# ============================================================

def resolve_advisor_runtime_settings(
    config: RuntimeConfig | None = None,
) -> AdvisorRuntimeSettings:
    """
    Resolve Advisor runtime behavior from EcoShield's existing
    centralized RuntimeConfig.

    Rules:
    - deterministic -> RAG disabled, AI disabled
    - rag           -> RAG enabled, AI disabled
    - ai            -> RAG enabled, AI enabled

    No Advisor-specific environment flags are introduced.
    """

    runtime_config = (
        config
        if config is not None
        else load_runtime_config()
    )

    if not isinstance(
        runtime_config,
        RuntimeConfig,
    ):
        raise TypeError(
            "config must be a RuntimeConfig."
        )

    return AdvisorRuntimeSettings(
        assessment_mode=runtime_config.assessment_mode,
        use_rag=runtime_config.use_rag,
        use_ai=runtime_config.use_ai,
    )

def build_advisor_llm_config(
    config: RuntimeConfig,
) -> LLMConfig:
    """
    Convert centralized RuntimeConfig into the frozen LLMConfig
    required by EcoShield's Responsible-AI generation layer.

    This function does not read environment variables itself.
    """

    if not isinstance(
        config,
        RuntimeConfig,
    ):
        raise TypeError(
            "config must be a RuntimeConfig."
        )

    return LLMConfig(
        provider=LLMProvider(
            config.llm_provider
        ),
        model=config.llm_model,
        base_url=config.llm_base_url,
        api_key=config.llm_api_key,
        temperature=config.llm_temperature,
        max_output_tokens=(
            config.llm_max_output_tokens
        ),
        timeout_seconds=(
            config.llm_timeout_seconds
        ),
        enabled=True,
    )


def build_advisor_llm_client(
    config: RuntimeConfig,
) -> LLMClient | None:
    """
    Build the configured LLM client only when EcoShield is
    running in AI mode.

    Deterministic and RAG-only modes never construct an LLM
    provider client.
    """

    if not isinstance(
        config,
        RuntimeConfig,
    ):
        raise TypeError(
            "config must be a RuntimeConfig."
        )

    if not config.use_ai:
        return None

    return build_llm_client(
        build_advisor_llm_config(
            config
        )
    )

# ============================================================
# QUESTION-SCOPE VOCABULARY
# ============================================================

_SECURITY_TERMS = frozenset(
    {
        "account",
        "accounts",
        "backup",
        "credential",
        "credentials",
        "data",
        "delete",
        "deleted",
        "deletion",
        "device security",
        "encrypt",
        "encrypted",
        "encryption",
        "erase",
        "erasure",
        "factory reset",
        "file",
        "files",
        "format",
        "formatting",
        "password",
        "personal data",
        "privacy",
        "reset",
        "sanitize",
        "sanitization",
        "secure erase",
        "security",
        "sensitive data",
        "sign out",
        "ssd",
        "storage",
        "wipe",
        "wiping",
    }
)


_SUSTAINABILITY_TERMS = frozenset(
    {
        "circular economy",
        "device lifecycle",
        "dispose",
        "disposal",
        "donate",
        "donation",
        "electronic waste",
        "environment",
        "environmental",
        "e-waste",
        "ewaste",
        "lifecycle",
        "recycle",
        "recycling",
        "repair",
        "resale",
        "resell",
        "reuse",
        "reusing",
        "sustainability",
        "sustainable",
    }
)


_DEVICE_TERMS = frozenset(
    {
        "computer",
        "desktop",
        "device",
        "electronics",
        "hard drive",
        "hdd",
        "laptop",
        "memory card",
        "mobile",
        "phone",
        "smartphone",
        "ssd",
        "storage",
        "tablet",
        "usb",
    }
)


_ASSESSMENT_REFERENCE_PHRASES = (
    "my assessment",
    "my result",
    "my results",
    "my risk",
    "my risk score",
    "my score",
    "my recommendation",
    "my recommendations",
    "my device",
    "this device",
    "this laptop",
    "this phone",
    "this computer",
    "this tablet",
    "my laptop",
    "my phone",
    "my computer",
    "my tablet",
    "based on my assessment",
    "based on my result",
    "why did i get",
    "why does ecoshield say",
    "why am i high risk",
    "why is it high risk",
    "why is my device high risk",
    "why is my laptop high risk",
    "why is my phone high risk",
    "why is it not ready",
    "why is my device not ready",
    "why is my laptop not ready",
    "why is my phone not ready",
    "what should i fix",
    "what did you detect",
    "what was detected",
)


_ASSESSMENT_EXPLANATION_PHRASES = (
    "explain my assessment",
    "explain my result",
    "explain my results",
    "explain my recommendation",
    "explain my recommendations",
    "why did i get",
    "why does ecoshield say",
    "why am i high risk",
    "why is my device high risk",
    "why is my laptop high risk",
    "why is my phone high risk",
    "why is my device not ready",
    "why is my laptop not ready",
    "why is my phone not ready",
    "why can't i donate",
    "why cant i donate",
    "why can't i sell",
    "why cant i sell",
    "what problems were detected",
    "what did you detect",
    "what should i fix from my assessment",

    # Assessment-specific transfer/readiness questions.
    "is my device safe to sell",
    "is my laptop safe to sell",
    "is my phone safe to sell",
    "is my computer safe to sell",
    "is my device safe to donate",
    "is my device safe to transfer",
    "is my device ready to sell",
    "is my device ready for sale",
    "is my device ready for resale",
    "is my device ready to donate",
    "is my device ready for transfer",
    "can i sell my device now",
    "can i donate my device now",
    "can i transfer my device now",
)

_TRANSFER_SECURITY_PHRASES = (
    "prepare a laptop for resale",
    "prepare a device for resale",
    "prepare a computer for resale",
    "prepare a phone for resale",
    "prepare a laptop for sale",
    "prepare a device for sale",
    "prepare a computer for sale",
    "prepare a phone for sale",
    "prepare a laptop for donation",
    "prepare a device for donation",
    "prepare a computer for donation",
    "prepare a phone for donation",
    "before selling a laptop",
    "before selling a device",
    "before selling a computer",
    "before selling a phone",
    "before donating a laptop",
    "before donating a device",
    "before transferring a device",
)

_GENERIC_READINESS_CLAIM_PATTERNS = (
    "device is ready for transfer",
    "device is ready for sale",
    "device is ready for resale",
    "device is ready for donation",
    "your device is ready for transfer",
    "your device is ready for sale",
    "your device is ready for resale",
    "your device is ready for donation",
    "ssd is securely erased and",
)

# ============================================================
# NORMALIZATION
# ============================================================

def normalize_advisor_question(question: str) -> str:
    """
    Validate and normalize a user question.

    Raises:
        TypeError:
            If question is not a string.

        ValueError:
            If the question is empty or exceeds the supported
            maximum length.
    """

    if not isinstance(question, str):
        raise TypeError(
            "Advisor question must be a string."
        )

    normalized = " ".join(
        question.strip().split()
    )

    if not normalized:
        raise ValueError(
            "Advisor question cannot be empty."
        )

    if len(normalized) > MAX_ADVISOR_QUESTION_LENGTH:
        raise ValueError(
            "Advisor question exceeds the maximum supported length."
        )

    return normalized


def _normalized_question_text(question: str) -> str:
    """
    Return a lowercase normalized representation used only for
    deterministic routing.
    """

    return normalize_advisor_question(
        question
    ).casefold()


# ============================================================
# GENERIC TEXT MATCHING
# ============================================================

def _contains_term(
    text: str,
    terms: frozenset[str],
) -> bool:
    """
    Return True when any supported phrase/term occurs in text.
    """

    return any(
        term in text
        for term in terms
    )


def _contains_phrase(
    text: str,
    phrases: tuple[str, ...],
) -> bool:
    """
    Return True when any supplied phrase occurs in text.
    """

    return any(
        phrase in text
        for phrase in phrases
    )


# ============================================================
# SCOPE DETECTION
# ============================================================

def is_ecoshield_scope_question(
    question: str,
) -> bool:
    """
    Determine whether a question falls inside EcoShield's
    cybersecurity, device-security, privacy, e-waste,
    sustainability, or assessment scope.
    """

    text = _normalized_question_text(
        question
    )

    if _contains_phrase(
        text,
        _ASSESSMENT_REFERENCE_PHRASES,
    ):
        return True

    if _contains_term(
        text,
        _SECURITY_TERMS,
    ):
        return True

    if _contains_term(
        text,
        _SUSTAINABILITY_TERMS,
    ):
        return True

    if _contains_term(
        text,
        _DEVICE_TERMS,
    ):
        return True

    ecoshield_terms = (
        "ecoshield",
        "risk assessment",
        "risk score",
        "device risk",
        "data protection",
        "ownership transfer",
    )

    return any(
        term in text
        for term in ecoshield_terms
    )


# ============================================================
# ASSESSMENT-REFERENCE DETECTION
# ============================================================

def question_references_assessment(
    question: str,
) -> bool:
    """
    Determine whether the question refers to the user's current
    device/assessment/result rather than only requesting generic
    educational knowledge.
    """

    text = _normalized_question_text(
        question
    )

    return _contains_phrase(
        text,
        _ASSESSMENT_REFERENCE_PHRASES,
    )


# ============================================================
# QUESTION CLASSIFICATION
# ============================================================

def classify_advisor_question(
    question: str,
) -> AdvisorQuestionType:
    """
    Classify a supported Advisor question deterministically.

    Priority:
    1. Assessment explanation
    2. Security guidance
    3. Sustainability guidance
    4. General knowledge

    This function does not invoke an LLM.
    """

    text = _normalized_question_text(
        question
    )

    # --------------------------------------------------------
    # 1. Assessment explanation
    # --------------------------------------------------------

    if _contains_phrase(
        text,
        _ASSESSMENT_EXPLANATION_PHRASES,
    ):
        return (
            AdvisorQuestionType.ASSESSMENT_EXPLANATION
        )

    if question_references_assessment(
        question
    ):
        assessment_explanation_terms = (
            "risk",
            "score",
            "not ready",
            "ready",
            "recommendation",
            "detected",
            "problem",
            "issue",
            "why",
            "explain",
        )

        if any(
            term in text
            for term in assessment_explanation_terms
        ):
            return (
                AdvisorQuestionType.ASSESSMENT_EXPLANATION
            )

        # --------------------------------------------------------
    # General educational / definition questions
    # --------------------------------------------------------

    general_knowledge_starters = (
        "what is ",
        "what are ",
        "what does ",
        "define ",
        "explain what ",
        "meaning of ",
        "what do you mean by ",
    )

    if text.startswith(
        general_knowledge_starters
    ):
        return (
            AdvisorQuestionType.GENERAL_KNOWLEDGE
        )
     
       # --------------------------------------------------------
    # 2. Security guidance
    # --------------------------------------------------------

    if _contains_phrase(
        text,
        _TRANSFER_SECURITY_PHRASES,
    ):
        return (
            AdvisorQuestionType.SECURITY_GUIDANCE
        )

    if _contains_term(
        text,
        _SECURITY_TERMS,
    ):
        return (
            AdvisorQuestionType.SECURITY_GUIDANCE
        )
    # --------------------------------------------------------
    # 3. Sustainability guidance
    # --------------------------------------------------------

    if _contains_term(
        text,
        _SUSTAINABILITY_TERMS,
    ):
        return (
            AdvisorQuestionType.SUSTAINABILITY_GUIDANCE
        )

    # --------------------------------------------------------
    # 4. General supported EcoShield knowledge
    # --------------------------------------------------------

    return (
        AdvisorQuestionType.GENERAL_KNOWLEDGE
    )


# ============================================================
# ASSESSMENT-CONTEXT SELECTION
# ============================================================

def should_use_assessment_context(
    question: str,
    question_type: AdvisorQuestionType,
    *,
    assessment: RiskAssessment | None = None,
    recommendation: RecommendationResult | None = None,
) -> bool:
    """
    Decide whether stored deterministic assessment context should
    be attached to the Advisor request.

    The mere existence of an assessment does not cause it to be
    included automatically.
    """

    if (
        assessment is None
        and recommendation is None
    ):
        return False

    if (
        question_type
        == AdvisorQuestionType.GENERAL_KNOWLEDGE
    ):
        return False

    if (
        question_type
        == AdvisorQuestionType.ASSESSMENT_EXPLANATION
    ):
        return True

    return question_references_assessment(
        question
    )


# ============================================================
# LLM MODE MAPPING
# ============================================================

def get_llm_mode_for_question_type(
    question_type: AdvisorQuestionType,
) -> LLMResponseMode:
    """
    Map Advisor question categories onto the existing frozen
    Responsible-AI LLM response modes.
    """

    if not isinstance(
        question_type,
        AdvisorQuestionType,
    ):
        raise TypeError(
            "question_type must be an AdvisorQuestionType."
        )

    mapping = {
        AdvisorQuestionType.GENERAL_KNOWLEDGE:
            LLMResponseMode.KNOWLEDGE_QA,

        AdvisorQuestionType.ASSESSMENT_EXPLANATION:
            LLMResponseMode.EXPLANATION,

        AdvisorQuestionType.SECURITY_GUIDANCE:
            LLMResponseMode.SECURITY_GUIDANCE,

        AdvisorQuestionType.SUSTAINABILITY_GUIDANCE:
            LLMResponseMode.SUSTAINABILITY_GUIDANCE,
    }

    return mapping[
        question_type
    ]


# ============================================================
# REQUEST CONSTRUCTION
# ============================================================

def build_advisor_request(
    question: str,
    *,
    assessment: RiskAssessment | None = None,
    recommendation: RecommendationResult | None = None,
    use_rag: bool = True,
    use_ai: bool = True,
) -> AdvisorRequest:
    """
    Normalize and classify a question, then construct the
    canonical Advisor request.
    """

    normalized_question = (
        normalize_advisor_question(
            question
        )
    )

    if not isinstance(
        use_rag,
        bool,
    ):
        raise TypeError(
            "use_rag must be a boolean."
        )

    if not isinstance(
        use_ai,
        bool,
    ):
        raise TypeError(
            "use_ai must be a boolean."
        )

    question_type = (
        classify_advisor_question(
            normalized_question
        )
    )

    assessment_context_used = (
        should_use_assessment_context(
            normalized_question,
            question_type,
            assessment=assessment,
            recommendation=recommendation,
        )
    )

    return AdvisorRequest(
        question=normalized_question,
        question_type=question_type,
        assessment=(
            assessment
            if assessment_context_used
            else None
        ),
        recommendation=(
            recommendation
            if assessment_context_used
            else None
        ),
        assessment_context_used=(
            assessment_context_used
        ),
        use_rag=use_rag,
        use_ai=use_ai,
    )

def build_advisor_request_from_runtime(
    question: str,
    *,
    assessment: RiskAssessment | None = None,
    recommendation: RecommendationResult | None = None,
    config: RuntimeConfig | None = None,
) -> AdvisorRequest:
    """
    Build the canonical AdvisorRequest using EcoShield's
    centralized runtime configuration.

    Production Advisor orchestration should use this helper
    instead of independently deciding RAG/AI flags.
    """

    runtime = resolve_advisor_runtime_settings(
        config
    )

    return build_advisor_request(
        question,
        assessment=assessment,
        recommendation=recommendation,
        use_rag=runtime.use_rag,
        use_ai=runtime.use_ai,
    )

# ============================================================
# ASSESSMENT-AWARE CONTEXT
# ============================================================

def build_advisor_assessment_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Return the validated device-assessment data only when the
    current Advisor question should use assessment context.

    The Advisor never recalculates or modifies assessment values.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if (
        not request.assessment_context_used
        or request.assessment is None
    ):
        return None

    return dict(
        request.assessment.validated_data
    )

def build_advisor_llm_assessment_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Build a compact assessment context for LLM generation.

    Retrieval may continue using the complete validated assessment,
    while the local LLM receives only the device fields needed to
    explain the deterministic result.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if (
        not request.assessment_context_used
        or request.assessment is None
    ):
        return None

    validated_data = (
        request.assessment.validated_data
    )

    preferred_fields = (
        "device_type",
        "operating_system",
        "storage_type",
        "intended_disposal_method",
    )

    return {
        key: validated_data[key]
        for key in preferred_fields
        if key in validated_data
    }

def build_advisor_risk_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Build authoritative deterministic risk context for the LLM.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    assessment = request.assessment

    if (
        not request.assessment_context_used
        or assessment is None
    ):
        return None

    return {
        "risk_score": assessment.score,
        "risk_level": assessment.risk_level,
        "risk_factors": tuple(
            {
                "code": factor.code,
                "category": factor.category,
                "points": factor.points,
                "message": factor.message,
            }
            for factor in assessment.factors
        ),
        "category_scores": dict(
            assessment.category_scores
        ),
        "uncertainties": tuple(
            assessment.uncertainties
        ),
        "requires_sanitization": (
            assessment.requires_sanitization
        ),
        "device_leaves_owner": (
            assessment.device_leaves_owner
        ),
    }

def build_advisor_llm_risk_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Build compact authoritative risk context for LLM generation.
    """

    risk_context = build_advisor_risk_context(
        request
    )

    if risk_context is None:
        return None

    if (
        request.question_type
        != AdvisorQuestionType.ASSESSMENT_EXPLANATION
    ):
        return risk_context

    return {
        "risk_score": risk_context["risk_score"],
        "risk_level": risk_context["risk_level"],
        "risk_factors": tuple(
            {
                "category": factor["category"],
                "points": factor["points"],
                "message": factor["message"],
            }
            for factor in risk_context[
                "risk_factors"
            ]
        ),
    }

def build_advisor_recommendation_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Build authoritative deterministic recommendation context.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    recommendation = request.recommendation

    if (
        not request.assessment_context_used
        or recommendation is None
    ):
        return None

    return {
        "risk_score": recommendation.risk_score,
        "risk_level": recommendation.risk_level,
        "readiness": recommendation.readiness,
        "summary": recommendation.summary,
        "security_actions": tuple(
            {
                "code": item.code,
                "priority": item.priority,
                "title": item.title,
                "action": item.action,
                "rationale": item.rationale,
            }
            for item in recommendation.security_actions
        ),
        "sustainability_actions": tuple(
            {
                "code": item.code,
                "priority": item.priority,
                "title": item.title,
                "action": item.action,
                "rationale": item.rationale,
            }
            for item in recommendation.sustainability_actions
        ),
        "next_steps": tuple(
            recommendation.next_steps
        ),
        "warnings": tuple(
            recommendation.warnings
        ),
    }

def build_advisor_llm_recommendation_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Build compact authoritative recommendation context for
    assessment-aware LLM explanations.
    """

    recommendation_context = (
        build_advisor_recommendation_context(
            request
        )
    )

    if recommendation_context is None:
        return None

    if (
        request.question_type
        != AdvisorQuestionType.ASSESSMENT_EXPLANATION
    ):
        return recommendation_context

    return {
        "risk_score": (
            recommendation_context["risk_score"]
        ),
        "risk_level": (
            recommendation_context["risk_level"]
        ),
        "readiness": (
            recommendation_context["readiness"]
        ),
        "summary": (
            recommendation_context["summary"]
        ),
        "security_actions": tuple(
            {
                "title": item["title"],
                "action": item["action"],
            }
            for item in recommendation_context[
                "security_actions"
            ]
        ),
        "sustainability_actions": tuple(
            {
                "title": item["title"],
                "action": item["action"],
            }
            for item in recommendation_context[
                "sustainability_actions"
            ]
        ),
        "next_steps": (
            recommendation_context["next_steps"]
        ),
    }

def build_advisor_authority_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Tell the frozen Responsible-AI layer how assessment-specific
    context must be treated.

    These instructions do not replace the frozen LLM safety layer.
    They provide Advisor-specific authority boundaries.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not request.assessment_context_used:
        return None

    return {
        "assessment_context_authoritative": True,
        "risk_score_authoritative": True,
        "risk_level_authoritative": True,
        "readiness_authoritative": True,
        "recommendations_authoritative": True,
        "advisor_must_not_recalculate_risk": True,
        "advisor_must_not_change_readiness": True,
        "advisor_must_not_invent_completed_actions": True,
        "advisor_role": (
            "Explain the existing deterministic EcoShield "
            "assessment and recommendations using retrieved "
            "evidence. Do not replace or override them."
        ),
    }

def resolve_advisor_top_k(
    request: AdvisorRequest,
    top_k: int | None = None,
) -> int:
    """
    Resolve the evidence budget used by the Advisor.

    General-knowledge and assessment-explanation questions use a
    smaller default evidence budget for faster local-LLM generation.

    An explicitly supplied top_k always takes precedence.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    # Explicit override always wins.
    if top_k is not None:
        if isinstance(top_k, bool) or not isinstance(
            top_k,
            int,
        ):
            raise TypeError(
                "top_k must be an integer."
            )

        if top_k <= 0:
            raise ValueError(
                "top_k must be greater than zero."
            )

        return top_k

    # Adaptive defaults.
    if (
        request.question_type
        == AdvisorQuestionType.GENERAL_KNOWLEDGE
    ):
        return GENERAL_KNOWLEDGE_ADVISOR_TOP_K

    if (
        request.question_type
        == AdvisorQuestionType.ASSESSMENT_EXPLANATION
    ):
        return ASSESSMENT_EXPLANATION_ADVISOR_TOP_K

    return DEFAULT_ADVISOR_TOP_K
    if isinstance(top_k, bool) or not isinstance(
        top_k,
        int,
    ):
        raise TypeError(
            "top_k must be an integer."
        )

    if top_k <= 0:
        raise ValueError(
            "top_k must be greater than zero."
        )

    return top_k

def build_advisor_generation_context(
    request: AdvisorRequest,
) -> dict[str, Any] | None:
    """
    Build Advisor-specific generation constraints.

    These constraints supplement the frozen LLM instructions
    without replacing deterministic authority or semantic
    validation.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    context: dict[str, Any] = {}

    authority_context = (
        build_advisor_authority_context(
            request
        )
    )

    if authority_context:
        context.update(
            authority_context
        )

    if (
        request.question_type
        == AdvisorQuestionType.SECURITY_GUIDANCE
    ):
        context[
            "advisor_security_grounding"
        ] = (
            "Use only security claims supported by the retrieved "
            "EcoShield evidence. Do not invent tools, commands, "
            "utilities, sanitization procedures, verification "
            "procedures, guarantees, or device-readiness claims. "
            "When the evidence does not specify an exact procedure, "
            "state that limitation and prefer current manufacturer "
            "or platform-supported documentation."
        )

    return context or None

_SECURITY_PROCEDURAL_TERMS = (
    "secure erase",
    "securely erase",
    "erase an ssd",
    "erase a ssd",
    "erase an hdd",
    "erase a hdd",
    "sanitize",
    "sanitization",
    "wipe",
    "wiping",
    "factory reset",
)


def requires_evidence_bounded_security_response(
    request: AdvisorRequest,
) -> bool:
    """
    Return True when a security question asks for a procedural
    sanitization/reset operation.

    EcoShield handles these questions using retrieved evidence
    directly instead of allowing the LLM to invent unsupported
    commands, tools, or procedures.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if (
        request.question_type
        != AdvisorQuestionType.SECURITY_GUIDANCE
    ):
        return False

    text = request.question.casefold()

    return any(
        term in text
        for term in _SECURITY_PROCEDURAL_TERMS
    )

def build_evidence_bounded_security_result(
    request: AdvisorRequest,
    retrieval_context: RetrievalContext,
) -> AdvisorResult:
    """
    Build a safe grounded response for procedural security
    questions where EcoShield should not allow the LLM to invent
    commands, tools, or sanitization procedures.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not isinstance(
        retrieval_context,
        RetrievalContext,
    ):
        raise TypeError(
            "retrieval_context must be a RetrievalContext."
        )

    answer = (
        "EcoShield's retrieved guidance supports using a "
        "storage-technology-appropriate sanitization process, "
        "but the available evidence does not define one universal "
        "step-by-step procedure for every SSD or device. "
        "Use the current sanitization procedure supported by the "
        "storage manufacturer or operating-system platform. "
        "EcoShield treats device reset and storage sanitization "
        "as separate security considerations, so a reset alone "
        "should not be treated as proof that storage sanitization "
        "has been completed."
    )

    return AdvisorResult(
        question=request.question,
        question_type=request.question_type,
        answer=answer,
        status=AdvisorGenerationStatus.SUCCESS,
        assessment_context_used=(
            request.assessment_context_used
        ),
        rag_enabled=True,
        ai_enabled=request.use_ai,
        rag_attempted=True,
        ai_attempted=False,
        rag_succeeded=True,
        ai_succeeded=False,
        used_fallback=False,
        retrieval=retrieval_context,
        llm_response=None,
        warnings=(
            "EcoShield used evidence-bounded security guidance "
            "for this procedural sanitization question.",
        ),
        errors=(),
    )
# ============================================================
# KNOWLEDGE RETRIEVAL
# ============================================================

def retrieve_advisor_knowledge(
    request: AdvisorRequest,
    *,
    retriever: EcoShieldRetriever | None = None,
    top_k: int = DEFAULT_ADVISOR_TOP_K,
) -> RetrievalContext:
    """
    Retrieve grounded EcoShield knowledge for an Advisor request.

    This function delegates retrieval completely to the existing
    frozen RAG layer. It does not duplicate retrieval, ranking,
    embedding, or document-loading logic.

    Assessment-aware retrieval context is connected separately in
    Phase-10 Step 9. Step 7 retrieves using the normalized user
    question only.
    """

    if not isinstance(
        request,
        AdvisorRequest,
    ):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if isinstance(top_k, bool) or not isinstance(
        top_k,
        int,
    ):
        raise TypeError(
            "top_k must be an integer."
        )

    if top_k <= 0:
        raise ValueError(
            "top_k must be greater than zero."
        )

    active_retriever = (
        retriever
        if retriever is not None
        else build_retriever()
    )

    assessment_context = (
        build_advisor_assessment_context(
            request
        )
    )

    return retrieve(
        active_retriever,
        request.question,
        assessment=assessment_context,
        top_k=top_k,
    )

# ============================================================
# RESPONSIBLE-AI GENERATION
# ============================================================

def generate_advisor_answer(
    request: AdvisorRequest,
    retrieval_context: RetrievalContext,
    *,
    llm_client: LLMClient,
) -> LLMResponse:
    """
    Generate a grounded Advisor answer using EcoShield's existing
    frozen Responsible-AI LLM pipeline.

    Step 8 supplies retrieved evidence and the appropriate
    question mode.

    Assessment/risk/recommendation context is connected more
    completely in Phase-10 Step 9.
    """

    if not isinstance(
        request,
        AdvisorRequest,
    ):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not isinstance(
        retrieval_context,
        RetrievalContext,
    ):
        raise TypeError(
            "retrieval_context must be a RetrievalContext."
        )

    if not isinstance(
        llm_client,
        LLMClient,
    ):
        raise TypeError(
            "llm_client must be an LLMClient."
        )

    assessment_context = (
        build_advisor_llm_assessment_context(
            request
        )
    )

    risk_context = (
        build_advisor_llm_risk_context(
            request
        )
    )

    recommendation_context = (
        build_advisor_llm_recommendation_context(
            request
        )
    )

    generation_context = (
        build_advisor_generation_context(
            request
        )
    )

    llm_request = (
        build_llm_request_from_retrieval(
            user_query=request.question,
            retrieval_context=retrieval_context,
            mode=get_llm_mode_for_question_type(
                request.question_type
            ),
            assessment=assessment_context,
            risk_context=risk_context,
            recommendation_context=(
                recommendation_context
            ),
            additional_context=(
                generation_context
            ),
        )
    )

    return generate_llm_response(
        llm_client,
        llm_request,
    )

# ============================================================
# ADVISOR SECURITY OUTPUT SAFETY
# ============================================================

_UNSUPPORTED_SECURITY_COMMAND_PATTERNS = (
    "sfc /scannow",
    "cipher /s /e",
)


def advisor_security_output_is_safe(
    request: AdvisorRequest,
    llm_response: LLMResponse,
) -> bool:
    """
    Apply a narrow Advisor-layer safety check to generated
    cybersecurity guidance.

    The frozen Responsible-AI layer remains the primary safety
    authority. This additional check prevents known unsupported
    command-level sanitization/reset instructions from being
    presented as accepted EcoShield security guidance.

    Broader semantic grounding is handled in the dedicated
    Phase-10 safety checkpoint.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not isinstance(llm_response, LLMResponse):
        raise TypeError(
            "llm_response must be an LLMResponse."
        )

    if (
        request.question_type
        != AdvisorQuestionType.SECURITY_GUIDANCE
    ):
        return True

    response_text = llm_response.text.casefold()

    return not any(
        pattern in response_text
        for pattern in _UNSUPPORTED_SECURITY_COMMAND_PATTERNS
    )

# ============================================================
# ADVISOR SEMANTIC OUTPUT VALIDATION
# ============================================================

_GENERIC_ASSESSMENT_CLAIM_PATTERNS = (
    "your ecoshield assessment",
    "your assessment context",
    "your risk score",
    "your readiness",
    "based on your assessment",
    "based on the ecoshield assessment",
    "ecoshield assessed your device",
)

_ABSOLUTE_SECURITY_CLAIM_PATTERNS = (
    "guarantee that",
    "guarantees that",
    "guaranteed to",
    "100% secure",
    "completely unrecoverable",
    "impossible to recover",
    "irretrievably deleted",
    "irretrievably erased",
    "make it unrecoverable",
    "make data unrecoverable",
    "makes it unrecoverable",
    "makes data unrecoverable",
    "ensure that no data remains",
    "ensures that no data remains",
    "ensure that the device is secure",
    "ensures that the device is secure",
    "ensure that your device is secure",
    "ensures that your device is secure",
    "ensure that your ssd is securely erased",
    "ensures that your ssd is securely erased",
)

_READY_AFTER_ACTION_PATTERNS = (
    "ensure that the device is secure and ready",
    "ensure that your device is secure and ready",
    "will ensure that the device is secure and ready",
    "will ensure that your device is secure and ready",
    "device will be ready for sale",
    "device will be ready for resale",
    "device will be ready for transfer",
    "device will be ready for donation",
)

_STORAGE_RESET_MISMATCH_PATTERNS = (
    "factory reset the ssd",
    "factory reset your ssd",
    "factory reset the hdd",
    "factory reset your hdd",
    "factory reset the hard drive",
    "factory reset your hard drive",
)

_COMMAND_LEVEL_GUIDANCE_MARKERS = (
    "system file checker",
    "disk cleanup",
    "ata secure erase command",
    "ccleaner",
    "eraser",
)


def validate_advisor_semantic_output(
    request: AdvisorRequest,
    llm_response: LLMResponse,
) -> tuple[str, ...]:
    """
    Validate generated Advisor text against EcoShield's semantic
    authority and grounding boundaries.

    This validator does not recalculate risk or recommendations.
    It only determines whether generated text is safe to accept.
    """

    if not isinstance(request, AdvisorRequest):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not isinstance(llm_response, LLMResponse):
        raise TypeError(
            "llm_response must be an LLMResponse."
        )

    text = llm_response.text.casefold()
    violations: list[str] = []

    # Existing narrow security-command safeguard.
    if not advisor_security_output_is_safe(
        request,
        llm_response,
    ):
        violations.append(
            "UNSUPPORTED_SECURITY_COMMAND"
        )

    # Generic questions must never imply that EcoShield supplied
    # device-specific assessment state.
    if not request.assessment_context_used:
        if any(
            pattern in text
            for pattern in _GENERIC_ASSESSMENT_CLAIM_PATTERNS
        ):
            violations.append(
                "INVENTED_ASSESSMENT_CONTEXT"
            )

    # EcoShield must not make absolute sanitization/security claims.
    if any(
        pattern in text
        for pattern in _ABSOLUTE_SECURITY_CLAIM_PATTERNS
    ):
        violations.append(
            "ABSOLUTE_SECURITY_CLAIM"
        )

    # A generated answer cannot independently promote readiness.
    if (
        request.assessment_context_used
        and request.recommendation is not None
        and request.recommendation.readiness != "Ready"
        and any(
            pattern in text
            for pattern in _READY_AFTER_ACTION_PATTERNS
        )
    ):
        violations.append(
            "UNAUTHORIZED_READINESS_CHANGE"
        )

        # Device reset and storage sanitization are distinct operations.
    if any(
        pattern in text
        for pattern in _STORAGE_RESET_MISMATCH_PATTERNS
    ):
        violations.append(
            "STORAGE_DEVICE_OPERATION_MISMATCH"
        )

    # Do not accept unsupported command/tool-level security guidance.
    if any(
        marker in text
        for marker in _COMMAND_LEVEL_GUIDANCE_MARKERS
    ):
        violations.append(
            "UNSUPPORTED_TOOL_GUIDANCE"
        )

    # Generic questions cannot independently declare device readiness.
    if not request.assessment_context_used:
        if any(
            pattern in text
            for pattern in _GENERIC_READINESS_CLAIM_PATTERNS
        ):
            violations.append(
                "UNSUPPORTED_GENERIC_READINESS_CLAIM"
            )

    return tuple(dict.fromkeys(violations))

# ============================================================
# RESULT HELPERS
# ============================================================

def build_ai_advisor_result(
    request: AdvisorRequest,
    retrieval_context: RetrievalContext,
    llm_response: LLMResponse,
) -> AdvisorResult:
    """
    Convert the frozen LLMResponse into the normalized
    AdvisorResult contract.
    """

    if not isinstance(
        request,
        AdvisorRequest,
    ):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not isinstance(
        retrieval_context,
        RetrievalContext,
    ):
        raise TypeError(
            "retrieval_context must be a RetrievalContext."
        )

    if not isinstance(
        llm_response,
        LLMResponse,
    ):
        raise TypeError(
            "llm_response must be an LLMResponse."
        )

    if (
        llm_response.status
        == LLMGenerationStatus.SUCCESS
        and not llm_response.used_fallback
    ):
        advisor_status = (
            AdvisorGenerationStatus.SUCCESS
        )
        ai_succeeded = True
        used_fallback = False
        errors: tuple[str, ...] = ()

    else:
        advisor_status = (
            AdvisorGenerationStatus.FALLBACK
        )
        ai_succeeded = False
        used_fallback = True
        errors = (
            "AI_GENERATION_FALLBACK",
        )

    warnings: tuple[str, ...] = ()

    if used_fallback:
        warnings = (
            "EcoShield used its safe grounded fallback because "
            "the requested AI response could not be accepted.",
        )

    return AdvisorResult(
        question=request.question,
        question_type=request.question_type,
        answer=llm_response.text,
        status=advisor_status,
        assessment_context_used=(
            request.assessment_context_used
        ),
        rag_enabled=True,
        ai_enabled=True,
        rag_attempted=True,
        ai_attempted=True,
        rag_succeeded=True,
        ai_succeeded=ai_succeeded,
        used_fallback=used_fallback,
        retrieval=retrieval_context,
        llm_response=llm_response,
        warnings=warnings,
        errors=errors,
    )

def build_retrieval_only_advisor_result(
    request: AdvisorRequest,
    retrieval_context: RetrievalContext,
) -> AdvisorResult:
    """
    Build the permanent Advisor result used in RAG-only mode.

    RAG-only mode is an intentional supported runtime mode.
    Grounded EcoShield knowledge is retrieved successfully while
    AI generation remains disabled by runtime configuration.
    """

    if not isinstance(
        request,
        AdvisorRequest,
    ):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    if not isinstance(
        retrieval_context,
        RetrievalContext,
    ):
        raise TypeError(
            "retrieval_context must be a RetrievalContext."
        )

    return AdvisorResult(
        question=request.question,
        question_type=request.question_type,
        answer=(
            "Relevant grounded EcoShield knowledge was retrieved "
            "successfully. AI generation is disabled in the current "
            "RAG-only runtime mode."
        ),
        status=AdvisorGenerationStatus.SUCCESS,
        assessment_context_used=(
            request.assessment_context_used
        ),
        rag_enabled=True,
        ai_enabled=False,
        rag_attempted=True,
        ai_attempted=False,
        rag_succeeded=True,
        ai_succeeded=False,
        used_fallback=False,
        retrieval=retrieval_context,
        llm_response=None,
        warnings=(),
        errors=(),
    )

def build_unavailable_advisor_result(
    request: AdvisorRequest,
    *,
    answer: str,
    warning: str | None = None,
    error: str | None = None,
) -> AdvisorResult:
    """
    Construct a normalized unavailable result.

    This helper is used by later Phase-10 orchestration when
    grounded guidance cannot currently be produced.
    """

    if not isinstance(
        request,
        AdvisorRequest,
    ):
        raise TypeError(
            "request must be an AdvisorRequest."
        )

    normalized_answer = (
        answer.strip()
        if isinstance(answer, str)
        else ""
    )

    if not normalized_answer:
        raise ValueError(
            "Unavailable Advisor result requires an answer."
        )

    warnings = (
        (warning.strip(),)
        if isinstance(warning, str)
        and warning.strip()
        else ()
    )

    errors = (
        (error.strip(),)
        if isinstance(error, str)
        and error.strip()
        else ()
    )

    return AdvisorResult(
        question=request.question,
        question_type=request.question_type,
        answer=normalized_answer,
        status=AdvisorGenerationStatus.UNAVAILABLE,
        assessment_context_used=(
            request.assessment_context_used
        ),
        rag_enabled=request.use_rag,
        ai_enabled=request.use_ai,
        warnings=warnings,
        errors=errors,
    )

def build_semantic_rejection_advisor_result(
    request: AdvisorRequest,
    retrieval_context: RetrievalContext,
    llm_response: LLMResponse,
    violations: tuple[str, ...],
) -> AdvisorResult:
    """
    Return a safe grounded fallback when generated Advisor text
    violates EcoShield semantic authority or safety boundaries.
    """

    if request.assessment_context_used:
        answer = (
            "EcoShield retrieved relevant grounded guidance, but the "
            "generated explanation could not be safely accepted against "
            "the current deterministic assessment. The existing risk "
            "result and recommendation remain authoritative. Complete "
            "the required deterministic actions and run a new assessment "
            "before treating the device's risk or readiness as changed."
        )
    else:
        answer = (
            "EcoShield retrieved relevant grounded guidance, but the "
            "generated answer could not be safely validated against "
            "EcoShield's security and grounding rules. Use the retrieved "
            "EcoShield evidence and the device or storage manufacturer's "
            "supported procedure instead."
        )

    return AdvisorResult(
        question=request.question,
        question_type=request.question_type,
        answer=answer,
        status=AdvisorGenerationStatus.FALLBACK,
        assessment_context_used=(
            request.assessment_context_used
        ),
        rag_enabled=True,
        ai_enabled=True,
        rag_attempted=True,
        ai_attempted=True,
        rag_succeeded=True,
        ai_succeeded=False,
        used_fallback=True,
        retrieval=retrieval_context,
        llm_response=llm_response,
        warnings=(
            "EcoShield rejected the generated answer because it "
            "violated Advisor semantic safety or authority rules.",
        ),
        errors=violations,
    )
# ============================================================
# PUBLIC SERVICE CONTRACT
# ============================================================

def ask_advisor(
    question: str,
    *,
    assessment: RiskAssessment | None = None,
    recommendation: RecommendationResult | None = None,
    config: RuntimeConfig | None = None,
    retriever: EcoShieldRetriever | None = None,
    llm_client: LLMClient | None = None,
       top_k: int | None = None,
) -> AdvisorResult:
    """
    Public EcoShield Advisor service entry point.

    Phase-10 Step 5 establishes the deterministic service
    foundation only.

    Runtime configuration, RAG execution, Responsible-AI LLM
    execution, enrichment fallbacks, and frontend state
    synchronization are connected in subsequent Phase-10
    checkpoints.
    """
    runtime_config = (
        config
        if config is not None
        else load_runtime_config()
    )

    if not isinstance(
        runtime_config,
        RuntimeConfig,
    ):
        raise TypeError(
            "config must be a RuntimeConfig."
        )
    
    request = build_advisor_request_from_runtime(
        question,
        assessment=assessment,
        recommendation=recommendation,
        config=runtime_config,
    )

    if not is_ecoshield_scope_question(
        request.question
    ):
        return build_unavailable_advisor_result(
            request,
            answer=(
                "That question is outside the EcoShield Advisor's "
                "device-security, privacy, e-waste, sustainability, "
                "and device-assessment scope."
            ),
            error="ADVISOR_OUT_OF_SCOPE",
        )

    if (
        request.question_type
        == AdvisorQuestionType.ASSESSMENT_EXPLANATION
        and not request.assessment_context_used
    ):
        return build_unavailable_advisor_result(
            request,
            answer=(
                "A completed EcoShield Device Assessment is needed "
                "before I can explain device-specific risk, readiness, "
                "or recommendation results."
            ),
            warning=(
                "Complete the Device Assessment to receive "
                "device-specific guidance."
            ),
            error="ASSESSMENT_CONTEXT_UNAVAILABLE",
        )

        # --------------------------------------------------------
    # Deterministic mode
    # --------------------------------------------------------

    if not request.use_rag:
        return build_unavailable_advisor_result(
            request,
            answer=(
                "EcoShield recognized this question, but knowledge "
                "retrieval and AI generation are disabled in the "
                "current deterministic runtime mode."
            ),
            warning=(
                "Use RAG or AI assessment mode to enable grounded "
                "Advisor knowledge retrieval."
            ),
            error="ADVISOR_GENERATION_DISABLED",
        )

    # --------------------------------------------------------
    # RAG retrieval
    # --------------------------------------------------------

        # --------------------------------------------------------
    # RAG retrieval
    # --------------------------------------------------------

    effective_top_k = resolve_advisor_top_k(
        request,
        top_k,
    )

    try:
        retrieval_context = retrieve_advisor_knowledge(
            request,
            retriever=retriever,
            top_k=effective_top_k,
        )
    except Exception:
        return AdvisorResult(
            question=request.question,
            question_type=request.question_type,
            answer=(
                "EcoShield could not retrieve grounded knowledge "
                "for this question."
            ),
            status=AdvisorGenerationStatus.UNAVAILABLE,
            assessment_context_used=(
                request.assessment_context_used
            ),
            rag_enabled=request.use_rag,
            ai_enabled=request.use_ai,
            rag_attempted=True,
            ai_attempted=False,
            rag_succeeded=False,
            ai_succeeded=False,
            used_fallback=False,
            retrieval=None,
            llm_response=None,
            warnings=(
                "Knowledge retrieval was unavailable.",
            ),
            errors=(
                "RAG_RETRIEVAL_FAILED",
            ),
        )

         # --------------------------------------------------------
    # RAG-only mode
    # --------------------------------------------------------

    if not request.use_ai:
        return build_retrieval_only_advisor_result(
            request,
            retrieval_context,
        )

    # --------------------------------------------------------
    # Evidence-bounded procedural security guidance
    # --------------------------------------------------------

    if requires_evidence_bounded_security_response(
        request
    ):
        return build_evidence_bounded_security_result(
            request,
            retrieval_context,
        )

    # --------------------------------------------------------
    # AI generation
    # --------------------------------------------------------

    try:
        active_llm_client = (
            llm_client
            if llm_client is not None
            else build_advisor_llm_client(
                runtime_config
            )
        )

        if active_llm_client is None:
            raise RuntimeError(
                "AI mode did not produce an LLM client."
            )

        llm_response = generate_advisor_answer(
            request,
            retrieval_context,
            llm_client=active_llm_client,
        )

    except Exception:
        return AdvisorResult(
            question=request.question,
            question_type=request.question_type,
            answer=(
                "EcoShield retrieved relevant grounded knowledge, "
                "but AI answer generation was unavailable."
            ),
            status=AdvisorGenerationStatus.FALLBACK,
            assessment_context_used=(
                request.assessment_context_used
            ),
            rag_enabled=True,
            ai_enabled=True,
            rag_attempted=True,
            ai_attempted=True,
            rag_succeeded=True,
            ai_succeeded=False,
            used_fallback=True,
            retrieval=retrieval_context,
            llm_response=None,
            warnings=(
                "Grounded EcoShield knowledge remains available "
                "even though AI generation could not complete.",
            ),
            errors=(
                "AI_GENERATION_FAILED",
            ),
        )

    semantic_violations = (
        validate_advisor_semantic_output(
            request,
            llm_response,
        )
    )

    if semantic_violations:
        return build_semantic_rejection_advisor_result(
            request,
            retrieval_context,
            llm_response,
            semantic_violations,
        )

    return build_ai_advisor_result(
        request,
        retrieval_context,
        llm_response,
    )