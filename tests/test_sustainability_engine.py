"""
EcoShield AI
Deterministic Sustainability Impact Engine Tests

These tests protect the Phase-11 sustainability contract.

Covered contracts:
- score boundaries
- opportunity-level boundaries
- result structure
- category limits
- factor explainability
- lifecycle-extension logic
- reuse / resale / donation logic
- repair / refurbishment logic
- responsible recycling logic
- device-age rules
- intended-action rules
- preferred lifecycle action
- sustainability uncertainty
- convenience helpers
- deterministic repeatability
- cybersecurity independence
- serialization
- invalid-input handling
"""

from __future__ import annotations

from dataclasses import FrozenInstanceError

import pytest

from src.sustainability_engine import (
    ACTION_CONTINUE_USE,
    ACTION_DONATE,
    ACTION_RECYCLE,
    ACTION_REPAIR,
    ACTION_REUSE,
    ACTION_REVIEW,
    ACTION_SELL,
    CATEGORY_END_OF_LIFE,
    CATEGORY_LIFECYCLE_EXTENSION,
    CATEGORY_MAX_SCORES,
    CATEGORY_REPAIR_POTENTIAL,
    CATEGORY_REUSE_POTENTIAL,
    MAX_SUSTAINABILITY_SCORE,
    MIN_SUSTAINABILITY_SCORE,
    OPPORTUNITY_HIGH,
    OPPORTUNITY_LOW,
    OPPORTUNITY_MODERATE,
    OPPORTUNITY_VERY_HIGH,
    POTENTIAL_HIGH,
    POTENTIAL_LOW,
    POTENTIAL_MODERATE,
    SustainabilityFactor,
    SustainabilityImpactResult,
    assess_sustainability,
    get_preferred_sustainable_action,
    get_sustainability_opportunity_level,
    get_sustainability_score,
)


# ============================================================
# TEST PAYLOAD
# ============================================================


def make_payload(**overrides):
    """
    Build one complete valid EcoShield assessment payload.

    Individual tests override only the fields relevant to the
    sustainability rule being tested.
    """

    payload = {
        "device_type": "Laptop",
        "operating_system": "Windows",
        "device_age": 3,
        "device_condition": "Working",
        "storage_type": "SSD",
        "storage_capacity": 512,
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
        "intended_disposal_method": "Reuse",
    }

    payload.update(overrides)

    return payload


def factor_codes(result):
    """
    Return factor codes for concise assertions.
    """

    return {
        factor.code
        for factor in result.factors
    }


# ============================================================
# RESULT CONTRACT
# ============================================================


def test_assessment_returns_sustainability_result():
    result = assess_sustainability(
        make_payload()
    )

    assert isinstance(
        result,
        SustainabilityImpactResult,
    )


def test_result_contains_complete_contract():
    result = assess_sustainability(
        make_payload()
    )

    assert isinstance(result.score, int)
    assert isinstance(result.opportunity_level, str)
    assert isinstance(result.preferred_action, str)

    assert isinstance(
        result.lifecycle_extension_potential,
        str,
    )

    assert isinstance(
        result.reuse_potential,
        str,
    )

    assert isinstance(
        result.repair_potential,
        str,
    )

    assert isinstance(
        result.recycling_priority,
        str,
    )

    assert isinstance(result.factors, tuple)
    assert isinstance(result.category_scores, dict)
    assert isinstance(result.uncertainties, tuple)
    assert isinstance(result.validated_data, dict)
    assert isinstance(result.summary, str)


def test_result_dataclass_is_frozen():
    result = assess_sustainability(
        make_payload()
    )

    with pytest.raises(FrozenInstanceError):
        result.score = 99


def test_factor_dataclass_is_frozen():
    factor = SustainabilityFactor(
        code="TEST",
        category=CATEGORY_LIFECYCLE_EXTENSION,
        points=1,
        message="Test factor.",
    )

    with pytest.raises(FrozenInstanceError):
        factor.points = 2


# ============================================================
# SCORE BOUNDARIES
# ============================================================


