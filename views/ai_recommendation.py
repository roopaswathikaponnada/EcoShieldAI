"""
EcoShield AI
AI Recommendation Page

This page presents EcoShield's security and sustainability
recommendations for the completed device assessment.

Responsibilities:
- Display deterministic security recommendations
- Display sustainability recommendations
- Display readiness decision
- Display ordered next steps and warnings
- Display stored RAG enrichment status
- Display stored AI explanation when available
- Communicate safe fallback behavior
- Provide navigation between assessment result pages

Recommendation generation, RAG retrieval, and LLM generation
must NOT be implemented in this module.

This page only presents results already produced by EcoShield's
backend service and stored in centralized application state.
"""

from __future__ import annotations

import streamlit as st

from ui.components import (
    render_ai_badge,
    render_empty_state,
    render_notice,
    render_page_header,
    render_readiness_badge,
    render_recommendation_card,
    render_risk_badge,
    render_section_header,
    render_spacer,
    render_stat_card,
)

from ui.navigation import (
    PAGE_AI_RECOMMENDATION,
    PAGE_ASSESSMENT,
    PAGE_RISK_ANALYSIS,
    force_navigate_to,
    render_protected_page,
)

from ui.state import (
    get_assessment_ai_explanation,
    get_assessment_enrichment_status,
    get_assessment_payload,
    get_assessment_retrieved_context,
    get_recommendation_result,
    get_risk_assessment,
    reset_assessment,
)


# ============================================================
# READINESS HELPERS
# ============================================================

def _readiness_notice_type(
    readiness: str,
) -> str:
    """
    Convert recommendation readiness into a semantic
    Streamlit notice type.
    """

    normalized = (
        readiness
        .strip()
        .lower()
    )

    if normalized == "not ready":
        return "error"

    if normalized == "conditional":
        return "warning"

    return "success"


def _readiness_explanation(
    readiness: str,
) -> str:
    """
    Return a concise explanation of the readiness decision.
    """

    normalized = (
        readiness
        .strip()
        .lower()
    )

    if normalized == "not ready":

        return (
            "Important security preparation remains incomplete. "
            "Resolve the recommended actions before allowing "
            "the device to leave your control."
        )

    if normalized == "conditional":

        return (
            "The intended action may be appropriate after the "
            "highlighted security conditions and uncertainties "
            "have been reviewed."
        )

    return (
        "No blocking security condition was identified by the "
        "deterministic assessment. Review the remaining guidance "
        "before proceeding."
    )


# ============================================================
# DEVICE CONTEXT
# ============================================================

def _render_device_context(
    assessment,
    recommendation,
) -> None:
    """
    Display the device and decision context used by EcoShield.
    """

    payload = (
        get_assessment_payload()
    )

    device_type = (
        payload.get("device_type")
        or "Unknown"
    )

    disposal_method = (
        payload.get(
            "intended_disposal_method"
        )
        or "Not Decided"
    )

    render_section_header(
        title="Assessment Context",
        description=(
            "EcoShield generated this guidance from your "
            "completed device security assessment."
        ),
        icon="🖥️",
    )

    col1, col2, col3, col4 = (
        st.columns(4)
    )

    with col1:

        render_stat_card(
            label="Device",
            value=device_type,
        )

    with col2:

        render_stat_card(
            label="Intended Action",
            value=disposal_method,
        )

    with col3:

        render_stat_card(
            label="Risk Score",
            value=f"{assessment.score}/100",
        )

        render_spacer("sm")

        render_risk_badge(
            assessment.risk_level
        )

    with col4:

        render_stat_card(
            label="Readiness",
            value=recommendation.readiness,
        )

        render_spacer("sm")

        render_readiness_badge(
            recommendation.readiness
        )


# ============================================================
# PRIMARY RECOMMENDATION
# ============================================================

