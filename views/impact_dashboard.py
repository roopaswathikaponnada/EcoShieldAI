"""
EcoShield AI
Impact Dashboard

This module renders EcoShield's sustainability and
security impact dashboard.

Responsibilities:
- Summarize the current session's assessment status
- Present secure-device handling indicators
- Present sustainability-oriented lifecycle indicators
- Explain the connection between data protection and
  responsible electronics lifecycle choices
- Avoid presenting fabricated global user statistics

Risk scoring, validation, RAG retrieval, and LLM calls must
NOT be implemented directly in this module.
"""

from __future__ import annotations

import streamlit as st

from ui.components import (
    render_feature_card,
    render_notice,
    render_page_header,
    render_section_header,
    render_spacer,
    render_stat_card,
)

from ui.navigation import (
    PAGE_ASSESSMENT,
    PAGE_SUSTAINABLE_DISPOSAL,
    force_navigate_to,
)

from ui.state import (
    get_assessment_payload,
    get_recommendation_result,
    get_risk_assessment,
    is_assessment_completed,
)


# ============================================================
# SESSION STATUS HELPERS
# ============================================================

def _session_status() -> str:
    """
    Return a concise current-session assessment status.
    """

    if is_assessment_completed():
        return "Assessment Complete"

    return "No Assessment Yet"


def _risk_status() -> str:
    """
    Return the current session's risk level when available.
    """

    assessment = (
        get_risk_assessment()
    )

    if assessment is None:
        return "Not Available"

    return assessment.risk_level


def _readiness_status() -> str:
    """
    Return current recommendation readiness when available.
    """

    recommendation = (
        get_recommendation_result()
    )

    if recommendation is None:
        return "Not Available"

    return recommendation.readiness


# ============================================================
# CURRENT SESSION OVERVIEW
# ============================================================

def _render_session_overview() -> None:
    """
    Render high-level session indicators.
    """

    render_section_header(
        title="Current Session",
        description=(
            "These indicators reflect only the assessment "
            "performed during your current EcoShield session."
        ),
        icon="📊",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_stat_card(
            label="Assessment Status",
            value=_session_status(),
        )

    with col2:

        render_stat_card(
            label="Security Risk",
            value=_risk_status(),
        )

    with col3:

        render_stat_card(
            label="Device Readiness",
            value=_readiness_status(),
        )


# ============================================================
# DEVICE LIFECYCLE SUMMARY
# ============================================================

def _render_device_lifecycle_summary() -> None:
    """
    Show the current device and lifecycle decision
    when an assessment exists.
    """

    payload = (
        get_assessment_payload()
    )

    device_type = (
        payload.get(
            "device_type"
        )
        or "Not Assessed"
    )

    condition = (
        payload.get(
            "device_condition"
        )
        or "Not Assessed"
    )

    intended_action = (
        payload.get(
            "intended_disposal_method"
        )
        or "Not Decided"
    )

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Device Lifecycle Snapshot",
        description=(
            "A device's sustainability potential depends "
            "on condition, security readiness, and intended "
            "next action."
        ),
        icon="♻️",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_stat_card(
            label="Device",
            value=device_type,
        )

    with col2:

        render_stat_card(
            label="Condition",
            value=condition,
        )

    with col3:

        render_stat_card(
            label="Intended Action",
            value=intended_action,
        )


# ============================================================
# IMPACT PRINCIPLES
# ============================================================

def _render_impact_principles() -> None:
    """
    Render the three main EcoShield impact dimensions.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="EcoShield Impact Areas",
        description=(
            "EcoShield focuses on three practical outcomes "
            "rather than claiming unverified environmental "
            "or user statistics."
        ),
        icon="🌍",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="🔐",
            title="Secure Data Handling",
            description=(
                "Reduce the chance of personal or sensitive "
                "information remaining exposed when devices "
                "change ownership or leave user control."
            ),
        )

    with col2:

        render_feature_card(
            icon="🔄",
            title="Lifecycle Extension",
            description=(
                "Encourage continued use, repair, donation, "
                "or resale when a device can still provide "
                "useful value."
            ),
        )

    with col3:

        render_feature_card(
            icon="♻️",
            title="Responsible End-of-Life",
            description=(
                "Guide users toward appropriate e-waste "
                "recycling when reuse or repair is no longer "
                "practical."
            ),
        )


# ============================================================
# SMART DEVICE LIFECYCLE
# ============================================================

def _render_lifecycle_flow() -> None:
    """
    Render a high-level responsible electronics lifecycle.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="The Smart Device Lifecycle",
        description=(
            "Security preparation belongs inside the device "
            "lifecycle, not only at the final disposal stage."
        ),
        icon="🌱",
    )

    st.markdown(
        """
        ### Purchase  
        ↓  
        ### Use  
        ↓  
        ### Maintain  
        ↓  
        ### Secure Data  
        ↓  
        **Reuse / Repair / Donate / Resell**  
        ↓  
        ### Responsible Recycling
        """
    )


