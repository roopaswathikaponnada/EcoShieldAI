"""
EcoShield AI
Cybersecurity Risk Engine Tests

Tests for src.risk_engine.

The suite verifies:
- Low / Medium / High risk behavior
- Deterministic 0-100 scoring
- Category score limits
- Major cybersecurity risk factors
- Disposal / transfer behavior
- Accessibility and condition risks
- Backup / removable-media risks
- Sanitization requirement flag
- Ownership-transfer flag
- Uncertainty collection
- Invalid input rejection
- Convenience functions
- Serializable result structure
- Repeatability of risk scoring
"""

import pytest

from config.config import (
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
)

from src.risk_engine import (
    CATEGORY_ACCESSIBILITY,
    CATEGORY_DATA_EXPOSURE,
    CATEGORY_MAX_SCORES,
    CATEGORY_MEDIA_BACKUP,
    CATEGORY_SANITIZATION,
    CATEGORY_TRANSFER,
    MAX_RISK_SCORE,
    MEDIUM_RISK_MAX,
    MIN_RISK_SCORE,
    LOW_RISK_MAX,
    RiskAssessment,
    RiskFactor,
    assess_device_risk,
    get_risk_level,
    get_risk_score,
)

from src.validators import (
    FIELD_ACCOUNTS_SIGNED_OUT,
    FIELD_DATA_BACKED_UP,
    FIELD_DEVICE_ACCESSIBLE,
    FIELD_DEVICE_AGE,
    FIELD_DEVICE_CONDITION,
    FIELD_DEVICE_TYPE,
    FIELD_DISPOSAL_METHOD,
    FIELD_ENCRYPTION,
    FIELD_FACTORY_RESET,
    FIELD_OPERATING_SYSTEM,
    FIELD_PERSONAL_DATA,
    FIELD_POWER_ON,
    FIELD_REMOVABLE_MEDIA_REMOVED,
    FIELD_SECURE_ERASE,
    FIELD_SENSITIVE_DATA,
    FIELD_STORAGE_CAPACITY,
    FIELD_STORAGE_TYPE,
)


# ============================================================
# TEST DATA FACTORY
# ============================================================

def make_base_payload(**overrides):
    """
    Return a complete, low-risk laptop assessment.

    Tests override only the values relevant to the scenario.
    """

    payload = {
        FIELD_DEVICE_TYPE: "Laptop",
        FIELD_OPERATING_SYSTEM: "Windows",
        FIELD_DEVICE_AGE: 2,
        FIELD_DEVICE_CONDITION: "Working",
        FIELD_STORAGE_TYPE: "SSD",
        FIELD_STORAGE_CAPACITY: "512 GB",
        FIELD_PERSONAL_DATA: "No",
        FIELD_SENSITIVE_DATA: "No",
        FIELD_DEVICE_ACCESSIBLE: "Yes",
        FIELD_POWER_ON: "Yes",
        FIELD_DATA_BACKED_UP: "Not Required",
        FIELD_FACTORY_RESET: "Yes",
        FIELD_SECURE_ERASE: "Yes",
        FIELD_ENCRYPTION: "Yes",
        FIELD_ACCOUNTS_SIGNED_OUT: "Yes",
        FIELD_REMOVABLE_MEDIA_REMOVED: "Not Applicable",
        FIELD_DISPOSAL_METHOD: "Reuse",
    }

    payload.update(overrides)

    return payload


# ============================================================
# BASIC RESULT TESTS
# ============================================================

def test_assessment_returns_risk_assessment():
    """Risk engine should return a RiskAssessment object."""

    result = assess_device_risk(
        make_base_payload()
    )

    assert isinstance(
        result,
        RiskAssessment,
    )


def test_low_risk_baseline():
    """Safe internal reuse should remain low risk."""

    result = assess_device_risk(
        make_base_payload()
    )

    assert result.score == 2

    assert result.risk_level == RISK_LOW

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 2


