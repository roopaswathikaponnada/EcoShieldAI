"""
EcoShield AI
Assessment Service Tests

Automated tests for the backend orchestration layer.

These tests verify:
- configuration behavior
- request normalization
- deterministic orchestration
- RAG orchestration
- AI orchestration
- deterministic authority
- graceful enrichment fallback
- dependency validation
- response normalization
- public service dispatch

External LLM services are not required.
"""

from __future__ import annotations

from dataclasses import replace
from unittest.mock import patch

import pytest

import src.services.assessment_service as service

from src.ai.llm_client import (
    LLMConfig,
    LLMProvider,
    build_llm_client,
)


# ============================================================
# TEST DATA
# ============================================================


@pytest.fixture
def high_risk_payload() -> dict[str, object]:
    """
    Return the known high-risk donation scenario.
    """

    return {
        "device_type": "Laptop",
        "operating_system": "Windows",
        "device_age": 4,
        "device_condition": "Working",
        "storage_type": "SSD",
        "storage_capacity": "512 GB",
        "contains_personal_data": "Yes",
        "contains_sensitive_data": "Yes",
        "device_accessible": "Yes",
        "can_power_on": "Yes",
        "data_backed_up": "Yes",
        "factory_reset_performed": "No",
        "secure_erase_performed": "No",
        "encryption_enabled": "Yes",
        "accounts_signed_out": "No",
        "sim_memory_card_removed": "Yes",
        "intended_disposal_method": "Donate",
    }


@pytest.fixture
def llm_client():
    """
    Build an LLM client object without making a provider request.
    """

    return build_llm_client(
        LLMConfig(
            provider=LLMProvider.OLLAMA,
            model="qwen2.5:3b",
        )
    )


# ============================================================
# CONFIGURATION
# ============================================================


def test_default_config_is_deterministic():
    config = service.AssessmentServiceConfig()

    assert config.use_rag is False
    assert config.use_ai is False
    assert config.effective_use_rag is False
    assert config.effective_use_ai is False
    assert service._resolve_service_mode(config) == "deterministic"


def test_rag_only_config_resolves_to_rag():
    config = service.AssessmentServiceConfig(
        use_rag=True
    )

    assert config.effective_use_rag is True
    assert config.effective_use_ai is False
    assert service._resolve_service_mode(config) == "rag"


def test_ai_config_implies_rag():
    config = service.AssessmentServiceConfig(
        use_ai=True
    )

    assert config.use_rag is False
    assert config.use_ai is True
    assert config.effective_use_rag is True
    assert config.effective_use_ai is True
    assert service._resolve_service_mode(config) == "ai"


def test_rag_and_ai_config_resolves_to_ai():
    config = service.AssessmentServiceConfig(
        use_rag=True,
        use_ai=True,
    )

    assert config.effective_use_rag is True
    assert config.effective_use_ai is True
    assert service._resolve_service_mode(config) == "ai"


def test_invalid_use_rag_type_rejected():
    with pytest.raises(
        TypeError,
        match="use_rag must be a boolean",
    ):
        service.AssessmentServiceConfig(
            use_rag="yes"  # type: ignore[arg-type]
        )


def test_invalid_use_ai_type_rejected():
    with pytest.raises(
        TypeError,
        match="use_ai must be a boolean",
    ):
        service.AssessmentServiceConfig(
            use_ai=1  # type: ignore[arg-type]
        )


def test_none_config_normalizes_to_default():
    config = service._normalize_service_config(
        None
    )

    assert isinstance(
        config,
        service.AssessmentServiceConfig,
    )
    assert (
        service._resolve_service_mode(config)
        == "deterministic"
    )


def test_invalid_config_object_rejected():
    with pytest.raises(
        TypeError,
        match="config must be an AssessmentServiceConfig",
    ):
        service._normalize_service_config(
            {"use_rag": True}  # type: ignore[arg-type]
        )


# ============================================================
# REQUEST NORMALIZATION
# ============================================================


def test_payload_keys_are_trimmed():
    payload = {
        " device_type ": "Laptop",
        " operating_system ": "Windows",
    }

    normalized = (
        service._normalize_assessment_payload(
            payload
        )
    )

    assert normalized == {
        "device_type": "Laptop",
        "operating_system": "Windows",
    }


def test_payload_values_are_not_silently_changed():
    payload = {
        "factory_reset_performed": "Unknown"
    }

    normalized = (
        service._normalize_assessment_payload(
            payload
        )
    )

    assert (
        normalized["factory_reset_performed"]
        == "Unknown"
    )


