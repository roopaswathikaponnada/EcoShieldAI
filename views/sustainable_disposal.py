"""
EcoShield AI
Sustainable Disposal Guide

This module renders EcoShield's sustainability-focused
device lifecycle guidance.

Responsibilities:
- Explain sustainable device lifecycle choices
- Encourage reuse and repair before recycling
- Explain donation and resale pathways
- Explain responsible recycling as the final option
- Provide navigation back to Device Assessment

Risk scoring, validation, RAG retrieval, and LLM calls must
NOT be implemented in this module.
"""

from __future__ import annotations

import streamlit as st

from ui.components import (
    render_feature_card,
    render_notice,
    render_page_header,
    render_section_header,
    render_spacer,
)

from ui.navigation import (
    PAGE_ASSESSMENT,
    force_navigate_to,
)


# ============================================================
# DEVICE LIFECYCLE OPTIONS
# ============================================================

LIFECYCLE_OPTIONS = (
    (
        "♻️",
        "Reuse",
        (
            "Continue using the device when it is still "
            "functional and meets your needs."
        ),
    ),
    (
        "🔧",
        "Repair",
        (
            "Repair a partially working device when the cost "
            "and effort are reasonable compared with replacing it."
        ),
    ),
    (
        "🎁",
        "Donate",
        (
            "Give a working device a second life after completing "
            "all required security and data-sanitization steps."
        ),
    ),
    (
        "💰",
        "Resell",
        (
            "Transfer a usable device to another owner after "
            "secure preparation and account removal."
        ),
    ),
    (
        "♻️",
        "Recycle",
        (
            "Use responsible e-waste recycling when the device "
            "cannot reasonably be reused or repaired."
        ),
    ),
)


# ============================================================
# LIFECYCLE DECISION FLOW
# ============================================================

def _render_lifecycle_flow() -> None:
    """
    Render the recommended sustainable decision sequence.
    """

    render_section_header(
        title="Smart Device Lifecycle",
        description=(
            "Choose the most sustainable option that is still "
            "safe, practical, and appropriate for the device."
        ),
        icon="🌱",
    )

    st.markdown(
        """
        ### Recommended decision order

        **1. Is the device still useful?**  
        → Continue using or reuse it.

        **2. Is it partially working?**  
        → Consider repair.

        **3. Is it functional but no longer needed?**  
        → Consider donation or resale.

        **4. Is reuse or repair no longer practical?**  
        → Use responsible recycling.
        """
    )


# ============================================================
# LIFECYCLE CARDS
# ============================================================

def _render_lifecycle_options() -> None:
    """
    Render sustainability action cards.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Lifecycle Options",
        description=(
            "EcoShield prefers extending useful device life "
            "before choosing final disposal."
        ),
        icon="♻️",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        icon, title, description = (
            LIFECYCLE_OPTIONS[0]
        )

        render_feature_card(
            icon=icon,
            title=title,
            description=description,
        )

    with col2:

        icon, title, description = (
            LIFECYCLE_OPTIONS[1]
        )

        render_feature_card(
            icon=icon,
            title=title,
            description=description,
        )

    with col3:

        icon, title, description = (
            LIFECYCLE_OPTIONS[2]
        )

        render_feature_card(
            icon=icon,
            title=title,
            description=description,
        )

    render_spacer(
        "sm"
    )

    col4, col5 = st.columns(
        2
    )

    with col4:

        icon, title, description = (
            LIFECYCLE_OPTIONS[3]
        )

        render_feature_card(
            icon=icon,
            title=title,
            description=description,
        )

    with col5:

        icon, title, description = (
            LIFECYCLE_OPTIONS[4]
        )

        render_feature_card(
            icon=icon,
            title=title,
            description=description,
        )


# ============================================================
# SECURITY + SUSTAINABILITY CONNECTION
# ============================================================

def _render_security_connection() -> None:
    """
    Explain why sustainable transfer still requires
    cybersecurity preparation.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Sustainability Still Requires Security",
        description=(
            "A reusable device should not be transferred until "
            "personal data and account risks are addressed."
        ),
        icon="🛡️",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        render_feature_card(
            icon="🔐",
            title="Protect Data First",
            description=(
                "Before donation or resale, complete the "
                "required account sign-out, sanitization, "
                "and reset steps."
            ),
        )

    with col2:

        render_feature_card(
            icon="🌱",
            title="Extend Life Safely",
            description=(
                "Security preparation allows useful devices "
                "to remain in service without exposing the "
                "previous owner's information."
            ),
        )


# ============================================================
# REPAIR GUIDANCE
# ============================================================