def test_high_risk_transfer_scenario():
    """Sensitive, unsanitized device sale should be high risk."""

    payload = make_base_payload(
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        data_backed_up="Yes",
        factory_reset_performed="No",
        secure_erase_performed="No",
        encryption_enabled="No",
        accounts_signed_out="No",
        intended_disposal_method="Sell",
    )

    result = assess_device_risk(
        payload
    )

    assert result.score == 80

    assert result.risk_level == RISK_HIGH

    assert result.category_scores[
        CATEGORY_DATA_EXPOSURE
    ] == 35

    assert result.category_scores[
        CATEGORY_SANITIZATION
    ] == 30

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 15


# ============================================================
# SCORE RANGE TESTS
# ============================================================

@pytest.mark.parametrize(
    "payload",
    [
        make_base_payload(),

        make_base_payload(
            contains_personal_data="Yes"
        ),

        make_base_payload(
            contains_sensitive_data="Yes",
            encryption_enabled="No",
            secure_erase_performed="No",
            intended_disposal_method="Donate",
        ),

        make_base_payload(
            device_condition="Physically Damaged",
            device_accessible="No",
            can_power_on="No",
            intended_disposal_method="Recycle",
        ),
    ],
)
def test_score_always_stays_within_range(payload):
    """Final scores must remain between 0 and 100."""

    result = assess_device_risk(
        payload
    )

    assert (
        MIN_RISK_SCORE
        <= result.score
        <= MAX_RISK_SCORE
    )


# ============================================================
# CATEGORY SCORE CAP TESTS
# ============================================================

def test_category_scores_do_not_exceed_caps():
    """No category may exceed its configured maximum."""

    payload = make_base_payload(
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        encryption_enabled="No",
        factory_reset_performed="No",
        secure_erase_performed="No",
        accounts_signed_out="No",
        intended_disposal_method="Sell",
        device_condition="Physically Damaged",
        device_accessible="No",
        can_power_on="No",
        data_backed_up="No",
        sim_memory_card_removed="No",
        storage_type="Unknown",
    )

    result = assess_device_risk(
        payload
    )

    for category, score in (
        result.category_scores.items()
    ):

        assert (
            score
            <= CATEGORY_MAX_SCORES[
                category
            ]
        )


def test_total_category_maximum_is_100():
    """Configured category maxima should total exactly 100."""

    assert sum(
        CATEGORY_MAX_SCORES.values()
    ) == 100


# ============================================================
# RISK LEVEL BOUNDARY TESTS
# ============================================================

def test_low_risk_boundary_configuration():
    """Low-risk upper boundary should be below medium."""

    assert LOW_RISK_MAX < MEDIUM_RISK_MAX


def test_low_risk_result_is_within_low_boundary():
    """Baseline Low score must sit inside Low range."""

    result = assess_device_risk(
        make_base_payload()
    )

    assert result.score <= LOW_RISK_MAX

    assert result.risk_level == RISK_LOW


def test_medium_risk_scenario():
    """A moderately exposed device should score Medium."""

    payload = make_base_payload(
        contains_personal_data="Yes",
        secure_erase_performed="No",
        intended_disposal_method="Repair",
    )

    result = assess_device_risk(
        payload
    )

    assert (
        LOW_RISK_MAX
        < result.score
        <= MEDIUM_RISK_MAX
    )

    assert result.risk_level == RISK_MEDIUM


def test_high_risk_result_is_above_medium_boundary():
    """High-risk scenario must exceed Medium threshold."""

    payload = make_base_payload(
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        encryption_enabled="No",
        factory_reset_performed="No",
        secure_erase_performed="No",
        accounts_signed_out="No",
        intended_disposal_method="Sell",
    )

    result = assess_device_risk(
        payload
    )

    assert result.score > MEDIUM_RISK_MAX

    assert result.risk_level == RISK_HIGH


# ============================================================
# DATA EXPOSURE FACTOR TESTS
# ============================================================

