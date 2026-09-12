"""
EcoShield AI
Assessment Service

Backend orchestration layer for the EcoShield AI device-assessment
workflow.

Architecture
------------
Assessment Payload
    -> Validation
    -> Risk Assessment
    -> Deterministic Recommendation
    -> Optional RAG Enrichment
    -> Optional LLM Explanation
    -> Unified Backend Result

Responsibilities
----------------
This service coordinates the existing EcoShield AI backend layers.

It must NOT:
- duplicate validation rules
- calculate risk independently
- duplicate recommendation rules
- implement retrieval algorithms
- implement LLM prompting or provider logic
- allow AI output to override deterministic assessment results

Deterministic authority remains with:
- src.validators
- src.risk_engine
- src.recommendation

Optional enrichment remains with:
- src.rag
- src.ai

Service Modes
-------------
1. Deterministic only
2. Deterministic + RAG
3. Deterministic + RAG + AI

AI enrichment must remain grounded in retrieved evidence.
Requesting AI therefore implies that RAG is required.

Failure Principle
-----------------
Validation failures stop the assessment pipeline.

Failures in optional RAG or AI enrichment must not destroy valid
deterministic risk and recommendation results.

The service should return deterministic guidance whenever optional
enrichment cannot safely be completed.
"""

from __future__ import annotations
from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from src.recommendation import (
    RecommendationResult,
    generate_recommendation,
)
from src.risk_engine import (
    RiskAssessment,
    assess_device_risk,
)
from src.sustainability_engine import (
    SustainabilityImpactResult,
    assess_sustainability,
)
from src.ai.llm_client import LLMClient
from src.ai.recommendation_enricher import (
    enrich_recommendation_with_ai,
    enrich_recommendation_with_rag,
)
from src.rag.retriever import EcoShieldRetriever
# ============================================================
# SERVICE DATA CONTRACTS
# ============================================================


@dataclass(frozen=True)
class AssessmentServiceConfig:
    """
    Controls optional backend enrichment.

    Deterministic assessment is always enabled.

    AI requires RAG grounding. Therefore, enabling AI makes
    RAG effectively enabled even when use_rag is False.
    """

    use_rag: bool = False
    use_ai: bool = False

    def __post_init__(self) -> None:
        """
        Validate configuration values.
        """

        if not isinstance(self.use_rag, bool):
            raise TypeError(
                "use_rag must be a boolean."
            )

        if not isinstance(self.use_ai, bool):
            raise TypeError(
                "use_ai must be a boolean."
            )

    @property
    def effective_use_rag(self) -> bool:
        """
        Return whether RAG is effectively required.
        """

        return self.use_rag or self.use_ai

    @property
    def effective_use_ai(self) -> bool:
        """
        Return whether AI enrichment is enabled.
        """

        return self.use_ai


@dataclass(frozen=True)
class AssessmentServiceResult:
    """
    Unified result returned by the EcoShield AI assessment service.

    The deterministic RiskAssessment and RecommendationResult remain
    authoritative. RAG and AI only enrich those results.
    """

    risk: RiskAssessment
    recommendation: RecommendationResult
    sustainability: SustainabilityImpactResult | None = None
    rag_enabled: bool = False
    ai_enabled: bool = False

    rag_attempted: bool = False
    ai_attempted: bool = False

    rag_succeeded: bool = False
    ai_succeeded: bool = False

    used_fallback: bool = False

    user_query: str | None = None

    retrieved_context: tuple[str, ...] = field(
        default_factory=tuple
    )

    ai_explanation: str | None = None

    warnings: tuple[str, ...] = field(
        default_factory=tuple
    )

    errors: tuple[str, ...] = field(
        default_factory=tuple
    )

    def to_dict(self) -> dict[str, Any]:
        """
        Return a serializable dictionary representation.
        """

        return asdict(self)


# ============================================================
# DETERMINISTIC AUTHORITY GUARD
# ============================================================


