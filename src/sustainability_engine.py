"""
EcoShield AI
Deterministic Sustainability Impact Engine

This module evaluates sustainability opportunity for an
electronic device using EcoShield's canonical validated
device-assessment data.

Responsibilities:
- Validate incoming assessment data defensively
- Calculate a deterministic 0-100 Sustainability Opportunity Score
- Evaluate explainable sustainability categories
- Generate structured sustainability factors
- Estimate lifecycle, reuse, repair, and recycling potential
- Identify uncertainty relevant to sustainability guidance
- Produce a preferred sustainable lifecycle action
- Return a stable SustainabilityImpactResult contract

Important:
This module does NOT calculate cybersecurity risk.

Cybersecurity scoring and transfer readiness remain owned by
src.risk_engine.py and src.recommendation.py.

The Sustainability Opportunity Score is NOT a carbon-footprint,
CO2-savings, environmental-certification, or lifecycle-analysis
score.

AI / LLM / RAG components MUST NOT override the deterministic
sustainability result produced by this module.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass, field
from typing import Any, Mapping

from src.validators import (
    FIELD_DEVICE_ACCESSIBLE,
    FIELD_DEVICE_AGE,
    FIELD_DEVICE_CONDITION,
    FIELD_DEVICE_TYPE,
    FIELD_DISPOSAL_METHOD,
    FIELD_POWER_ON,
    validate_device_input,
)


# ============================================================
# SUSTAINABILITY SCORE BOUNDARIES
# ============================================================

MIN_SUSTAINABILITY_SCORE = 0

MAX_SUSTAINABILITY_SCORE = 100

LOW_OPPORTUNITY_MAX = 24

MODERATE_OPPORTUNITY_MAX = 49

HIGH_OPPORTUNITY_MAX = 74


# ============================================================
# OPPORTUNITY LEVELS
# ============================================================

OPPORTUNITY_LOW = "Low Opportunity"

OPPORTUNITY_MODERATE = "Moderate Opportunity"

OPPORTUNITY_HIGH = "High Opportunity"

OPPORTUNITY_VERY_HIGH = "Very High Opportunity"


# ============================================================
# SUSTAINABILITY CATEGORIES
# ============================================================

CATEGORY_LIFECYCLE_EXTENSION = "Lifecycle Extension"

CATEGORY_REUSE_POTENTIAL = "Reuse Potential"

CATEGORY_REPAIR_POTENTIAL = "Repair / Refurbishment"

CATEGORY_END_OF_LIFE = "End-of-Life Responsibility"


CATEGORY_MAX_SCORES = {
    CATEGORY_LIFECYCLE_EXTENSION: 25,
    CATEGORY_REUSE_POTENTIAL: 25,
    CATEGORY_REPAIR_POTENTIAL: 25,
    CATEGORY_END_OF_LIFE: 25,
}


# ============================================================
# POTENTIAL LEVELS
# ============================================================

POTENTIAL_LOW = "Low"

POTENTIAL_MODERATE = "Moderate"

POTENTIAL_HIGH = "High"


# ============================================================
# PREFERRED LIFECYCLE ACTIONS
# ============================================================

ACTION_CONTINUE_USE = "Continue Use"

ACTION_REUSE = "Reuse"

ACTION_SELL = "Sell"

ACTION_DONATE = "Donate"

ACTION_REPAIR = "Repair / Refurbish"

ACTION_RECYCLE = "Responsible Recycling"

ACTION_REVIEW = "Review Options"


# ============================================================
# ACTION GROUPS
# ============================================================

REUSE_ACTIONS = {
    "Reuse",
    "Sell",
    "Donate",
}

FINAL_DISPOSAL_ACTIONS = {
    "Recycle",
    "Dispose",
}

REPAIR_ACTIONS = {
    "Repair",
}


# ============================================================
# DEVICE CONDITIONS
# ============================================================

CONDITION_WORKING = "Working"

CONDITION_PARTIALLY_WORKING = "Partially Working"

CONDITION_NOT_WORKING = "Not Working"

CONDITION_PHYSICALLY_DAMAGED = "Physically Damaged"


# ============================================================
# UNCERTAINTY VALUES
# ============================================================

UNCERTAIN_VALUES = {
    "Unsure",
    "Unknown",
    "Not Decided",
}


# ============================================================
# SUSTAINABILITY FACTOR
# ============================================================

@dataclass(frozen=True)
class SustainabilityFactor:
    """
    One explainable factor contributing to the deterministic
    sustainability opportunity assessment.

    Attributes
    ----------
    code:
        Stable machine-readable factor identifier.

    category:
        Sustainability category associated with the factor.

    points:
        Number of opportunity points contributed.

    message:
        Human-readable explanation of the factor.
    """

    code: str

    category: str

    points: int

    message: str


# ============================================================
# SUSTAINABILITY IMPACT RESULT
# ============================================================

@dataclass(frozen=True)
class SustainabilityImpactResult:
    """
    Final structured EcoShield sustainability assessment.

    Attributes
    ----------
    score:
        Deterministic Sustainability Opportunity Score from
        0 to 100.

    opportunity_level:
        Low, Moderate, High, or Very High Opportunity.

    preferred_action:
        Preferred lifecycle direction based on the available
        assessment information.

    lifecycle_extension_potential:
        Low / Moderate / High estimate of useful-life extension
        opportunity.

    reuse_potential:
        Low / Moderate / High estimate of continued-use,
        resale, or donation opportunity.

    repair_potential:
        Low / Moderate / High estimate of repair or
        refurbishment opportunity.

    recycling_priority:
        Low / Moderate / High indication of whether responsible
        end-of-life handling should be prioritized.

    factors:
        Explainable sustainability factors.

    category_scores:
        Deterministic score contribution for each category.

    uncertainties:
        Assessment fields whose values reduce confidence in
        sustainability guidance.

    validated_data:
        Canonical normalized assessment data used by the engine.

    summary:
        Concise deterministic explanation of the result.
    """

    score: int

    opportunity_level: str

    preferred_action: str

    lifecycle_extension_potential: str

    reuse_potential: str

    repair_potential: str

    recycling_priority: str

    factors: tuple[SustainabilityFactor, ...] = field(
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

    summary: str = ""

    def to_dict(self) -> dict[str, Any]:
        """
        Return a serializable dictionary representation.
        """

        return asdict(self)


# ============================================================
# CATEGORY SCORE INITIALIZER
# ============================================================

def _new_category_scores() -> dict[str, int]:
    """
    Return a fresh sustainability-category score mapping.
    """

    return {
        category: 0
        for category in CATEGORY_MAX_SCORES
    }


# ============================================================
# FACTOR ADDITION
# ============================================================

def _add_factor(
    factors: list[SustainabilityFactor],
    category_scores: dict[str, int],
    *,
    code: str,
    category: str,
    points: int,
    message: str,
) -> None:
    """
    Add one sustainability factor while respecting the
    configured category maximum.

    Duplicate factor codes are ignored.
    """

    if points <= 0:
        return

    if any(
        factor.code == code
        for factor in factors
    ):
        return

    maximum = CATEGORY_MAX_SCORES[
        category
    ]

    current = category_scores[
        category
    ]

    remaining = max(
        maximum - current,
        0,
    )

    applied_points = min(
        int(points),
        remaining,
    )

    if applied_points <= 0:
        return

    category_scores[category] += (
        applied_points
    )

    factors.append(
        SustainabilityFactor(
            code=code,
            category=category,
            points=applied_points,
            message=message,
        )
    )


# ============================================================
# OPPORTUNITY LEVEL
# ============================================================

def get_sustainability_opportunity_level(
    score: int,
) -> str:
    """
    Convert a 0-100 sustainability score into its
    opportunity level.
    """

    normalized_score = max(
        MIN_SUSTAINABILITY_SCORE,
        min(
            MAX_SUSTAINABILITY_SCORE,
            int(score),
        ),
    )

    if normalized_score <= LOW_OPPORTUNITY_MAX:
        return OPPORTUNITY_LOW

    if normalized_score <= MODERATE_OPPORTUNITY_MAX:
        return OPPORTUNITY_MODERATE

    if normalized_score <= HIGH_OPPORTUNITY_MAX:
        return OPPORTUNITY_HIGH

    return OPPORTUNITY_VERY_HIGH


# ============================================================
# POTENTIAL LEVEL
# ============================================================

def _potential_level(
    category_score: int,
) -> str:
    """
    Convert a 0-25 category score into Low / Moderate / High.
    """

    if category_score <= 8:
        return POTENTIAL_LOW

    if category_score <= 17:
        return POTENTIAL_MODERATE

    return POTENTIAL_HIGH


# ============================================================
# LIFECYCLE EXTENSION ASSESSMENT
# ============================================================

def _assess_lifecycle_extension(
    data: Mapping[str, Any],
    factors: list[SustainabilityFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess useful-life extension opportunity.
    """

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    power_on = data.get(
        FIELD_POWER_ON
    )

    accessible = data.get(
        FIELD_DEVICE_ACCESSIBLE
    )

    if condition == CONDITION_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="WORKING_DEVICE",
            category=CATEGORY_LIFECYCLE_EXTENSION,
            points=15,
            message=(
                "The device is reported as working and may "
                "retain useful service life."
            ),
        )

    elif condition == CONDITION_PARTIALLY_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="PARTIAL_FUNCTIONALITY_REMAINS",
            category=CATEGORY_LIFECYCLE_EXTENSION,
            points=10,
            message=(
                "The device is partially working and may still "
                "have useful-life extension potential."
            ),
        )

    elif condition in {
        CONDITION_NOT_WORKING,
        CONDITION_PHYSICALLY_DAMAGED,
    }:

        _add_factor(
            factors,
            category_scores,
            code="RECOVERY_POTENTIAL_REMAINS",
            category=CATEGORY_LIFECYCLE_EXTENSION,
            points=4,
            message=(
                "The device is not fully functional, but repair, "
                "refurbishment, component recovery, or recycling "
                "may still provide lifecycle value."
            ),
        )

    if power_on == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="DEVICE_POWERS_ON",
            category=CATEGORY_LIFECYCLE_EXTENSION,
            points=6,
            message=(
                "The device can power on, supporting further "
                "use, evaluation, repair, or refurbishment."
            ),
        )

    if accessible == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="DEVICE_ACCESSIBLE_FOR_EVALUATION",
            category=CATEGORY_LIFECYCLE_EXTENSION,
            points=4,
            message=(
                "The device is accessible and can be evaluated "
                "for continued use or lifecycle extension."
            ),
        )