def test_personal_data_adds_risk_factor():
    """Known personal data should create a risk factor."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "PERSONAL_DATA_PRESENT" in codes


def test_sensitive_data_adds_risk_factor():
    """Known sensitive data should create a risk factor."""

    result = assess_device_risk(
        make_base_payload(
            contains_sensitive_data="Yes"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "SENSITIVE_DATA_PRESENT" in codes


def test_unencrypted_data_adds_risk_factor():
    """Data present without encryption should increase risk."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            encryption_enabled="No",
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "ENCRYPTION_DISABLED" in codes


def test_encryption_disabled_without_data_does_not_add_factor():
    """No data means encryption state alone should not add exposure."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="No",
            contains_sensitive_data="No",
            encryption_enabled="No",
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "ENCRYPTION_DISABLED" not in codes


# ============================================================
# SANITIZATION FACTOR TESTS
# ============================================================

def test_secure_erase_not_performed_adds_factor_when_data_exists():
    """Missing secure erase should matter when data may exist."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            secure_erase_performed="No",
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert (
        "SECURE_ERASE_NOT_PERFORMED"
        in codes
    )


def test_factory_reset_not_performed_adds_factor():
    """Missing factory reset should add sanitization risk."""

    result = assess_device_risk(
        make_base_payload(
            factory_reset_performed="No"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert (
        "FACTORY_RESET_NOT_PERFORMED"
        in codes
    )


def test_accounts_not_signed_out_adds_factor():
    """Signed-in accounts should add sanitization risk."""

    result = assess_device_risk(
        make_base_payload(
            accounts_signed_out="No"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "ACCOUNTS_NOT_SIGNED_OUT" in codes


# ============================================================
# DISPOSAL / TRANSFER TESTS
# ============================================================

@pytest.mark.parametrize(
    "method",
    [
        "Sell",
        "Donate",
    ],
)
def test_sell_and_donate_are_high_transfer_actions(method):
    """Sell and Donate should receive maximum transfer score."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method=method
        )
    )

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 15

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "OWNERSHIP_TRANSFER" in codes


@pytest.mark.parametrize(
    "method",
    [
        "Recycle",
        "Dispose",
    ],
)
def test_final_disposal_actions_add_transfer_risk(method):
    """Recycle and Dispose should add final-disposal risk."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method=method
        )
    )

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 12

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "FINAL_DISPOSAL" in codes


def test_repair_adds_third_party_risk():
    """Repair may expose the device to a third party."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method="Repair"
        )
    )

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 8

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "THIRD_PARTY_REPAIR" in codes


def test_reuse_has_small_residual_transfer_score():
    """Reuse should carry only small residual preparation risk."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method="Reuse"
        )
    )

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 2


def test_not_decided_adds_uncertainty_transfer_score():
    """Undecided disposal should add limited transfer risk."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method="Not Decided"
        )
    )

    assert result.category_scores[
        CATEGORY_TRANSFER
    ] == 5

    assert (
        "Disposal method: Not Decided"
        in result.uncertainties
    )


# ============================================================
# ACCESSIBILITY / CONDITION TESTS
# ============================================================

def test_inaccessible_device_adds_factor():
    """Inaccessible device should add accessibility risk."""

    result = assess_device_risk(
        make_base_payload(
            device_condition="Partially Working",
            device_accessible="No",
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "DEVICE_INACCESSIBLE" in codes


def test_device_that_cannot_power_on_adds_factor():
    """Power failure should add accessibility risk."""

    result = assess_device_risk(
        make_base_payload(
            device_condition="Not Working",
            can_power_on="No",
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "DEVICE_CANNOT_POWER_ON" in codes


def test_physically_damaged_device_adds_factor():
    """Physical damage should add an accessibility factor."""

    result = assess_device_risk(
        make_base_payload(
            device_condition="Physically Damaged"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "PHYSICAL_DAMAGE" in codes


# ============================================================
# MEDIA / BACKUP TESTS
# ============================================================

def test_removable_media_present_adds_factor():
    """Unremoved SIM/memory card should add risk."""

    result = assess_device_risk(
        make_base_payload(
            sim_memory_card_removed="No"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "REMOVABLE_MEDIA_PRESENT" in codes


def test_backup_not_completed_adds_factor_when_data_exists():
    """Data without backup should add media/backup risk."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            data_backed_up="No",
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "BACKUP_NOT_COMPLETED" in codes