@pytest.mark.parametrize(
    (
        "score",
        "expected",
    ),
    (
        (-50, OPPORTUNITY_LOW),
        (0, OPPORTUNITY_LOW),
        (24, OPPORTUNITY_LOW),
        (25, OPPORTUNITY_MODERATE),
        (49, OPPORTUNITY_MODERATE),
        (50, OPPORTUNITY_HIGH),
        (74, OPPORTUNITY_HIGH),
        (75, OPPORTUNITY_VERY_HIGH),
        (100, OPPORTUNITY_VERY_HIGH),
        (150, OPPORTUNITY_VERY_HIGH),
    ),
)
def test_opportunity_level_boundaries(
    score,
    expected,
):
    assert (
        get_sustainability_opportunity_level(
            score
        )
        == expected
    )


def test_score_always_within_zero_to_one_hundred():
    result = assess_sustainability(
        make_payload()
    )

    assert (
        MIN_SUSTAINABILITY_SCORE
        <= result.score
        <= MAX_SUSTAINABILITY_SCORE
    )


# ============================================================
# CATEGORY CONTRACT
# ============================================================


def test_result_contains_all_four_categories():
    result = assess_sustainability(
        make_payload()
    )

    assert set(
        result.category_scores
    ) == {
        CATEGORY_LIFECYCLE_EXTENSION,
        CATEGORY_REUSE_POTENTIAL,
        CATEGORY_REPAIR_POTENTIAL,
        CATEGORY_END_OF_LIFE,
    }


def test_each_category_respects_maximum():
    result = assess_sustainability(
        make_payload(
            device_age=12,
        )
    )

    for category, score in (
        result.category_scores.items()
    ):
        assert score >= 0

        assert (
            score
            <= CATEGORY_MAX_SCORES[
                category
            ]
        )


def test_total_score_equals_category_sum():
    result = assess_sustainability(
        make_payload()
    )

    assert result.score == sum(
        result.category_scores.values()
    )


# ============================================================
# WORKING DEVICE
# ============================================================


def test_working_reuse_device_has_expected_score():
    result = assess_sustainability(
        make_payload(
            device_condition="Working",
            intended_disposal_method="Reuse",
        )
    )

    assert result.score == 63
    assert result.opportunity_level == OPPORTUNITY_HIGH


def test_working_reuse_device_has_high_lifecycle_potential():
    result = assess_sustainability(
        make_payload(
            device_condition="Working",
            intended_disposal_method="Reuse",
        )
    )

    assert (
        result.lifecycle_extension_potential
        == POTENTIAL_HIGH
    )


def test_working_reuse_device_has_high_reuse_potential():
    result = assess_sustainability(
        make_payload(
            intended_disposal_method="Reuse",
        )
    )

    assert (
        result.reuse_potential
        == POTENTIAL_HIGH
    )


def test_working_device_recycling_priority_is_low():
    result = assess_sustainability(
        make_payload(
            device_condition="Working",
        )
    )

    assert (
        result.recycling_priority
        == POTENTIAL_LOW
    )


def test_working_device_contains_working_factor():
    result = assess_sustainability(
        make_payload()
    )

    assert (
        "WORKING_DEVICE"
        in factor_codes(result)
    )


def test_power_on_adds_lifecycle_factor():
    result = assess_sustainability(
        make_payload(
            can_power_on="Yes",
        )
    )

    assert (
        "DEVICE_POWERS_ON"
        in factor_codes(result)
    )


def test_accessible_device_adds_evaluation_factor():
    result = assess_sustainability(
        make_payload(
            device_accessible="Yes",
        )
    )

    assert (
        "DEVICE_ACCESSIBLE_FOR_EVALUATION"
        in factor_codes(result)
    )


# ============================================================
# PREFERRED ACTION — WORKING DEVICE
# ============================================================


@pytest.mark.parametrize(
    (
        "intended_action",
        "expected",
    ),
    (
        ("Reuse", ACTION_REUSE),
        ("Sell", ACTION_SELL),
        ("Donate", ACTION_DONATE),
        ("Repair", ACTION_CONTINUE_USE),
        ("Recycle", ACTION_CONTINUE_USE),
        ("Dispose", ACTION_CONTINUE_USE),
        ("Not Decided", ACTION_CONTINUE_USE),
    ),
)
def test_working_device_preferred_action(
    intended_action,
    expected,
):
    result = assess_sustainability(
        make_payload(
            device_condition="Working",
            intended_disposal_method=(
                intended_action
            ),
        )
    )

    assert result.preferred_action == expected


