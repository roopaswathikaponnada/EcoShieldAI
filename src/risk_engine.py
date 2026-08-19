"""
EcoShield AI
Cybersecurity Risk Assessment Engine

This module calculates an explainable security-risk assessment
for electronic devices being sold, donated, reused, repaired,
recycled, or disposed of.

The risk engine consumes device data that conforms to the
canonical EcoShield validator interface.

Responsibilities:
- Validate incoming assessment data defensively
- Calculate deterministic security-risk scores
- Evaluate multiple cybersecurity risk categories
- Generate explainable risk factors
- Identify uncertainty in the assessment
- Produce Low / Medium / High risk levels
- Return structured results for recommendation.py and app.py

Important:
This engine provides decision-support scoring. It does not claim
to represent a formal regulatory, legal, or compliance score.

AI / LLM components MUST NOT override the deterministic risk
score produced by this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from config.config import (
    DEVICE_LEAVES_OWNER_ACTIONS,
    RISK_HIGH,
    RISK_LOW,
    RISK_MEDIUM,
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
    validate_device_input,
)


# ============================================================
# RISK SCORE BOUNDARIES
# ============================================================

MIN_RISK_SCORE = 0

MAX_RISK_SCORE = 100

LOW_RISK_MAX = 24

MEDIUM_RISK_MAX = 49


# ============================================================
# RISK CATEGORIES
# ============================================================

CATEGORY_DATA_EXPOSURE = "Data Exposure"

CATEGORY_SANITIZATION = "Sanitization"

CATEGORY_TRANSFER = "Transfer / Disposal"

CATEGORY_ACCESSIBILITY = "Accessibility / Condition"

CATEGORY_MEDIA_BACKUP = "Media / Backup"


# ============================================================
# CATEGORY MAXIMUM SCORES
# ============================================================

CATEGORY_MAX_SCORES = {
    CATEGORY_DATA_EXPOSURE: 35,
    CATEGORY_SANITIZATION: 30,
    CATEGORY_TRANSFER: 15,
    CATEGORY_ACCESSIBILITY: 10,
    CATEGORY_MEDIA_BACKUP: 10,
}


# ============================================================
# DISPOSAL ACTION GROUPS
# ============================================================

HIGH_TRANSFER_ACTIONS = {
    "Sell",
    "Donate",
}

FINAL_DISPOSAL_ACTIONS = {
    "Recycle",
    "Dispose",
}

SERVICE_ACTIONS = {
    "Repair",
}


# ============================================================
# UNCERTAIN VALUES
# ============================================================

UNCERTAIN_VALUES = {
    "Unsure",
    "Unknown",
    "Not Decided",
}


# ============================================================
# RISK FACTOR
# ============================================================

@dataclass(frozen=True)
class RiskFactor:
    """
    A single explainable factor contributing to device risk.

    Attributes
    ----------
    code:
        Stable machine-readable factor identifier.

    category:
        Risk category to which this factor belongs.

    points:
        Number of risk points contributed.

    message:
        Human-readable explanation of the risk factor.
    """

    code: str

    category: str

    points: int

    message: str


# ============================================================
# RISK ASSESSMENT RESULT
# ============================================================

@dataclass(frozen=True)
class RiskAssessment:
    """
    Final structured EcoShield cybersecurity risk assessment.

    Attributes
    ----------
    score:
        Final risk score from 0 to 100.

    risk_level:
        Low, Medium, or High.

    factors:
        Individual explainable risk factors.

    category_scores:
        Risk score contribution for each category.

    uncertainties:
        Assessment fields whose values are unknown or uncertain.

    validated_data:
        Normalized device information used during scoring.

    requires_sanitization:
        Whether the current device state indicates that data
        sanitization should be considered before transfer.

    device_leaves_owner:
        Whether the selected action may transfer the device
        outside the current owner's control.
    """

    score: int

    risk_level: str

    factors: tuple[RiskFactor, ...] = field(
        default_factory=tuple
    )

    category_scores: dict[str, int] = field(
        default_factory=dict
    )

    uncertainties: tuple[str, ...] = field(
        default_factory=tuple
    )

    validated_data: dict[str, Any] = field(
        default_factory=dict
    )

    requires_sanitization: bool = False

    device_leaves_owner: bool = False

    def to_dict(self) -> dict[str, Any]:
        """
        Return a serializable dictionary representation.

        Useful for:
        - Streamlit
        - JSON APIs
        - logging
        - future reporting
        - RAG / LLM context
        """

        return asdict(self)


# ============================================================
# INTERNAL CATEGORY SCORE INITIALIZER
# ============================================================

def _new_category_scores() -> dict[str, int]:
    """
    Create a fresh category-score dictionary.
    """

    return {
        category: 0
        for category in CATEGORY_MAX_SCORES
    }


# ============================================================
# CATEGORY SCORE ADDITION
# ============================================================

def _add_factor(
    factors: list[RiskFactor],
    category_scores: dict[str, int],
    *,
    code: str,
    category: str,
    points: int,
    message: str,
) -> None:
    """
    Add one explainable risk factor and safely update
    the corresponding category score.

    Category scores are capped at their configured maximum.
    """

    if points <= 0:
        return

    current_score = category_scores[category]

    category_maximum = CATEGORY_MAX_SCORES[
        category
    ]

    available_points = max(
        category_maximum - current_score,
        0,
    )

    applied_points = min(
        points,
        available_points,
    )

    if applied_points <= 0:
        return

    category_scores[category] += applied_points

    factors.append(
        RiskFactor(
            code=code,
            category=category,
            points=applied_points,
            message=message,
        )
    )


# ============================================================
# DATA PRESENCE HELPERS
# ============================================================

def _data_may_exist(
    data: Mapping[str, Any],
) -> bool:
    """
    Return whether personal or sensitive data is known or
    potentially present.
    """

    personal_data = data.get(
        FIELD_PERSONAL_DATA
    )

    sensitive_data = data.get(
        FIELD_SENSITIVE_DATA
    )

    return (
        personal_data in {"Yes", "Unsure"}
        or sensitive_data in {"Yes", "Unsure"}
    )


def _sensitive_data_may_exist(
    data: Mapping[str, Any],
) -> bool:
    """
    Return whether sensitive information is known or
    potentially present.
    """

    return data.get(
        FIELD_SENSITIVE_DATA
    ) in {
        "Yes",
        "Unsure",
    }


# ============================================================
# DATA EXPOSURE ASSESSMENT
# ============================================================

def _assess_data_exposure(
    data: Mapping[str, Any],
    factors: list[RiskFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess data sensitivity and encryption exposure.

    Maximum category contribution: 35 points.
    """

    personal_data = data.get(
        FIELD_PERSONAL_DATA
    )

    sensitive_data = data.get(
        FIELD_SENSITIVE_DATA
    )

    encryption = data.get(
        FIELD_ENCRYPTION
    )

    # --------------------------------------------------------
    # Personal data
    # --------------------------------------------------------

    if personal_data == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="PERSONAL_DATA_PRESENT",
            category=CATEGORY_DATA_EXPOSURE,
            points=10,
            message=(
                "Personal data is reported to be present "
                "on the device."
            ),
        )

    elif personal_data == "Unsure":

        _add_factor(
            factors,
            category_scores,
            code="PERSONAL_DATA_UNCERTAIN",
            category=CATEGORY_DATA_EXPOSURE,
            points=6,
            message=(
                "It is uncertain whether personal data "
                "remains on the device."
            ),
        )

    # --------------------------------------------------------
    # Sensitive data
    # --------------------------------------------------------

    if sensitive_data == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="SENSITIVE_DATA_PRESENT",
            category=CATEGORY_DATA_EXPOSURE,
            points=18,
            message=(
                "Sensitive data is reported to be present "
                "on the device."
            ),
        )

    elif sensitive_data == "Unsure":

        _add_factor(
            factors,
            category_scores,
            code="SENSITIVE_DATA_UNCERTAIN",
            category=CATEGORY_DATA_EXPOSURE,
            points=10,
            message=(
                "The presence of sensitive information "
                "is uncertain."
            ),
        )

    # --------------------------------------------------------
    # Encryption
    # --------------------------------------------------------

    if _data_may_exist(data):

        if encryption == "No":

            _add_factor(
                factors,
                category_scores,
                code="ENCRYPTION_DISABLED",
                category=CATEGORY_DATA_EXPOSURE,
                points=7,
                message=(
                    "Data may be present while device "
                    "encryption is disabled."
                ),
            )

        elif encryption == "Unsure":

            _add_factor(
                factors,
                category_scores,
                code="ENCRYPTION_UNCERTAIN",
                category=CATEGORY_DATA_EXPOSURE,
                points=4,
                message=(
                    "Encryption status is uncertain while "
                    "data may remain on the device."
                ),
            )