class DeterministicAuthorityError(RuntimeError):
    """
    Raised when an enrichment layer attempts to alter an
    authoritative deterministic assessment value.
    """


def _verify_deterministic_authority(
    risk: RiskAssessment,
    original: RecommendationResult,
    enriched: RecommendationResult,
) -> None:
    """
    Ensure RAG or AI enrichment has not modified authoritative
    deterministic assessment or recommendation values.

    Enrichment may add evidence, explanation, and fallback metadata,
    but it must not change the underlying deterministic decision.
    """

    violations: list[str] = []

    if enriched.risk_score != original.risk_score:
        violations.append("risk_score")

    if enriched.risk_level != original.risk_level:
        violations.append("risk_level")

    if enriched.readiness != original.readiness:
        violations.append("readiness")

    if enriched.summary != original.summary:
        violations.append("summary")

    if enriched.security_actions != original.security_actions:
        violations.append("security_actions")

    if (
        enriched.sustainability_actions
        != original.sustainability_actions
    ):
        violations.append("sustainability_actions")

    if enriched.next_steps != original.next_steps:
        violations.append("next_steps")

    if enriched.assessment is not risk:
        violations.append("assessment_identity")

    if enriched.risk_score != risk.score:
        violations.append("risk_score_vs_assessment")

    if enriched.risk_level != risk.risk_level:
        violations.append("risk_level_vs_assessment")

    if violations:
        fields = ", ".join(violations)

        raise DeterministicAuthorityError(
            "Enrichment attempted to alter authoritative "
            f"deterministic fields: {fields}."
        )

# ============================================================
# SERVICE ERROR CODES
# ============================================================


RAG_ENRICHMENT_FAILED = "RAG_ENRICHMENT_FAILED"
AI_ENRICHMENT_FAILED = "AI_ENRICHMENT_FAILED"

# ============================================================
# REQUEST NORMALIZATION
# ============================================================


