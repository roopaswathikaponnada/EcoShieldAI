"""
Automated tests for the EcoShield AI Advisor.

These tests protect the Phase-10 Advisor contracts without
requiring a live Ollama server or external LLM provider.
"""

from __future__ import annotations

from types import SimpleNamespace

import pytest

from config.config import RuntimeConfig
from src.services.advisor_service import (
    AdvisorGenerationStatus,
    AdvisorQuestionType,
    AdvisorRequest,
    should_use_assessment_context,
    build_advisor_llm_assessment_context,
    build_advisor_llm_risk_context,
    build_advisor_llm_recommendation_context,
    ask_advisor,
    classify_advisor_question,
    requires_evidence_bounded_security_response,
    build_advisor_generation_context,
    resolve_advisor_top_k,
    validate_advisor_semantic_output,
)
from src.ai.llm_client import (
    LLMGenerationStatus,
    LLMResponse,
)
from src.recommendation import generate_recommendation
from src.risk_engine import assess_device_risk
from tests.test_risk_engine import make_base_payload
from views.knowledge_center import (
    _should_generate_advisor_answer,
)


# ============================================================
# HELPERS
# ============================================================


def _make_high_risk_context():
    """
    Build the known authoritative EcoShield assessment used
    throughout Phase-10 acceptance testing.
    """

    payload = make_base_payload(
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        encryption_enabled="No",
        factory_reset_performed="No",
        secure_erase_performed="No",
        accounts_signed_out="No",
        intended_disposal_method="Sell",
    )

    assessment = assess_device_risk(
        payload
    )

    recommendation = generate_recommendation(
        assessment
    )

    return assessment, recommendation


def _make_llm_response(
    text: str,
) -> LLMResponse:
    """
    Build a successful synthetic LLM response for semantic tests.
    """

    return LLMResponse(
        text=text,
        status=LLMGenerationStatus.SUCCESS,
        provider="test",
        model="test-model",
        sources=(),
        grounded=True,
        used_fallback=False,
        error_message=None,
        metadata={},
    )


def _make_request(
    question_type: AdvisorQuestionType,
    *,
    assessment_context_used: bool = False,
) -> AdvisorRequest:
    """
    Build a minimal Advisor request for deterministic tests.
    """

    return AdvisorRequest(
        question="Test question",
        question_type=question_type,
        assessment_context_used=assessment_context_used,
        use_rag=True,
        use_ai=True,
    )


# ============================================================
# QUESTION CLASSIFICATION
# ============================================================


@pytest.mark.parametrize(
    ("question", "expected"),
    (
        (
            "What is e-waste?",
            AdvisorQuestionType.GENERAL_KNOWLEDGE,
        ),
        (
            "What is secure data erasure?",
            AdvisorQuestionType.GENERAL_KNOWLEDGE,
        ),
        (
            "How should I securely erase an SSD?",
            AdvisorQuestionType.SECURITY_GUIDANCE,
        ),
        (
    "How do I protect my data before transferring a device?",
    AdvisorQuestionType.SECURITY_GUIDANCE,
),
        (
            "How can device reuse help sustainability?",
            AdvisorQuestionType.SUSTAINABILITY_GUIDANCE,
        ),
        (
            "How should electronics be recycled responsibly?",
            AdvisorQuestionType.SUSTAINABILITY_GUIDANCE,
        ),
        (
            "Is my device safe to sell now?",
            AdvisorQuestionType.ASSESSMENT_EXPLANATION,
        ),
        (
            "Is my device ready for transfer?",
            AdvisorQuestionType.ASSESSMENT_EXPLANATION,
        ),
    ),
)
def test_advisor_question_classification(
    question,
    expected,
):
    assert (
        classify_advisor_question(question)
        == expected
    )


def test_definition_question_remains_general_knowledge():
    assert (
        classify_advisor_question(
            "What is encryption?"
        )
        == AdvisorQuestionType.GENERAL_KNOWLEDGE
    )


# ============================================================
# ASSESSMENT CONTEXT RULES
# ============================================================


def test_general_question_does_not_use_assessment_context():
    assessment, recommendation = (
        _make_high_risk_context()
    )

    assert (
    should_use_assessment_context(
        "What is e-waste?",
        AdvisorQuestionType.GENERAL_KNOWLEDGE,
        assessment=assessment,
        recommendation=recommendation,
    )
    is False
)


def test_assessment_explanation_uses_available_context():
    assessment, recommendation = (
        _make_high_risk_context()
    )

    assert (
    should_use_assessment_context(
        "Is my device safe to sell now?",
        AdvisorQuestionType.ASSESSMENT_EXPLANATION,
        assessment=assessment,
        recommendation=recommendation,
    )
    is True
)