def _render_repair_guidance() -> None:
    """
    Render repair-focused sustainability guidance.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="When Repair Makes Sense",
        description=(
            "Repair can extend device life and reduce premature "
            "electronic waste."
        ),
        icon="🔧",
    )

    st.markdown(
        """
        Repair may be worth considering when:

        - the device is still useful for its intended purpose;
        - only a limited component is damaged;
        - replacement parts are available;
        - repair cost is reasonable;
        - the device can still receive safe software support;
        - the repair process does not create unacceptable data risk.
        """
    )

    render_notice(
        title="Security before repair",
        message=(
            "If a device will be handled by a third party, "
            "consider backing up important data, signing out "
            "where practical, and reducing access to sensitive "
            "information before handing over the device."
        ),
        notice_type="warning",
    )


# ============================================================
# DONATION / RESALE GUIDANCE
# ============================================================

def _render_transfer_guidance() -> None:
    """
    Render sustainable transfer guidance.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Donation and Resale",
        description=(
            "Working devices can often provide more value through "
            "reuse than immediate recycling."
        ),
        icon="🎁",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        render_feature_card(
            icon="🎓",
            title="Donation",
            description=(
                "A prepared device may support education, "
                "community use, or another user who still "
                "benefits from the hardware."
            ),
        )

    with col2:

        render_feature_card(
            icon="💰",
            title="Resale",
            description=(
                "Reselling a functional device can extend its "
                "useful life while recovering some remaining value."
            ),
        )

    render_spacer(
        "sm"
    )

    render_notice(
        title="Do not transfer before preparation",
        message=(
            "Donation and resale should happen only after "
            "appropriate backups, account removal, data "
            "sanitization, removable-media checks, and reset steps."
        ),
        notice_type="info",
    )


# ============================================================
# RECYCLING GUIDANCE
# ============================================================

def _render_recycling_guidance() -> None:
    """
    Explain recycling as the final lifecycle option.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="When Recycling Is Appropriate",
        description=(
            "Responsible recycling is generally the final option "
            "when continued use, repair, donation, or resale are "
            "no longer practical."
        ),
        icon="♻️",
    )

    st.markdown(
        """
        Recycling may be appropriate when:

        - the device is severely damaged;
        - repair is impractical;
        - important components are no longer usable;
        - safe software support is no longer available;
        - the device has reached the end of its useful lifecycle.
        """
    )

    render_notice(
        title="Use responsible e-waste channels",
        message=(
            "Do not treat electronic devices like ordinary household "
            "waste. Use an appropriate e-waste collection or recycling "
            "route and complete relevant data-protection steps first."
        ),
        notice_type="warning",
    )


# ============================================================
# ECOSHIELD DECISION MODEL
# ============================================================

def _render_decision_model() -> None:
    """
    Explain how EcoShield combines sustainability and security.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="EcoShield Decision Principle",
        description=(
            "The best lifecycle option should protect both "
            "your information and the environment."
        ),
        icon="🛡️🌱",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="1️⃣",
            title="Assess Condition",
            description=(
                "Determine whether the device still works, "
                "can be repaired, or has reached end-of-life."
            ),
        )

    with col2:

        render_feature_card(
            icon="2️⃣",
            title="Secure the Data",
            description=(
                "Resolve data exposure, accounts, storage, "
                "and sanitization risks before transfer."
            ),
        )

    with col3:

        render_feature_card(
            icon="3️⃣",
            title="Choose the Lifecycle",
            description=(
                "Prefer continued use, repair, donation, or "
                "resale before responsible recycling."
            ),
        )


# ============================================================
# ASSESSMENT CTA
# ============================================================

def _render_assessment_cta() -> None:
    """
    Navigate into the actual EcoShield assessment.
    """

    render_spacer(
        "lg"
    )

    st.divider()

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        st.markdown(
            "### Not sure what to do with your device?"
        )

        st.caption(
            "Complete the EcoShield assessment to receive "
            "security-risk analysis and lifecycle guidance "
            "for your specific device."
        )

        if st.button(
            "♻️ Assess Device Lifecycle",
            key="sustainable_assessment_cta",
            type="primary",
            use_container_width=True,
        ):

            force_navigate_to(
                PAGE_ASSESSMENT
            )


# ============================================================
# PUBLIC PAGE RENDERER
# ============================================================

def render() -> None:
    """
    Render the complete Sustainable Disposal page.
    """

    render_page_header(
        kicker="Sustainable Electronics Lifecycle",
        title="Sustainable Disposal",
        subtitle=(
            "Choose reuse, repair, donation, resale, or "
            "responsible recycling based on the condition "
            "and security readiness of your device."
        ),
        icon="♻️",
    )

    render_notice(
        title="Reuse before disposal",
        message=(
            "A working or repairable device may still have "
            "useful life remaining. EcoShield encourages "
            "lifecycle extension when it can be done safely."
        ),
        notice_type="success",
    )

    render_spacer(
        "lg"
    )

    _render_lifecycle_flow()

    _render_lifecycle_options()

    _render_security_connection()

    _render_repair_guidance()

    _render_transfer_guidance()

    _render_recycling_guidance()

    _render_decision_model()

    _render_assessment_cta()