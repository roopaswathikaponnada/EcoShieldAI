"""
EcoShield AI
Security and Sustainability Recommendation Engine

This module converts an EcoShield cybersecurity RiskAssessment
into structured, explainable security and sustainability guidance.

Responsibilities:
- Interpret deterministic risk-engine results
- Determine whether a device is ready for transfer/disposal
- Generate prioritized security actions
- Generate sustainability-oriented recommendations
- Produce ordered next steps
- Preserve explainability through stable recommendation codes
- Provide a stable interface for later RAG + LLM enrichment

Important:
This module does NOT calculate cybersecurity risk.
Risk scoring belongs exclusively to src/risk_engine.py.

This module also deliberately avoids inventing detailed
sanitization procedures. Later RAG components will retrieve
authoritative guidance for device/storage-specific procedures.
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

from src.risk_engine import (
    RiskAssessment,
    assess_device_risk,
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
# RECOMMENDATION PRIORITIES
# ============================================================

PRIORITY_CRITICAL = "Critical"

PRIORITY_HIGH = "High"

PRIORITY_MEDIUM = "Medium"

PRIORITY_LOW = "Low"


PRIORITY_ORDER = {
    PRIORITY_CRITICAL: 0,
    PRIORITY_HIGH: 1,
    PRIORITY_MEDIUM: 2,
    PRIORITY_LOW: 3,
}


# ============================================================
# RECOMMENDATION CATEGORIES
# ============================================================

CATEGORY_SECURITY = "Security"

CATEGORY_PRIVACY = "Privacy"

CATEGORY_DATA_PROTECTION = "Data Protection"

CATEGORY_ACCOUNT_SECURITY = "Account Security"

CATEGORY_DEVICE_PREPARATION = "Device Preparation"

CATEGORY_SUSTAINABILITY = "Sustainability"

CATEGORY_DISPOSAL = "Disposal"

CATEGORY_UNCERTAINTY = "Uncertainty"

CATEGORY_ORDER = {
    CATEGORY_SECURITY: 0,
    CATEGORY_DATA_PROTECTION: 1,
    CATEGORY_ACCOUNT_SECURITY: 2,
    CATEGORY_DEVICE_PREPARATION: 3,
    CATEGORY_PRIVACY: 4,
    CATEGORY_UNCERTAINTY: 5,
    CATEGORY_DISPOSAL: 6,
    CATEGORY_SUSTAINABILITY: 7,
}
# ============================================================
# DISPOSAL READINESS
# ============================================================

READINESS_READY = "Ready"

READINESS_CONDITIONAL = "Conditional"

READINESS_NOT_READY = "Not Ready"


# ============================================================
# RECOMMENDATION SOURCES
# ============================================================

SOURCE_RULE_ENGINE = "EcoShield deterministic rules"

SOURCE_RAG = "Retrieved guidance"

SOURCE_AI = "AI-assisted explanation"


# ============================================================
# ACTION GROUPS
# ============================================================

OWNERSHIP_TRANSFER_ACTIONS = {
    "Sell",
    "Donate",
}

FINAL_DISPOSAL_ACTIONS = {
    "Recycle",
    "Dispose",
}

REUSE_ACTIONS = {
    "Reuse",
}

REPAIR_ACTIONS = {
    "Repair",
}


# ============================================================
# SECURITY FACTOR GROUPS
# ============================================================

DATA_EXPOSURE_FACTORS = {
    "PERSONAL_DATA_PRESENT",
    "PERSONAL_DATA_UNCERTAIN",
    "SENSITIVE_DATA_PRESENT",
    "SENSITIVE_DATA_UNCERTAIN",
    "ENCRYPTION_DISABLED",
    "ENCRYPTION_UNCERTAIN",
}


SANITIZATION_FACTORS = {
    "SECURE_ERASE_NOT_PERFORMED",
    "SECURE_ERASE_UNCERTAIN",
    "FACTORY_RESET_NOT_PERFORMED",
    "FACTORY_RESET_UNCERTAIN",
    "ACCOUNTS_NOT_SIGNED_OUT",
    "ACCOUNT_SIGNOUT_UNCERTAIN",
}


ACCESSIBILITY_FACTORS = {
    "DEVICE_INACCESSIBLE",
    "DEVICE_CANNOT_POWER_ON",
    "PHYSICAL_DAMAGE",
    "DEVICE_NOT_WORKING",
    "DEVICE_PARTIALLY_WORKING",
}


MEDIA_BACKUP_FACTORS = {
    "REMOVABLE_MEDIA_PRESENT",
    "REMOVABLE_MEDIA_UNCERTAIN",
    "BACKUP_NOT_COMPLETED",
    "BACKUP_UNCERTAIN",
    "STORAGE_TYPE_UNKNOWN",
}


# ============================================================
# RECOMMENDATION ITEM
# ============================================================

@dataclass(frozen=True)
class RecommendationItem:
    """
    A single actionable EcoShield recommendation.

    Attributes
    ----------
    code:
        Stable machine-readable recommendation identifier.

    category:
        Recommendation category.

    priority:
        Critical, High, Medium, or Low.

    title:
        Short user-facing action title.

    action:
        What the user should do.

    rationale:
        Why the action is recommended.

    source:
        Origin of the recommendation.

        Initially this will normally be:
        "EcoShield deterministic rules"

        Later RAG / AI enrichment can populate other sources.

    evidence:
        Supporting retrieved evidence references.

        Empty during the deterministic stage and populated
        later by the RAG pipeline.
    """

    code: str

    category: str

    priority: str

    title: str

    action: str

    rationale: str

    source: str = SOURCE_RULE_ENGINE

    evidence: tuple[str, ...] = field(
        default_factory=tuple
    )


# ============================================================
# RECOMMENDATION RESULT
# ============================================================

@dataclass(frozen=True)
class RecommendationResult:
    """
    Final structured EcoShield recommendation output.

    Attributes
    ----------
    risk_score:
        Deterministic 0-100 score from risk_engine.py.

    risk_level:
        Low / Medium / High.

    readiness:
        Ready / Conditional / Not Ready.

    summary:
        Short deterministic summary.

    security_actions:
        Prioritized cybersecurity/privacy actions.

    sustainability_actions:
        Sustainability-oriented recommendations.

    next_steps:
        Ordered action titles intended for UI display.

    warnings:
        Important decision-support notices.

    assessment:
        Full RiskAssessment used to create recommendations.

    ai_explanation:
        Optional future AI-generated explanation.

        Left as None during the deterministic stage.

    retrieved_context:
        Optional future RAG context.

        Left empty during the deterministic stage.
    """

    risk_score: int

    risk_level: str

    readiness: str

    summary: str

    security_actions: tuple[
        RecommendationItem,
        ...
    ] = field(
        default_factory=tuple
    )

    sustainability_actions: tuple[
        RecommendationItem,
        ...
    ] = field(
        default_factory=tuple
    )

    next_steps: tuple[str, ...] = field(
        default_factory=tuple
    )

    warnings: tuple[str, ...] = field(
        default_factory=tuple
    )

    assessment: RiskAssessment | None = None

    ai_explanation: str | None = None

    retrieved_context: tuple[str, ...] = field(
        default_factory=tuple
    )

    used_ai: bool = False

    used_fallback: bool = False

    def to_dict(self) -> dict[str, Any]:
        """
        Return a serializable dictionary representation.

        Useful for:
        - Streamlit
        - reports
        - JSON APIs
        - future RAG / LLM prompts
        """

        return asdict(self)


# ============================================================
# INTERNAL RECOMMENDATION ADDER
# ============================================================

def _add_recommendation(
    recommendations: list[RecommendationItem],
    *,
    code: str,
    category: str,
    priority: str,
    title: str,
    action: str,
    rationale: str,
) -> None:
    """
    Add a recommendation only when its code has not already
    been generated.

    This prevents duplicate advice from overlapping rules.
    """

    existing_codes = {
        item.code
        for item in recommendations
    }

    if code in existing_codes:
        return

    recommendations.append(
        RecommendationItem(
            code=code,
            category=category,
            priority=priority,
            title=title,
            action=action,
            rationale=rationale,
        )
    )


# ============================================================
# PRIORITY SORTING
# ============================================================

def _sort_recommendations(
    recommendations: list[RecommendationItem],
) -> tuple[RecommendationItem, ...]:
    """
    Sort recommendations from most to least important.
    """

    return tuple(
        sorted(
            recommendations,
            key=lambda item: (
    PRIORITY_ORDER.get(
        item.priority,
        99,
    ),
    CATEGORY_ORDER.get(
        item.category,
        99,
    ),
    item.code,
),
        )
    )


# ============================================================
# RISK FACTOR CODE EXTRACTION
# ============================================================

def _factor_codes(
    assessment: RiskAssessment,
) -> set[str]:
    """
    Return all machine-readable risk-factor codes.
    """

    return {
        factor.code
        for factor in assessment.factors
    }


# ============================================================
# DATA PRESENCE HELPERS
# ============================================================

def _data_may_exist(
    data: Mapping[str, Any],
) -> bool:
    """
    Return whether personal or sensitive data is known
    or potentially present.
    """

    return (
        data.get(
            FIELD_PERSONAL_DATA
        )
        in {
            "Yes",
            "Unsure",
        }
        or data.get(
            FIELD_SENSITIVE_DATA
        )
        in {
            "Yes",
            "Unsure",
        }
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
# TRANSFER READINESS
# ============================================================

def _determine_readiness(
    assessment: RiskAssessment,
) -> str:
    """
    Determine whether the selected device action is currently
    ready to proceed.

    Readiness is action-aware:

    - External transfer/disposal is blocked when unresolved
      sanitization requirements remain.
    - High-risk assessments that do not involve ownership
      transfer are treated conservatively as Conditional.
    - Medium risk or unresolved uncertainty is Conditional.
    - Low-risk assessments without blocking conditions are
      Ready.
    """

    leaves_owner = (
        assessment.device_leaves_owner
    )

    # --------------------------------------------------------
    # External transfer + unresolved sanitization
    # --------------------------------------------------------

    if (
        leaves_owner
        and assessment.requires_sanitization
    ):
        return READINESS_NOT_READY

    # --------------------------------------------------------
    # High risk during external transfer
    # --------------------------------------------------------

    if (
        leaves_owner
        and assessment.risk_level == RISK_HIGH
    ):
        return READINESS_NOT_READY

    # --------------------------------------------------------
    # High risk while device remains with owner
    # --------------------------------------------------------

    if assessment.risk_level == RISK_HIGH:
        return READINESS_CONDITIONAL

    # --------------------------------------------------------
    # Medium cybersecurity risk
    # --------------------------------------------------------

    if assessment.risk_level == RISK_MEDIUM:
        return READINESS_CONDITIONAL

    # --------------------------------------------------------
    # Remaining uncertainty
    # --------------------------------------------------------

    if assessment.uncertainties:
        return READINESS_CONDITIONAL

    return READINESS_READY

# ============================================================
# SUMMARY GENERATION
# ============================================================

def _build_summary(
    assessment: RiskAssessment,
    readiness: str,
) -> str:
    """
    Generate a concise deterministic assessment summary.
    """

    data = assessment.validated_data

    device_type = data.get(
        FIELD_DEVICE_TYPE,
        "Device",
    )

    disposal_method = data.get(
        FIELD_DISPOSAL_METHOD,
        "selected action",
    )

    if readiness == READINESS_NOT_READY:

        return (
            f"{device_type} is currently assessed as "
            f"{assessment.risk_level} security risk "
            f"({assessment.score}/100) and is not ready "
            f"to proceed with '{disposal_method}' until "
            "the identified security actions are addressed."
        )

    if readiness == READINESS_CONDITIONAL:

        return (
            f"{device_type} is assessed as "
            f"{assessment.risk_level} security risk "
            f"({assessment.score}/100). The selected action "
            f"'{disposal_method}' may proceed only after "
            "the highlighted conditions and uncertainties "
            "are reviewed."
        )

    return (
        f"{device_type} is assessed as "
        f"{assessment.risk_level} security risk "
        f"({assessment.score}/100) and no blocking "
        "security condition has been identified for the "
        f"selected action '{disposal_method}'."
    )


# ============================================================
# BACKUP RECOMMENDATIONS
# ============================================================

def _recommend_backup(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Recommend backup when relevant data exists and backup
    preparation is incomplete or uncertain.
    """

    data = assessment.validated_data

    if not _data_may_exist(data):
        return

    backup = data.get(
        FIELD_DATA_BACKED_UP
    )

    if backup == "No":

        _add_recommendation(
            recommendations,
            code="COMPLETE_BACKUP",
            category=CATEGORY_DATA_PROTECTION,
            priority=PRIORITY_HIGH,
            title="Back up important data",
            action=(
                "Create and verify a backup of information "
                "that must be retained before performing "
                "reset, sanitization, repair, or disposal."
            ),
            rationale=(
                "Data is reported to be present and the "
                "assessment indicates that a backup has "
                "not been completed."
            ),
        )

    elif backup == "Unsure":

        _add_recommendation(
            recommendations,
            code="VERIFY_BACKUP",
            category=CATEGORY_DATA_PROTECTION,
            priority=PRIORITY_MEDIUM,
            title="Verify backup status",
            action=(
                "Confirm whether important information has "
                "been safely backed up before continuing."
            ),
            rationale=(
                "The current backup status is uncertain."
            ),
        )


