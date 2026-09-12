"""
EcoShield AI
Secure Data Guide Page

This module renders EcoShield's secure device-preparation guide.

Responsibilities:
- Explain the general secure-preparation workflow
- Provide platform-specific guidance sections
- Educate users before selling, donating, repairing, recycling,
  or disposing of electronic devices
- Provide direct navigation back to the Device Assessment flow

Current stage:
- Static secure-device educational guidance
- RAG-grounded knowledge retrieval
- Source-grounded AI explanations

Risk scoring and recommendation generation must NOT be
implemented in this module.
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
# GENERAL SECURITY WORKFLOW
# ============================================================

SECURE_PREPARATION_STEPS = (
    (
        "☁️",
        "1. Back Up Important Data",
        (
            "Save important files, photos, documents, and "
            "other information to a trusted backup location "
            "before making destructive changes to the device."
        ),
    ),
    (
        "👤",
        "2. Sign Out of Accounts",
        (
            "Sign out of device accounts, browsers, cloud "
            "services, email applications, and other linked "
            "services before transferring the device."
        ),
    ),
    (
        "🔐",
        "3. Verify Encryption",
        (
            "Check whether device or storage encryption is "
            "enabled. Encryption can reduce exposure if data "
            "remains on storage media."
        ),
    ),
    (
        "🧹",
        "4. Securely Remove Data",
        (
            "Use an appropriate sanitization method for the "
            "device and storage type before the device leaves "
            "your control."
        ),
    ),
    (
        "🔄",
        "5. Perform a Factory Reset",
        (
            "Where supported, restore the device to its "
            "factory state after required backups and secure "
            "data-removal steps are complete."
        ),
    ),
    (
        "💳",
        "6. Remove Removable Media",
        (
            "Remove SIM cards, memory cards, USB storage, "
            "external drives, and other removable media that "
            "should remain with you."
        ),
    ),
    (
        "✅",
        "7. Verify the Result",
        (
            "Confirm that personal data, user accounts, and "
            "removable media are no longer accessible before "
            "selling, donating, repairing, recycling, or "
            "disposing of the device."
        ),
    ),
)


# ============================================================
# PLATFORM GUIDANCE
# ============================================================

PLATFORM_GUIDES = {
    "Windows": {
        "icon": "🪟",
        "summary": (
            "Prepare Windows laptops and desktops before "
            "ownership transfer or recycling."
        ),
        "steps": (
            "Back up required files.",
            "Sign out of Microsoft and browser accounts.",
            "Verify BitLocker or device-encryption status.",
            "Use an appropriate data-sanitization method.",
            "Reset Windows after sanitization where appropriate.",
            "Remove external drives, SD cards, and USB media.",
            "Verify that the device starts without your account.",
        ),
    },

    "macOS": {
        "icon": "🍎",
        "summary": (
            "Prepare Mac devices before resale, donation, "
            "repair, or recycling."
        ),
        "steps": (
            "Back up important files.",
            "Sign out of Apple-linked services where required.",
            "Verify FileVault encryption status.",
            "Erase the device using an appropriate supported method.",
            "Remove external storage and accessories containing data.",
            "Complete the reset or setup-assistant handoff process.",
            "Confirm personal data is no longer accessible.",
        ),
    },

    "Android": {
        "icon": "🤖",
        "summary": (
            "Prepare Android smartphones and tablets before "
            "ownership transfer or disposal."
        ),
        "steps": (
            "Back up photos, contacts, and required application data.",
            "Sign out of Google and manufacturer-linked accounts.",
            "Confirm device encryption status.",
            "Remove SIM and removable memory cards.",
            "Perform an appropriate factory reset.",
            "Verify that activation starts without your account.",
        ),
    },

    "iPhone / iPad": {
        "icon": "📱",
        "summary": (
            "Prepare Apple mobile devices before resale, "
            "donation, repair, or recycling."
        ),
        "steps": (
            "Create a backup if required.",
            "Sign out of Apple services as appropriate.",
            "Remove SIM cards where applicable.",
            "Erase all content and settings.",
            "Confirm personal content is no longer accessible.",
            "Verify the device reaches the setup screen.",
        ),
    },

    "Storage Drives": {
        "icon": "💾",
        "summary": (
            "Storage media may require different sanitization "
            "approaches depending on whether it is HDD, SSD, "
            "flash storage, or removable media."
        ),
        "steps": (
            "Identify the storage technology before sanitization.",
            "Back up any information that must be retained.",
            "Do not assume normal file deletion removes data securely.",
            "Use a sanitization method appropriate to the storage type.",
            "Verify that the required information is no longer accessible.",
            "Use responsible recycling when storage cannot be safely reused.",
        ),
    },
}


# ============================================================
# GENERAL WORKFLOW
# ============================================================

def _render_general_workflow() -> None:
    """
    Render the seven-step secure device-preparation workflow.
    """

    render_section_header(
        title="Before a Device Leaves Your Control",
        description=(
            "Use this sequence as a general preparation "
            "framework before selling, donating, repairing, "
            "recycling, or disposing of a device."
        ),
        icon="🔐",
    )

    for icon, title, description in SECURE_PREPARATION_STEPS:

        render_feature_card(
            icon=icon,
            title=title,
            description=description,
        )

        render_spacer(
            "sm"
        )


# ============================================================
# PLATFORM-SPECIFIC GUIDANCE
# ============================================================

def _render_platform_guides() -> None:
    """
    Render platform-specific preparation guidance.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Platform Guidance",
        description=(
            "Choose the device platform that most closely "
            "matches what you are preparing."
        ),
        icon="🖥️",
    )

    tabs = st.tabs(
        list(
            PLATFORM_GUIDES.keys()
        )
    )

    for tab, (
        platform,
        guide,
    ) in zip(
        tabs,
        PLATFORM_GUIDES.items(),
    ):

        with tab:

            st.markdown(
                f"### {guide['icon']} {platform}"
            )

            st.caption(
                guide["summary"]
            )

            render_spacer(
                "sm"
            )

            for index, step in enumerate(
                guide["steps"],
                start=1,
            ):

                st.markdown(
                    f"**{index}. {step}**"
                )