def _render_primary_recommendation(
    recommendation,
) -> None:
    """
    Display EcoShield's overall recommendation decision.
    """

    render_section_header(
        title="EcoShield Recommendation",
        description=(
            "Your security and sustainability guidance is "
            "prioritized according to the completed assessment."
        ),
        icon="🎯",
    )

    render_ai_badge(
        "ECOSHIELD GUIDANCE"
    )

    render_spacer("sm")

    render_notice(
        title=(
            f"Device Status: "
            f"{recommendation.readiness}"
        ),
        message=recommendation.summary,
        notice_type=(
            _readiness_notice_type(
                recommendation.readiness
            )
        ),
    )

    st.caption(
        _readiness_explanation(
            recommendation.readiness
        )
    )


# ============================================================
# SECURITY ACTIONS
# ============================================================

def _render_security_actions(
    recommendation,
) -> None:
    """
    Display prioritized cybersecurity recommendations.
    """

    render_section_header(
        title="Security Action Plan",
        description=(
            "Complete these actions to reduce privacy and "
            "data-exposure risk before transferring or "
            "disposing of the device."
        ),
        icon="🛡️",
    )

    actions = (
        recommendation.security_actions
    )

    if not actions:

        render_notice(
            title="No additional security actions required",
            message=(
                "The deterministic recommendation engine did "
                "not identify an outstanding security action."
            ),
            notice_type="success",
        )

        return

    for action in actions:

        render_recommendation_card(
            title=action.title,
            action=action.action,
            rationale=action.rationale,
            priority=action.priority,
            category="Security",
        )


# ============================================================
# SUSTAINABILITY ACTIONS
# ============================================================

def _render_sustainability_actions(
    recommendation,
) -> None:
    """
    Display responsible lifecycle recommendations.
    """

    render_section_header(
        title="Sustainability Guidance",
        description=(
            "EcoShield considers whether the device can be "
            "reused, repaired, donated, resold, or responsibly "
            "recycled instead of unnecessarily discarded."
        ),
        icon="♻️",
    )

    actions = (
        recommendation
        .sustainability_actions
    )

    if not actions:

        render_notice(
            title="No additional lifecycle action identified",
            message=(
                "No separate sustainability recommendation "
                "was generated for the current assessment."
            ),
            notice_type="info",
        )

        return

    for action in actions:

        render_recommendation_card(
            title=action.title,
            action=action.action,
            rationale=action.rationale,
            priority="Low",
            category="Sustainability",
        )


# ============================================================
# NEXT STEPS
# ============================================================

def _render_next_steps(
    recommendation,
) -> None:
    """
    Display the ordered action sequence generated by
    recommendation.py.
    """

    steps = (
        recommendation.next_steps
    )

    if not steps:
        return

    render_section_header(
        title="Recommended Next Steps",
        description=(
            "Follow this sequence before completing the "
            "intended device action."
        ),
        icon="📋",
    )

    for index, step in enumerate(
        steps,
        start=1,
    ):

        st.markdown(
            f"""
            **{index}. {step}**
            """
        )


# ============================================================
# WARNINGS
# ============================================================

def _render_warnings(
    recommendation,
) -> None:
    """
    Display important recommendation warnings.
    """

    warnings = (
        recommendation.warnings
    )

    if not warnings:
        return

    render_section_header(
        title="Important Notices",
        description=(
            "Review these conditions before making the final "
            "device-transfer or disposal decision."
        ),
        icon="⚠️",
    )

    for warning in warnings:

        st.warning(
            warning
        )


# ============================================================
# CURRENT AI STATUS
# ============================================================