# ============================================================
# ACCOUNT SECURITY RECOMMENDATIONS
# ============================================================

def _recommend_account_security(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Recommend account/session preparation.
    """

    data = assessment.validated_data

    account_status = data.get(
        FIELD_ACCOUNTS_SIGNED_OUT
    )

    if account_status == "No":

        _add_recommendation(
            recommendations,
            code="SIGN_OUT_ACCOUNTS",
            category=CATEGORY_ACCOUNT_SECURITY,
            priority=PRIORITY_HIGH,
            title="Sign out of device accounts",
            action=(
                "Sign out of user accounts and remove "
                "device-linked account access before the "
                "device leaves your control."
            ),
            rationale=(
                "The assessment indicates that one or more "
                "accounts may still be signed in."
            ),
        )

    elif account_status == "Unsure":

        _add_recommendation(
            recommendations,
            code="VERIFY_ACCOUNT_SIGNOUT",
            category=CATEGORY_ACCOUNT_SECURITY,
            priority=PRIORITY_MEDIUM,
            title="Verify account sign-out",
            action=(
                "Confirm that active user accounts and "
                "sessions are no longer accessible from "
                "the device."
            ),
            rationale=(
                "Account sign-out status is uncertain."
            ),
        )


# ============================================================
# REMOVABLE MEDIA RECOMMENDATIONS
# ============================================================

def _recommend_removable_media(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Recommend removal or verification of SIM cards and
    removable storage.
    """

    data = assessment.validated_data

    media_status = data.get(
        FIELD_REMOVABLE_MEDIA_REMOVED
    )

    if media_status == "No":

        _add_recommendation(
            recommendations,
            code="REMOVE_REMOVABLE_MEDIA",
            category=CATEGORY_DEVICE_PREPARATION,
            priority=PRIORITY_HIGH,
            title="Remove removable media",
            action=(
                "Remove any SIM card or removable memory "
                "card before transfer, repair, recycling, "
                "or disposal."
            ),
            rationale=(
                "Removable media may still contain personal "
                "or account-related information."
            ),
        )

    elif media_status == "Unsure":

        _add_recommendation(
            recommendations,
            code="VERIFY_REMOVABLE_MEDIA",
            category=CATEGORY_DEVICE_PREPARATION,
            priority=PRIORITY_MEDIUM,
            title="Check for removable media",
            action=(
                "Inspect the device and confirm whether "
                "any SIM card or removable memory card "
                "is present."
            ),
            rationale=(
                "The removable-media status is uncertain."
            ),
        )


# ============================================================
# SANITIZATION RECOMMENDATIONS
# ============================================================

def _recommend_sanitization(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Recommend appropriate sanitization preparation.

    Detailed technical sanitization methods are deliberately
    deferred to the future RAG knowledge layer.
    """

    data = assessment.validated_data

    data_may_exist = _data_may_exist(
        data
    )

    secure_erase = data.get(
        FIELD_SECURE_ERASE
    )

    factory_reset = data.get(
        FIELD_FACTORY_RESET
    )

    storage_type = data.get(
        FIELD_STORAGE_TYPE
    )

    accessible = data.get(
        FIELD_DEVICE_ACCESSIBLE
    )

    power_on = data.get(
        FIELD_POWER_ON
    )

    # --------------------------------------------------------
    # Secure erase
    # --------------------------------------------------------

    if (
        data_may_exist
        and secure_erase == "No"
    ):

        priority = (
            PRIORITY_CRITICAL
            if assessment.device_leaves_owner
            else PRIORITY_HIGH
        )

        _add_recommendation(
            recommendations,
            code="PERFORM_SECURE_SANITIZATION",
            category=CATEGORY_SECURITY,
            priority=priority,
            title="Complete secure data sanitization",
            action=(
                "Do not transfer the device until an "
                "appropriate storage-specific data "
                "sanitization process has been completed."
            ),
            rationale=(
                "Data may remain on the device and secure "
                "erasure has not been performed."
            ),
        )

    elif (
        data_may_exist
        and secure_erase == "Unsure"
    ):

        _add_recommendation(
            recommendations,
            code="VERIFY_SECURE_SANITIZATION",
            category=CATEGORY_SECURITY,
            priority=PRIORITY_HIGH,
            title="Verify secure data sanitization",
            action=(
                "Confirm whether an appropriate secure "
                "sanitization process has already been "
                "completed."
            ),
            rationale=(
                "Secure-erasure status is uncertain."
            ),
        )

    # --------------------------------------------------------
    # Factory reset
    # --------------------------------------------------------

    if factory_reset == "No":

        _add_recommendation(
            recommendations,
            code="COMPLETE_FACTORY_RESET",
            category=CATEGORY_DEVICE_PREPARATION,
            priority=PRIORITY_HIGH,
            title="Complete device reset",
            action=(
                "Complete the appropriate device reset "
                "process as part of preparation for the "
                "selected action."
            ),
            rationale=(
                "The assessment indicates that a factory "
                "reset has not been performed."
            ),
        )

    elif factory_reset == "Unsure":

        _add_recommendation(
            recommendations,
            code="VERIFY_FACTORY_RESET",
            category=CATEGORY_DEVICE_PREPARATION,
            priority=PRIORITY_MEDIUM,
            title="Verify reset status",
            action=(
                "Confirm whether the device reset process "
                "has already been completed."
            ),
            rationale=(
                "Factory-reset status is uncertain."
            ),
        )

    # --------------------------------------------------------
    # Unknown storage
    # --------------------------------------------------------

    if storage_type == "Unknown":

        _add_recommendation(
            recommendations,
            code="IDENTIFY_STORAGE_TYPE",
            category=CATEGORY_SECURITY,
            priority=PRIORITY_HIGH,
            title="Identify the storage technology",
            action=(
                "Determine the device's storage technology "
                "before selecting a sanitization approach."
            ),
            rationale=(
                "Appropriate sanitization guidance depends "
                "on the storage technology."
            ),
        )

    # --------------------------------------------------------
    # Device unavailable for normal sanitization
    # --------------------------------------------------------

    if (
        data_may_exist
        and (
            accessible == "No"
            or power_on == "No"
        )
    ):

        _add_recommendation(
            recommendations,
            code="USE_ALTERNATIVE_SANITIZATION_PATH",
            category=CATEGORY_SECURITY,
            priority=PRIORITY_HIGH,
            title="Use an alternative sanitization path",
            action=(
                "Because normal software-based preparation "
                "may not be possible, obtain appropriate "
                "device/storage-specific sanitization "
                "guidance before transfer or disposal."
            ),
            rationale=(
                "The device is inaccessible or cannot "
                "power on."
            ),
        )


# ============================================================
# ENCRYPTION RECOMMENDATIONS
# ============================================================

def _recommend_encryption_review(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Generate encryption-related recommendations.
    """

    data = assessment.validated_data

    if not _data_may_exist(data):
        return

    encryption = data.get(
        FIELD_ENCRYPTION
    )

    if encryption == "No":

        _add_recommendation(
            recommendations,
            code="UNENCRYPTED_DATA_CAUTION",
            category=CATEGORY_PRIVACY,
            priority=(
                PRIORITY_HIGH
                if _sensitive_data_may_exist(data)
                else PRIORITY_MEDIUM
            ),
            title="Treat stored data as exposed",
            action=(
                "Use additional caution when preparing "
                "the device because stored data is not "
                "protected by device encryption."
            ),
            rationale=(
                "The assessment reports that encryption "
                "is disabled while data may remain."
            ),
        )

    elif encryption == "Unsure":

        _add_recommendation(
            recommendations,
            code="VERIFY_ENCRYPTION_STATUS",
            category=CATEGORY_PRIVACY,
            priority=PRIORITY_MEDIUM,
            title="Verify encryption status",
            action=(
                "Confirm whether device or storage "
                "encryption is enabled before determining "
                "the final security preparation."
            ),
            rationale=(
                "Encryption status is uncertain."
            ),
        )


# ============================================================
# TRANSFER / DISPOSAL RECOMMENDATIONS
# ============================================================

def _recommend_transfer_controls(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Generate recommendations related to ownership transfer,
    repair, recycling, and disposal.
    """

    data = assessment.validated_data

    method = data.get(
        FIELD_DISPOSAL_METHOD
    )

    if (
    assessment.device_leaves_owner
    and assessment.requires_sanitization
):

        _add_recommendation(
            recommendations,
            code="BLOCK_TRANSFER_UNTIL_SECURE",
            category=CATEGORY_SECURITY,
            priority=PRIORITY_CRITICAL,
            title="Do not transfer the device yet",
            action=(
                "Complete the outstanding security and "
                "data-preparation actions before the device "
                "leaves your control."
            ),
            rationale=(
                "The selected action transfers control of "
                "the device while sanitization requirements "
                "remain unresolved."
            ),
        )

    if method == "Repair":

        _add_recommendation(
            recommendations,
            code="PREPARE_FOR_REPAIR",
            category=CATEGORY_PRIVACY,
            priority=PRIORITY_MEDIUM,
            title="Prepare the device for third-party repair",
            action=(
    "Back up required information, remove "
    "unnecessary sensitive data where practical, "
    "remove removable media where appropriate, "
    "and review account access before handing "
    "the device to a repair provider."
),
            rationale=(
                "Repair can expose the device to a "
                "third-party service provider."
            ),
        )

    if method == "Not Decided":

        _add_recommendation(
            recommendations,
            code="SELECT_DISPOSAL_METHOD",
            category=CATEGORY_DISPOSAL,
            priority=PRIORITY_LOW,
            title="Choose the intended device action",
            action=(
                "Decide whether the device will be reused, "
                "repaired, sold, donated, recycled, or "
                "disposed of before final preparation."
            ),
            rationale=(
                "Security and sustainability guidance "
                "depends partly on the intended action."
            ),
        )


# ============================================================
# UNCERTAINTY RECOMMENDATIONS
# ============================================================

def _recommend_uncertainty_resolution(
    assessment: RiskAssessment,
    recommendations: list[RecommendationItem],
) -> None:
    """
    Encourage users to resolve important unknown values.
    """

    if not assessment.uncertainties:
        return

    _add_recommendation(
        recommendations,
        code="RESOLVE_ASSESSMENT_UNCERTAINTY",
        category=CATEGORY_UNCERTAINTY,
        priority=PRIORITY_MEDIUM,
        title="Resolve uncertain device information",
        action=(
            "Verify the unknown or unsure assessment fields "
            "before making the final disposal decision."
        ),
        rationale=(
            "One or more security-relevant properties of "
            "the device remain uncertain."
        ),
    )


# ============================================================
# SUSTAINABILITY RECOMMENDATIONS
# ============================================================

def _generate_sustainability_actions(
    assessment: RiskAssessment,
) -> tuple[RecommendationItem, ...]:
    """
    Generate sustainability-oriented device recommendations.

    Cybersecurity preparation remains a prerequisite whenever
    the device may leave the owner's control.
    """

    data = assessment.validated_data

    recommendations: list[
        RecommendationItem
    ] = []

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    disposal_method = data.get(
        FIELD_DISPOSAL_METHOD
    )

    age = data.get(
        FIELD_DEVICE_AGE
    )

    # --------------------------------------------------------
    # Working device
    # --------------------------------------------------------

    if condition == "Working":

        _add_recommendation(
            recommendations,
            code="PREFER_REUSE_FOR_WORKING_DEVICE",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_MEDIUM,
            title="Prefer continued use or reuse",
            action=(
                "Where practical, extend the useful life of "
                "the working device through continued use, "
                "reuse, responsible resale, or donation "
                "after security preparation is complete."
            ),
            rationale=(
                "Extending the useful life of functional "
                "electronics can avoid unnecessary premature "
                "disposal."
            ),
        )

    # --------------------------------------------------------
    # Partially working device
    # --------------------------------------------------------

    elif condition == "Partially Working":

        _add_recommendation(
            recommendations,
            code="CONSIDER_REPAIR_OR_REFURBISHMENT",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_MEDIUM,
            title="Consider repair or refurbishment",
            action=(
                "Assess whether repair or refurbishment "
                "can safely extend the device's useful life "
                "before choosing disposal."
            ),
            rationale=(
                "A partially working device may still retain "
                "significant reuse value."
            ),
        )

    # --------------------------------------------------------
    # Not working / physically damaged
    # --------------------------------------------------------

    elif condition in {
        "Not Working",
        "Physically Damaged",
    }:

        _add_recommendation(
            recommendations,
            code="ASSESS_RECOVERY_BEFORE_RECYCLING",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_MEDIUM,
            title="Assess repairability before final disposal",
            action=(
                "Determine whether safe repair, component "
                "recovery, refurbishment, or responsible "
                "electronics recycling is appropriate."
            ),
            rationale=(
                "Non-working electronics may still contain "
                "reusable components and recyclable materials."
            ),
        )
    # --------------------------------------------------------
    # Explicit reuse choice
    # --------------------------------------------------------

    if disposal_method in REUSE_ACTIONS:

        _add_recommendation(
            recommendations,
            code="SUPPORT_CONTINUED_REUSE",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_LOW,
            title="Support continued device reuse",
            action=(
                "Continue using the device while it remains "
                "safe, functional, and suitable for its "
                "intended purpose."
            ),
            rationale=(
                "Continued responsible use can extend the "
                "device lifecycle and delay unnecessary "
                "replacement or disposal."
            ),
        )

    # --------------------------------------------------------
    # Explicit recycling choice
    # --------------------------------------------------------

    if disposal_method == "Recycle":

        _add_recommendation(
            recommendations,
            code="USE_RESPONSIBLE_EWASTE_CHANNEL",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_HIGH,
            title="Use an appropriate e-waste recycling channel",
            action=(
    "If continued use, reuse, repair, or refurbishment is "
    "not practical and recycling remains the selected "
    "lifecycle path, use an authorized or otherwise "
    "appropriate electronics collection or recycling "
    "channel after required security preparation is "
    "complete."
           ),
            rationale=(
                "Responsible e-waste recycling helps route "
                "electronic equipment toward appropriate "
                "material recovery and handling."
            ),
        )

    # --------------------------------------------------------
    # Explicit disposal choice
    # --------------------------------------------------------

    elif disposal_method == "Dispose":

        _add_recommendation(
            recommendations,
            code="PREFER_EWASTE_CHANNEL_OVER_GENERAL_DISPOSAL",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_HIGH,
            title="Avoid ordinary waste disposal",
            action=(
    "If continued use, reuse, repair, or refurbishment is "
    "not practical, prefer an appropriate e-waste "
    "collection or recycling channel over ordinary waste "
    "disposal after required security preparation is "
    "complete."
            ),
            rationale=(
                "Electronic equipment may contain recoverable "
                "materials and should be directed to suitable "
                "e-waste handling channels where available."
            ),
        )
    # --------------------------------------------------------
    # Repair choice
    # --------------------------------------------------------

    if disposal_method in REPAIR_ACTIONS:

        _add_recommendation(
            recommendations,
            code="SUPPORT_LIFETIME_EXTENSION",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_LOW,
            title="Extend device life where practical",
            action=(
                "If repair is technically and economically "
                "reasonable, restoring the device can extend "
                "its useful life."
            ),
            rationale=(
                "Repair can delay replacement and reduce "
                "premature electronic waste."
            ),
        )

    # --------------------------------------------------------
    # Older device
    # --------------------------------------------------------

    if (
        isinstance(
            age,
            (int, float),
        )
        and age >= 10
    ):

        _add_recommendation(
            recommendations,
            code="ASSESS_OLD_DEVICE_VIABILITY",
            category=CATEGORY_SUSTAINABILITY,
            priority=PRIORITY_LOW,
            title="Assess older-device viability",
            action=(
                "Review the device's reliability, "
                "repairability, energy use, and practical "
                "reuse value before choosing between continued "
                "use, repair, reuse, or recycling."
            ),
            rationale=(
                "Older hardware may require a more balanced "
                "reuse-versus-recycling decision."
            ),
        )

    return _sort_recommendations(
        recommendations
    )


# ============================================================
# SECURITY RECOMMENDATION GENERATION
# ============================================================

def _generate_security_actions(
    assessment: RiskAssessment,
) -> tuple[RecommendationItem, ...]:
    """
    Generate complete security/privacy recommendations.
    """

    recommendations: list[
        RecommendationItem
    ] = []

    _recommend_backup(
        assessment,
        recommendations,
    )

    _recommend_account_security(
        assessment,
        recommendations,
    )

    _recommend_removable_media(
        assessment,
        recommendations,
    )

    _recommend_sanitization(
        assessment,
        recommendations,
    )

    _recommend_encryption_review(
        assessment,
        recommendations,
    )

    _recommend_transfer_controls(
        assessment,
        recommendations,
    )

    _recommend_uncertainty_resolution(
        assessment,
        recommendations,
    )

    return _sort_recommendations(
        recommendations
    )


# ============================================================
# WARNING GENERATION
# ============================================================

def _build_warnings(
    assessment: RiskAssessment,
    readiness: str,
) -> tuple[str, ...]:
    """
    Build high-level recommendation warnings.
    """

    warnings: list[str] = []

    if readiness == READINESS_NOT_READY:

        warnings.append(
            "Do not proceed with the selected transfer or "
            "disposal action until the blocking security "
            "issues have been addressed."
        )

    if assessment.requires_sanitization:

        warnings.append(
            "Data sanitization requirements remain unresolved."
        )

    if assessment.uncertainties:

        warnings.append(
            "The assessment contains uncertain values; "
            "final guidance should be reviewed after those "
            "details are confirmed."
        )

    warnings.append(
        "EcoShield provides decision-support guidance and "
        "does not replace applicable manufacturer, "
        "organizational, regulatory, or certified recycling "
        "requirements."
    )

    return tuple(
        dict.fromkeys(
            warnings
        )
    )

# ============================================================
# NEXT-STEP EXECUTION ORDER
# ============================================================

NEXT_STEP_ORDER = {
    # Immediate transfer blocker
    "BLOCK_TRANSFER_UNTIL_SECURE": 0,

    # Preserve required information first
    "COMPLETE_BACKUP": 10,
    "VERIFY_BACKUP": 11,

    # Resolve device/security uncertainty
    "RESOLVE_ASSESSMENT_UNCERTAINTY": 20,
    "IDENTIFY_STORAGE_TYPE": 21,
    "VERIFY_ENCRYPTION_STATUS": 22,

    # Account and removable-media preparation
    "SIGN_OUT_ACCOUNTS": 30,
    "VERIFY_ACCOUNT_SIGNOUT": 31,
    "REMOVE_REMOVABLE_MEDIA": 32,
    "VERIFY_REMOVABLE_MEDIA": 33,

    # Device sanitization/reset preparation
    "VERIFY_SECURE_SANITIZATION": 40,
    "PERFORM_SECURE_SANITIZATION": 41,
    "VERIFY_FACTORY_RESET": 42,
    "COMPLETE_FACTORY_RESET": 43,
    "USE_ALTERNATIVE_SANITIZATION_PATH": 44,

    # Other security / transfer preparation
    "UNENCRYPTED_DATA_CAUTION": 50,
    "PREPARE_FOR_REPAIR": 51,
    "SELECT_DISPOSAL_METHOD": 52,

    # Sustainability actions
    "PREFER_REUSE_FOR_WORKING_DEVICE": 100,
    "CONSIDER_REPAIR_OR_REFURBISHMENT": 101,
    "ASSESS_RECOVERY_BEFORE_RECYCLING": 102,
    "SUPPORT_CONTINUED_REUSE": 103,
    "SUPPORT_LIFETIME_EXTENSION": 104,
    "ASSESS_OLD_DEVICE_VIABILITY": 105,
    "USE_RESPONSIBLE_EWASTE_CHANNEL": 106,
    "PREFER_EWASTE_CHANNEL_OVER_GENERAL_DISPOSAL": 107,
}

# ============================================================
# NEXT STEP GENERATION
# ============================================================

def _build_next_steps(
    security_actions: tuple[
        RecommendationItem,
        ...
    ],
    sustainability_actions: tuple[
        RecommendationItem,
        ...
    ],
) -> tuple[str, ...]:
    """
    Build concise user-facing next steps in a safe,
    deterministic execution order.

    Recommendation-card priority and execution order are
    intentionally separate. For example, required backups
    should occur before destructive sanitization actions even
    when sanitization carries a higher risk priority.

    Security preparation remains ahead of sustainability
    actions.
    """

    security_items = sorted(
        security_actions,
        key=lambda item: (
            NEXT_STEP_ORDER.get(
                item.code,
                90,
            ),
            PRIORITY_ORDER.get(
                item.priority,
                99,
            ),
            item.code,
        ),
    )

    sustainability_items = sorted(
        sustainability_actions,
        key=lambda item: (
            NEXT_STEP_ORDER.get(
                item.code,
                999,
            ),
            PRIORITY_ORDER.get(
                item.priority,
                99,
            ),
            item.code,
        ),
    )

    ordered_items = (
        security_items
        + sustainability_items
    )

    seen_titles: set[str] = set()

    next_steps: list[str] = []

    for item in ordered_items:

        if item.title in seen_titles:
            continue

        seen_titles.add(
            item.title
        )

        next_steps.append(
            item.title
        )

    return tuple(
        next_steps
    )

# ============================================================
# PRIMARY PUBLIC RECOMMENDATION FUNCTION
# ============================================================

def generate_recommendation(
    assessment_or_payload:
        RiskAssessment | Mapping[str, Any],
) -> RecommendationResult:
    """
    Generate a complete EcoShield recommendation.

    This function accepts either:

    1. A RiskAssessment already produced by risk_engine.py
       OR
    2. A raw/normalized EcoShield device-assessment mapping

    Passing an existing RiskAssessment avoids recalculating
    risk when app.py has already performed the assessment.

    Parameters
    ----------
    assessment_or_payload:
        RiskAssessment or EcoShield input mapping.

    Returns
    -------
    RecommendationResult
        Structured security + sustainability recommendation.

    Raises
    ------
    TypeError
        If the supplied value is neither a RiskAssessment nor
        dictionary-like mapping.

    ValueError
        Propagated from risk_engine.py when input validation
        fails.
    """

    if isinstance(
        assessment_or_payload,
        RiskAssessment,
    ):

        assessment = (
            assessment_or_payload
        )

    elif isinstance(
        assessment_or_payload,
        Mapping,
    ):

        assessment = assess_device_risk(
            assessment_or_payload
        )

    else:

        raise TypeError(
            "Recommendation input must be either a "
            "RiskAssessment or a dictionary-like "
            "device-assessment mapping."
        )

    readiness = _determine_readiness(
        assessment
    )

    security_actions = (
        _generate_security_actions(
            assessment
        )
    )

    sustainability_actions = (
        _generate_sustainability_actions(
            assessment
        )
    )

    summary = _build_summary(
        assessment,
        readiness,
    )

    warnings = _build_warnings(
        assessment,
        readiness,
    )

    next_steps = _build_next_steps(
        security_actions,
        sustainability_actions,
    )

        # --------------------------------------------------------
    # Risk Engine integration invariant
    # --------------------------------------------------------

    risk_score = assessment.score
    risk_level = assessment.risk_level

    if not isinstance(risk_score, int):
        raise TypeError(
            "RiskAssessment.score must be an integer."
        )

    if risk_score < 0 or risk_score > 100:
        raise ValueError(
            "RiskAssessment.score must be between 0 and 100."
        )

    if risk_level not in {
        RISK_LOW,
        RISK_MEDIUM,
        RISK_HIGH,
    }:
        raise ValueError(
            "RiskAssessment.risk_level is not recognized."
        )

    return RecommendationResult(
        risk_score=risk_score,
        risk_level=risk_level,
        readiness=readiness,
        summary=summary,
        security_actions=security_actions,
        sustainability_actions=sustainability_actions,
        next_steps=next_steps,
        warnings=warnings,
        assessment=assessment,
        ai_explanation=None,
        retrieved_context=(),
        used_ai=False,
        used_fallback=False,
    )


# ============================================================
# CONVENIENCE FUNCTION: READINESS ONLY
# ============================================================

def get_disposal_readiness(
    assessment_or_payload:
        RiskAssessment | Mapping[str, Any],
) -> str:
    """
    Return only Ready / Conditional / Not Ready.
    """

    return generate_recommendation(
        assessment_or_payload
    ).readiness


# ============================================================
# CONVENIENCE FUNCTION: SECURITY ACTIONS ONLY
# ============================================================

def get_security_actions(
    assessment_or_payload:
        RiskAssessment | Mapping[str, Any],
) -> tuple[RecommendationItem, ...]:
    """
    Return only prioritized security recommendations.
    """

    return generate_recommendation(
        assessment_or_payload
    ).security_actions


# ============================================================
# CONVENIENCE FUNCTION: SUSTAINABILITY ACTIONS ONLY
# ============================================================

def get_sustainability_actions(
    assessment_or_payload:
        RiskAssessment | Mapping[str, Any],
) -> tuple[RecommendationItem, ...]:
    """
    Return only sustainability recommendations.
    """

    return generate_recommendation(
        assessment_or_payload
    ).sustainability_actions