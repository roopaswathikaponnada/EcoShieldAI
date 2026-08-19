"""
EcoShield AI
Device Assessment Input Validation

This module validates and normalizes all device information
before it is passed to the cybersecurity risk assessment engine.

Responsibilities:
- Validate required categorical inputs
- Validate numeric device age
- Validate and normalize storage capacity
- Validate allowed option values
- Detect logically inconsistent field combinations
- Generate non-blocking security/data-preparation warnings
- Return structured, normalized data for downstream modules

Risk scoring is intentionally NOT performed here.
That responsibility belongs to src/risk_engine.py.
"""

from __future__ import annotations

import re
from dataclasses import dataclass, field
from typing import Any, Mapping, Sequence
from config.config import (
    ACCOUNT_SIGNOUT_OPTIONS,
    BACKUP_OPTIONS,
    DEVICE_ACCESSIBLE_OPTIONS,
    DEVICE_CONDITIONS,
    DEVICE_LEAVES_OWNER_ACTIONS,
    DEVICE_TYPES,
    DEVICES_EXPECTED_TO_HAVE_STORAGE,
    DISPOSAL_METHODS,
    ENCRYPTION_OPTIONS,
    EXTERNAL_STORAGE_DEVICES,
    FACTORY_RESET_OPTIONS,
    MAX_DEVICE_AGE,
    MAX_STORAGE_CAPACITY_GB,
    MIN_DEVICE_AGE,
    MOBILE_DEVICES,
    OPERATING_SYSTEMS,
    PERSONAL_DATA_OPTIONS,
    POWER_ON_OPTIONS,
    REMOVABLE_MEDIA_OPTIONS,
    SECURE_ERASE_OPTIONS,
    SENSITIVE_DATA_OPTIONS,
    STORAGE_TYPES,
)


# ============================================================
# FIELD NAMES
# ============================================================

FIELD_DEVICE_TYPE = "device_type"

FIELD_OPERATING_SYSTEM = "operating_system"

FIELD_DEVICE_AGE = "device_age"

FIELD_DEVICE_CONDITION = "device_condition"

FIELD_STORAGE_TYPE = "storage_type"

FIELD_STORAGE_CAPACITY = "storage_capacity"

FIELD_PERSONAL_DATA = "contains_personal_data"

FIELD_SENSITIVE_DATA = "contains_sensitive_data"

FIELD_DEVICE_ACCESSIBLE = "device_accessible"

FIELD_POWER_ON = "can_power_on"

FIELD_DATA_BACKED_UP = "data_backed_up"

FIELD_FACTORY_RESET = "factory_reset_performed"

FIELD_SECURE_ERASE = "secure_erase_performed"

FIELD_ENCRYPTION = "encryption_enabled"

FIELD_ACCOUNTS_SIGNED_OUT = "accounts_signed_out"

FIELD_REMOVABLE_MEDIA_REMOVED = "sim_memory_card_removed"

FIELD_DISPOSAL_METHOD = "intended_disposal_method"


# ============================================================
# REQUIRED CATEGORICAL FIELDS
# ============================================================

REQUIRED_CATEGORICAL_FIELDS = (
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
)


# ============================================================
# FIELD LABELS
# ============================================================

FIELD_LABELS = {
    FIELD_DEVICE_TYPE: "Device type",
    FIELD_OPERATING_SYSTEM: "Operating system",
    FIELD_DEVICE_AGE: "Device age",
    FIELD_DEVICE_CONDITION: "Device condition",
    FIELD_STORAGE_TYPE: "Storage type",
    FIELD_STORAGE_CAPACITY: "Storage capacity",
    FIELD_PERSONAL_DATA: "Personal data status",
    FIELD_SENSITIVE_DATA: "Sensitive data status",
    FIELD_DEVICE_ACCESSIBLE: "Device accessibility",
    FIELD_POWER_ON: "Power-on status",
    FIELD_DATA_BACKED_UP: "Data backup status",
    FIELD_FACTORY_RESET: "Factory reset status",
    FIELD_SECURE_ERASE: "Secure erase status",
    FIELD_ENCRYPTION: "Encryption status",
    FIELD_ACCOUNTS_SIGNED_OUT: "Account sign-out status",
    FIELD_REMOVABLE_MEDIA_REMOVED: "SIM / memory card removal status",
    FIELD_DISPOSAL_METHOD: "Intended disposal method",
}