def test_non_mapping_payload_rejected():
    with pytest.raises(
        TypeError,
        match="Assessment payload must be a mapping",
    ):
        service._normalize_assessment_payload(
            ["invalid"]  # type: ignore[arg-type]
        )


def test_non_string_payload_key_rejected():
    with pytest.raises(
        TypeError,
        match="Assessment payload keys must be strings",
    ):
        service._normalize_assessment_payload(
            {1: "Laptop"}  # type: ignore[dict-item]
        )


def test_empty_normalized_key_rejected():
    with pytest.raises(
        ValueError,
        match="Assessment payload keys cannot be empty",
    ):
        service._normalize_assessment_payload(
            {"   ": "Laptop"}
        )


def test_duplicate_normalized_key_rejected():
    with pytest.raises(
        ValueError,
        match="duplicate normalized key",
    ):
        service._normalize_assessment_payload(
            {
                "device_type": "Laptop",
                " device_type ": "Desktop",
            }
        )


def test_user_query_is_trimmed():
    assert (
        service._normalize_user_query(
            "   How should I donate this laptop?   "
        )
        == "How should I donate this laptop?"
    )


def test_empty_user_query_becomes_none():
    assert (
        service._normalize_user_query("   ")
        is None
    )


def test_none_user_query_remains_none():
    assert (
        service._normalize_user_query(None)
        is None
    )


def test_invalid_user_query_type_rejected():
    with pytest.raises(
        TypeError,
        match="user_query must be a string or None",
    ):
        service._normalize_user_query(
            123  # type: ignore[arg-type]
        )


# ============================================================
# DETERMINISTIC ORCHESTRATION
# ============================================================


def test_deterministic_service_known_high_risk_result(
    high_risk_payload,
):
    result = service.assess_device(
        high_risk_payload
    )

    assert result.risk.score == 73
    assert result.risk.risk_level == "High"

    assert (
        result.recommendation.readiness
        == "Not Ready"
    )

    assert result.rag_enabled is False
    assert result.ai_enabled is False

    assert result.rag_attempted is False
    assert result.ai_attempted is False

    assert result.rag_succeeded is False
    assert result.ai_succeeded is False

    assert result.used_fallback is False

    assert (
        result.recommendation.assessment
        is result.risk
    )


def test_deterministic_service_normalizes_query(
    high_risk_payload,
):
    result = service.assess_device(
        high_risk_payload,
        user_query=(
            "   How should I donate this laptop?   "
        ),
    )

    assert (
        result.user_query
        == "How should I donate this laptop?"
    )


def test_deterministic_pipeline_reuses_risk_object(
    high_risk_payload,
):
    risk, recommendation, sustainability = (
    service._run_deterministic_assessment(
        high_risk_payload
    )
)

    assert recommendation.assessment is risk
    assert recommendation.risk_score == risk.score
    assert (
        recommendation.risk_level
        == risk.risk_level
    )
    assert sustainability is not None
    assert (
    sustainability.validated_data
    == risk.validated_data
    )


# ============================================================
# DEPENDENCY HARDENING
# ============================================================


def test_invalid_retriever_rejected():
    config = service.AssessmentServiceConfig(
        use_rag=True
    )

    with pytest.raises(
        TypeError,
        match="retriever must be an EcoShieldRetriever",
    ):
        service.assess_device(
            {},
            config=config,
            retriever="invalid",  # type: ignore[arg-type]
        )


def test_missing_llm_client_rejected():
    config = service.AssessmentServiceConfig(
        use_ai=True
    )

    with pytest.raises(
        ValueError,
        match="llm_client is required",
    ):
        service.assess_device(
            {},
            config=config,
        )


def test_invalid_llm_client_rejected():
    config = service.AssessmentServiceConfig(
        use_ai=True
    )

    with pytest.raises(
        TypeError,
        match="llm_client must be an LLMClient",
    ):
        service.assess_device(
            {},
            config=config,
            llm_client="invalid",  # type: ignore[arg-type]
        )


def test_unsupported_mode_rejected():
    with pytest.raises(
        ValueError,
        match="Unsupported assessment service mode",
    ):
        service._validate_service_dependencies(
            mode="unsupported",
            retriever=None,
            llm_client=None,
        )


# ============================================================
# RAG ORCHESTRATION
# ============================================================


def test_public_rag_mode(
    high_risk_payload,
):
    result = service.assess_device(
        high_risk_payload,
        config=service.AssessmentServiceConfig(
            use_rag=True
        ),
        user_query=(
            "How should I safely donate "
            "this laptop?"
        ),
    )

    assert result.risk.score == 73
    assert result.risk.risk_level == "High"

    assert result.rag_enabled is True
    assert result.rag_attempted is True
    assert result.rag_succeeded is True

    assert result.ai_enabled is False
    assert result.ai_attempted is False

    assert len(result.retrieved_context) > 0

    assert (
        result.recommendation.assessment
        is result.risk
    )