# ============================================================
# CURRENT SECURITY IMPACT
# ============================================================

def _render_security_impact() -> None:
    """
    Display current session security indicators when available.
    """

    assessment = (
        get_risk_assessment()
    )

    if assessment is None:

        render_spacer(
            "lg"
        )

        render_notice(
            title="Run an assessment to unlock session indicators",
            message=(
                "EcoShield can display your current device's "
                "risk score, sanitization requirement, and "
                "security preparation status after assessment."
            ),
            notice_type="info",
        )

        return

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Current Security Impact",
        description=(
            "These values are generated only from the active "
            "device assessment."
        ),
        icon="🛡️",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_stat_card(
            label="Risk Score",
            value=(
                f"{assessment.score}/100"
            ),
        )

    with col2:

        render_stat_card(
            label="Risk Factors",
            value=len(
                assessment.factors
            ),
        )

    with col3:

        render_stat_card(
            label="Sanitization Required",
            value=(
                "Yes"
                if assessment.requires_sanitization
                else "No"
            ),
        )


# ============================================================
# SUSTAINABILITY READINESS
# ============================================================

def _render_sustainability_readiness() -> None:
    """
    Display current recommendation/lifecycle readiness.
    """

    recommendation = (
        get_recommendation_result()
    )

    if recommendation is None:
        return

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Current Lifecycle Readiness",
        description=(
            "Security readiness and sustainability decisions "
            "should be considered together."
        ),
        icon="♻️",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_stat_card(
            label="Readiness",
            value=recommendation.readiness,
        )

    with col2:

        render_stat_card(
            label="Security Actions",
            value=len(
                recommendation.security_actions
            ),
        )

    with col3:

        render_stat_card(
            label="Sustainability Actions",
            value=len(
                recommendation.sustainability_actions
            ),
        )

# ============================================================
# TRANSPARENCY NOTICE
# ============================================================

def _render_transparency_notice() -> None:
    """
    Explain that EcoShield does not fabricate global impact
    statistics.
    """

    render_spacer(
        "lg"
    )

    render_notice(
        title="Transparent impact reporting",
        message=(
            "EcoShield currently does not maintain a database "
            "of users or aggregate device-disposal statistics. "
            "For that reason, this dashboard shows current-session "
            "indicators and educational lifecycle guidance instead "
            "of fabricated totals such as devices recycled or "
            "carbon emissions saved."
        ),
        notice_type="info",
    )


# ============================================================
# FUTURE IMPACT CAPABILITIES
# ============================================================

def _render_future_capabilities() -> None:
    """
    Present possible future enhancements without claiming
    they already exist.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Future Impact Capabilities",
        description=(
            "These features could be added later if EcoShield "
            "adopts privacy-preserving analytics."
        ),
        icon="🚀",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="📈",
            title="Anonymous Trends",
            description=(
                "Aggregate non-identifying device-lifecycle "
                "patterns without storing personal device content."
            ),
        )

    with col2:

        render_feature_card(
            icon="🌱",
            title="Lifecycle Metrics",
            description=(
                "Estimate how often users choose repair, reuse, "
                "donation, resale, or recycling."
            ),
        )

    with col3:

        render_feature_card(
            icon="🔐",
            title="Security Readiness Trends",
            description=(
                "Track anonymous patterns in common device "
                "preparation mistakes and security controls."
            ),
        )


# ============================================================
# PAGE ACTIONS
# ============================================================

def _render_page_actions() -> None:
    """
    Render links into assessment and sustainability flows.
    """

    render_spacer(
        "lg"
    )

    st.divider()

    col1, col2 = st.columns(
        2
    )

    with col1:

        if st.button(
            "🛡️ Assess My Device",
            key="impact_assess_device",
            type="primary",
            use_container_width=True,
        ):
            force_navigate_to(
                PAGE_ASSESSMENT
            )

    with col2:

        if st.button(
            "♻️ Explore Sustainable Disposal",
            key="impact_sustainability",
            use_container_width=True,
        ):

            force_navigate_to(
                PAGE_SUSTAINABLE_DISPOSAL
            )


# ============================================================
# PUBLIC PAGE RENDERER
# ============================================================

def render() -> None:
    """
    Render the complete EcoShield Impact Dashboard.
    """

    render_page_header(
        kicker="Security + Sustainability",
        title="Impact Dashboard",
        subtitle=(
            "Explore how secure device preparation and "
            "responsible electronics lifecycle choices work "
            "together in EcoShield."
        ),
        icon="🌍",
    )

    _render_session_overview()

    _render_device_lifecycle_summary()

    _render_impact_principles()

    _render_lifecycle_flow()

    _render_security_impact()

    _render_sustainability_readiness()

    _render_transparency_notice()

    _render_future_capabilities()

    _render_page_actions()