# ============================================================
# ALLOWED VALUES
# ============================================================

ALLOWED_VALUES = {
    FIELD_DEVICE_TYPE: tuple(DEVICE_TYPES),
    FIELD_OPERATING_SYSTEM: tuple(OPERATING_SYSTEMS),
    FIELD_DEVICE_CONDITION: tuple(DEVICE_CONDITIONS),
    FIELD_STORAGE_TYPE: tuple(STORAGE_TYPES),
    FIELD_PERSONAL_DATA: tuple(PERSONAL_DATA_OPTIONS),
    FIELD_SENSITIVE_DATA: tuple(SENSITIVE_DATA_OPTIONS),
    FIELD_DEVICE_ACCESSIBLE: tuple(DEVICE_ACCESSIBLE_OPTIONS),
    FIELD_POWER_ON: tuple(POWER_ON_OPTIONS),
    FIELD_DATA_BACKED_UP: tuple(BACKUP_OPTIONS),
    FIELD_FACTORY_RESET: tuple(FACTORY_RESET_OPTIONS),
    FIELD_SECURE_ERASE: tuple(SECURE_ERASE_OPTIONS),
    FIELD_ENCRYPTION: tuple(ENCRYPTION_OPTIONS),
    FIELD_ACCOUNTS_SIGNED_OUT: tuple(ACCOUNT_SIGNOUT_OPTIONS),
    FIELD_REMOVABLE_MEDIA_REMOVED: tuple(REMOVABLE_MEDIA_OPTIONS),
    FIELD_DISPOSAL_METHOD: tuple(DISPOSAL_METHODS),
}

# ============================================================
# VALIDATION RESULT
# ============================================================

@dataclass(frozen=True)
class ValidationResult:
    """
    Structured result returned by EcoShield input validation.

    Attributes
    ----------
    is_valid:
        True when no blocking validation errors exist.

    data:
        Normalized device assessment values.

        Storage capacity is normalized into GB.

    errors:
        Blocking validation issues.

    warnings:
        Non-blocking security or data-quality observations.
    """

    is_valid: bool

    data: dict[str, Any] = field(
        default_factory=dict
    )

    errors: tuple[str, ...] = field(
        default_factory=tuple
    )

    warnings: tuple[str, ...] = field(
        default_factory=tuple
    )


# ============================================================
# BASIC STRING NORMALIZATION
# ============================================================

def _normalize_string(
    value: Any,
) -> str:
    """
    Normalize arbitrary input into a clean string.

    Examples
    --------
    "  Laptop  " -> "Laptop"

    "Not    Applicable" -> "Not Applicable"

    None -> ""
    """

    if value is None:
        return ""

    if not isinstance(value, str):
        value = str(value)

    return " ".join(
        value.strip().split()
    )


# ============================================================
# CANONICAL OPTION NORMALIZATION
# ============================================================

def _canonicalize_option(
    value: Any,
    allowed_values: Sequence[str],
) -> str:
    """
    Match user input against configured values
    case-insensitively.

    Examples
    --------
    "laptop" -> "Laptop"

    "YES" -> "Yes"

    " not applicable " -> "Not Applicable"
    """

    normalized = _normalize_string(
        value
    )

    if not normalized:
        return ""

    lookup = {
        option.casefold(): option
        for option in allowed_values
    }

    return lookup.get(
        normalized.casefold(),
        normalized,
    )


# ============================================================
# DEVICE AGE NORMALIZATION
# ============================================================

def _normalize_device_age(
    value: Any,
) -> float | None:
    """
    Convert device age into years.

    Accepted examples
    -----------------
    3
    3.5
    "3"
    "3.5"
    "3 years"
    """

    if value is None:
        return None

    if isinstance(
        value,
        (int, float),
    ):
        return float(value)

    normalized = _normalize_string(
        value
    )

    if not normalized:
        return None

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)"
        r"(?:\s*(?:year|years|yr|yrs))?",
        normalized,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    return float(
        match.group(1)
    )