def _render_ai_status() -> None:
    """
    Display the stored recommendation-enrichment status.

    This page does not execute RAG retrieval or LLM generation.
    It only presents enrichment results already produced by the
    backend assessment service and synchronized into session state.
    """

    enrichment = (
        get_assessment_enrichment_status()
    )

    retrieved_context = (
        get_assessment_retrieved_context()
    )

    ai_explanation = (
        get_assessment_ai_explanation()
    )

    rag_enabled = bool(
        enrichment.get("rag_enabled", False)
    )

    ai_enabled = bool(
        enrichment.get("ai_enabled", False)
    )

    rag_attempted = bool(
        enrichment.get("rag_attempted", False)
    )

    ai_attempted = bool(
        enrichment.get("ai_attempted", False)
    )

    rag_succeeded = bool(
        enrichment.get("rag_succeeded", False)
    )

    ai_succeeded = bool(
        enrichment.get("ai_succeeded", False)
    )

    used_fallback = bool(
        enrichment.get("used_fallback", False)
    )

    render_section_header(
        title="How This Guidance Was Generated",
        description=(
            "EcoShield keeps deterministic risk calculation "
            "separate from optional knowledge retrieval and "
            "AI explanation so security decisions remain "
            "traceable and explainable."
        ),
        icon="🤖",
    )

    # --------------------------------------------------------
    # Determine current enrichment mode
    # --------------------------------------------------------

    if ai_enabled:

        mode_label = "AI + RAG"

    elif rag_enabled:

        mode_label = "RAG Grounded"

    else:

        mode_label = "Deterministic"

    # --------------------------------------------------------
    # Determine enrichment status
    # --------------------------------------------------------

    if used_fallback:

        enrichment_label = "Safe Fallback"

    elif ai_enabled and ai_succeeded:

        enrichment_label = "AI Generated"

    elif rag_enabled and rag_succeeded:

        enrichment_label = "RAG Grounded"

    elif ai_enabled and ai_attempted:

        enrichment_label = "AI Unavailable"

    elif rag_enabled and rag_attempted:

        enrichment_label = "RAG Unavailable"

    else:

        enrichment_label = "Not Requested"

    # --------------------------------------------------------
    # Summary cards
    # --------------------------------------------------------

    col1, col2, col3 = (
        st.columns(3)
    )

    with col1:

        render_stat_card(
            label="Risk Analysis",
            value="Deterministic",
        )

    with col2:

        render_stat_card(
            label="Guidance Mode",
            value=mode_label,
        )

    with col3:

        render_stat_card(
            label="Enrichment",
            value=enrichment_label,
        )

    render_spacer("sm")

    # --------------------------------------------------------
    # Deterministic-only mode
    # --------------------------------------------------------

    if (
        not rag_enabled
        and not ai_enabled
    ):

        st.info(
            "This assessment used EcoShield's deterministic "
            "risk and recommendation engines. Optional RAG "
            "retrieval and AI explanation were not requested."
        )

        return

    # --------------------------------------------------------
    # Safe fallback mode
    # --------------------------------------------------------

    if used_fallback:

        render_notice(
            title="Safe deterministic fallback active",
            message=(
                "Optional RAG or AI enrichment could not be "
                "completed successfully. EcoShield preserved "
                "the deterministic risk assessment and "
                "rule-based recommendations."
            ),
            notice_type="warning",
        )

    # --------------------------------------------------------
    # Successful RAG status
    # --------------------------------------------------------

    elif (
        rag_enabled
        and rag_succeeded
        and not ai_enabled
    ):

        render_notice(
            title="Knowledge-grounded guidance",
            message=(
                "EcoShield successfully retrieved relevant "
                "knowledge-base evidence to support this "
                "recommendation. The deterministic risk score "
                "was not changed."
            ),
            notice_type="success",
        )

    # --------------------------------------------------------
    # Successful AI status
    # --------------------------------------------------------

    elif (
        ai_enabled
        and ai_succeeded
    ):

        render_notice(
            title="Grounded AI explanation available",
            message=(
                "EcoShield successfully generated an AI "
                "explanation grounded in retrieved knowledge. "
                "The deterministic risk score and rule-based "
                "recommendations remain authoritative."
            ),
            notice_type="success",
        )

    # --------------------------------------------------------
    # Other incomplete enrichment state
    # --------------------------------------------------------

    else:

        render_notice(
            title="Optional enrichment unavailable",
            message=(
                "EcoShield completed the deterministic "
                "assessment, but optional enrichment was "
                "not available for this result."
            ),
            notice_type="warning",
        )

    # --------------------------------------------------------
    # Stored AI explanation
    # --------------------------------------------------------

    if ai_explanation:

        render_spacer("sm")

        render_section_header(
            title="AI Explanation",
            description=(
                "A source-grounded explanation generated "
                "for this completed assessment."
            ),
            icon="✨",
        )

        st.write(
            ai_explanation
        )

    # --------------------------------------------------------
    # Stored retrieval context status
    # --------------------------------------------------------

    if retrieved_context:

        render_spacer("sm")

        st.caption(
            f"Knowledge evidence available: "
            f"{len(retrieved_context)} retrieved item(s)."
        )