# ============================================================
# REUSE / SELL / DONATE
# ============================================================


@pytest.mark.parametrize(
    "action",
    (
        "Reuse",
        "Sell",
        "Donate",
    ),
)
def test_reuse_path_selected_factor(
    action,
):
    result = assess_sustainability(
        make_payload(
            intended_disposal_method=action,
        )
    )

    assert (
        "REUSE_PATH_SELECTED"
        in factor_codes(result)
    )


def test_recycling_does_not_add_reuse_path_factor():
    result = assess_sustainability(
        make_payload(
            intended_disposal_method="Recycle",
        )
    )

    assert (
        "REUSE_PATH_SELECTED"
        not in factor_codes(result)
    )


# ============================================================
# PARTIALLY WORKING DEVICE
# ============================================================


def test_partial_device_prefers_repair():
    result = assess_sustainability(
        make_payload(
            device_condition=(
                "Partially Working"
            ),
            intended_disposal_method="Recycle",
        )
    )

    assert (
        result.preferred_action
        == ACTION_REPAIR
    )


def test_partial_device_has_repair_factor():
    result = assess_sustainability(
        make_payload(
            device_condition=(
                "Partially Working"
            ),
        )
    )

    assert (
        "PARTIAL_DEVICE_REPAIR_OPPORTUNITY"
        in factor_codes(result)
    )


def test_partial_repair_path_has_high_repair_potential():
    result = assess_sustainability(
        make_payload(
            device_condition=(
                "Partially Working"
            ),
            intended_disposal_method="Repair",
        )
    )

    assert (
        result.repair_potential
        == POTENTIAL_HIGH
    )


def test_partial_device_recycling_priority_is_moderate():
    result = assess_sustainability(
        make_payload(
            device_condition=(
                "Partially Working"
            ),
            intended_disposal_method="Recycle",
        )
    )

    assert (
        result.recycling_priority
        == POTENTIAL_MODERATE
    )


def test_repair_selection_adds_repair_path_factor():
    result = assess_sustainability(
        make_payload(
            device_condition=(
                "Partially Working"
            ),
            intended_disposal_method="Repair",
        )
    )

    assert (
        "REPAIR_PATH_SELECTED"
        in factor_codes(result)
    )


# ============================================================
# NOT WORKING / DAMAGED DEVICE
# ============================================================


@pytest.mark.parametrize(
    "condition",
    (
        "Not Working",
        "Physically Damaged",
    ),
)
def test_nonfunctional_device_has_recovery_factor(
    condition,
):
    result = assess_sustainability(
        make_payload(
            device_condition=condition,
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Recycle",
        )
    )

    assert (
        "RECOVERY_POTENTIAL_REMAINS"
        in factor_codes(result)
    )


@pytest.mark.parametrize(
    "condition",
    (
        "Not Working",
        "Physically Damaged",
    ),
)
def test_nonfunctional_recycle_prefers_responsible_recycling(
    condition,
):
    result = assess_sustainability(
        make_payload(
            device_condition=condition,
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Recycle",
        )
    )

    assert (
        result.preferred_action
        == ACTION_RECYCLE
    )


@pytest.mark.parametrize(
    "condition",
    (
        "Not Working",
        "Physically Damaged",
    ),
)
def test_nonfunctional_repair_selection_prefers_repair(
    condition,
):
    result = assess_sustainability(
        make_payload(
            device_condition=condition,
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Repair",
        )
    )

    assert (
        result.preferred_action
        == ACTION_REPAIR
    )


@pytest.mark.parametrize(
    "condition",
    (
        "Not Working",
        "Physically Damaged",
    ),
)
def test_nonfunctional_undecided_path_requires_review(
    condition,
):
    result = assess_sustainability(
        make_payload(
            device_condition=condition,
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method=(
                "Not Decided"
            ),
        )
    )

    assert (
        result.preferred_action
        == ACTION_REVIEW
    )


def test_nonworking_device_has_repairability_review():
    result = assess_sustainability(
        make_payload(
            device_condition="Not Working",
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Recycle",
        )
    )

    assert (
        "NONWORKING_DEVICE_RECOVERY_REVIEW"
        in factor_codes(result)
    )