def test_rag_failure_preserves_deterministic_result(
    high_risk_payload,
):
    with patch.object(
        service,
        "enrich_recommendation_with_rag",
        side_effect=RuntimeError(
            "private internal failure"
        ),
    ):
        result = service.assess_device(
            high_risk_payload,
            config=service.AssessmentServiceConfig(
                use_rag=True
            ),
        )

    assert result.risk.score == 73
    assert result.risk.risk_level == "High"

    assert (
        result.recommendation.readiness
        == "Not Ready"
    )

    assert result.rag_enabled is True
    assert result.rag_attempted is True
    assert result.rag_succeeded is False

    assert result.used_fallback is True

    assert result.errors == (
        service.RAG_ENRICHMENT_FAILED,
    )

    assert "private internal failure" not in str(
        result.errors
    )

    assert (
        result.recommendation.assessment
        is result.risk
    )


# ============================================================
# AI ORCHESTRATION
# ============================================================


def test_ai_failure_preserves_deterministic_result(
    high_risk_payload,
    llm_client,
):
    with patch.object(
        service,
        "enrich_recommendation_with_ai",
        side_effect=RuntimeError(
            "private AI provider failure"
        ),
    ):
        result = service.assess_device(
            high_risk_payload,
            config=service.AssessmentServiceConfig(
                use_ai=True
            ),
            llm_client=llm_client,
            user_query=(
                "How should I safely donate "
                "this laptop?"
            ),
        )

    assert result.risk.score == 73
    assert result.risk.risk_level == "High"

    assert result.rag_enabled is True
    assert result.ai_enabled is True

    assert result.rag_attempted is True
    assert result.ai_attempted is True

    assert result.rag_succeeded is False
    assert result.ai_succeeded is False

    assert result.used_fallback is True

    assert result.errors == (
        service.AI_ENRICHMENT_FAILED,
    )

    assert (
        "private AI provider failure"
        not in str(result.errors)
    )

    assert (
        result.recommendation.assessment
        is result.risk
    )


# ============================================================
# DETERMINISTIC AUTHORITY
# ============================================================


def test_authority_guard_rejects_risk_score_change(
    high_risk_payload,
):
    risk, recommendation, sustainability = (
    service._run_deterministic_assessment(
        high_risk_payload
    )
)

    tampered = replace(
        recommendation,
        risk_score=recommendation.risk_score + 1,
    )

    with pytest.raises(
        service.DeterministicAuthorityError,
        match="risk_score",
    ):
        service._verify_deterministic_authority(
            risk,
            recommendation,
            tampered,
        )


def test_authority_guard_rejects_readiness_change(
    high_risk_payload,
):
    risk, recommendation, sustainability = (
    service._run_deterministic_assessment(
        high_risk_payload
    )
)

    tampered = replace(
        recommendation,
        readiness="Ready",
    )

    with pytest.raises(
        service.DeterministicAuthorityError,
        match="readiness",
    ):
        service._verify_deterministic_authority(
            risk,
            recommendation,
            tampered,
        )


def test_authority_guard_accepts_untampered_result(
    high_risk_payload,
):
    risk, recommendation, sustainability = (
    service._run_deterministic_assessment(
        high_risk_payload
    )
)

    service._verify_deterministic_authority(
        risk,
        recommendation,
        recommendation,
    )


# ============================================================
# RESPONSE NORMALIZATION
# ============================================================


def test_normalized_response_structure(
    high_risk_payload,
):
    result = service.assess_device(
        high_risk_payload
    )

    response = (
        service._normalize_service_response(
            result
        )
    )

    assert list(response.keys()) == [
        "assessment",
        "recommendations",
        "enrichment",
        "meta",
    ]

    assert (
        response["assessment"]["risk_score"]
        == 73
    )

    assert (
        response["assessment"]["risk_level"]
        == "High"
    )

    assert (
        response["assessment"]["readiness"]
        == "Not Ready"
    )

    assert (
        len(
            response["recommendations"][
                "security_actions"
            ]
        )
        == 4
    )

    assert (
        response["enrichment"]["rag_enabled"]
        is False
    )

    assert (
        response["enrichment"]["ai_enabled"]
        is False
    )


def test_invalid_response_object_rejected():
    with pytest.raises(
        TypeError,
        match=(
            "result must be an "
            "AssessmentServiceResult instance"
        ),
    ):
        service._normalize_service_response(
            {"risk": 73}  # type: ignore[arg-type]
        )