# ============================================================
# PAGE ACTIONS
# ============================================================

def _render_page_actions() -> None:
    """
    Render navigation actions for the recommendation page.
    """

    st.divider()

    col1, col2 = st.columns(
        2
    )

    with col1:

        risk_clicked = (
            st.button(
                "← Back to Risk Analysis",
                key="recommendation_back_risk",
                use_container_width=True,
            )
        )

    with col2:

        new_clicked = (
            st.button(
                "Assess Another Device",
                key="recommendation_new_assessment",
                type="primary",
                use_container_width=True,
            )
        )

    if risk_clicked:

        force_navigate_to(
            PAGE_RISK_ANALYSIS
        )

    if new_clicked:

        reset_assessment()

        force_navigate_to(
            PAGE_ASSESSMENT
        )


# ============================================================
# PUBLIC PAGE RENDERER
# ============================================================

def render() -> None:
    """
    Render the complete EcoShield recommendation page.
    """

    # --------------------------------------------------------
    # Protect page from direct access without results.
    # --------------------------------------------------------

    if not render_protected_page(
        PAGE_AI_RECOMMENDATION
    ):
        return

    assessment = (
        get_risk_assessment()
    )

    recommendation = (
        get_recommendation_result()
    )

    if (
        assessment is None
        or recommendation is None
    ):

        render_empty_state(
            title="Recommendation unavailable",
            description=(
                "Complete a device assessment before viewing "
                "EcoShield security and sustainability "
                "recommendations."
            ),
            icon="🤖",
        )

        return

    # --------------------------------------------------------
    # Header
    # --------------------------------------------------------

    render_page_header(
        kicker="Security + Sustainability Decision Support",
        title="AI Recommendation",
        subtitle=(
            "Review EcoShield's prioritized actions for "
            "protecting your data and choosing a responsible "
            "next step for your electronic device."
        ),
        icon="🤖",
    )

    # --------------------------------------------------------
    # Context
    # --------------------------------------------------------

    _render_device_context(
        assessment,
        recommendation,
    )

    render_spacer("lg")

    # --------------------------------------------------------
    # Primary recommendation
    # --------------------------------------------------------

    _render_primary_recommendation(
        recommendation
    )

    render_spacer("lg")

    # --------------------------------------------------------
    # Security recommendations
    # --------------------------------------------------------

    _render_security_actions(
        recommendation
    )

    render_spacer("lg")

    # --------------------------------------------------------
    # Sustainability recommendations
    # --------------------------------------------------------

    _render_sustainability_actions(
        recommendation
    )

    render_spacer("lg")

    # --------------------------------------------------------
    # Next steps
    # --------------------------------------------------------

    _render_next_steps(
        recommendation
    )

    render_spacer("lg")

    # --------------------------------------------------------
    # Warnings
    # --------------------------------------------------------

    _render_warnings(
        recommendation
    )

    render_spacer("lg")

    # --------------------------------------------------------
    # AI architecture status
    # --------------------------------------------------------

    _render_ai_status()

    # --------------------------------------------------------
    # Navigation
    # --------------------------------------------------------

    _render_page_actions()