# ============================================================
# FACTORY RESET WARNING
# ============================================================

def _render_reset_warning() -> None:
    """
    Explain why factory reset should not automatically be
    treated as equivalent to secure sanitization.
    """

    render_spacer(
        "lg"
    )

    render_notice(
        title="Factory reset is not always the whole security process",
        message=(
            "The appropriate preparation method depends on "
            "the device, storage technology, operating system, "
            "encryption status, and intended destination. "
            "EcoShield treats secure erasure and factory reset "
            "as separate assessment controls."
        ),
        notice_type="warning",
    )


# ============================================================
# CURRENT KNOWLEDGE MODE
# ============================================================

def _render_knowledge_status() -> None:
    """
    Explain EcoShield's current guidance architecture.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Guidance Architecture",
        description=(
            "EcoShield separates general education from "
            "device-specific risk scoring."
        ),
        icon="📚",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="📘",
            title="Current Guide",
            description=(
                "General secure-device preparation guidance "
                "built directly into EcoShield."
            ),
        )

    with col2:

        render_feature_card(
            icon="🔎",
            title="RAG Grounding",
            description=(
                "Trusted cybersecurity documents are retrieved "
                "according to device context, platform, and "
                "security topic."
            ),
        )

    with col3:

        render_feature_card(
            icon="🤖",
            title="Grounded AI",
            description=(
                "AI explanations are generated from retrieved "
                "evidence while the deterministic risk engine "
                "remains authoritative."
            ),
        )

# ============================================================
# ASSESSMENT CALL TO ACTION
# ============================================================

def _render_assessment_cta() -> None:
    """
    Send the user into the device assessment workflow.
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
            "### Want guidance for your own device?"
        )

        st.caption(
            "Run the EcoShield assessment to identify "
            "security risks and required preparation steps "
            "for your specific device."
        )

        if st.button(
            "🛡️ Assess My Device",
            key="secure_guide_assessment",
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
    Render the complete Secure Data Guide page.
    """

    render_page_header(
        kicker="Cybersecurity Guidance",
        title="Secure Data Guide",
        subtitle=(
            "Prepare electronic devices carefully before "
            "selling, donating, repairing, recycling, or "
            "disposing of them."
        ),
        icon="🔐",
    )

    render_notice(
        title="Security-first preparation",
        message=(
            "Do not provide EcoShield with passwords, "
            "personal files, account credentials, or other "
            "sensitive content. This guide focuses on device "
            "preparation practices."
        ),
        notice_type="info",
    )

    render_spacer(
        "lg"
    )

    _render_general_workflow()

    _render_platform_guides()

    _render_reset_warning()

    _render_knowledge_status()

    _render_assessment_cta()