def test_security_question_uses_context_when_assessment_referenced():
    assessment, recommendation = (
        _make_high_risk_context()
    )

    assert (
    should_use_assessment_context(
        "What security issue was found in my assessment?",
        AdvisorQuestionType.SECURITY_GUIDANCE,
        assessment=assessment,
        recommendation=recommendation,
    )
    is True
)

# ============================================================
# ADVISOR EVIDENCE BUDGET
# ============================================================


def test_general_knowledge_uses_smaller_default_top_k():
    request = AdvisorRequest(
        question="What is e-waste?",
        question_type=AdvisorQuestionType.GENERAL_KNOWLEDGE,
        assessment=None,
        recommendation=None,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    assert resolve_advisor_top_k(request) == 3


@pytest.mark.parametrize(
    ("question_type", "expected_top_k"),
    (
        (
            AdvisorQuestionType.GENERAL_KNOWLEDGE,
            3,
        ),
        (
            AdvisorQuestionType.ASSESSMENT_EXPLANATION,
            3,
        ),
        (
            AdvisorQuestionType.SECURITY_GUIDANCE,
            5,
        ),
        (
            AdvisorQuestionType.SUSTAINABILITY_GUIDANCE,
            5,
        ),
    ),
)
def test_advisor_mode_default_top_k(
    question_type,
    expected_top_k,
):
    request = AdvisorRequest(
        question="EcoShield question",
        question_type=question_type,
        assessment=None,
        recommendation=None,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    assert (
        resolve_advisor_top_k(request)
        == expected_top_k
    )


def test_explicit_top_k_overrides_adaptive_default():
    request = AdvisorRequest(
        question="What is e-waste?",
        question_type=AdvisorQuestionType.GENERAL_KNOWLEDGE,
        assessment=None,
        recommendation=None,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    assert resolve_advisor_top_k(request, 2) == 2
    assert resolve_advisor_top_k(request, 5) == 5

# ============================================================
# ASSESSMENT EXPLANATION CONTEXT BUDGET
# ============================================================


def _make_assessment_explanation_request():
    assessment, recommendation = (
        _make_high_risk_context()
    )

    return AdvisorRequest(
        question="Is my device safe to sell now?",
        question_type=(
            AdvisorQuestionType.ASSESSMENT_EXPLANATION
        ),
        assessment=assessment,
        recommendation=recommendation,
        assessment_context_used=True,
        use_rag=True,
        use_ai=True,
    )


def test_assessment_llm_context_is_compact():
    request = (
        _make_assessment_explanation_request()
    )

    context = (
        build_advisor_llm_assessment_context(
            request
        )
    )

    assert context is not None

    assert set(context).issubset(
        {
            "device_type",
            "operating_system",
            "storage_type",
            "intended_disposal_method",
        }
    )

    assert len(context) <= 4


def test_assessment_llm_risk_context_preserves_authority():
    request = (
        _make_assessment_explanation_request()
    )

    context = build_advisor_llm_risk_context(
        request
    )

    assert context is not None
    assert (
        context["risk_score"]
        == request.assessment.score
    )
    assert (
        context["risk_level"]
        == request.assessment.risk_level
    )

    assert set(context) == {
        "risk_score",
        "risk_level",
        "risk_factors",
    }


def test_assessment_llm_recommendation_preserves_readiness():
    request = (
        _make_assessment_explanation_request()
    )

    context = (
        build_advisor_llm_recommendation_context(
            request
        )
    )

    assert context is not None

    assert (
        context["risk_score"]
        == request.recommendation.risk_score
    )
    assert (
        context["risk_level"]
        == request.recommendation.risk_level
    )
    assert (
        context["readiness"]
        == request.recommendation.readiness
    )

    assert "warnings" not in context

# ============================================================
# DETERMINISTIC AUTHORITY
# ============================================================


def test_known_high_risk_assessment_remains_authoritative():
    assessment, recommendation = (
        _make_high_risk_context()
    )

    assert assessment.score == 80
    assert assessment.risk_level == "High"
    assert recommendation.readiness == "Not Ready"


# ============================================================
# OUT-OF-SCOPE / FAIL-CLOSED
# ============================================================


def test_out_of_scope_question_is_unavailable_without_ai():
    result = ask_advisor(
        "Who won the cricket match yesterday?",
        config=RuntimeConfig(
            assessment_mode="ai",
        ),
    )

    assert (
        result.status
        == AdvisorGenerationStatus.UNAVAILABLE
    )

    assert result.rag_attempted is False
    assert result.ai_attempted is False
    assert result.ai_succeeded is False


def test_assessment_question_without_context_fails_closed():
    result = ask_advisor(
        "Is my device safe to sell now?",
        config=RuntimeConfig(
            assessment_mode="ai",
        ),
    )

    assert (
        result.status
        == AdvisorGenerationStatus.UNAVAILABLE
    )

    assert result.assessment_context_used is False
    assert result.rag_attempted is False
    assert result.ai_attempted is False


# ============================================================
# SEMANTIC SAFETY
# ============================================================


def test_semantic_validator_rejects_absolute_security_claim():
    request = _make_request(
        AdvisorQuestionType.SECURITY_GUIDANCE
    )

    response = _make_llm_response(
        "This will guarantee that your data is secure."
    )

    violations = (
        validate_advisor_semantic_output(
            request,
            response,
        )
    )

    assert (
        "ABSOLUTE_SECURITY_CLAIM"
        in violations
    )


def test_semantic_validator_rejects_generic_readiness_claim():
    request = _make_request(
        AdvisorQuestionType.SECURITY_GUIDANCE
    )

    response = _make_llm_response(
        "Your device is ready for sale."
    )

    violations = (
        validate_advisor_semantic_output(
            request,
            response,
        )
    )

    assert (
        "UNSUPPORTED_GENERIC_READINESS_CLAIM"
        in violations
    )


def test_semantic_validator_rejects_known_tool_guidance():
    request = _make_request(
        AdvisorQuestionType.SUSTAINABILITY_GUIDANCE
    )

    response = _make_llm_response(
        "Use CCleaner to prepare the device."
    )

    violations = (
        validate_advisor_semantic_output(
            request,
            response,
        )
    )

    assert (
        "UNSUPPORTED_TOOL_GUIDANCE"
        in violations
    )


def test_semantic_validator_accepts_safe_sustainability_text():
    request = _make_request(
        AdvisorQuestionType.SUSTAINABILITY_GUIDANCE
    )

    response = _make_llm_response(
        "Reusing a functional device can extend its useful "
        "life and reduce premature electronic waste."
    )

    violations = (
        validate_advisor_semantic_output(
            request,
            response,
        )
    )

    assert violations == ()

# ============================================================
# EVIDENCE-BOUNDED SECURITY GUIDANCE
# ============================================================


def test_procedural_ssd_question_uses_evidence_bounded_path():
    request = AdvisorRequest(
        question="How should I securely erase an SSD?",
        question_type=AdvisorQuestionType.SECURITY_GUIDANCE,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    assert (
        requires_evidence_bounded_security_response(
            request
        )
        is True
    )


def test_normal_security_question_can_use_llm_path():
    request = AdvisorRequest(
        question=(
            "How do I protect my data before "
            "transferring a device?"
        ),
        question_type=AdvisorQuestionType.SECURITY_GUIDANCE,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    assert (
        requires_evidence_bounded_security_response(
            request
        )
        is False
    )


def test_security_generation_context_contains_grounding_rule():
    request = AdvisorRequest(
        question="How do I protect my data?",
        question_type=AdvisorQuestionType.SECURITY_GUIDANCE,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    context = build_advisor_generation_context(
        request
    )

    assert context is not None
    assert (
        "advisor_security_grounding"
        in context
    )


def test_general_generation_context_has_no_security_rule():
    request = AdvisorRequest(
        question="What is e-waste?",
        question_type=AdvisorQuestionType.GENERAL_KNOWLEDGE,
        assessment_context_used=False,
        use_rag=True,
        use_ai=True,
    )

    context = build_advisor_generation_context(
        request
    )

    assert context is None

# ============================================================
# FRONTEND DUPLICATE-GENERATION CONTRACT
# ============================================================


def test_first_advisor_question_requires_generation(
    monkeypatch,
):
    monkeypatch.setattr(
        "views.knowledge_center.get_advisor_result",
        lambda: None,
    )

    assert (
        _should_generate_advisor_answer(
            "What is e-waste?"
        )
        is True
    )


def test_same_stored_question_does_not_regenerate(
    monkeypatch,
):
    stored_result = SimpleNamespace(
        answer="Stored answer"
    )

    monkeypatch.setattr(
        "views.knowledge_center.get_advisor_result",
        lambda: stored_result,
    )

    monkeypatch.setattr(
        "views.knowledge_center.get_last_question",
        lambda: "What is e-waste?",
    )

    assert (
        _should_generate_advisor_answer(
            "What is e-waste?"
        )
        is False
    )


def test_different_question_requires_new_generation(
    monkeypatch,
):
    stored_result = SimpleNamespace(
        answer="Stored answer"
    )

    monkeypatch.setattr(
        "views.knowledge_center.get_advisor_result",
        lambda: stored_result,
    )

    monkeypatch.setattr(
        "views.knowledge_center.get_last_question",
        lambda: "What is e-waste?",
    )

    assert (
        _should_generate_advisor_answer(
            "How does reuse help sustainability?"
        )
        is True
    )