# ============================================================
# REUSE POTENTIAL ASSESSMENT
# ============================================================

def _assess_reuse_potential(
    data: Mapping[str, Any],
    factors: list[SustainabilityFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess continued-use, resale, and donation potential.
    """

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    power_on = data.get(
        FIELD_POWER_ON
    )

    action = data.get(
        FIELD_DISPOSAL_METHOD
    )

    if condition == CONDITION_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="FUNCTIONAL_REUSE_POTENTIAL",
            category=CATEGORY_REUSE_POTENTIAL,
            points=15,
            message=(
                "A working device may be suitable for continued "
                "use, reuse, resale, or donation."
            ),
        )

    elif condition == CONDITION_PARTIALLY_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="LIMITED_REUSE_POTENTIAL",
            category=CATEGORY_REUSE_POTENTIAL,
            points=7,
            message=(
                "The partially working device may retain reuse "
                "potential after appropriate evaluation or repair."
            ),
        )

    if power_on == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="POWER_SUPPORTS_REUSE_EVALUATION",
            category=CATEGORY_REUSE_POTENTIAL,
            points=4,
            message=(
                "The device can power on, which supports "
                "evaluation for continued use or reuse."
            ),
        )

    if action in REUSE_ACTIONS:

        _add_factor(
            factors,
            category_scores,
            code="REUSE_PATH_SELECTED",
            category=CATEGORY_REUSE_POTENTIAL,
            points=6,
            message=(
                "The intended action keeps the device in a "
                "continued-use lifecycle pathway."
            ),
        )


# ============================================================
# REPAIR / REFURBISHMENT ASSESSMENT
# ============================================================

def _assess_repair_potential(
    data: Mapping[str, Any],
    factors: list[SustainabilityFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess repair and refurbishment opportunity.

    EcoShield does not claim that repair is technically or
    economically feasible; it identifies opportunities for
    further evaluation.
    """

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    power_on = data.get(
        FIELD_POWER_ON
    )

    accessible = data.get(
        FIELD_DEVICE_ACCESSIBLE
    )

    action = data.get(
        FIELD_DISPOSAL_METHOD
    )

    if condition == CONDITION_PARTIALLY_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="PARTIAL_DEVICE_REPAIR_OPPORTUNITY",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=14,
            message=(
                "Partial functionality suggests that repair or "
                "refurbishment may extend useful device life."
            ),
        )

    elif condition == CONDITION_NOT_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="NONWORKING_DEVICE_RECOVERY_REVIEW",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=8,
            message=(
                "A non-working device may still warrant "
                "repairability or component-recovery evaluation."
            ),
        )

    elif condition == CONDITION_PHYSICALLY_DAMAGED:

        _add_factor(
            factors,
            category_scores,
            code="DAMAGED_DEVICE_RECOVERY_REVIEW",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=7,
            message=(
                "Physical damage does not by itself prove that "
                "repair or component recovery is impractical."
            ),
        )

    elif condition == CONDITION_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="WORKING_DEVICE_LOW_REPAIR_NEED",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=4,
            message=(
                "The device is already working, so immediate "
                "repair is not the primary lifecycle opportunity."
            ),
        )

    if power_on == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="POWER_SUPPORTS_REPAIR_ASSESSMENT",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=4,
            message=(
                "The ability to power on may support further "
                "repair or refurbishment assessment."
            ),
        )

    if accessible == "Yes":

        _add_factor(
            factors,
            category_scores,
            code="ACCESS_SUPPORTS_REPAIR_ASSESSMENT",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=3,
            message=(
                "Device accessibility supports further evaluation "
                "for repair or refurbishment."
            ),
        )

    if action in REPAIR_ACTIONS:

        _add_factor(
            factors,
            category_scores,
            code="REPAIR_PATH_SELECTED",
            category=CATEGORY_REPAIR_POTENTIAL,
            points=8,
            message=(
                "Repair has been selected as the intended action, "
                "which directly supports lifecycle extension."
            ),
        )


