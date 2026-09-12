"""
EcoShield AI
Recommendation RAG + LLM Enrichment Layer

This hybrid module connects deterministic EcoShield recommendations
with the frozen RAG retrieval and LLM pipelines.

Responsibilities:
- Accept a deterministic RecommendationResult
- Build retrieval context from the assessment and recommendations
- Retrieve relevant cybersecurity and sustainability evidence
- Build grounded LLM explanation requests
- Attach validated AI explanations when available
- Provide safe deterministic fallback when AI is unavailable
- Preserve all authoritative deterministic decisions

This module does NOT:
- calculate cybersecurity risk
- replace deterministic recommendation rules
- modify risk score, risk level, or readiness
- modify deterministic security or sustainability actions
- allow the LLM to become the decision-making authority

Architecture rule:
Deterministic EcoShield results remain authoritative.
RAG provides evidence.
The LLM only explains and contextualizes those results.
"""

from __future__ import annotations

from dataclasses import dataclass, replace
from typing import Any, Mapping

from src.recommendation import (
    RecommendationResult,
    generate_recommendation,
)

from src.rag.retriever import (
    DEFAULT_FINAL_TOP_K,
    EcoShieldRetriever,
    RetrievalContext,
    build_retriever,
    retrieve,
)

from src.ai.llm_client import (
    LLMClient,
    LLMGenerationStatus,
    LLMResponse,
    LLMResponseMode,
    build_llm_request_from_retrieval,
    generate_llm_response,
)

# ============================================================
# RAG ENRICHMENT RESULT
# ============================================================

@dataclass(frozen=True)
class RecommendationEnrichmentResult:
    """
    Complete output of recommendation enrichment.

    Attributes
    ----------
    recommendation:
        RecommendationResult containing deterministic guidance,
        retrieved source context, and optional AI explanation.

    retrieval:
        Complete structured RetrievalContext returned by the
        EcoShield retriever.

    retrieval_query:
        Natural-language retrieval query created from the
        deterministic recommendation context.

    llm_response:
        Structured LLMResponse when AI generation was attempted.

        None means RAG-only enrichment was performed.
    """

    recommendation: RecommendationResult

    retrieval: RetrievalContext

    retrieval_query: str

    llm_response: LLMResponse | None = None

# ============================================================
# RETRIEVAL QUERY BUILDER
# ============================================================

def build_recommendation_retrieval_query(
    recommendation: RecommendationResult,
) -> str:
    """
    Build a deterministic natural-language retrieval query.

    The query describes the device context, intended action,
    risk/readiness state, and generated recommendation topics.

    No LLM is used to construct this query.
    """

    if not isinstance(
        recommendation,
        RecommendationResult,
    ):
        raise TypeError(
            "recommendation must be a RecommendationResult."
        )

    assessment = recommendation.assessment

    if assessment is None:
        raise ValueError(
            "RecommendationResult must contain its "
            "RiskAssessment before RAG enrichment."
        )

    data = assessment.validated_data

    parts: list[str] = [
        "Secure and sustainable electronic device handling guidance"
    ]

    # --------------------------------------------------------
    # Device context
    # --------------------------------------------------------

    device_type = data.get(
        "device_type"
    )

    if device_type:
        parts.append(
            f"device type {device_type}"
        )

    operating_system = data.get(
        "operating_system"
    )

    if operating_system:
        parts.append(
            f"platform {operating_system}"
        )

    storage_type = data.get(
        "storage_type"
    )

    if storage_type:
        parts.append(
            f"storage type {storage_type}"
        )

    disposal_method = data.get(
        "intended_disposal_method"
    )

    if disposal_method:
        parts.append(
            f"intended action {disposal_method}"
        )

    # --------------------------------------------------------
    # Deterministic security context
    # --------------------------------------------------------

    parts.append(
        f"security risk {recommendation.risk_level}"
    )

    parts.append(
        f"disposal readiness {recommendation.readiness}"
    )

    if assessment.requires_sanitization:
        parts.append(
            "secure data sanitization"
        )

    if assessment.device_leaves_owner:
        parts.append(
            "secure device transfer"
        )

    # --------------------------------------------------------
    # Recommendation topics
    # --------------------------------------------------------

    action_titles = [
        item.title
        for item in (
            recommendation.security_actions
            + recommendation.sustainability_actions
        )
    ]

    if action_titles:
        parts.append(
            "recommended topics "
            + ", ".join(
                action_titles
            )
        )

    # --------------------------------------------------------
    # Uncertainty context
    # --------------------------------------------------------

    if assessment.uncertainties:
        parts.append(
            "assessment uncertainty "
            + ", ".join(
                assessment.uncertainties
            )
        )

    return ". ".join(
        parts
    )


