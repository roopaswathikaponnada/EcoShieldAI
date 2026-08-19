"""
EcoShield AI
Device Assessment Validation Tests

Tests for src.validators.

The suite verifies:
- Valid device assessments
- Input normalization
- Device age validation
- Storage capacity validation
- Required fields
- Allowed categorical values
- Device/storage compatibility
- Device/OS compatibility
- Logical consistency
- Security warnings
- Malformed input handling
- Convenience validation functions
"""

import pytest

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
    ValidationResult,
    is_device_input_valid,
    normalize_device_input,
    validate_device_input,
)


# ============================================================
# TEST DATA FACTORY
# ============================================================

def make_valid_laptop_payload(**overrides):
    """
    Return a complete valid laptop assessment.

    Individual tests can override only the fields they need.
    """

    payload = {
        FIELD_DEVICE_TYPE: "Laptop",
        FIELD_OPERATING_SYSTEM: "Windows",
        FIELD_DEVICE_AGE: 3,
        FIELD_DEVICE_CONDITION: "Working",
        FIELD_STORAGE_TYPE: "SSD",
        FIELD_STORAGE_CAPACITY: "512 GB",
        FIELD_PERSONAL_DATA: "Yes",
        FIELD_SENSITIVE_DATA: "No",
        FIELD_DEVICE_ACCESSIBLE: "Yes",
        FIELD_POWER_ON: "Yes",
        FIELD_DATA_BACKED_UP: "Yes",
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
# BASIC VALID ASSESSMENT TESTS
# ============================================================

def test_valid_laptop_assessment():
    """A complete valid laptop assessment should pass."""

    payload = make_valid_laptop_payload()

    result = validate_device_input(payload)

    assert isinstance(result, ValidationResult)

    assert result.is_valid is True

    assert result.errors == ()

    assert result.data[FIELD_DEVICE_TYPE] == "Laptop"

    assert result.data[FIELD_DEVICE_AGE] == 3.0

    assert result.data[FIELD_STORAGE_CAPACITY] == 512.0


def test_boolean_convenience_function_for_valid_input():
    """Convenience validator should return True."""

    payload = make_valid_laptop_payload()

    assert is_device_input_valid(payload) is True


# ============================================================
# NORMALIZATION TESTS
# ============================================================

def test_categorical_values_are_normalized_case_insensitively():
    """Supported categorical values should be canonicalized."""

    payload = make_valid_laptop_payload(
        device_type="  laptop  ",
        operating_system="WINDOWS",
        device_condition=" working ",
        storage_type="ssd",
        contains_personal_data="yes",
        contains_sensitive_data="NO",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert result.data[FIELD_DEVICE_TYPE] == "Laptop"

    assert result.data[FIELD_OPERATING_SYSTEM] == "Windows"

    assert result.data[FIELD_DEVICE_CONDITION] == "Working"

    assert result.data[FIELD_STORAGE_TYPE] == "SSD"

    assert result.data[FIELD_PERSONAL_DATA] == "Yes"

    assert result.data[FIELD_SENSITIVE_DATA] == "No"


def test_extra_fields_are_ignored():
    """Unexpected input fields should not enter normalized data."""

    payload = make_valid_laptop_payload()

    payload["unexpected_field"] = "should be ignored"

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert "unexpected_field" not in result.data


# ============================================================
# DEVICE AGE NORMALIZATION
# ============================================================

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (0, 0.0),
        (3, 3.0),
        (3.5, 3.5),
        ("4", 4.0),
        ("4.5", 4.5),
        ("5 years", 5.0),
        ("6 year", 6.0),
        ("7 yrs", 7.0),
        ("8 yr", 8.0),
    ],
)
def test_valid_device_age_formats(value, expected):
    """Supported device-age formats should normalize to years."""

    payload = make_valid_laptop_payload(
        device_age=value
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert result.data[FIELD_DEVICE_AGE] == expected


def test_missing_device_age_is_invalid():
    """Device age is required."""

    payload = make_valid_laptop_payload(
        device_age=None
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert "Device age is required." in result.errors


@pytest.mark.parametrize(
    "value",
    [
        "",
        "abc",
        "three years",
        "3 months",
        "3.5.2",
    ],
)
def test_invalid_device_age_formats(value):
    """Malformed age values should fail validation."""

    payload = make_valid_laptop_payload(
        device_age=value
    )

    result = validate_device_input(payload)

    assert result.is_valid is False


def test_device_age_above_maximum_is_invalid():
    """Age above the configured maximum should fail."""

    payload = make_valid_laptop_payload(
        device_age=51
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert (
        "Device age cannot exceed 50 years."
        in result.errors
    )


# ============================================================
# STORAGE CAPACITY NORMALIZATION
# ============================================================

@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (512, 512.0),
        (256.5, 256.5),
        ("512", 512.0),
        ("512 GB", 512.0),
        ("512gb", 512.0),
        ("1 TB", 1024.0),
        ("1TB", 1024.0),
        ("1.5 TB", 1536.0),
        ("2tb", 2048.0),
    ],
)
def test_valid_storage_capacity_formats(value, expected):
    """Storage capacities should normalize into GB."""

    payload = make_valid_laptop_payload(
        storage_capacity=value
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert (
        result.data[FIELD_STORAGE_CAPACITY]
        == expected
    )


def test_missing_storage_capacity_is_invalid():
    """Storage capacity is required for storage devices."""

    payload = make_valid_laptop_payload(
        storage_capacity=None
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert (
        "Storage capacity is required."
        in result.errors
    )


@pytest.mark.parametrize(
    "value",
    [
        "abc",
        "512 MB",
        "1 PB",
        "500 gigabytes",
    ],
)
def test_invalid_storage_capacity_formats(value):
    """Unsupported storage-capacity formats should fail."""

    payload = make_valid_laptop_payload(
        storage_capacity=value
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert any(
        "Storage capacity must be a numeric value"
        in error
        for error in result.errors
    )


@pytest.mark.parametrize(
    "value",
    [
        0,
        "0",
        "0 GB",
    ],
)
def test_zero_storage_capacity_is_invalid(value):
    """Storage-bearing devices cannot have zero capacity."""

    payload = make_valid_laptop_payload(
        storage_capacity=value
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert (
        "Storage capacity must be greater than zero."
        in result.errors
    )


def test_storage_capacity_above_maximum_is_invalid():
    """Unreasonably large capacity should fail validation."""

    payload = make_valid_laptop_payload(
        storage_capacity="1000001 GB"
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert (
        "Storage capacity exceeds the supported "
        "validation range."
        in result.errors
    )


# ============================================================
# REQUIRED FIELD TESTS
# ============================================================

@pytest.mark.parametrize(
    "field_name",
    [
        FIELD_DEVICE_TYPE,
        FIELD_OPERATING_SYSTEM,
        FIELD_DEVICE_CONDITION,
        FIELD_STORAGE_TYPE,
        FIELD_PERSONAL_DATA,
        FIELD_SENSITIVE_DATA,
        FIELD_DEVICE_ACCESSIBLE,
        FIELD_POWER_ON,
        FIELD_DATA_BACKED_UP,
        FIELD_FACTORY_RESET,
        FIELD_SECURE_ERASE,
        FIELD_ENCRYPTION,
        FIELD_ACCOUNTS_SIGNED_OUT,
        FIELD_REMOVABLE_MEDIA_REMOVED,
        FIELD_DISPOSAL_METHOD,
    ],
)
def test_missing_required_categorical_field_is_invalid(
    field_name,
):
    """Every required categorical field must be supplied."""

    payload = make_valid_laptop_payload()

    payload.pop(field_name)

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert len(result.errors) >= 1


# ============================================================
# INVALID CATEGORICAL VALUE TESTS
# ============================================================

@pytest.mark.parametrize(
    ("field_name", "invalid_value"),
    [
        (FIELD_DEVICE_TYPE, "Gaming Console"),
        (FIELD_OPERATING_SYSTEM, "TempleOS"),
        (FIELD_DEVICE_CONDITION, "Perfect"),
        (FIELD_STORAGE_TYPE, "Cloud Storage"),
        (FIELD_PERSONAL_DATA, "Maybe"),
        (FIELD_SENSITIVE_DATA, "Probably"),
        (FIELD_DEVICE_ACCESSIBLE, "Sometimes"),
        (FIELD_POWER_ON, "Maybe"),
        (FIELD_DATA_BACKED_UP, "Partially"),
        (FIELD_FACTORY_RESET, "Unknown"),
        (FIELD_SECURE_ERASE, "Unknown"),
        (FIELD_ENCRYPTION, "Unknown"),
        (FIELD_ACCOUNTS_SIGNED_OUT, "Unknown"),
        (FIELD_REMOVABLE_MEDIA_REMOVED, "Unknown"),
        (FIELD_DISPOSAL_METHOD, "Throw Away"),
    ],
)
def test_invalid_categorical_values_are_rejected(
    field_name,
    invalid_value,
):
    """Unsupported categorical options must fail validation."""

    payload = make_valid_laptop_payload(
        **{
            field_name: invalid_value,
        }
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert any(
        "Invalid" in error
        for error in result.errors
    )


# ============================================================
# DEVICE / STORAGE RELATIONSHIP TESTS
# ============================================================

def test_laptop_storage_cannot_be_not_applicable():
    """Laptop should have a real or unknown storage type."""

    payload = make_valid_laptop_payload(
        storage_type="Not Applicable",
        storage_capacity=None,
        secure_erase_performed="Not Applicable",
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert any(
        "Laptop normally contains storage"
        in error
        for error in result.errors
    )


@pytest.mark.parametrize(
    "storage_type",
    [
        "HDD",
        "SSD",
        "Hybrid",
        "Unknown",
    ],
)
def test_external_hard_drive_valid_storage_types(
    storage_type,
):
    """External hard drives should accept supported media."""

    payload = make_valid_laptop_payload(
        device_type="External Hard Drive",
        operating_system="Not Applicable",
        storage_type=storage_type,
        accounts_signed_out="Not Applicable",
        sim_memory_card_removed="Not Applicable",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True


def test_external_hard_drive_rejects_flash_storage():
    """External Hard Drive should reject Flash Storage."""

    payload = make_valid_laptop_payload(
        device_type="External Hard Drive",
        operating_system="Not Applicable",
        storage_type="Flash Storage",
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert any(
        "External Hard Drive must use"
        in error
        for error in result.errors
    )


@pytest.mark.parametrize(
    "storage_type",
    [
        "Flash Storage",
        "Unknown",
    ],
)
def test_usb_drive_valid_storage_types(storage_type):
    """USB drives should accept Flash Storage or Unknown."""

    payload = make_valid_laptop_payload(
        device_type="USB Drive",
        operating_system="Not Applicable",
        storage_type=storage_type,
        accounts_signed_out="Not Applicable",
        sim_memory_card_removed="Not Applicable",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True


def test_usb_drive_rejects_hdd():
    """USB Drive should reject HDD storage type."""

    payload = make_valid_laptop_payload(
        device_type="USB Drive",
        operating_system="Not Applicable",
        storage_type="HDD",
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert any(
        "USB Drive should use Flash Storage"
        in error
        for error in result.errors
    )


# ============================================================
# DEVICE / OPERATING SYSTEM TESTS
# ============================================================

@pytest.mark.parametrize(
    "device_type",
    [
        "External Hard Drive",
        "USB Drive",
    ],
)
def test_external_storage_rejects_regular_os(device_type):
    """External storage should not have a normal OS."""

    payload = make_valid_laptop_payload(
        device_type=device_type,
        operating_system="Windows",
        storage_type=(
            "HDD"
            if device_type == "External Hard Drive"
            else "Flash Storage"
        ),
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert any(
        "operating system"
        in error.lower()
        for error in result.errors
    )


# ============================================================
# LOGICAL CONSISTENCY TESTS
# ============================================================

def test_working_device_must_be_able_to_power_on():
    """Working device + cannot power on is contradictory."""

    payload = make_valid_laptop_payload(
        device_condition="Working",
        can_power_on="No",
    )

    result = validate_device_input(payload)

    assert result.is_valid is False

    assert (
        "A device marked as 'Working' cannot also "
        "be marked as unable to power on."
        in result.errors
    )


# ============================================================
# WARNING TESTS
# ============================================================

def test_sensitive_data_without_encryption_generates_warning():
    """Unencrypted sensitive data should generate warning."""

    payload = make_valid_laptop_payload(
        contains_sensitive_data="Yes",
        encryption_enabled="No",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "Sensitive data is present"
        in warning
        for warning in result.warnings
    )


def test_personal_data_unsure_generates_warning():
    """Uncertain personal-data status should generate warning."""

    payload = make_valid_laptop_payload(
        contains_personal_data="Unsure"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "unclear whether personal data"
        in warning
        for warning in result.warnings
    )


def test_sensitive_data_unsure_generates_warning():
    """Uncertain sensitive-data status should generate warning."""

    payload = make_valid_laptop_payload(
        contains_sensitive_data="Unsure"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "Sensitive-data presence is uncertain"
        in warning
        for warning in result.warnings
    )


def test_missing_backup_generates_warning_when_data_present():
    """Data without backup should produce a warning."""

    payload = make_valid_laptop_payload(
        contains_personal_data="Yes",
        data_backed_up="No",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "has not been backed up"
        in warning
        for warning in result.warnings
    )


def test_factory_reset_not_performed_generates_warning():
    """Missing factory reset should be non-blocking."""

    payload = make_valid_laptop_payload(
        factory_reset_performed="No"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "factory reset has not been performed"
        in warning.lower()
        for warning in result.warnings
    )


def test_secure_erase_not_performed_generates_warning():
    """Missing secure erase should be non-blocking."""

    payload = make_valid_laptop_payload(
        secure_erase_performed="No"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "Secure data erasure has not been performed"
        in warning
        for warning in result.warnings
    )


def test_accounts_not_signed_out_generates_warning():
    """Signed-in accounts should generate a warning."""

    payload = make_valid_laptop_payload(
        accounts_signed_out="No"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "Accounts may still be signed in"
        in warning
        for warning in result.warnings
    )


def test_removable_media_not_removed_generates_warning():
    """Remaining SIM/memory media should generate warning."""

    payload = make_valid_laptop_payload(
        sim_memory_card_removed="No"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "SIM card or removable memory card"
        in warning
        for warning in result.warnings
    )


def test_inaccessible_device_generates_warning():
    """Inaccessible device should produce sanitization warning."""

    payload = make_valid_laptop_payload(
        device_condition="Partially Working",
        device_accessible="No",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "not accessible"
        in warning
        for warning in result.warnings
    )


def test_device_that_cannot_power_on_generates_warning():
    """Power failure should generate sanitization warning."""

    payload = make_valid_laptop_payload(
        device_condition="Not Working",
        can_power_on="No",
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "cannot power on"
        in warning
        for warning in result.warnings
    )


@pytest.mark.parametrize(
    "method",
    [
        "Sell",
        "Donate",
        "Recycle",
        "Dispose",
    ],
)
def test_external_transfer_actions_generate_warning(method):
    """Actions leaving owner's control should warn the user."""

    payload = make_valid_laptop_payload(
        intended_disposal_method=method
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "outside the current owner's control"
        in warning
        for warning in result.warnings
    )


def test_not_decided_disposal_generates_warning():
    """Undecided disposal method should generate warning."""

    payload = make_valid_laptop_payload(
        intended_disposal_method="Not Decided"
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "has not yet been decided"
        in warning
        for warning in result.warnings
    )


def test_old_device_generates_warning():
    """Device age >= 10 should generate informational warning."""

    payload = make_valid_laptop_payload(
        device_age=10
    )

    result = validate_device_input(payload)

    assert result.is_valid is True

    assert any(
        "relatively old"
        in warning
        for warning in result.warnings
    )


# ============================================================
# NORMALIZE DEVICE INPUT TESTS
# ============================================================

def test_normalize_device_input_returns_dictionary():
    """Normalization should return a dictionary."""

    payload = make_valid_laptop_payload()

    data = normalize_device_input(payload)

    assert isinstance(data, dict)


def test_normalize_device_input_converts_tb_to_gb():
    """TB values should normalize into GB."""

    payload = make_valid_laptop_payload(
        storage_capacity="2 TB"
    )

    data = normalize_device_input(payload)

    assert data[FIELD_STORAGE_CAPACITY] == 2048.0


def test_normalize_device_input_ignores_unknown_fields():
    """Normalization should use only known assessment fields."""

    payload = make_valid_laptop_payload()

    payload["malicious_or_unknown_field"] = "unexpected"

    data = normalize_device_input(payload)

    assert "malicious_or_unknown_field" not in data


# ============================================================
# MALFORMED PAYLOAD TESTS
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
def test_validate_device_input_rejects_non_mapping(payload):
    """Primary validator should reject non-mapping payloads."""

    with pytest.raises(TypeError):
        validate_device_input(payload)


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
def test_normalize_device_input_rejects_non_mapping(payload):
    """Normalizer should reject non-mapping payloads."""

    with pytest.raises(TypeError):
        normalize_device_input(payload)


# ============================================================
# INVALID BOOLEAN CONVENIENCE TEST
# ============================================================

def test_boolean_convenience_function_for_invalid_input():
    """Convenience validator should return False."""

    payload = make_valid_laptop_payload(
        device_type="Invalid Device"
    )

    assert is_device_input_valid(payload) is False