"""
EcoShield AI
Recommendation Engine Tests

Tests deterministic recommendation behavior and its core
security/sustainability contracts.

The recommendation engine is authoritative and deterministic.
These tests must not require RAG, an LLM, Ollama, or internet access.
"""

from __future__ import annotations

import sys
from pathlib import Path

import pytest


PROJECT_ROOT = Path(__file__).resolve().parents[1]

if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))


from src.recommendation import (
    RecommendationItem,
    RecommendationResult,
    generate_recommendation,
    get_disposal_readiness,
    get_security_actions,
    get_sustainability_actions,
)


# ============================================================
# REUSABLE PAYLOADS
# ============================================================


def build_low_risk_payload() -> dict:
    """
    Return a fully prepared working device.

    Expected behavior:
    - Low risk
    - Ready
    - No unnecessary security actions
    - Reuse-oriented sustainability guidance
    """

    return {
        "device_type": "Laptop",
        "operating_system": "Windows",
        "device_age": 3,
        "device_condition": "Working",
        "storage_type": "SSD",
        "storage_capacity": "512 GB",
        "contains_personal_data": "No",
        "contains_sensitive_data": "No",
        "device_accessible": "Yes",
        "can_power_on": "Yes",
        "data_backed_up": "Yes",
        "factory_reset_performed": "Yes",
        "secure_erase_performed": "Yes",
        "encryption_enabled": "Yes",
        "accounts_signed_out": "Yes",
        "sim_memory_card_removed": "Yes",
        "intended_disposal_method": "Donate",
    }