# ============================================================
# RETRIEVED CONTEXT FORMATTER
# ============================================================

def _build_retrieved_context(
    retrieval: RetrievalContext,
) -> tuple[str, ...]:
    """
    Build lightweight, user/application-friendly source context.

    Full evidence remains available in RetrievalContext.
    RecommendationResult stores only concise source references.
    """

    context: list[str] = []

    for evidence in retrieval.evidence:

        source_reference = (
            f"{evidence.title} "
            f"({evidence.source_name})"
        )

        if source_reference not in context:
            context.append(
                source_reference
            )

    return tuple(
        context
    )

# ============================================================
# LLM CONTEXT BUILDERS
# ============================================================

def _build_risk_context(
    recommendation: RecommendationResult,
) -> dict[str, Any]:
    """
    Convert authoritative deterministic risk data into a
    provider-independent mapping for the LLM layer.

    No risk is calculated here.
    """

    assessment = recommendation.assessment

    if assessment is None:
        raise ValueError(
            "RecommendationResult must contain its "
            "RiskAssessment before AI enrichment."
        )

    return {
        "risk_score": assessment.score,
        "risk_level": assessment.risk_level,
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

def _build_recommendation_context(
    recommendation: RecommendationResult,
) -> dict[str, Any]:
    """
    Convert deterministic recommendation output into a compact
    mapping for grounded LLM explanation.
    """

    security_actions = [
        {
            "code": item.code,
            "priority": item.priority,
            "category": item.category,
            "title": item.title,
            "action": item.action,
            "rationale": item.rationale,
        }
        for item in recommendation.security_actions
    ]

    sustainability_actions = [
        {
            "code": item.code,
            "priority": item.priority,
            "category": item.category,
            "title": item.title,
            "action": item.action,
            "rationale": item.rationale,
        }
        for item in recommendation.sustainability_actions
    ]

    return {
        "readiness": recommendation.readiness,
        "summary": recommendation.summary,
        "security_actions": security_actions,
        "sustainability_actions": sustainability_actions,
        "next_steps": tuple(
            recommendation.next_steps
        ),
        "warnings": tuple(
            recommendation.warnings
        ),
    }

def _build_responsible_ai_context(
    recommendation: RecommendationResult,
) -> dict[str, Any]:
    """
    Build recommendation-level Responsible-AI constraints.

    These constraints tell the explanation layer exactly which
    device-specific actions are authoritative.

    Retrieved evidence may explain these actions or provide
    clearly labelled general guidance, but must not create new
    mandatory device-specific actions.
    """

    security_codes = tuple(
        item.code
        for item in recommendation.security_actions
    )

    security_titles = tuple(
        item.title
        for item in recommendation.security_actions
    )

    sustainability_codes = tuple(
        item.code
        for item in recommendation.sustainability_actions
    )

    sustainability_titles = tuple(
        item.title
        for item in recommendation.sustainability_actions
    )

    return {
        "ai_role": (
            "Explain the authoritative deterministic EcoShield "
            "result. Do not replace it with a new recommendation."
        ),
        "authoritative_security_action_codes": (
            security_codes
        ),
        "authoritative_security_action_titles": (
            security_titles
        ),
        "authoritative_sustainability_action_codes": (
            sustainability_codes
        ),
        "authoritative_sustainability_action_titles": (
            sustainability_titles
        ),
        "action_scope_rule": (
            "Present only the deterministic actions above as "
            "device-specific required or recommended actions. "
            "Retrieved evidence may be used to explain why those "
            "actions matter. Other information from retrieved "
            "evidence must be labelled as general guidance and "
            "must not be presented as a required action for this "
            "specific device."
        ),
        "uncertainty_rule": (
            "If an assessment field was not supplied or is "
            "uncertain, do not assume its state."
        ),
        "authority_rule": (
            "Risk score, risk level, readiness, security actions, "
            "sustainability actions, and next steps are determined "
            "only by EcoShield deterministic logic."
        ),
    }

# ============================================================
# RESPONSIBLE-AI ACTION-SCOPE GUARD
# ============================================================

SECURITY_ACTION_LANGUAGE: dict[
    str,
    tuple[str, ...],
] = {
    "COMPLETE_BACKUP": (
        "complete a backup",
        "back up your data",
        "backup your data",
    ),
    "VERIFY_BACKUP": (
        "verify your backup",
        "verify the backup",
    ),
    "SIGN_OUT_ACCOUNTS": (
        "sign out of accounts",
        "sign out of all accounts",
        "remove all accounts",
    ),
    "VERIFY_ACCOUNT_SIGNOUT": (
        "verify account sign-out",
        "verify that accounts are signed out",
    ),
    "REMOVE_REMOVABLE_MEDIA": (
        "remove removable media",
        "remove the sim card",
        "remove memory card",
        "remove the memory card",
    ),
    "VERIFY_REMOVABLE_MEDIA": (
        "verify removable media",
        "check for removable media",
    ),
    "PERFORM_SECURE_SANITIZATION": (
        "perform secure sanitization",
        "perform secure data sanitization",
        "securely erase the device",
        "securely erase the drive",
        "secure erase the drive",
    ),
    "VERIFY_SECURE_SANITIZATION": (
        "verify secure sanitization",
        "verify secure erase",
    ),
    "COMPLETE_FACTORY_RESET": (
        "complete a factory reset",
        "perform a factory reset",
        "factory reset the device",
    ),
    "VERIFY_FACTORY_RESET": (
        "verify the factory reset",
        "verify factory reset",
    ),
}

def _find_unsupported_security_action(
    text: str,
    recommendation: RecommendationResult,
) -> str | None:
    """
    Detect a conservative set of security actions that the LLM
    presents even though EcoShield's deterministic recommendation
    did not authorize that action.

    This is intentionally narrow. It protects high-impact security
    preparation actions without trying to understand arbitrary
    natural language.
    """

    normalized_text = (
        " ".join(
            str(text)
            .lower()
            .split()
        )
    )

    allowed_codes = {
        item.code
        for item in recommendation.security_actions
    }

    for code, phrases in (
        SECURITY_ACTION_LANGUAGE.items()
    ):

        if code in allowed_codes:
            continue

        for phrase in phrases:

            if phrase in normalized_text:
                return code

    return None

def _build_recommendation_safe_fallback(
    recommendation: RecommendationResult,
    *,
    reason: str,
) -> str:
    """
    Build concise deterministic fallback guidance.

    The text contains only authoritative EcoShield results and
    never creates new recommendations.
    """

    lines: list[str] = [
        (
            "EcoShield AI could not safely provide an "
            "AI-generated explanation. The guidance below "
            "comes from EcoShield's deterministic assessment."
        ),
        "",
        (
            f"Risk: {recommendation.risk_level} "
            f"({recommendation.risk_score}/100)"
        ),
        (
            f"Readiness: {recommendation.readiness}"
        ),
        "",
        recommendation.summary,
    ]

    if recommendation.next_steps:

        lines.extend(
            [
                "",
                "Recommended next steps:",
            ]
        )

        for step in recommendation.next_steps:
            lines.append(
                f"- {step}"
            )

    if recommendation.retrieved_context:

        lines.extend(
            [
                "",
                "Retrieved guidance sources:",
            ]
        )

        for source in (
            recommendation.retrieved_context
        ):
            lines.append(
                f"- {source}"
            )

    lines.extend(
        [
            "",
            (
                "AI fallback reason: "
                f"{reason}"
            ),
        ]
    )

    return "\n".join(
        lines
    )
# ============================================================
# RAG ENRICHMENT
# ============================================================

def enrich_recommendation_with_rag(
    recommendation_or_payload:
        RecommendationResult | Mapping[str, Any],
    *,
    retriever: EcoShieldRetriever | None = None,
    top_k: int = DEFAULT_FINAL_TOP_K,
) -> RecommendationEnrichmentResult:
    """
    Retrieve RAG evidence for an EcoShield recommendation.

    Parameters
    ----------
    recommendation_or_payload:
        Existing deterministic RecommendationResult or an
        EcoShield assessment mapping.

    retriever:
        Optional reusable EcoShieldRetriever.

        Application code should normally build this once and
        reuse it rather than rebuilding the vector store for
        every request.

    top_k:
        Maximum number of final evidence sources.

    Returns
    -------
    RecommendationEnrichmentResult
        Deterministic recommendation plus structured retrieval
        context.

    Important
    ---------
    This function does not invoke an LLM and does not change
    deterministic risk or recommendation decisions.
    """

    # --------------------------------------------------------
    # Resolve deterministic recommendation
    # --------------------------------------------------------

    if isinstance(
        recommendation_or_payload,
        RecommendationResult,
    ):

        recommendation = (
            recommendation_or_payload
        )

    elif isinstance(
        recommendation_or_payload,
        Mapping,
    ):

        recommendation = (
            generate_recommendation(
                recommendation_or_payload
            )
        )

    else:

        raise TypeError(
            "RAG enrichment input must be either a "
            "RecommendationResult or a dictionary-like "
            "device-assessment mapping."
        )

    # --------------------------------------------------------
    # Require authoritative assessment context
    # --------------------------------------------------------

    assessment = recommendation.assessment

    if assessment is None:

        raise ValueError(
            "RecommendationResult must contain its "
            "RiskAssessment before RAG enrichment."
        )

    # --------------------------------------------------------
    # Build deterministic retrieval query
    # --------------------------------------------------------

    retrieval_query = (
        build_recommendation_retrieval_query(
            recommendation
        )
    )

    # --------------------------------------------------------
    # Resolve reusable retriever
    # --------------------------------------------------------

    active_retriever = (
        retriever
        if retriever is not None
        else build_retriever()
    )

    if not isinstance(
        active_retriever,
        EcoShieldRetriever,
    ):

        raise TypeError(
            "retriever must be an EcoShieldRetriever."
        )

    # --------------------------------------------------------
    # Retrieve evidence
    # --------------------------------------------------------

    retrieval = retrieve(
        active_retriever,
        retrieval_query,
        assessment=(
            assessment.validated_data
        ),
        top_k=top_k,
    )

    # --------------------------------------------------------
    # Attach concise retrieval metadata
    # --------------------------------------------------------

    retrieved_context = (
        _build_retrieved_context(
            retrieval
        )
    )

    enriched_recommendation = replace(
        recommendation,
        retrieved_context=(
            retrieved_context
        ),
        used_ai=False,
        used_fallback=False,
    )

    # --------------------------------------------------------
    # Deterministic integrity checks
    # --------------------------------------------------------

    if (
        enriched_recommendation.risk_score
        != recommendation.risk_score
    ):
        raise RuntimeError(
            "RAG enrichment changed the deterministic "
            "risk score."
        )

    if (
        enriched_recommendation.risk_level
        != recommendation.risk_level
    ):
        raise RuntimeError(
            "RAG enrichment changed the deterministic "
            "risk level."
        )

    if (
        enriched_recommendation.readiness
        != recommendation.readiness
    ):
        raise RuntimeError(
            "RAG enrichment changed deterministic readiness."
        )

    if (
        enriched_recommendation.security_actions
        != recommendation.security_actions
    ):
        raise RuntimeError(
            "RAG enrichment changed deterministic "
            "security recommendations."
        )

    if (
        enriched_recommendation.sustainability_actions
        != recommendation.sustainability_actions
    ):
        raise RuntimeError(
            "RAG enrichment changed deterministic "
            "sustainability recommendations."
        )

    return RecommendationEnrichmentResult(
        recommendation=(
            enriched_recommendation
        ),
        retrieval=retrieval,
        retrieval_query=(
            retrieval_query
        ),
    )

# ============================================================
# RAG + LLM RECOMMENDATION ENRICHMENT
# ============================================================

def enrich_recommendation_with_ai(
    recommendation_or_payload:
        RecommendationResult | Mapping[str, Any],
    *,
    llm_client: LLMClient,
    retriever: EcoShieldRetriever | None = None,
    top_k: int = DEFAULT_FINAL_TOP_K,
    user_query: str | None = None,
) -> RecommendationEnrichmentResult:
    """
    Enrich an EcoShield deterministic recommendation using
    retrieved RAG evidence and the configured LLM.

    The deterministic recommendation remains authoritative.

    The LLM may explain and contextualize the recommendation,
    but it cannot change:
    - risk score
    - risk level
    - readiness
    - security actions
    - sustainability actions
    - next steps
    """

    if not isinstance(
        llm_client,
        LLMClient,
    ):
        raise TypeError(
            "llm_client must be an LLMClient."
        )

    # --------------------------------------------------------
    # Complete deterministic + RAG enrichment first
    # --------------------------------------------------------

    rag_result = (
        enrich_recommendation_with_rag(
            recommendation_or_payload,
            retriever=retriever,
            top_k=top_k,
        )
    )

    recommendation = (
        rag_result.recommendation
    )

    assessment = recommendation.assessment

    if assessment is None:
        raise ValueError(
            "RecommendationResult must contain its "
            "RiskAssessment before AI enrichment."
        )

    # --------------------------------------------------------
    # Resolve AI question
    # --------------------------------------------------------

    normalized_query = (
        str(
            user_query
            if user_query is not None
            else (
                "Explain the existing EcoShield assessment and deterministic "
                "recommendations in clear, user-friendly language. "
                "Only explain actions and next steps that are explicitly present "
                "in the deterministic EcoShield recommendation. "
                "Do not add, suggest, recommend, require, or imply any new "
                "device-specific security action. "
                "In particular, do not suggest factory reset, secure erase, "
                "account sign-out, backup, encryption changes, removable-media "
                "removal, or any other preparation action unless that exact action "
                "is already present in the deterministic recommendation. "
                "General background information may be explained, but it must not "
                "be presented as an additional action the user should perform. "
                "The deterministic recommendation is authoritative."
            )
        )
        .strip()
    )

    if not normalized_query:
        raise ValueError(
            "user_query cannot be empty."
        )

    # --------------------------------------------------------
    # Build deterministic context
    # --------------------------------------------------------

    risk_context = (
        _build_risk_context(
            recommendation
        )
    )

    recommendation_context = (
        _build_recommendation_context(
            recommendation
        )
    )

    responsible_ai_context = (
        _build_responsible_ai_context(
            recommendation
        )
    )

    # --------------------------------------------------------
    # Build grounded request from RAG evidence
    # --------------------------------------------------------

    llm_request = (
        build_llm_request_from_retrieval(
            user_query=normalized_query,
            retrieval_context=(
                rag_result.retrieval
            ),
            mode=(
                LLMResponseMode.EXPLANATION
            ),
            assessment=(
                assessment.validated_data
            ),
            risk_context=risk_context,
            recommendation_context=(
                recommendation_context
            ),
            additional_context=(
                responsible_ai_context
            ),
        )
    )

    # --------------------------------------------------------
    # Execute frozen LLM pipeline
    # --------------------------------------------------------

    llm_response = (
        generate_llm_response(
            llm_client,
            llm_request,
        )
    )

    # --------------------------------------------------------
    # Determine whether validated AI was actually accepted
    # --------------------------------------------------------

    used_ai = (
        llm_response.status
        == LLMGenerationStatus.SUCCESS
        and not llm_response.used_fallback
    )

    used_fallback = (
        llm_response.used_fallback
    )

    ai_explanation: str | None = None

    if used_ai:

        unsupported_action = (
            _find_unsupported_security_action(
                llm_response.text,
                recommendation,
            )
        )

        if unsupported_action is None:

            ai_explanation = (
                llm_response.text
            )

        else:

            used_ai = False
            used_fallback = True

            fallback_reason = (
                "The AI explanation introduced a "
                "device-specific security action that was "
                "not present in the deterministic EcoShield "
                "recommendation: "
                f"{unsupported_action}."
            )

            ai_explanation = (
                _build_recommendation_safe_fallback(
                    recommendation,
                    reason=fallback_reason,
                )
            )

    elif llm_response.used_fallback:

        ai_explanation = (
            _build_recommendation_safe_fallback(
                recommendation,
                reason=(
                    llm_response.error_message
                    or "AI generation was unavailable."
                ),
            )
        )

    # --------------------------------------------------------
    # Attach explanation only — never deterministic decisions
    # --------------------------------------------------------

    enriched_recommendation = replace(
        recommendation,
        ai_explanation=(
            ai_explanation
        ),
        used_ai=used_ai,
        used_fallback=used_fallback,
    )

    # --------------------------------------------------------
    # Authoritative-value integrity checks
    # --------------------------------------------------------

    if (
        enriched_recommendation.risk_score
        != recommendation.risk_score
    ):
        raise RuntimeError(
            "AI enrichment changed the deterministic "
            "risk score."
        )

    if (
        enriched_recommendation.risk_level
        != recommendation.risk_level
    ):
        raise RuntimeError(
            "AI enrichment changed the deterministic "
            "risk level."
        )

    if (
        enriched_recommendation.readiness
        != recommendation.readiness
    ):
        raise RuntimeError(
            "AI enrichment changed deterministic readiness."
        )

    if (
        enriched_recommendation.security_actions
        != recommendation.security_actions
    ):
        raise RuntimeError(
            "AI enrichment changed deterministic "
            "security recommendations."
        )

    if (
        enriched_recommendation.sustainability_actions
        != recommendation.sustainability_actions
    ):
        raise RuntimeError(
            "AI enrichment changed deterministic "
            "sustainability recommendations."
        )

    if (
        enriched_recommendation.next_steps
        != recommendation.next_steps
    ):
        raise RuntimeError(
            "AI enrichment changed deterministic next steps."
        )

    if (
        enriched_recommendation.assessment
        is not recommendation.assessment
    ):
        raise RuntimeError(
            "AI enrichment replaced the authoritative "
            "RiskAssessment."
        )

    return RecommendationEnrichmentResult(
        recommendation=(
            enriched_recommendation
        ),
        retrieval=(
            rag_result.retrieval
        ),
        retrieval_query=(
            rag_result.retrieval_query
        ),
        llm_response=(
            llm_response
        ),
    )
# ============================================================
# CONVENIENCE FUNCTION: EVIDENCE ONLY
# ============================================================

def get_recommendation_evidence(
    recommendation_or_payload:
        RecommendationResult | Mapping[str, Any],
    *,
    retriever: EcoShieldRetriever | None = None,
    top_k: int = DEFAULT_FINAL_TOP_K,
):
    """
    Return only structured retrieved evidence.

    Useful for testing and later LLM integration.
    """

    result = enrich_recommendation_with_rag(
        recommendation_or_payload,
        retriever=retriever,
        top_k=top_k,
    )

    return result.retrieval.evidence