def _normalize_assessment_payload(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Convert an assessment request into the canonical dictionary
    shape expected by the deterministic backend.

    This function performs structural normalization only.

    It deliberately does NOT:
    - validate assessment values
    - invent missing fields
    - convert invalid values into valid ones
    - calculate risk
    - apply recommendation rules

    Those responsibilities remain with the existing authoritative
    backend layers.
    """

    if not isinstance(payload, Mapping):
        raise TypeError(
            "Assessment payload must be a mapping."
        )

    normalized: dict[str, Any] = {}

    for raw_key, value in payload.items():
        if not isinstance(raw_key, str):
            raise TypeError(
                "Assessment payload keys must be strings."
            )

        key = raw_key.strip()

        if not key:
            raise ValueError(
                "Assessment payload keys cannot be empty."
            )

        if key in normalized:
            raise ValueError(
                "Assessment payload contains duplicate "
                f"normalized key: {key}."
            )

        normalized[key] = value

    return normalized

def _normalize_user_query(
    user_query: str | None,
) -> str | None:
    """
    Normalize optional free-text user context.

    Empty or whitespace-only text becomes None.
    """

    if user_query is None:
        return None

    if not isinstance(user_query, str):
        raise TypeError(
            "user_query must be a string or None."
        )

    normalized = user_query.strip()

    return normalized or None

def _normalize_service_config(
    config: AssessmentServiceConfig | None,
) -> AssessmentServiceConfig:
    """
    Normalize optional orchestration configuration.

    None means deterministic-only mode.
    """

    if config is None:
        return AssessmentServiceConfig()

    if not isinstance(
        config,
        AssessmentServiceConfig,
    ):
        raise TypeError(
            "config must be an AssessmentServiceConfig "
            "instance or None."
        )

    return config

def _resolve_service_mode(
    config: AssessmentServiceConfig,
) -> str:
    """
    Resolve the effective backend orchestration mode.
    """

    if config.effective_use_ai:
        return "ai"

    if config.effective_use_rag:
        return "rag"

    return "deterministic"

def _validate_service_dependencies(
    *,
    mode: str,
    retriever: EcoShieldRetriever | None,
    llm_client: LLMClient | None,
) -> None:
    """
    Validate optional service dependencies for the resolved mode.

    Deterministic mode requires no optional dependencies.

    RAG mode may use an injected retriever or allow the enrichment
    layer to construct/use its default retriever.

    AI mode requires an explicit LLM client.
    """

    if mode not in {
        "deterministic",
        "rag",
        "ai",
    }:
        raise ValueError(
            f"Unsupported assessment service mode: {mode}."
        )

    if (
        retriever is not None
        and not isinstance(
            retriever,
            EcoShieldRetriever,
        )
    ):
        raise TypeError(
            "retriever must be an EcoShieldRetriever "
            "instance or None."
        )

    if mode == "ai":
        if llm_client is None:
            raise ValueError(
                "llm_client is required when AI "
                "enrichment is enabled."
            )

        if not isinstance(
            llm_client,
            LLMClient,
        ):
            raise TypeError(
                "llm_client must be an LLMClient "
                "instance when AI enrichment is enabled."
            )

def _normalize_service_response(
    result: AssessmentServiceResult,
) -> dict[str, Any]:
    """
    Convert an internal AssessmentServiceResult into a stable,
    frontend-friendly response dictionary.

    Internal dataclass objects are not exposed directly.
    """

    if not isinstance(
        result,
        AssessmentServiceResult,
    ):
        raise TypeError(
            "result must be an AssessmentServiceResult instance."
        )

    return {
        "assessment": {
            "risk_score": result.risk.score,
            "risk_level": result.risk.risk_level,
            "readiness": result.recommendation.readiness,
            "summary": result.recommendation.summary,
        },
        "recommendations": {
            "security_actions": [
                asdict(item)
                for item in (
                    result.recommendation.security_actions
                )
            ],
            "sustainability_actions": [
                asdict(item)
                for item in (
                    result.recommendation.sustainability_actions
                )
            ],
            "next_steps": list(
                result.recommendation.next_steps
            ),
        },
        "enrichment": {
            "rag_enabled": result.rag_enabled,
            "ai_enabled": result.ai_enabled,
            "rag_attempted": result.rag_attempted,
            "ai_attempted": result.ai_attempted,
            "rag_succeeded": result.rag_succeeded,
            "ai_succeeded": result.ai_succeeded,
            "used_fallback": result.used_fallback,
            "retrieved_context": list(
                result.retrieved_context
            ),
            "ai_explanation": result.ai_explanation,
        },
        "meta": {
            "user_query": result.user_query,
            "warnings": list(result.warnings),
            "errors": list(result.errors),
        },
    }

def _build_enrichment_fallback_warning(
    layer: str,
) -> str:
    """
    Return a safe user-facing warning when optional enrichment
    cannot be completed.

    Internal exception details are deliberately not exposed here.
    """

    return (
        f"{layer} enrichment could not be completed. "
        "The deterministic assessment remains available "
        "and authoritative."
    )


# ============================================================
# DETERMINISTIC ASSESSMENT PIPELINE
# ============================================================


def _run_deterministic_assessment(
    payload: Mapping[str, Any],
) -> tuple[
    RiskAssessment,
    RecommendationResult,
    SustainabilityImpactResult,
]:
    """
    Run EcoShield's authoritative deterministic assessment pipeline.

    Cybersecurity risk remains owned by risk_engine.py.

    Recommendation readiness and security guidance remain owned by
    recommendation.py.

    Sustainability opportunity remains owned by
    sustainability_engine.py.

    Sustainability consumes the canonical validated assessment data
    produced by the risk assessment so that both deterministic engines
    operate on the same normalized device information.

    No RAG or LLM functionality is used here.
    """

    risk = assess_device_risk(
        payload
    )

    sustainability = assess_sustainability(
        risk.validated_data
    )

    recommendation = generate_recommendation(
        risk
    )

    return (
        risk,
        recommendation,
        sustainability,
    )

def _build_deterministic_service_result(
    payload: Mapping[str, Any],
    *,
    user_query: str | None = None,
) -> AssessmentServiceResult:
    """
    Build the unified service result for deterministic-only mode.

    Optional RAG and AI enrichment are deliberately not executed
    by this function.
    """

    normalized_payload = (
        _normalize_assessment_payload(
            payload
        )
    )

    normalized_query = (
        _normalize_user_query(
            user_query
        )
    )

    risk, recommendation, sustainability = (
        _run_deterministic_assessment(
            normalized_payload
        )
    )
    
    return AssessmentServiceResult(
        risk=risk,
        recommendation=recommendation,
        sustainability=sustainability,
        rag_enabled=False,
        ai_enabled=False,
        rag_attempted=False,
        ai_attempted=False,
        rag_succeeded=False,
        ai_succeeded=False,
        used_fallback=False,
        user_query=normalized_query,
        retrieved_context=(),
        ai_explanation=None,
        warnings=(),
        errors=(),
    )  

# ============================================================
# OPTIONAL RAG ENRICHMENT
# ============================================================


def _build_rag_service_result(
    payload: Mapping[str, Any],
    *,
    user_query: str | None = None,
    retriever: EcoShieldRetriever | None = None,
) -> AssessmentServiceResult:
    """
    Run deterministic assessment and optionally enrich the
    recommendation with retrieved knowledge.

    Deterministic assessment failures are allowed to propagate.

    If optional RAG enrichment fails, the valid deterministic
    assessment is preserved and returned as a safe fallback.
    """

    normalized_payload = (
        _normalize_assessment_payload(
            payload
        )
    )

    normalized_query = (
        _normalize_user_query(
            user_query
        )
    )

    risk, recommendation, sustainability = (
        _run_deterministic_assessment(
            normalized_payload
        )
    )

    try:
        enrichment = enrich_recommendation_with_rag(
            recommendation,
            retriever=retriever,
        )

        enriched_recommendation = (
            enrichment.recommendation
        )

        _verify_deterministic_authority(
            risk,
            recommendation,
            enriched_recommendation,
        )

        retrieved_context = (
            enriched_recommendation.retrieved_context
        )

        return AssessmentServiceResult(
            risk=risk,
            recommendation=enriched_recommendation,
            sustainability=sustainability,
            rag_enabled=True,
            ai_enabled=False,
            rag_attempted=True,
            ai_attempted=False,
            rag_succeeded=bool(
                enrichment.retrieval.evidence
            ),
            ai_succeeded=False,
            used_fallback=False,
            user_query=normalized_query,
            retrieved_context=retrieved_context,
            ai_explanation=None,
            warnings=(
                enriched_recommendation.warnings
            ),
            errors=(),
        )

    except DeterministicAuthorityError:
        raise

    except Exception:
        return AssessmentServiceResult(
            risk=risk,
            recommendation=recommendation,
            sustainability=sustainability,
            rag_enabled=True,
            ai_enabled=False,
            rag_attempted=True,
            ai_attempted=False,
            rag_succeeded=False,
            ai_succeeded=False,
            used_fallback=True,
            user_query=normalized_query,
            retrieved_context=(),
            ai_explanation=None,
                        warnings=(
                _build_enrichment_fallback_warning(
                    "RAG"
                ),
            ),
            errors=(
                RAG_ENRICHMENT_FAILED,
            ),
        )
# ============================================================
# OPTIONAL RAG + AI ENRICHMENT
# ============================================================


def _build_ai_service_result(
    payload: Mapping[str, Any],
    *,
    llm_client: LLMClient,
    user_query: str | None = None,
    retriever: EcoShieldRetriever | None = None,
) -> AssessmentServiceResult:
    """
    Run deterministic assessment and optionally enrich the
    recommendation with grounded RAG + LLM explanation.

    Deterministic assessment failures are allowed to propagate.

    If optional RAG/AI enrichment raises an operational exception,
    the valid deterministic assessment is preserved and returned
    as a safe fallback.

    Responsible-AI fallback returned normally by the frozen
    enrichment layer is preserved as-is.
    """

    normalized_payload = (
        _normalize_assessment_payload(
            payload
        )
    )

    normalized_query = (
        _normalize_user_query(
            user_query
        )
    )

    risk, recommendation, sustainability = (
        _run_deterministic_assessment(
            normalized_payload
        )
    )

    try:
        enrichment = enrich_recommendation_with_ai(
            recommendation,
            llm_client=llm_client,
            retriever=retriever,
            user_query=normalized_query,
        )

        enriched_recommendation = (
            enrichment.recommendation
        )

        _verify_deterministic_authority(
            risk,
            recommendation,
            enriched_recommendation,
        )

        llm_response = enrichment.llm_response

        rag_succeeded = bool(
            enrichment.retrieval.evidence
        )

        ai_succeeded = bool(
            enriched_recommendation.used_ai
            and not enriched_recommendation.used_fallback
        )

        return AssessmentServiceResult(
            risk=risk,
            recommendation=enriched_recommendation,
            sustainability=sustainability,
            rag_enabled=True,
            ai_enabled=True,
            rag_attempted=True,
            ai_attempted=True,
            rag_succeeded=rag_succeeded,
            ai_succeeded=ai_succeeded,
            used_fallback=(
                enriched_recommendation.used_fallback
            ),
            user_query=normalized_query,
            retrieved_context=(
                enriched_recommendation.retrieved_context
            ),
            ai_explanation=(
                enriched_recommendation.ai_explanation
            ),
            warnings=(
                enriched_recommendation.warnings
            ),
            errors=(
                (llm_response.error_message,)
                if (
                    llm_response is not None
                    and llm_response.error_message
                )
                else ()
            ),
        )

    except DeterministicAuthorityError:
        raise

    except Exception:
        return AssessmentServiceResult(
            risk=risk,
            recommendation=recommendation,
            sustainability=sustainability,
            rag_enabled=True,
            ai_enabled=True,
            rag_attempted=True,
            ai_attempted=True,
            rag_succeeded=False,
            ai_succeeded=False,
            used_fallback=True,
            user_query=normalized_query,
            retrieved_context=(),
            ai_explanation=None,
                        warnings=(
                _build_enrichment_fallback_warning(
                    "AI/RAG"
                ),
            ),
            errors=(
                AI_ENRICHMENT_FAILED,
            ),
        )

    # ============================================================
# PUBLIC ASSESSMENT SERVICE
# ============================================================


def assess_device(
    payload: Mapping[str, Any],
    *,
    config: AssessmentServiceConfig | None = None,
    user_query: str | None = None,
    retriever: EcoShieldRetriever | None = None,
    llm_client: LLMClient | None = None,
) -> AssessmentServiceResult:
    """
    Run the EcoShield AI device-assessment workflow.

    This is the primary backend service entry point.

    Supported modes:
    - deterministic only
    - deterministic + RAG
    - deterministic + RAG + AI

    AI requires RAG grounding.

    Validation, risk calculation, recommendation logic,
    retrieval, and LLM generation remain delegated to their
    authoritative backend modules.
    """

    normalized_config = (
        _normalize_service_config(
            config
        )
    )

    mode = _resolve_service_mode(
        normalized_config
    )

    _validate_service_dependencies(
        mode=mode,
        retriever=retriever,
        llm_client=llm_client,
    )

    if mode == "ai":
        return _build_ai_service_result(
            payload,
            llm_client=llm_client,
            user_query=user_query,
            retriever=retriever,
        )

    if mode == "rag":
        return _build_rag_service_result(
            payload,
            user_query=user_query,
            retriever=retriever,
        )

    return _build_deterministic_service_result(
        payload,
        user_query=user_query,
    )