# ============================================================
# SANITIZATION ASSESSMENT
# ============================================================

def _assess_sanitization(
    data: Mapping[str, Any],
    factors: list[RiskFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess secure erase, factory reset, and account state.

    Maximum category contribution: 30 points.
    """

    storage_type = data.get(
        FIELD_STORAGE_TYPE
    )

    factory_reset = data.get(
        FIELD_FACTORY_RESET
    )

    secure_erase = data.get(
        FIELD_SECURE_ERASE
    )

    accounts_signed_out = data.get(
        FIELD_ACCOUNTS_SIGNED_OUT
    )

    data_present = _data_may_exist(
        data
    )

    # --------------------------------------------------------
    # Secure erase
    # --------------------------------------------------------

    if (
        storage_type != "Not Applicable"
        and data_present
    ):

        if secure_erase == "No":

            _add_factor(
                factors,
                category_scores,
                code="SECURE_ERASE_NOT_PERFORMED",
                category=CATEGORY_SANITIZATION,
                points=15,
                message=(
                    "Secure data erasure has not been "
                    "performed while data may remain."
                ),
            )

        elif secure_erase == "Unsure":

            _add_factor(
                factors,
                category_scores,
                code="SECURE_ERASE_UNCERTAIN",
                category=CATEGORY_SANITIZATION,
                points=9,
                message=(
                    "It is uncertain whether secure data "
                    "erasure has been completed."
                ),
            )

    # --------------------------------------------------------
    # Factory reset
    # --------------------------------------------------------

    if factory_reset == "No":

        _add_factor(
            factors,
            category_scores,
            code="FACTORY_RESET_NOT_PERFORMED",
            category=CATEGORY_SANITIZATION,
            points=8,
            message=(
                "A factory reset has not been performed."
            ),
        )

    elif factory_reset == "Unsure":

        _add_factor(
            factors,
            category_scores,
            code="FACTORY_RESET_UNCERTAIN",
            category=CATEGORY_SANITIZATION,
            points=5,
            message=(
                "Factory-reset status is uncertain."
            ),
        )

    # --------------------------------------------------------
    # Account sign-out
    # --------------------------------------------------------

    if accounts_signed_out == "No":

        _add_factor(
            factors,
            category_scores,
            code="ACCOUNTS_NOT_SIGNED_OUT",
            category=CATEGORY_SANITIZATION,
            points=7,
            message=(
                "One or more user accounts may still "
                "be signed in on the device."
            ),
        )

    elif accounts_signed_out == "Unsure":

        _add_factor(
            factors,
            category_scores,
            code="ACCOUNT_SIGNOUT_UNCERTAIN",
            category=CATEGORY_SANITIZATION,
            points=4,
            message=(
                "Account sign-out status is uncertain."
            ),
        )


# ============================================================
# TRANSFER / DISPOSAL ASSESSMENT
# ============================================================

def _assess_transfer_context(
    data: Mapping[str, Any],
    factors: list[RiskFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess exposure introduced by the intended device action.

    Maximum category contribution: 15 points.
    """

    disposal_method = data.get(
        FIELD_DISPOSAL_METHOD
    )

    if disposal_method in HIGH_TRANSFER_ACTIONS:

        _add_factor(
            factors,
            category_scores,
            code="OWNERSHIP_TRANSFER",
            category=CATEGORY_TRANSFER,
            points=15,
            message=(
                f"The device is intended to be "
                f"{disposal_method.lower()}d, which transfers "
                "it to another party."
            ),
        )

    elif disposal_method in FINAL_DISPOSAL_ACTIONS:

        _add_factor(
            factors,
            category_scores,
            code="FINAL_DISPOSAL",
            category=CATEGORY_TRANSFER,
            points=12,
            message=(
                "The selected disposal method may place "
                "the device outside the owner's control."
            ),
        )

    elif disposal_method in SERVICE_ACTIONS:

        _add_factor(
            factors,
            category_scores,
            code="THIRD_PARTY_REPAIR",
            category=CATEGORY_TRANSFER,
            points=8,
            message=(
                "Repair may expose the device to a "
                "third-party service provider."
            ),
        )

    elif disposal_method == "Not Decided":

        _add_factor(
            factors,
            category_scores,
            code="DISPOSAL_UNDECIDED",
            category=CATEGORY_TRANSFER,
            points=5,
            message=(
                "The final disposal or transfer method "
                "has not yet been decided."
            ),
        )

    elif disposal_method == "Reuse":

        _add_factor(
            factors,
            category_scores,
            code="INTERNAL_REUSE",
            category=CATEGORY_TRANSFER,
            points=2,
            message=(
                "The device is intended for reuse and may "
                "still require appropriate data preparation."
            ),
        )


# ============================================================
# ACCESSIBILITY / CONDITION ASSESSMENT
# ============================================================

def _assess_accessibility_condition(
    data: Mapping[str, Any],
    factors: list[RiskFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess conditions that may prevent normal sanitization.

    Maximum category contribution: 10 points.
    """

    accessible = data.get(
        FIELD_DEVICE_ACCESSIBLE
    )

    power_on = data.get(
        FIELD_POWER_ON
    )

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    if accessible == "No":

        _add_factor(
            factors,
            category_scores,
            code="DEVICE_INACCESSIBLE",
            category=CATEGORY_ACCESSIBILITY,
            points=4,
            message=(
                "The device is not accessible, which may "
                "limit software-based sanitization."
            ),
        )

    if power_on == "No":

        _add_factor(
            factors,
            category_scores,
            code="DEVICE_CANNOT_POWER_ON",
            category=CATEGORY_ACCESSIBILITY,
            points=4,
            message=(
                "The device cannot power on, which may "
                "prevent normal reset or erasure procedures."
            ),
        )

    if condition == "Physically Damaged":

        _add_factor(
            factors,
            category_scores,
            code="PHYSICAL_DAMAGE",
            category=CATEGORY_ACCESSIBILITY,
            points=2,
            message=(
                "Physical damage may complicate secure "
                "data sanitization or recovery."
            ),
        )

    elif condition == "Not Working":

        _add_factor(
            factors,
            category_scores,
            code="DEVICE_NOT_WORKING",
            category=CATEGORY_ACCESSIBILITY,
            points=2,
            message=(
                "The device is not working, which may "
                "restrict normal sanitization procedures."
            ),
        )

    elif condition == "Partially Working":

        _add_factor(
            factors,
            category_scores,
            code="DEVICE_PARTIALLY_WORKING",
            category=CATEGORY_ACCESSIBILITY,
            points=1,
            message=(
                "The device is only partially working."
            ),
        )


# ============================================================
# MEDIA / BACKUP ASSESSMENT
# ============================================================

def _assess_media_backup(
    data: Mapping[str, Any],
    factors: list[RiskFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess removable-media, backup, and storage uncertainty.

    Maximum category contribution: 10 points.
    """

    media_removed = data.get(
        FIELD_REMOVABLE_MEDIA_REMOVED
    )

    backup_status = data.get(
        FIELD_DATA_BACKED_UP
    )

    storage_type = data.get(
        FIELD_STORAGE_TYPE
    )

    data_present = _data_may_exist(
        data
    )

    # --------------------------------------------------------
    # SIM / removable memory
    # --------------------------------------------------------

    if media_removed == "No":

        _add_factor(
            factors,
            category_scores,
            code="REMOVABLE_MEDIA_PRESENT",
            category=CATEGORY_MEDIA_BACKUP,
            points=5,
            message=(
                "A SIM card or removable memory card "
                "may still be present."
            ),
        )

    elif media_removed == "Unsure":

        _add_factor(
            factors,
            category_scores,
            code="REMOVABLE_MEDIA_UNCERTAIN",
            category=CATEGORY_MEDIA_BACKUP,
            points=3,
            message=(
                "It is uncertain whether removable media "
                "has been removed."
            ),
        )

    # --------------------------------------------------------
    # Backup readiness
    # --------------------------------------------------------

    if data_present:

        if backup_status == "No":

            _add_factor(
                factors,
                category_scores,
                code="BACKUP_NOT_COMPLETED",
                category=CATEGORY_MEDIA_BACKUP,
                points=3,
                message=(
                    "Data may be present but has not been "
                    "backed up before sanitization."
                ),
            )

        elif backup_status == "Unsure":

            _add_factor(
                factors,
                category_scores,
                code="BACKUP_UNCERTAIN",
                category=CATEGORY_MEDIA_BACKUP,
                points=2,
                message=(
                    "Backup status is uncertain."
                ),
            )

    # --------------------------------------------------------
    # Storage uncertainty
    # --------------------------------------------------------

    if storage_type == "Unknown":

        _add_factor(
            factors,
            category_scores,
            code="STORAGE_TYPE_UNKNOWN",
            category=CATEGORY_MEDIA_BACKUP,
            points=2,
            message=(
                "Storage technology is unknown, which may "
                "affect the appropriate sanitization method."
            ),
        )


# ============================================================
# UNCERTAINTY COLLECTION
# ============================================================

def _collect_uncertainties(
    data: Mapping[str, Any],
) -> tuple[str, ...]:
    """
    Return human-readable descriptions of fields whose
    values remain uncertain.
    """

    field_labels = {
        FIELD_OPERATING_SYSTEM: "Operating system",
        FIELD_STORAGE_TYPE: "Storage type",
        FIELD_PERSONAL_DATA: "Personal data",
        FIELD_SENSITIVE_DATA: "Sensitive data",
        FIELD_DATA_BACKED_UP: "Backup status",
        FIELD_FACTORY_RESET: "Factory-reset status",
        FIELD_SECURE_ERASE: "Secure-erasure status",
        FIELD_ENCRYPTION: "Encryption status",
        FIELD_ACCOUNTS_SIGNED_OUT: "Account sign-out status",
        FIELD_REMOVABLE_MEDIA_REMOVED: (
            "SIM / memory-card removal status"
        ),
        FIELD_DISPOSAL_METHOD: "Disposal method",
    }

    uncertainties: list[str] = []

    for field_name, label in field_labels.items():

        value = data.get(
            field_name
        )

        if value in UNCERTAIN_VALUES:

            uncertainties.append(
                f"{label}: {value}"
            )

    return tuple(
        uncertainties
    )


# ============================================================
# FINAL RISK LEVEL
# ============================================================

def _risk_level_from_score(
    score: int,
) -> str:
    """
    Convert a 0-100 score to the canonical EcoShield
    Low / Medium / High risk levels.
    """

    if score <= LOW_RISK_MAX:
        return RISK_LOW

    if score <= MEDIUM_RISK_MAX:
        return RISK_MEDIUM

    return RISK_HIGH


# ============================================================
# SANITIZATION REQUIREMENT
# ============================================================

def _requires_sanitization(
    data: Mapping[str, Any],
) -> bool:
    """
    Determine whether the current device state indicates
    that sanitization should be considered before transfer.

    This is a decision-support flag, not a specific
    sanitization-method instruction.
    """

    data_present = _data_may_exist(
        data
    )

    if not data_present:
        return False

    secure_erase = data.get(
        FIELD_SECURE_ERASE
    )

    factory_reset = data.get(
        FIELD_FACTORY_RESET
    )

    accounts_signed_out = data.get(
        FIELD_ACCOUNTS_SIGNED_OUT
    )

    media_removed = data.get(
        FIELD_REMOVABLE_MEDIA_REMOVED
    )

    unfinished_controls = {
        "No",
        "Unsure",
    }

    return (
        secure_erase in unfinished_controls
        or factory_reset in unfinished_controls
        or accounts_signed_out in unfinished_controls
        or media_removed in unfinished_controls
    )


# ============================================================
# SCORE CALCULATION
# ============================================================

def _calculate_total_score(
    category_scores: Mapping[str, int],
) -> int:
    """
    Calculate and clamp final risk score to 0-100.
    """

    score = sum(
        category_scores.values()
    )

    return max(
        MIN_RISK_SCORE,
        min(
            int(score),
            MAX_RISK_SCORE,
        ),
    )


# ============================================================
# PRIMARY PUBLIC RISK ASSESSMENT
# ============================================================

def assess_device_risk(
    payload: Mapping[str, Any],
) -> RiskAssessment:
    """
    Perform a complete EcoShield security-risk assessment.

    The payload may contain raw user input or already normalized
    validator output. It is validated defensively before scoring.

    Parameters
    ----------
    payload:
        EcoShield device assessment mapping.

    Returns
    -------
    RiskAssessment
        Structured, explainable security-risk assessment.

    Raises
    ------
    TypeError
        If the payload is not dictionary-like.

    ValueError
        If device information fails EcoShield validation.
    """

    validation = validate_device_input(
        payload
    )

    if not validation.is_valid:

        formatted_errors = "; ".join(
            validation.errors
        )

        raise ValueError(
            "Device assessment cannot be scored because "
            f"validation failed: {formatted_errors}"
        )

    data = validation.data

    factors: list[RiskFactor] = []

    category_scores = (
        _new_category_scores()
    )

    # --------------------------------------------------------
    # Category 1: Data exposure
    # --------------------------------------------------------

    _assess_data_exposure(
        data,
        factors,
        category_scores,
    )

    # --------------------------------------------------------
    # Category 2: Sanitization
    # --------------------------------------------------------

    _assess_sanitization(
        data,
        factors,
        category_scores,
    )

    # --------------------------------------------------------
    # Category 3: Transfer / disposal
    # --------------------------------------------------------

    _assess_transfer_context(
        data,
        factors,
        category_scores,
    )

    # --------------------------------------------------------
    # Category 4: Accessibility / condition
    # --------------------------------------------------------

    _assess_accessibility_condition(
        data,
        factors,
        category_scores,
    )

    # --------------------------------------------------------
    # Category 5: Media / backup
    # --------------------------------------------------------

    _assess_media_backup(
        data,
        factors,
        category_scores,
    )

    # --------------------------------------------------------
    # Final score
    # --------------------------------------------------------

    score = _calculate_total_score(
        category_scores
    )

    risk_level = (
        _risk_level_from_score(
            score
        )
    )

    uncertainties = (
        _collect_uncertainties(
            data
        )
    )

    device_leaves_owner = (
        data.get(
            FIELD_DISPOSAL_METHOD
        )
        in DEVICE_LEAVES_OWNER_ACTIONS
    )

    requires_sanitization = (
        _requires_sanitization(
            data
        )
    )

    return RiskAssessment(
        score=score,
        risk_level=risk_level,
        factors=tuple(factors),
        category_scores=dict(
            category_scores
        ),
        uncertainties=uncertainties,
        validated_data=dict(data),
        requires_sanitization=requires_sanitization,
        device_leaves_owner=device_leaves_owner,
    )


# ============================================================
# CONVENIENCE FUNCTION: SCORE ONLY
# ============================================================

def get_risk_score(
    payload: Mapping[str, Any],
) -> int:
    """
    Return only the final 0-100 risk score.
    """

    return assess_device_risk(
        payload
    ).score


# ============================================================
# CONVENIENCE FUNCTION: LEVEL ONLY
# ============================================================

def get_risk_level(
    payload: Mapping[str, Any],
) -> str:
    """
    Return only Low / Medium / High risk level.
    """

    return assess_device_risk(
        payload
    ).risk_level