# ============================================================
# END-OF-LIFE RESPONSIBILITY ASSESSMENT
# ============================================================

def _assess_end_of_life(
    data: Mapping[str, Any],
    factors: list[SustainabilityFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Assess responsible end-of-life opportunity.

    Recycling is treated as appropriate primarily when continued
    use or practical recovery is uncertain or limited.
    """

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    power_on = data.get(
        FIELD_POWER_ON
    )

    action = data.get(
        FIELD_DISPOSAL_METHOD
    )

    if condition in {
        CONDITION_NOT_WORKING,
        CONDITION_PHYSICALLY_DAMAGED,
    }:

        _add_factor(
            factors,
            category_scores,
            code="END_OF_LIFE_REVIEW_RELEVANT",
            category=CATEGORY_END_OF_LIFE,
            points=12,
            message=(
                "The device condition makes responsible recovery "
                "or end-of-life evaluation especially relevant."
            ),
        )

    elif condition == CONDITION_PARTIALLY_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="END_OF_LIFE_NOT_YET_PRIMARY",
            category=CATEGORY_END_OF_LIFE,
            points=5,
            message=(
                "The device is partially working, so repair or "
                "refurbishment should be considered before final "
                "end-of-life handling."
            ),
        )

    elif condition == CONDITION_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="WORKING_DEVICE_PREMATURE_EOL_CAUTION",
            category=CATEGORY_END_OF_LIFE,
            points=2,
            message=(
                "The device remains functional, so final disposal "
                "may be premature where continued use is practical."
            ),
        )

    if action == "Recycle":

        points = (
            13
            if condition in {
                CONDITION_NOT_WORKING,
                CONDITION_PHYSICALLY_DAMAGED,
            }
            else 5
        )

        _add_factor(
            factors,
            category_scores,
            code="RECYCLING_PATH_SELECTED",
            category=CATEGORY_END_OF_LIFE,
            points=points,
            message=(
                "Responsible electronics recycling is the "
                "selected end-of-life pathway."
            ),
        )

    elif action == "Dispose":

        _add_factor(
            factors,
            category_scores,
            code="DISPOSAL_REQUIRES_EWASTE_REVIEW",
            category=CATEGORY_END_OF_LIFE,
            points=4,
            message=(
                "General disposal should be reviewed in favor of "
                "an appropriate electronics or e-waste channel."
            ),
        )

    if (
        power_on == "No"
        and condition in {
            CONDITION_NOT_WORKING,
            CONDITION_PHYSICALLY_DAMAGED,
        }
    ):

        _add_factor(
            factors,
            category_scores,
            code="NONPOWERING_DEVICE_EOL_RELEVANCE",
            category=CATEGORY_END_OF_LIFE,
            points=5,
            message=(
                "A device that cannot power on may require "
                "repairability, component-recovery, or responsible "
                "end-of-life evaluation."
            ),
        )


# ============================================================
# DEVICE AGE ASSESSMENT
# ============================================================

def _assess_device_age(
    data: Mapping[str, Any],
    factors: list[SustainabilityFactor],
    category_scores: dict[str, int],
) -> None:
    """
    Apply conservative age-aware sustainability context.

    Age alone never determines disposal.
    """

    age = data.get(
        FIELD_DEVICE_AGE
    )

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    if not isinstance(
        age,
        (int, float),
    ):
        return

    if age < 5:
        return

    if condition == CONDITION_WORKING:

        _add_factor(
            factors,
            category_scores,
            code="OLDER_WORKING_DEVICE_LIFECYCLE_VALUE",
            category=CATEGORY_LIFECYCLE_EXTENSION,
            points=3,
            message=(
                "The device has several years of service history "
                "but remains working; age alone does not justify "
                "premature replacement or disposal."
            ),
        )

    elif (
        age >= 10
        and condition
        in {
            CONDITION_PARTIALLY_WORKING,
            CONDITION_NOT_WORKING,
            CONDITION_PHYSICALLY_DAMAGED,
        }
    ):

        _add_factor(
            factors,
            category_scores,
            code="OLDER_DEVICE_VIABILITY_REVIEW",
            category=CATEGORY_END_OF_LIFE,
            points=3,
            message=(
                "The older device should be reviewed for practical "
                "continued use, repair, recovery, or responsible "
                "recycling rather than judged by age alone."
            ),
        )


# ============================================================
# UNCERTAINTY COLLECTION
# ============================================================

def _collect_uncertainties(
    data: Mapping[str, Any],
) -> tuple[str, ...]:
    """
    Collect sustainability-relevant uncertainty.
    """

    relevant_fields = (
        FIELD_DEVICE_TYPE,
        FIELD_DEVICE_CONDITION,
        FIELD_POWER_ON,
        FIELD_DEVICE_ACCESSIBLE,
        FIELD_DISPOSAL_METHOD,
    )

    uncertainties: list[str] = []

    for field_name in relevant_fields:

        value = data.get(
            field_name
        )

        if (
            value is None
            or value in UNCERTAIN_VALUES
        ):
            uncertainties.append(
                field_name
            )

    return tuple(
        dict.fromkeys(
            uncertainties
        )
    )


# ============================================================
# RECYCLING PRIORITY
# ============================================================

def _determine_recycling_priority(
    data: Mapping[str, Any],
    end_of_life_score: int,
) -> str:
    """
    Determine recycling priority using condition and the
    end-of-life category score.
    """

    condition = data.get(
        FIELD_DEVICE_CONDITION
    )

    if condition == CONDITION_WORKING:
        return POTENTIAL_LOW

    if condition == CONDITION_PARTIALLY_WORKING:
        return POTENTIAL_MODERATE

    return _potential_level(
        end_of_life_score
    )


# ============================================================
# PREFERRED ACTION
# ============================================================

def _determine_preferred_action(
    data: Mapping[str, Any],
) -> str:
    condition = data.get(FIELD_DEVICE_CONDITION)
    intended_action = data.get(FIELD_DISPOSAL_METHOD)

    # Fully working devices should generally remain in useful service.
    if condition == CONDITION_WORKING:
        if intended_action == "Sell":
            return ACTION_SELL

        if intended_action == "Donate":
            return ACTION_DONATE

        if intended_action == "Reuse":
            return ACTION_REUSE

        # Repair, recycling, disposal, or an undecided action should not
        # displace continued use when the device is already working.
        return ACTION_CONTINUE_USE

    # Partially working devices should be evaluated for repair or
    # refurbishment before transfer or end-of-life handling.
    if condition == CONDITION_PARTIALLY_WORKING:
        return ACTION_REPAIR

    # Non-working or physically damaged devices require a more
    # conservative decision because the assessment does not establish
    # whether repair or recovery is technically/economically practical.
    if condition in {
        CONDITION_NOT_WORKING,
        CONDITION_PHYSICALLY_DAMAGED,
    }:
        if intended_action == "Repair":
            return ACTION_REPAIR

        if intended_action in {"Recycle", "Dispose"}:
            return ACTION_RECYCLE

        return ACTION_REVIEW

    return ACTION_REVIEW

# ============================================================
# SUMMARY GENERATION
# ============================================================

def _build_summary(
    data: Mapping[str, Any],
    *,
    score: int,
    opportunity_level: str,
    preferred_action: str,
) -> str:
    """
    Generate a concise deterministic sustainability summary.
    """

    device_type = data.get(
        FIELD_DEVICE_TYPE,
        "Device",
    )

    condition = data.get(
        FIELD_DEVICE_CONDITION,
        "unknown condition",
    )

    return (
        f"{device_type} has a Sustainability Opportunity Score "
        f"of {score}/100 ({opportunity_level}). Based on the "
        f"reported condition '{condition}', EcoShield's preferred "
        f"sustainability direction is '{preferred_action}'. "
        "This is lifecycle decision-support guidance and not a "
        "carbon-footprint or certified environmental assessment."
    )


# ============================================================
# VALIDATED DATA EXTRACTION
# ============================================================

def _validated_data_from_payload(
    payload: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Validate an EcoShield assessment and return canonical data.

    Existing validator rules remain authoritative.
    """

    validation = validate_device_input(
        payload
    )

    if not validation.is_valid:

        message = (
            "; ".join(validation.errors)
            if validation.errors
            else (
                "Device assessment failed validation."
            )
        )

        raise ValueError(
            message
        )

    return dict(
        validation.data
    )


# ============================================================
# PRIMARY PUBLIC SUSTAINABILITY FUNCTION
# ============================================================

def assess_sustainability(
    payload: Mapping[str, Any],
) -> SustainabilityImpactResult:
    """
    Calculate a deterministic EcoShield sustainability
    opportunity assessment.

    Parameters
    ----------
    payload:
        Raw or normalized canonical EcoShield assessment mapping.

    Returns
    -------
    SustainabilityImpactResult
        Structured sustainability opportunity assessment.

    Raises
    ------
    TypeError
        If payload is not mapping-like.

    ValueError
        If EcoShield validation fails.
    """

    if not isinstance(
        payload,
        Mapping,
    ):
        raise TypeError(
            "Sustainability assessment input must be a mapping."
        )

    data = _validated_data_from_payload(
        payload
    )

    factors: list[
        SustainabilityFactor
    ] = []

    category_scores = (
        _new_category_scores()
    )

    _assess_lifecycle_extension(
        data,
        factors,
        category_scores,
    )

    _assess_reuse_potential(
        data,
        factors,
        category_scores,
    )

    _assess_repair_potential(
        data,
        factors,
        category_scores,
    )

    _assess_end_of_life(
        data,
        factors,
        category_scores,
    )

    _assess_device_age(
        data,
        factors,
        category_scores,
    )

    score = sum(
        category_scores.values()
    )

    score = max(
        MIN_SUSTAINABILITY_SCORE,
        min(
            MAX_SUSTAINABILITY_SCORE,
            int(score),
        ),
    )

    opportunity_level = (
        get_sustainability_opportunity_level(
            score
        )
    )

    preferred_action = (
        _determine_preferred_action(
            data
        )
    )

    lifecycle_extension_potential = (
        _potential_level(
            category_scores[
                CATEGORY_LIFECYCLE_EXTENSION
            ]
        )
    )

    reuse_potential = (
        _potential_level(
            category_scores[
                CATEGORY_REUSE_POTENTIAL
            ]
        )
    )

    repair_potential = (
        _potential_level(
            category_scores[
                CATEGORY_REPAIR_POTENTIAL
            ]
        )
    )

    recycling_priority = (
        _determine_recycling_priority(
            data,
            category_scores[
                CATEGORY_END_OF_LIFE
            ],
        )
    )

    uncertainties = (
        _collect_uncertainties(
            data
        )
    )

    summary = _build_summary(
        data,
        score=score,
        opportunity_level=opportunity_level,
        preferred_action=preferred_action,
    )

    return SustainabilityImpactResult(
        score=score,
        opportunity_level=opportunity_level,
        preferred_action=preferred_action,
        lifecycle_extension_potential=(
            lifecycle_extension_potential
        ),
        reuse_potential=reuse_potential,
        repair_potential=repair_potential,
        recycling_priority=recycling_priority,
        factors=tuple(factors),
        category_scores=dict(
            category_scores
        ),
        uncertainties=uncertainties,
        validated_data=dict(data),
        summary=summary,
    )


# ============================================================
# CONVENIENCE FUNCTIONS
# ============================================================

def get_sustainability_score(
    payload: Mapping[str, Any],
) -> int:
    """
    Return only the Sustainability Opportunity Score.
    """

    return assess_sustainability(
        payload
    ).score


def get_preferred_sustainable_action(
    payload: Mapping[str, Any],
) -> str:
    """
    Return only the preferred sustainability lifecycle action.
    """

    return assess_sustainability(
        payload
    ).preferred_action