def test_physically_damaged_device_has_recovery_review():
    result = assess_sustainability(
        make_payload(
            device_condition=(
                "Physically Damaged"
            ),
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Recycle",
        )
    )

    assert (
        "DAMAGED_DEVICE_RECOVERY_REVIEW"
        in factor_codes(result)
    )


# ============================================================
# END-OF-LIFE RESPONSIBILITY
# ============================================================


def test_recycle_selection_adds_recycling_factor():
    result = assess_sustainability(
        make_payload(
            intended_disposal_method="Recycle",
        )
    )

    assert (
        "RECYCLING_PATH_SELECTED"
        in factor_codes(result)
    )


def test_general_disposal_adds_ewaste_review_factor():
    result = assess_sustainability(
        make_payload(
            intended_disposal_method="Dispose",
        )
    )

    assert (
        "DISPOSAL_REQUIRES_EWASTE_REVIEW"
        in factor_codes(result)
    )


def test_nonpowering_end_of_life_category_respects_cap():
    result = assess_sustainability(
        make_payload(
            device_condition="Not Working",
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Recycle",
        )
    )

    assert (
        result.category_scores[
            CATEGORY_END_OF_LIFE
        ]
        == CATEGORY_MAX_SCORES[
            CATEGORY_END_OF_LIFE
        ]
    )

    assert (
        "END_OF_LIFE_REVIEW_RELEVANT"
        in factor_codes(result)
    )

    assert (
        "RECYCLING_PATH_SELECTED"
        in factor_codes(result)
    )


# ============================================================
# DEVICE AGE
# ============================================================


def test_older_working_device_keeps_max_lifecycle_value():
    result = assess_sustainability(
        make_payload(
            device_age=6,
            device_condition="Working",
        )
    )

    assert (
        result.category_scores[
            CATEGORY_LIFECYCLE_EXTENSION
        ]
        == CATEGORY_MAX_SCORES[
            CATEGORY_LIFECYCLE_EXTENSION
        ]
    )

    assert (
        result.lifecycle_extension_potential
        == POTENTIAL_HIGH
    )

    assert (
        result.preferred_action
        == ACTION_REUSE
    )


def test_young_working_device_has_no_older_device_factor():
    result = assess_sustainability(
        make_payload(
            device_age=3,
        )
    )

    assert (
        "OLDER_WORKING_DEVICE_LIFECYCLE_VALUE"
        not in factor_codes(result)
    )


def test_very_old_nonworking_device_respects_eol_cap():
    result = assess_sustainability(
        make_payload(
            device_age=10,
            device_condition="Not Working",
            can_power_on="No",
            device_accessible="No",
            intended_disposal_method="Recycle",
        )
    )

    assert (
        result.category_scores[
            CATEGORY_END_OF_LIFE
        ]
        == CATEGORY_MAX_SCORES[
            CATEGORY_END_OF_LIFE
        ]
    )

    assert (
        result.preferred_action
        == ACTION_RECYCLE
    )

    assert (
        result.recycling_priority
        == POTENTIAL_HIGH
    )


def test_age_alone_does_not_force_recycling():
    result = assess_sustainability(
        make_payload(
            device_age=12,
            device_condition="Working",
            intended_disposal_method="Reuse",
        )
    )

    assert (
        result.preferred_action
        == ACTION_REUSE
    )


# ============================================================
# UNCERTAINTY
# ============================================================


def test_not_decided_action_is_reported_as_uncertainty():
    result = assess_sustainability(
        make_payload(
            intended_disposal_method=(
                "Not Decided"
            ),
        )
    )

    assert (
        "intended_disposal_method"
        in result.uncertainties
    )


def test_fully_known_payload_has_no_sustainability_uncertainty():
    result = assess_sustainability(
        make_payload()
    )

    assert result.uncertainties == ()


# ============================================================
# EXPLAINABILITY
# ============================================================


def test_every_factor_has_valid_content():
    result = assess_sustainability(
        make_payload()
    )

    assert result.factors

    for factor in result.factors:

        assert factor.code
        assert factor.category
        assert factor.message
        assert factor.points > 0


def test_every_factor_category_is_known():
    result = assess_sustainability(
        make_payload()
    )

    for factor in result.factors:

        assert (
            factor.category
            in CATEGORY_MAX_SCORES
        )