def build_high_risk_payload() -> dict:
    """
    Return an unsafe ownership-transfer scenario.

    Expected behavior:
    - High risk
    - Not Ready
    - transfer blocked
    - sanitization required
    - account sign-out required
    - reset required
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


def build_uncertain_payload() -> dict:
    """
    Return a valid assessment containing supported uncertainty values.
    """

    return {
        "device_type": "Laptop",
        "operating_system": "Windows",
        "device_age": 4,
        "device_condition": "Working",
        "storage_type": "SSD",
        "storage_capacity": "512 GB",
        "contains_personal_data": "Unsure",
        "contains_sensitive_data": "Unsure",
        "device_accessible": "Yes",
        "can_power_on": "Yes",
        "data_backed_up": "Unsure",
        "factory_reset_performed": "Unsure",
        "secure_erase_performed": "Unsure",
        "encryption_enabled": "Unsure",
        "accounts_signed_out": "Unsure",
        "sim_memory_card_removed": "Unsure",
        "intended_disposal_method": "Donate",
    }


# ============================================================
# DATA CONTRACT TESTS
# ============================================================


def test_recommendation_item_contract() -> None:
    item = RecommendationItem(
        code="TEST_ACTION",
        category="Security",
        priority="High",
        title="Test action",
        action="Perform the test action.",
        rationale="Required for testing.",
    )

    assert item.code == "TEST_ACTION"
    assert item.category == "Security"
    assert item.priority == "High"
    assert item.title == "Test action"
    assert item.source
    assert isinstance(item.evidence, tuple)


def test_generate_recommendation_returns_result() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    assert isinstance(
        result,
        RecommendationResult,
    )

    assert result.assessment is not None
    assert isinstance(result.security_actions, tuple)
    assert isinstance(result.sustainability_actions, tuple)
    assert isinstance(result.next_steps, tuple)
    assert isinstance(result.warnings, tuple)


def test_deterministic_result_has_no_ai_by_default() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    assert result.ai_explanation is None
    assert result.retrieved_context == ()
    assert result.used_ai is False
    assert result.used_fallback is False


# ============================================================
# LOW-RISK / READY TESTS
# ============================================================


def test_prepared_device_is_low_risk() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    assert result.risk_level == "Low"
    assert result.risk_score <= 24


def test_prepared_device_is_ready() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    assert result.readiness == "Ready"


def test_prepared_device_has_no_security_actions() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    assert result.security_actions == ()


def test_prepared_working_device_prefers_reuse() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    action_codes = {
        item.code
        for item in result.sustainability_actions
    }

    assert (
        "PREFER_REUSE_FOR_WORKING_DEVICE"
        in action_codes
    )


def test_low_risk_next_steps_are_sustainability_focused() -> None:
    result = generate_recommendation(
        build_low_risk_payload()
    )

    assert result.next_steps == (
        "Prefer continued use or reuse",
    )


# ============================================================
# CONVENIENCE PUBLIC API TESTS
# ============================================================


def test_get_disposal_readiness_matches_result() -> None:
    payload = build_low_risk_payload()

    result = generate_recommendation(payload)

    assert (
        get_disposal_readiness(payload)
        == result.readiness
    )


def test_get_security_actions_matches_result() -> None:
    payload = build_high_risk_payload()

    result = generate_recommendation(payload)

    assert (
        get_security_actions(payload)
        == result.security_actions
    )


def test_get_sustainability_actions_matches_result() -> None:
    payload = build_low_risk_payload()

    result = generate_recommendation(payload)

    assert (
        get_sustainability_actions(payload)
        == result.sustainability_actions
    )

# ============================================================
# HIGH-RISK / NOT READY TESTS
# ============================================================


def test_high_risk_transfer_is_not_ready() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    assert result.risk_level == "High"
    assert result.risk_score >= 50
    assert result.readiness == "Not Ready"


def test_high_risk_transfer_blocks_device_transfer() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    action_codes = {
        item.code
        for item in result.security_actions
    }

    assert "BLOCK_TRANSFER_UNTIL_SECURE" in action_codes


def test_high_risk_transfer_requires_sanitization() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    action_codes = {
        item.code
        for item in result.security_actions
    }

    assert "PERFORM_SECURE_SANITIZATION" in action_codes


def test_high_risk_transfer_requires_account_signout() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    action_codes = {
        item.code
        for item in result.security_actions
    }

    assert "SIGN_OUT_ACCOUNTS" in action_codes


def test_high_risk_transfer_requires_factory_reset() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    action_codes = {
        item.code
        for item in result.security_actions
    }

    assert "COMPLETE_FACTORY_RESET" in action_codes


def test_high_risk_working_device_still_gets_reuse_guidance() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    sustainability_codes = {
        item.code
        for item in result.sustainability_actions
    }

    assert (
        "PREFER_REUSE_FOR_WORKING_DEVICE"
        in sustainability_codes
    )


# ============================================================
# UNCERTAINTY TESTS
# ============================================================


def test_uncertain_payload_records_uncertainties() -> None:
    result = generate_recommendation(
        build_uncertain_payload()
    )

    assert result.assessment is not None
    assert len(result.assessment.uncertainties) > 0


def test_uncertain_transfer_is_not_ready() -> None:
    result = generate_recommendation(
        build_uncertain_payload()
    )

    assert result.readiness == "Not Ready"


def test_uncertain_payload_requires_uncertainty_resolution() -> None:
    result = generate_recommendation(
        build_uncertain_payload()
    )

    action_codes = {
        item.code
        for item in result.security_actions
    }

    assert (
        "RESOLVE_ASSESSMENT_UNCERTAINTY"
        in action_codes
    )


def test_uncertain_payload_uses_verification_actions() -> None:
    result = generate_recommendation(
        build_uncertain_payload()
    )

    action_codes = {
        item.code
        for item in result.security_actions
    }

    expected_codes = {
        "VERIFY_SECURE_SANITIZATION",
        "VERIFY_BACKUP",
        "VERIFY_ACCOUNT_SIGNOUT",
        "VERIFY_FACTORY_RESET",
        "VERIFY_REMOVABLE_MEDIA",
        "VERIFY_ENCRYPTION_STATUS",
    }

    assert expected_codes.issubset(
        action_codes
    )


# ============================================================
# ORDERING TESTS
# ============================================================


def test_high_risk_next_steps_start_with_transfer_block() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    assert result.next_steps[0] == (
        "Do not transfer the device yet"
    )


def test_security_steps_appear_before_sustainability_step() -> None:
    result = generate_recommendation(
        build_high_risk_payload()
    )

    reuse_index = result.next_steps.index(
        "Prefer continued use or reuse"
    )

    assert reuse_index == (
        len(result.next_steps) - 1
    )    

# ============================================================
# RISK ASSESSMENT PRESERVATION TESTS
# ============================================================


def test_existing_risk_assessment_is_preserved() -> None:
    from src.risk_engine import assess_device_risk

    assessment = assess_device_risk(
        build_high_risk_payload()
    )

    result = generate_recommendation(
        assessment
    )

    assert result.assessment is assessment
    assert result.risk_score == assessment.score
    assert result.risk_level == assessment.risk_level


def test_generate_recommendation_does_not_change_assessment_values() -> None:
    from src.risk_engine import assess_device_risk

    assessment = assess_device_risk(
        build_high_risk_payload()
    )

    original_score = assessment.score
    original_level = assessment.risk_level
    original_uncertainties = assessment.uncertainties
    original_requires_sanitization = (
        assessment.requires_sanitization
    )

    generate_recommendation(
        assessment
    )

    assert assessment.score == original_score
    assert assessment.risk_level == original_level
    assert (
        assessment.uncertainties
        == original_uncertainties
    )
    assert (
        assessment.requires_sanitization
        == original_requires_sanitization
    )


# ============================================================
# INVALID INPUT TESTS
# ============================================================


@pytest.mark.parametrize(
    "invalid_input",
    [
        None,
        "invalid",
        123,
        3.14,
        [],
    ],
)
def test_invalid_recommendation_input_raises_type_error(
    invalid_input,
) -> None:

    with pytest.raises(
        TypeError,
        match=(
            "Recommendation input must be either"
        ),
    ):
        generate_recommendation(
            invalid_input
        )


def test_invalid_payload_raises_value_error() -> None:
    invalid_payload = {
        "device_type": "Laptop",
    }

    with pytest.raises(
        ValueError,
        match=(
            "Device assessment cannot be scored"
        ),
    ):
        generate_recommendation(
            invalid_payload
        )


# ============================================================
# REPEATABILITY TESTS
# ============================================================


def test_recommendation_is_deterministic() -> None:
    payload = build_high_risk_payload()

    result_1 = generate_recommendation(
        payload
    )

    result_2 = generate_recommendation(
        payload
    )

    assert result_1.risk_score == result_2.risk_score
    assert result_1.risk_level == result_2.risk_level
    assert result_1.readiness == result_2.readiness
    assert (
        result_1.security_actions
        == result_2.security_actions
    )
    assert (
        result_1.sustainability_actions
        == result_2.sustainability_actions
    )
    assert (
        result_1.next_steps
        == result_2.next_steps
    )
    assert result_1.warnings == result_2.warnings


# ============================================================
# RESPONSIBLE-AI ACTION-SCOPE GUARD TESTS
# ============================================================


def test_unsupported_security_action_is_detected() -> None:
    from src.ai.recommendation_enricher import (
        _find_unsupported_security_action,
    )

    result = generate_recommendation(
        build_low_risk_payload()
    )

    detected = (
        _find_unsupported_security_action(
            (
                "Perform a factory reset before "
                "donating the device."
            ),
            result,
        )
    )

    assert detected == (
        "COMPLETE_FACTORY_RESET"
    )


def test_allowed_security_action_is_not_rejected() -> None:
    from src.ai.recommendation_enricher import (
        _find_unsupported_security_action,
    )

    result = generate_recommendation(
        build_high_risk_payload()
    )

    detected = (
        _find_unsupported_security_action(
            (
                "Perform a factory reset before "
                "transfer."
            ),
            result,
        )
    )

    assert detected is None


@pytest.mark.parametrize(
    "general_guidance",
    [
        (
            "Factory reset is a common general "
            "device-preparation concept."
        ),
        (
            "Secure erase is a general "
            "sanitization technique."
        ),
        (
            "Accounts can sometimes remain "
            "linked to devices."
        ),
    ],
)
def test_general_security_guidance_does_not_trigger_guard(
    general_guidance,
) -> None:
    from src.ai.recommendation_enricher import (
        _find_unsupported_security_action,
    )

    result = generate_recommendation(
        build_low_risk_payload()
    )

    detected = (
        _find_unsupported_security_action(
            general_guidance,
            result,
        )
    )

    assert detected is None


# ============================================================
# SAFE FALLBACK TESTS
# ============================================================


def test_safe_fallback_uses_authoritative_result() -> None:
    from src.ai.recommendation_enricher import (
        _build_recommendation_safe_fallback,
    )

    result = generate_recommendation(
        build_high_risk_payload()
    )

    fallback = (
        _build_recommendation_safe_fallback(
            result,
            reason="AI unavailable.",
        )
    )

    assert (
        f"Risk: {result.risk_level} "
        f"({result.risk_score}/100)"
        in fallback
    )

    assert (
        f"Readiness: {result.readiness}"
        in fallback
    )

    assert result.summary in fallback

    for step in result.next_steps:
        assert step in fallback

    assert (
        "AI fallback reason: AI unavailable."
        in fallback
    )


def test_safe_fallback_handles_empty_next_steps() -> None:
    from src.ai.recommendation_enricher import (
        _build_recommendation_safe_fallback,
    )

    result = RecommendationResult(
        risk_score=15,
        risk_level="Low",
        readiness="Ready",
        summary="Device is ready.",
        next_steps=(),
    )

    fallback = (
        _build_recommendation_safe_fallback(
            result,
            reason="AI unavailable.",
        )
    )

    assert "Risk: Low (15/100)" in fallback
    assert "Readiness: Ready" in fallback
    assert "Device is ready." in fallback

    assert (
        "Recommended next steps:"
        not in fallback
    )


def test_safe_fallback_does_not_mark_ai_as_success() -> None:
    from src.ai.recommendation_enricher import (
        _build_recommendation_safe_fallback,
    )

    result = generate_recommendation(
        build_low_risk_payload()
    )

    fallback = (
        _build_recommendation_safe_fallback(
            result,
            reason=(
                "Unsupported AI-generated action."
            ),
        )
    )

    assert (
        "could not safely provide an "
        "AI-generated explanation"
        in fallback
    )    