def test_unknown_storage_adds_factor():
    """Unknown storage technology should add uncertainty risk."""

    result = assess_device_risk(
        make_base_payload(
            storage_type="Unknown"
        )
    )

    codes = {
        factor.code
        for factor in result.factors
    }

    assert "STORAGE_TYPE_UNKNOWN" in codes


# ============================================================
# SANITIZATION FLAG TESTS
# ============================================================

def test_requires_sanitization_true_for_unsanitized_data():
    """Data + unfinished controls should require sanitization."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            secure_erase_performed="No",
        )
    )

    assert result.requires_sanitization is True


def test_requires_sanitization_false_when_no_data_present():
    """No known/uncertain data should not trigger flag."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="No",
            contains_sensitive_data="No",
            secure_erase_performed="No",
            factory_reset_performed="No",
            accounts_signed_out="No",
        )
    )

    assert result.requires_sanitization is False


def test_requires_sanitization_false_when_controls_complete():
    """Data can remain low preparation risk if controls complete."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            secure_erase_performed="Yes",
            factory_reset_performed="Yes",
            accounts_signed_out="Yes",
            sim_memory_card_removed="Not Applicable",
        )
    )

    assert result.requires_sanitization is False


# ============================================================
# DEVICE LEAVES OWNER FLAG TESTS
# ============================================================

@pytest.mark.parametrize(
    "method",
    [
        "Sell",
        "Donate",
        "Recycle",
        "Dispose",
    ],
)
def test_device_leaves_owner_true_for_external_actions(method):
    """Configured external-control actions should set flag."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method=method
        )
    )

    assert result.device_leaves_owner is True


@pytest.mark.parametrize(
    "method",
    [
        "Reuse",
        "Repair",
        "Not Decided",
    ],
)
def test_device_leaves_owner_false_for_other_actions(method):
    """Non-final ownership actions should not set flag."""

    result = assess_device_risk(
        make_base_payload(
            intended_disposal_method=method
        )
    )

    assert result.device_leaves_owner is False


# ============================================================
# UNCERTAINTY TESTS
# ============================================================

def test_uncertain_values_are_collected():
    """Unsure/Unknown values should be exposed explicitly."""

    payload = make_base_payload(
        operating_system="Unknown",
        storage_type="Unknown",
        contains_personal_data="Unsure",
        contains_sensitive_data="Unsure",
        data_backed_up="Unsure",
        factory_reset_performed="Unsure",
        secure_erase_performed="Unsure",
        encryption_enabled="Unsure",
        accounts_signed_out="Unsure",
        sim_memory_card_removed="Unsure",
        intended_disposal_method="Not Decided",
    )

    result = assess_device_risk(
        payload
    )

    assert len(
        result.uncertainties
    ) >= 10

    assert (
        "Operating system: Unknown"
        in result.uncertainties
    )

    assert (
        "Sensitive data: Unsure"
        in result.uncertainties
    )

    assert (
        "Disposal method: Not Decided"
        in result.uncertainties
    )


def test_no_uncertainties_for_known_values():
    """Known assessment values should produce no uncertainty list."""

    result = assess_device_risk(
        make_base_payload()
    )

    assert result.uncertainties == ()


# ============================================================
# RISK FACTOR STRUCTURE TESTS
# ============================================================

def test_risk_factors_have_valid_structure():
    """Each risk factor should be a structured RiskFactor."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes"
        )
    )

    assert len(
        result.factors
    ) > 0

    for factor in result.factors:

        assert isinstance(
            factor,
            RiskFactor,
        )

        assert factor.code

        assert factor.category

        assert factor.points > 0

        assert factor.message


def test_risk_factor_codes_are_unique():
    """The same factor code should not appear twice."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            contains_sensitive_data="Yes",
            encryption_enabled="No",
            factory_reset_performed="No",
            secure_erase_performed="No",
            accounts_signed_out="No",
            intended_disposal_method="Sell",
        )
    )

    codes = [
        factor.code
        for factor in result.factors
    ]

    assert len(codes) == len(set(codes))


