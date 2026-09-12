"""
EcoShield AI
Frontend / Backend Integration Adapter

This module is the permanent integration boundary between
the Streamlit frontend and EcoShield's backend assessment
service.

Responsibilities
----------------
- Load validated runtime configuration
- Convert runtime configuration into assessment-service config
- Build optional RAG and LLM runtime dependencies
- Call the frozen assessment service exactly once per submission
- Synchronize successful backend results with application state
- Return a small frontend-safe submission result
- Expose the active assessment mode for presentation

This module must NOT:
- implement validation rules
- calculate cybersecurity risk
- generate deterministic recommendations
- implement retrieval algorithms
- implement LLM prompting
- perform navigation
- render Streamlit UI
- expose secrets or provider credentials

Deterministic authority remains with the frozen backend layers.
"""

from __future__ import annotations

from collections.abc import Mapping
from dataclasses import dataclass
from typing import Any
from unittest import result

from config.config import (
    RuntimeConfig,
    load_runtime_config,
)

from src.ai.llm_client import (
    LLMClient,
    LLMConfig,
    LLMProvider,
    build_llm_client,
)

from src.rag.retriever import (
    EcoShieldRetriever,
    build_retriever,
)

from src.services.assessment_service import (
    AssessmentServiceConfig,
    AssessmentServiceResult,
    assess_device,
)

from ui.state import (
    clear_assessment_results,
    mark_assessment_completed,
    set_assessment_enrichment_state,
    set_assessment_service_result,
    set_recommendation_result,
    set_risk_assessment,
    set_sustainability_result,
)


# ============================================================
# FRONTEND RESULT CONTRACT
# ============================================================


@dataclass(frozen=True)
class AssessmentSubmissionResult:
    """
    Small frontend-facing result describing one submission.

    The complete authoritative backend result is stored separately
    in centralized application state.

    Attributes
    ----------
    succeeded:
        Whether the authoritative deterministic assessment
        completed successfully.

    assessment_completed:
        Whether the frontend may treat the device assessment as
        complete.

    validation_failed:
        Whether the submitted assessment could not pass the
        deterministic assessment input boundary.

    used_fallback:
        Whether optional RAG or AI enrichment fell back to the
        deterministic result.

    message:
        Optional safe user-facing status or error message.
    """

    succeeded: bool

    assessment_completed: bool

    validation_failed: bool

    used_fallback: bool

    message: str | None = None


# ============================================================
# RUNTIME MODE CONTRACT
# ============================================================


@dataclass(frozen=True)
class RuntimeModeStatus:
    """
    Frontend-safe description of the active EcoShield mode.

    This intentionally exposes no API keys, credentials, provider
    clients, or other sensitive runtime configuration.
    """

    mode: str

    label: str

    use_rag: bool

    use_ai: bool


# ============================================================
# MODE LABELS
# ============================================================


_RUNTIME_MODE_LABELS: dict[str, str] = {
    "deterministic": "Deterministic",
    "rag": "RAG-Grounded",
    "ai": "RAG + AI",
}


# ============================================================
# SERVICE CONFIGURATION
# ============================================================


def _build_service_config(
    runtime_config: RuntimeConfig,
) -> AssessmentServiceConfig:
    """
    Convert centralized runtime configuration into the frozen
    assessment-service configuration contract.
    """

    return AssessmentServiceConfig(
        use_rag=runtime_config.use_rag,
        use_ai=runtime_config.use_ai,
    )


# ============================================================
# LLM CONFIGURATION
# ============================================================


def _build_llm_config(
    runtime_config: RuntimeConfig,
) -> LLMConfig:
    """
    Convert centralized runtime configuration into the frozen
    LLM configuration contract.

    This helper is used only when AI mode is enabled.
    """

    provider = LLMProvider(
        runtime_config.llm_provider
    )

    return LLMConfig(
        provider=provider,
        model=runtime_config.llm_model,
        base_url=runtime_config.llm_base_url,
        api_key=runtime_config.llm_api_key,
        temperature=runtime_config.llm_temperature,
        max_output_tokens=(
            runtime_config.llm_max_output_tokens
        ),
        timeout_seconds=(
            runtime_config.llm_timeout_seconds
        ),
        enabled=True,
    )


# ============================================================
# RUNTIME LLM CLIENT
# ============================================================


def _build_runtime_llm_client(
    runtime_config: RuntimeConfig,
) -> LLMClient | None:
    """
    Build an LLM client only when AI enrichment is enabled.

    Deterministic and RAG-only modes never construct an LLM
    provider client.
    """

    if not runtime_config.use_ai:
        return None

    llm_config = _build_llm_config(
        runtime_config
    )

    return build_llm_client(
        llm_config
    )


# ============================================================
# RUNTIME RETRIEVER
# ============================================================


def _build_runtime_retriever(
    runtime_config: RuntimeConfig,
) -> EcoShieldRetriever | None:
    """
    Build the EcoShield knowledge retriever only when RAG is
    required.

    AI mode also requires RAG grounding, so use_rag is True for
    both RAG and AI modes.
    """

    if not runtime_config.use_rag:
        return None

    return build_retriever()


# ============================================================
# RESULT STATE SYNCHRONIZATION
# ============================================================