# ============================================================
# STORAGE CAPACITY NORMALIZATION
# ============================================================

def _normalize_storage_capacity(
    value: Any,
) -> float | None:
    """
    Convert storage capacity into GB.

    Accepted examples
    -----------------
    512
        -> 512 GB

    "512"
        -> 512 GB

    "512 GB"
        -> 512 GB

    "1 TB"
        -> 1024 GB

    "1.5TB"
        -> 1536 GB

    Numeric values without a unit are interpreted as GB.

    Returns
    -------
    float | None
        Capacity normalized into GB.
    """

    if value is None:
        return None

    if isinstance(
        value,
        (int, float),
    ):

        return float(value)

    normalized = _normalize_string(
        value
    )

    if not normalized:
        return None

    match = re.fullmatch(
        r"(\d+(?:\.\d+)?)"
        r"\s*(GB|TB)?",
        normalized,
        flags=re.IGNORECASE,
    )

    if not match:
        return None

    number = float(
        match.group(1)
    )

    unit = (
        match.group(2) or "GB"
    ).upper()

    if unit == "TB":
        number *= 1024

    return number


# ============================================================
# NORMALIZE COMPLETE PAYLOAD
# ============================================================

def normalize_device_input(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Normalize the complete EcoShield assessment payload.

    Unknown additional fields are ignored deliberately.

    This prevents unexpected UI/API data from entering
    downstream cybersecurity logic.
    """

    if not isinstance(
        payload,
        Mapping,
    ):
        raise TypeError(
            "Device assessment input must be a "
            "dictionary-like mapping."
        )

    normalized: dict[str, Any] = {}

    for field_name in REQUIRED_CATEGORICAL_FIELDS:

        normalized[field_name] = (
            _canonicalize_option(
                payload.get(field_name),
                ALLOWED_VALUES[field_name],
            )
        )

    normalized[FIELD_DEVICE_AGE] = (
        _normalize_device_age(
            payload.get(
                FIELD_DEVICE_AGE
            )
        )
    )

    normalized[
        FIELD_STORAGE_CAPACITY
    ] = _normalize_storage_capacity(
        payload.get(
            FIELD_STORAGE_CAPACITY
        )
    )

    return normalized


# ============================================================
# REQUIRED FIELD VALIDATION
# ============================================================

def _validate_required_fields(
    original_payload: Mapping[str, Any],
    data: Mapping[str, Any],
) -> list[str]:
    """
    Ensure all mandatory EcoShield assessment fields
    have been supplied.
    """

    errors: list[str] = []

    for field_name in REQUIRED_CATEGORICAL_FIELDS:

        if not data.get(
            field_name
        ):

            errors.append(
                f"{FIELD_LABELS[field_name]} "
                "is required."
            )

    # Device age requires separate handling because
    # zero is a valid numeric value.

    raw_age = original_payload.get(
        FIELD_DEVICE_AGE
    )

    if (
        raw_age is None
        or _normalize_string(
            raw_age
        ) == ""
    ):

        errors.append(
            "Device age is required."
        )

    return errors


# ============================================================
# ALLOWED VALUE VALIDATION
# ============================================================

def _validate_allowed_values(
    data: Mapping[str, Any],
) -> list[str]:
    """
    Ensure categorical values belong to supported
    EcoShield option lists.
    """

    errors: list[str] = []

    for (
        field_name,
        allowed_values,
    ) in ALLOWED_VALUES.items():

        value = data.get(
            field_name
        )

        if not value:
            continue

        if value not in allowed_values:

            errors.append(
                f"Invalid "
                f"{FIELD_LABELS[field_name].lower()}: "
                f"'{value}'."
            )

    return errors


# ============================================================
# DEVICE AGE VALIDATION
# ============================================================

def _validate_device_age(
    original_payload: Mapping[str, Any],
    data: Mapping[str, Any],
) -> list[str]:
    """
    Validate device age.
    """

    errors: list[str] = []

    raw_value = original_payload.get(
        FIELD_DEVICE_AGE
    )

    if (
        raw_value is None
        or _normalize_string(
            raw_value
        ) == ""
    ):
        return errors

    age = data.get(
        FIELD_DEVICE_AGE
    )

    if age is None:

        errors.append(
            "Device age must be a numeric value "
            "expressed in years."
        )

        return errors

    if age < MIN_DEVICE_AGE:

        errors.append(
            "Device age cannot be negative."
        )

    elif age > MAX_DEVICE_AGE:

        errors.append(
            f"Device age cannot exceed "
            f"{MAX_DEVICE_AGE:g} years."
        )

    return errors


# ============================================================
# STORAGE CAPACITY VALIDATION
# ============================================================

def _validate_storage_capacity(
    original_payload: Mapping[str, Any],
    data: Mapping[str, Any],
) -> list[str]:
    """
    Validate storage capacity.

    Capacity is required whenever storage type is not
    'Not Applicable'.

    Capacity is normalized internally into GB.
    """

    errors: list[str] = []

    storage_type = data.get(
        FIELD_STORAGE_TYPE,
        "",
    )

    raw_capacity = original_payload.get(
        FIELD_STORAGE_CAPACITY
    )

    capacity = data.get(
        FIELD_STORAGE_CAPACITY
    )

    # --------------------------------------------------------
    # No-storage / not-applicable case
    # --------------------------------------------------------

    if storage_type == "Not Applicable":

        if (
            raw_capacity is not None
            and _normalize_string(
                raw_capacity
            )
            not in {
                "",
                "0",
                "0.0",
            }
        ):

            errors.append(
                "Storage capacity should not be provided "
                "when storage type is 'Not Applicable'."
            )

        return errors

    # --------------------------------------------------------
    # Capacity required for storage-bearing devices
    # --------------------------------------------------------

    if (
        raw_capacity is None
        or _normalize_string(
            raw_capacity
        ) == ""
    ):

        errors.append(
            "Storage capacity is required."
        )

        return errors

    # --------------------------------------------------------
    # Invalid format
    # --------------------------------------------------------

    if capacity is None:

        errors.append(
            "Storage capacity must be a numeric value "
            "such as '512 GB' or '1 TB'."
        )

        return errors

    # --------------------------------------------------------
    # Capacity range
    # --------------------------------------------------------

    if capacity <= 0:

        errors.append(
            "Storage capacity must be greater than zero."
        )

    elif (
        capacity
        > MAX_STORAGE_CAPACITY_GB
    ):

        errors.append(
            "Storage capacity exceeds the supported "
            "validation range."
        )

    return errors


# ============================================================
# DEVICE / STORAGE CONSISTENCY
# ============================================================

def _validate_device_storage_relationship(
    data: Mapping[str, Any],
) -> list[str]:
    """
    Validate obvious device/storage inconsistencies.

    The validator deliberately avoids over-restricting
    legitimate hardware configurations.
    """

    errors: list[str] = []

    device_type = data.get(
        FIELD_DEVICE_TYPE,
        "",
    )

    storage_type = data.get(
        FIELD_STORAGE_TYPE,
        "",
    )

    if (
        not device_type
        or not storage_type
    ):
        return errors

    # --------------------------------------------------------
    # Storage-bearing devices should not normally have
    # storage marked as Not Applicable.
    # --------------------------------------------------------

    if (
        device_type
        in DEVICES_EXPECTED_TO_HAVE_STORAGE
        and storage_type
        == "Not Applicable"
    ):

        errors.append(
            f"{device_type} normally contains storage; "
            "select the actual storage type or 'Unknown'."
        )

    # --------------------------------------------------------
    # External hard drive
    # --------------------------------------------------------

    if (
        device_type
        == "External Hard Drive"
        and storage_type
        not in {
            "HDD",
            "SSD",
            "Hybrid",
            "Unknown",
        }
    ):

        errors.append(
            "External Hard Drive must use HDD, SSD, "
            "Hybrid, or Unknown storage type."
        )

    # --------------------------------------------------------
    # USB drive
    # --------------------------------------------------------

    if (
        device_type
        == "USB Drive"
        and storage_type
        not in {
            "Flash Storage",
            "Unknown",
        }
    ):

        errors.append(
            "USB Drive should use Flash Storage "
            "or Unknown as its storage type."
        )

    return errors


# ============================================================
# DEVICE / OS CONSISTENCY
# ============================================================

def _validate_device_os_relationship(
    data: Mapping[str, Any],
) -> list[str]:
    """
    Validate only clearly incompatible OS/device combinations.

    Less-certain combinations generate warnings elsewhere
    instead of blocking valid edge cases.
    """

    errors: list[str] = []

    device_type = data.get(
        FIELD_DEVICE_TYPE,
        "",
    )

    operating_system = data.get(
        FIELD_OPERATING_SYSTEM,
        "",
    )

    if (
        not device_type
        or not operating_system
    ):
        return errors

    if (
        device_type
        in EXTERNAL_STORAGE_DEVICES
        and operating_system
        not in {
            "Not Applicable",
            "Unknown",
        }
    ):

        errors.append(
            f"{device_type} should normally use "
            "'Not Applicable' or 'Unknown' "
            "for operating system."
        )

    return errors


# ============================================================
# LOGICAL STATE VALIDATION
# ============================================================

def _validate_logical_relationships(
    data: Mapping[str, Any],
) -> list[str]:
    """
    Detect strongly contradictory assessment states.

    Only combinations that are logically inconsistent are
    blocking errors. Security weaknesses remain warnings
    and are scored later by risk_engine.py.
    """

    errors: list[str] = []

    device_accessible = data.get(
        FIELD_DEVICE_ACCESSIBLE,
        "",
    )

    power_on = data.get(
        FIELD_POWER_ON,
        "",
    )

    condition = data.get(
        FIELD_DEVICE_CONDITION,
        "",
    )

    factory_reset = data.get(
        FIELD_FACTORY_RESET,
        "",
    )

    secure_erase = data.get(
        FIELD_SECURE_ERASE,
        "",
    )

    storage_type = data.get(
        FIELD_STORAGE_TYPE,
        "",
    )

    # --------------------------------------------------------
    # Working device but cannot power on
    # --------------------------------------------------------

    if (
        condition == "Working"
        and power_on == "No"
    ):

        errors.append(
            "A device marked as 'Working' cannot also "
            "be marked as unable to power on."
        )

    # --------------------------------------------------------
    # No applicable storage but secure erase performed
    # --------------------------------------------------------

    if (
        storage_type
        == "Not Applicable"
        and secure_erase
        in {
            "Yes",
            "No",
        }
    ):

        errors.append(
            "Secure erase should be 'Not Applicable' "
            "when storage type is 'Not Applicable'."
        )

    # --------------------------------------------------------
    # Completely inaccessible + reset assertion
    #
    # This is intentionally not treated as invalid because
    # reset may have been performed before the device became
    # inaccessible.
    # --------------------------------------------------------

    _ = (
        device_accessible,
        factory_reset,
    )

    return errors


# ============================================================
# SECURITY / DATA QUALITY WARNINGS
# ============================================================

def _generate_warnings(
    data: Mapping[str, Any],
) -> list[str]:
    """
    Generate non-blocking observations.

    These warnings DO NOT determine final risk.
    risk_engine.py will perform actual security scoring.
    """

    warnings: list[str] = []

    personal_data = data.get(
        FIELD_PERSONAL_DATA,
        "",
    )

    sensitive_data = data.get(
        FIELD_SENSITIVE_DATA,
        "",
    )

    accessible = data.get(
        FIELD_DEVICE_ACCESSIBLE,
        "",
    )

    power_on = data.get(
        FIELD_POWER_ON,
        "",
    )

    backup = data.get(
        FIELD_DATA_BACKED_UP,
        "",
    )

    factory_reset = data.get(
        FIELD_FACTORY_RESET,
        "",
    )

    secure_erase = data.get(
        FIELD_SECURE_ERASE,
        "",
    )

    encryption = data.get(
        FIELD_ENCRYPTION,
        "",
    )

    accounts_signed_out = data.get(
        FIELD_ACCOUNTS_SIGNED_OUT,
        "",
    )

    media_removed = data.get(
        FIELD_REMOVABLE_MEDIA_REMOVED,
        "",
    )

    disposal_method = data.get(
        FIELD_DISPOSAL_METHOD,
        "",
    )

    device_type = data.get(
        FIELD_DEVICE_TYPE,
        "",
    )

    operating_system = data.get(
        FIELD_OPERATING_SYSTEM,
        "",
    )

    device_age = data.get(
        FIELD_DEVICE_AGE
    )

    # --------------------------------------------------------
    # Personal data uncertainty
    # --------------------------------------------------------

    if personal_data == "Unsure":

        warnings.append(
            "It is unclear whether personal data remains "
            "on the device."
        )

    # --------------------------------------------------------
    # Sensitive data uncertainty
    # --------------------------------------------------------

    if sensitive_data == "Unsure":

        warnings.append(
            "Sensitive-data presence is uncertain; "
            "the device should be treated cautiously."
        )

    # --------------------------------------------------------
    # Sensitive data without encryption
    # --------------------------------------------------------

    if (
        sensitive_data == "Yes"
        and encryption == "No"
    ):

        warnings.append(
            "Sensitive data is present while device "
            "encryption is disabled."
        )

    # --------------------------------------------------------
    # Encryption unknown
    # --------------------------------------------------------

    if encryption == "Unsure":

        warnings.append(
            "Encryption status is uncertain."
        )

    # --------------------------------------------------------
    # Backup
    # --------------------------------------------------------

    if (
        personal_data == "Yes"
        or sensitive_data == "Yes"
    ):

        if backup == "No":

            warnings.append(
                "Data is present but has not been "
                "backed up."
            )

        elif backup == "Unsure":

            warnings.append(
                "Backup status is uncertain."
            )

    # --------------------------------------------------------
    # Factory reset
    # --------------------------------------------------------

    if factory_reset == "No":

        warnings.append(
            "A factory reset has not been performed."
        )

    elif factory_reset == "Unsure":

        warnings.append(
            "Factory-reset status is uncertain."
        )

    # --------------------------------------------------------
    # Secure erase
    # --------------------------------------------------------

    if secure_erase == "No":

        warnings.append(
            "Secure data erasure has not been performed."
        )

    elif secure_erase == "Unsure":

        warnings.append(
            "Secure-erasure status is uncertain."
        )

    # --------------------------------------------------------
    # Account sessions
    # --------------------------------------------------------

    if accounts_signed_out == "No":

        warnings.append(
            "Accounts may still be signed in on the device."
        )

    elif accounts_signed_out == "Unsure":

        warnings.append(
            "Account sign-out status is uncertain."
        )

    # --------------------------------------------------------
    # SIM / memory card
    # --------------------------------------------------------

    if media_removed == "No":

        warnings.append(
            "A SIM card or removable memory card may "
            "still be present."
        )

    elif media_removed == "Unsure":

        warnings.append(
            "SIM / memory-card removal status "
            "is uncertain."
        )

    # --------------------------------------------------------
    # Device inaccessible
    # --------------------------------------------------------

    if accessible == "No":

        warnings.append(
            "The device is not accessible, which may limit "
            "software-based data sanitization options."
        )

    # --------------------------------------------------------
    # Device cannot power on
    # --------------------------------------------------------

    if power_on == "No":

        warnings.append(
            "The device cannot power on, which may prevent "
            "normal reset or secure-erasure procedures."
        )

    # --------------------------------------------------------
    # Ownership transfer / disposal
    # --------------------------------------------------------

    if disposal_method in DEVICE_LEAVES_OWNER_ACTIONS:

        warnings.append(
            "The selected disposal method may transfer "
            "the device outside the current owner's control."
        )

    # --------------------------------------------------------
    # Disposal method undecided
    # --------------------------------------------------------

    if disposal_method == "Not Decided":

        warnings.append(
            "The disposal method has not yet been decided."
        )

    # --------------------------------------------------------
    # Mobile removable media relevance
    # --------------------------------------------------------

    if (
        device_type
        in MOBILE_DEVICES
        and media_removed
        == "Not Applicable"
    ):

        warnings.append(
            "Verify whether the mobile device contains "
            "a removable SIM or memory card."
        )

    # --------------------------------------------------------
    # Computer/mobile OS uncertainty
    # --------------------------------------------------------

    if (
        device_type
        not in EXTERNAL_STORAGE_DEVICES
        and operating_system
        == "Unknown"
    ):

        warnings.append(
            "Operating system is unknown."
        )

    # --------------------------------------------------------
    # Older hardware informational warning
    # --------------------------------------------------------

    if (
        isinstance(
            device_age,
            (int, float),
        )
        and device_age >= 10
    ):

        warnings.append(
            "The device is relatively old; repairability, "
            "reuse potential, and storage reliability may "
            "require additional assessment."
        )

    return warnings


# ============================================================
# REMOVE DUPLICATE MESSAGES
# ============================================================

def _deduplicate_messages(
    messages: list[str],
) -> tuple[str, ...]:
    """
    Remove duplicate messages while preserving order.
    """

    return tuple(
        dict.fromkeys(
            messages
        )
    )


# ============================================================
# PRIMARY VALIDATION FUNCTION
# ============================================================

def validate_device_input(
    payload: Mapping[str, Any],
) -> ValidationResult:
    """
    Validate a complete EcoShield device assessment.

    This is the primary public function used by app.py and
    downstream modules.

    Parameters
    ----------
    payload:
        Dictionary-like object containing device assessment
        values.

    Returns
    -------
    ValidationResult
        Structured validation result containing:

        - is_valid
        - normalized data
        - blocking errors
        - non-blocking warnings

    Raises
    ------
    TypeError
        If payload is not a dictionary-like mapping.
    """

    if not isinstance(
        payload,
        Mapping,
    ):

        raise TypeError(
            "Device assessment input must be a "
            "dictionary-like mapping."
        )

    normalized_data = (
        normalize_device_input(
            payload
        )
    )

    errors: list[str] = []

    warnings: list[str] = []

    # --------------------------------------------------------
    # Required values
    # --------------------------------------------------------

    errors.extend(
        _validate_required_fields(
            payload,
            normalized_data,
        )
    )

    # --------------------------------------------------------
    # Option validation
    # --------------------------------------------------------

    errors.extend(
        _validate_allowed_values(
            normalized_data
        )
    )

    # --------------------------------------------------------
    # Numeric validation
    # --------------------------------------------------------

    errors.extend(
        _validate_device_age(
            payload,
            normalized_data,
        )
    )

    errors.extend(
        _validate_storage_capacity(
            payload,
            normalized_data,
        )
    )

    # --------------------------------------------------------
    # Cross-field validation
    # --------------------------------------------------------

    errors.extend(
        _validate_device_storage_relationship(
            normalized_data
        )
    )

    errors.extend(
        _validate_device_os_relationship(
            normalized_data
        )
    )

    errors.extend(
        _validate_logical_relationships(
            normalized_data
        )
    )

    # --------------------------------------------------------
    # Non-blocking observations
    # --------------------------------------------------------

    warnings.extend(
        _generate_warnings(
            normalized_data
        )
    )

    unique_errors = (
        _deduplicate_messages(
            errors
        )
    )

    unique_warnings = (
        _deduplicate_messages(
            warnings
        )
    )

    return ValidationResult(
        is_valid=not unique_errors,
        data=normalized_data,
        errors=unique_errors,
        warnings=unique_warnings,
    )


# ============================================================
# BOOLEAN CONVENIENCE FUNCTION
# ============================================================

def is_device_input_valid(
    payload: Mapping[str, Any],
) -> bool:
    """
    Return only whether an EcoShield assessment is valid.

    Use validate_device_input() whenever detailed errors,
    warnings, or normalized data are required.
    """

    return validate_device_input(
        payload
    ).is_valid