# ============================================================
# SERIALIZATION TESTS
# ============================================================

def test_to_dict_returns_serializable_structure():
    """RiskAssessment.to_dict should expose stable fields."""

    result = assess_device_risk(
        make_base_payload()
    )

    data = result.to_dict()

    assert isinstance(
        data,
        dict,
    )

    assert data["score"] == result.score

    assert (
        data["risk_level"]
        == result.risk_level
    )

    assert "factors" in data

    assert "category_scores" in data

    assert "uncertainties" in data

    assert "validated_data" in data

    assert "requires_sanitization" in data

    assert "device_leaves_owner" in data


# ============================================================
# CONVENIENCE FUNCTION TESTS
# ============================================================

def test_get_risk_score_matches_full_assessment():
    """Score convenience function should match main engine."""

    payload = make_base_payload(
        contains_personal_data="Yes"
    )

    result = assess_device_risk(
        payload
    )

    assert (
        get_risk_score(payload)
        == result.score
    )


def test_get_risk_level_matches_full_assessment():
    """Level convenience function should match main engine."""

    payload = make_base_payload(
        contains_sensitive_data="Yes"
    )

    result = assess_device_risk(
        payload
    )

    assert (
        get_risk_level(payload)
        == result.risk_level
    )


# ============================================================
# INVALID INPUT TESTS
# ============================================================

@pytest.mark.parametrize(
    "payload",
    [
        None,
        [],
        "invalid",
        123,
        3.14,
    ],
)
def test_non_mapping_payloads_are_rejected(payload):
    """Non-mapping inputs should fail defensively."""

    with pytest.raises(TypeError):
        assess_device_risk(payload)


def test_invalid_device_assessment_raises_value_error():
    """Validated-but-invalid assessments must not be scored."""

    with pytest.raises(
        ValueError,
        match="validation failed",
    ):

        assess_device_risk(
            {
                FIELD_DEVICE_TYPE: "Invalid",
            }
        )


# ============================================================
# VALIDATED DATA TESTS
# ============================================================

def test_risk_engine_returns_normalized_validated_data():
    """Assessment should expose validator-normalized values."""

    payload = make_base_payload(
        device_type=" laptop ",
        storage_capacity="1 TB",
    )

    result = assess_device_risk(
        payload
    )

    assert (
        result.validated_data[
            FIELD_DEVICE_TYPE
        ]
        == "Laptop"
    )

    assert (
        result.validated_data[
            FIELD_STORAGE_CAPACITY
        ]
        == 1024.0
    )


# ============================================================
# DETERMINISTIC BEHAVIOR TESTS
# ============================================================

def test_identical_input_always_returns_identical_score():
    """Risk engine must be deterministic."""

    payload = make_base_payload(
        contains_personal_data="Yes",
        contains_sensitive_data="Yes",
        encryption_enabled="No",
        secure_erase_performed="No",
        intended_disposal_method="Donate",
    )

    first = assess_device_risk(
        payload
    )

    second = assess_device_risk(
        payload
    )

    assert first.score == second.score

    assert (
        first.risk_level
        == second.risk_level
    )

    assert (
        first.category_scores
        == second.category_scores
    )

    assert first.factors == second.factors


# ============================================================
# CATEGORY CONSISTENCY TEST
# ============================================================

def test_final_score_equals_sum_of_category_scores():
    """Final score should equal summed category contributions."""

    result = assess_device_risk(
        make_base_payload(
            contains_personal_data="Yes",
            secure_erase_performed="No",
            intended_disposal_method="Repair",
        )
    )

    assert result.score == sum(
        result.category_scores.values()
    )