def _store_service_result(
    result: AssessmentServiceResult,
) -> None:
    """
    Synchronize one successful backend result with centralized
    application state.

    No result is recalculated or transformed here. The frozen
    backend result remains authoritative.
    """

    set_assessment_service_result(
    result
    )

    set_risk_assessment(
    result.risk
    )

    set_recommendation_result(
    result.recommendation
    )

    set_sustainability_result(
    result.sustainability
    )

    set_assessment_enrichment_state(
        rag_enabled=result.rag_enabled,
        ai_enabled=result.ai_enabled,
        rag_attempted=result.rag_attempted,
        ai_attempted=result.ai_attempted,
        rag_succeeded=result.rag_succeeded,
        ai_succeeded=result.ai_succeeded,
        used_fallback=result.used_fallback,
        retrieved_context=result.retrieved_context,
        ai_explanation=result.ai_explanation,
        warnings=result.warnings,
        errors=result.errors,
    )

    mark_assessment_completed(
        True
    )


# ============================================================
# RUNTIME MODE STATUS
# ============================================================


def get_runtime_mode_status() -> RuntimeModeStatus:
    """
    Return a frontend-safe description of the active assessment
    mode.

    Calling this function does not execute an assessment, build a
    retriever, create an LLM client, or perform network activity.
    """

    runtime_config = (
        load_runtime_config()
    )

    mode = (
        runtime_config.assessment_mode
    )

    label = _RUNTIME_MODE_LABELS.get(
        mode,
        "Deterministic",
    )

    return RuntimeModeStatus(
        mode=mode,
        label=label,
        use_rag=runtime_config.use_rag,
        use_ai=runtime_config.use_ai,
    )


# ============================================================
# PUBLIC ASSESSMENT SUBMISSION
# ============================================================


def submit_device_assessment(
    payload: Mapping[str, Any],
    *,
    user_query: str | None = None,
) -> AssessmentSubmissionResult:
    """
    Submit one device assessment through EcoShield's unified
    backend service.

    This is the primary frontend-to-backend integration entry
    point.

    Execution lifecycle
    -------------------
    1. Clear stale derived assessment results.
    2. Load centralized runtime configuration.
    3. Build assessment-service configuration.
    4. Build optional RAG / AI dependencies.
    5. Call assess_device() exactly once.
    6. Store the complete successful backend result.
    7. Return a small frontend-safe submission result.

    Optional RAG or AI failures are handled by the frozen backend
    service and may return a successful deterministic assessment
    with used_fallback=True.

    Deterministic assessment failures do not create fabricated
    results and do not mark the assessment as completed.
    """

    # --------------------------------------------------------
    # Submission boundary
    #
    # Previous derived results must never survive into a new
    # explicit Analyze submission.
    # --------------------------------------------------------

    clear_assessment_results()

    # --------------------------------------------------------
    # Runtime configuration
    # --------------------------------------------------------

    try:

        runtime_config = (
            load_runtime_config()
        )

        service_config = (
            _build_service_config(
                runtime_config
            )
        )

        # ----------------------------------------------------
        # Optional runtime dependencies
        # ----------------------------------------------------

        retriever = (
            _build_runtime_retriever(
                runtime_config
            )
        )

        llm_client = (
            _build_runtime_llm_client(
                runtime_config
            )
        )

    except Exception as exc:

        # ----------------------------------------------------
        # Configuration/dependency construction failed before
        # authoritative assessment execution.
        # ----------------------------------------------------

        mark_assessment_completed(
            False
        )

        print(
            "[EcoShield] Frontend integration setup error: "
            f"{type(exc).__name__}: {exc}"
        )

        return AssessmentSubmissionResult(
            succeeded=False,
            assessment_completed=False,
            validation_failed=False,
            used_fallback=False,
            message=(
                "EcoShield could not prepare the assessment "
                "service. Please try again."
            ),
        )

    # --------------------------------------------------------
    # Authoritative backend execution
    #
    # assess_device() is called exactly once.
    # --------------------------------------------------------

    try:

        result = assess_device(
            payload,
            config=service_config,
            user_query=user_query,
            retriever=retriever,
            llm_client=llm_client,
        )

    except (TypeError, ValueError) as exc:

        # ----------------------------------------------------
        # Deterministic input/assessment boundary failure.
        #
        # No RiskAssessment or RecommendationResult is
        # fabricated here.
        # ----------------------------------------------------

        mark_assessment_completed(
            False
        )

        print(
            "[EcoShield] Assessment input error: "
            f"{type(exc).__name__}: {exc}"
        )

        return AssessmentSubmissionResult(
            succeeded=False,
            assessment_completed=False,
            validation_failed=True,
            used_fallback=False,
            message=(
                "EcoShield could not validate the submitted "
                "device information. Please review the "
                "assessment answers and try again."
            ),
        )

    except Exception as exc:

        # ----------------------------------------------------
        # Unexpected authoritative assessment failure.
        # ----------------------------------------------------

        mark_assessment_completed(
            False
        )

        print(
            "[EcoShield] Assessment integration error: "
            f"{type(exc).__name__}: {exc}"
        )

        return AssessmentSubmissionResult(
            succeeded=False,
            assessment_completed=False,
            validation_failed=False,
            used_fallback=False,
            message=(
                "EcoShield could not complete the assessment. "
                "Please try again."
            ),
        )

    # --------------------------------------------------------
    # Successful authoritative result
    # --------------------------------------------------------

    _store_service_result(
        result
    )

    # --------------------------------------------------------
    # Optional enrichment fallback does NOT mean that the
    # deterministic assessment failed.
    # --------------------------------------------------------

    if result.used_fallback:

        message = (
            "The device assessment completed successfully. "
            "Optional AI or knowledge enrichment was unavailable, "
            "so EcoShield preserved the deterministic guidance."
        )

    else:

        message = (
            "Device assessment completed successfully."
        )

    return AssessmentSubmissionResult(
        succeeded=True,
        assessment_completed=True,
        validation_failed=False,
        used_fallback=result.used_fallback,
        message=message,
    )