def test_factor_codes_are_unique():
    result = assess_sustainability(
        make_payload(
            device_age=12,
        )
    )

    codes = [
        factor.code
        for factor in result.factors
    ]

    assert len(codes) == len(
        set(codes)
    )


# ============================================================
# SUMMARY
# ============================================================


def test_summary_contains_score():
    result = assess_sustainability(
        make_payload()
    )

    assert (
        f"{result.score}/100"
        in result.summary
    )


def test_summary_contains_opportunity_level():
    result = assess_sustainability(
        make_payload()
    )

    assert (
        result.opportunity_level
        in result.summary
    )


def test_summary_contains_preferred_action():
    result = assess_sustainability(
        make_payload()
    )

    assert (
        result.preferred_action
        in result.summary
    )


def test_summary_does_not_claim_carbon_footprint():
    result = assess_sustainability(
        make_payload()
    )

    assert (
        "not a carbon-footprint"
        in result.summary.lower()
    )


# ============================================================
# VALIDATED DATA
# ============================================================


def test_result_preserves_validated_device_data():
    payload = make_payload(
        device_age=4,
        intended_disposal_method="Donate",
    )

    result = assess_sustainability(
        payload
    )

    assert (
        result.validated_data[
            "device_condition"
        ]
        == "Working"
    )

    assert (
        result.validated_data[
            "intended_disposal_method"
        ]
        == "Donate"
    )


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================


def test_get_sustainability_score_matches_full_result():
    payload = make_payload()

    result = assess_sustainability(
        payload
    )

    assert (
        get_sustainability_score(
            payload
        )
        == result.score
    )


def test_get_preferred_action_matches_full_result():
    payload = make_payload(
        intended_disposal_method="Donate",
    )

    result = assess_sustainability(
        payload
    )

    assert (
        get_preferred_sustainable_action(
            payload
        )
        == result.preferred_action
    )


# ============================================================
# SERIALIZATION
# ============================================================


def test_to_dict_returns_complete_serializable_mapping():
    result = assess_sustainability(
        make_payload()
    )

    data = result.to_dict()

    assert data["score"] == result.score

    assert (
        data["opportunity_level"]
        == result.opportunity_level
    )

    assert (
        data["preferred_action"]
        == result.preferred_action
    )

    assert (
        data["category_scores"]
        == result.category_scores
    )

    assert isinstance(
        data["factors"],
        tuple,
    )


# ============================================================
# DETERMINISM
# ============================================================


def test_same_payload_produces_same_result():
    payload = make_payload(
        device_condition=(
            "Partially Working"
        ),
        intended_disposal_method="Repair",
    )

    first = assess_sustainability(
        payload
    )

    second = assess_sustainability(
        payload
    )

    assert first == second


# ============================================================
# CYBERSECURITY INDEPENDENCE
# ============================================================


def test_security_status_does_not_change_sustainability_direction():
    secure_payload = make_payload(
        intended_disposal_method="Sell",
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        secure_erase_performed="Yes",
        factory_reset_performed="Yes",
        accounts_signed_out="Yes",
    )

    insecure_payload = make_payload(
        intended_disposal_method="Sell",
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        secure_erase_performed="No",
        factory_reset_performed="No",
        accounts_signed_out="No",
    )

    secure = assess_sustainability(
        secure_payload
    )

    insecure = assess_sustainability(
        insecure_payload
    )

    assert (
        secure.preferred_action
        == ACTION_SELL
    )

    assert (
        insecure.preferred_action
        == ACTION_SELL
    )

    assert secure.score == insecure.score


# ============================================================
# INPUT VALIDATION
# ============================================================


@pytest.mark.parametrize(
    "invalid_payload",
    (
        None,
        123,
        "Laptop",
        ["Laptop"],
    ),
)
def test_non_mapping_input_is_rejected(
    invalid_payload,
):
    with pytest.raises(TypeError):
        assess_sustainability(
            invalid_payload
        )


def test_invalid_assessment_payload_is_rejected():
    payload = make_payload()

    payload[
        "device_condition"
    ] = "Completely Magical"

    with pytest.raises(ValueError):
        assess_sustainability(
            payload
        )