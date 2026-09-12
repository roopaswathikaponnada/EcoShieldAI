"""
EcoShield AI
Home / Landing Page — Frontend V2

Presentation-only redesign. Business logic, risk scoring, RAG,
recommendation generation, and validation remain outside this file.
"""

from __future__ import annotations

import streamlit as st

from ui.components import (
    render_feature_card,
    render_notice,
    render_section_header,
    render_spacer,
)

from ui.navigation import (
    PAGE_ABOUT,
    PAGE_ASSESSMENT,
    PAGE_KNOWLEDGE_CENTER,
    PAGE_SECURE_DATA_GUIDE,
    PAGE_SUSTAINABLE_DISPOSAL,
    force_navigate_to,
)


def _hero() -> None:
    st.html(
        """
        <section class="eco-v2-hero">
            <div class="eco-v2-eyebrow">
                🛡️ AI-Powered E-Waste Security & Sustainability Advisor
            </div>
            <h1>
                Secure your data.<br>
                <span>Give devices a better next chapter.</span>
            </h1>
            <p>
                EcoShield AI helps you assess security readiness before
                selling, donating, reusing, repairing, recycling, or
                disposing of an electronic device — so data protection
                comes first and sustainable action follows safely.
            </p>
        </section>
        """
    )

    render_spacer("sm")

    c1, c2, c3 = st.columns([1.45, 1.1, 3.2])

    with c1:
        if st.button(
            "🛡️ Start Device Assessment",
            key="home_assess_device",
            type="primary",
            use_container_width=True,
        ):
            force_navigate_to(
                PAGE_ASSESSMENT
            )

    with c2:
        if st.button(
            "▶ Learn More",
            key="home_learn_more",
            use_container_width=True,
        ):
            force_navigate_to(
                PAGE_ABOUT
            )

    st.html(
        """
        <div class="eco-v2-feature-strip">
            <div class="eco-v2-mini">
                <div class="eco-v2-mini-icon">🛡️</div>
                <div><strong>Data Security First</strong>
                <span>Security readiness before transfer</span></div>
            </div>
            <div class="eco-v2-mini">
                <div class="eco-v2-mini-icon">🤖</div>
                <div><strong>AI-Guided</strong>
                <span>Explainable, evidence-aware guidance</span></div>
            </div>
            <div class="eco-v2-mini">
                <div class="eco-v2-mini-icon">🌱</div>
                <div><strong>Sustainable Choices</strong>
                <span>Reuse, repair and recycle responsibly</span></div>
            </div>
            <div class="eco-v2-mini">
                <div class="eco-v2-mini-icon">📚</div>
                <div><strong>Evidence-Based</strong>
                <span>RAG-supported knowledge and guidance</span></div>
            </div>
        </div>
        """
    )


def _why_ecoshield() -> None:
    st.html(
        """
        <div class="eco-v2-section-title">
            <div class="k">Why EcoShield</div>
            <h2>One decision, two responsibilities</h2>
            <p>
                Device disposal is not only an environmental decision.
                It is also a cybersecurity decision. EcoShield brings
                both together in one guided workflow.
            </p>
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_feature_card(
            icon="🔐",
            title="Protect Personal Data",
            description=(
                "Identify unresolved risks such as retained accounts, "
                "missing sanitization, removable media, or unprotected "
                "sensitive information before a device leaves your control."
            ),
        )

    with c2:
        render_feature_card(
            icon="♻️",
            title="Extend Device Life",
            description=(
                "Prefer reuse, repair, donation, or resale when practical, "
                "while keeping security requirements authoritative."
            ),
        )

    with c3:
        render_feature_card(
            icon="🧠",
            title="Make Informed Decisions",
            description=(
                "Combine deterministic assessment, sustainability logic, "
                "retrieved evidence, and safe AI assistance in one experience."
            ),
        )


def _workflow() -> None:
    st.html(
        """
        <div class="eco-v2-section-title">
            <div class="k">Simple workflow</div>
            <h2>From device details to a safer next action</h2>
            <p>
                EcoShield turns structured device information into clear,
                actionable security and sustainability guidance.
            </p>
        </div>
        """
    )

    cols = st.columns(4)

    cards = (
        (
            "01",
            "Device Assessment",
            "Answer structured questions about device condition, storage, data, and preparation status.",
            "🖥️",
        ),
        (
            "02",
            "Cybersecurity Risk",
            "Receive a deterministic 0–100 risk score with category-level factors and sanitization requirements.",
            "🛡️",
        ),
        (
            "03",
            "Recommended Actions",
            "See prioritized security steps and the device's readiness for its intended lifecycle action.",
            "✅",
        ),
        (
            "04",
            "Responsible Lifecycle",
            "Use security-aware sustainability guidance for reuse, repair, donation, resale, or recycling.",
            "🌱",
        ),
    )

    for col, (_, title, description, icon) in zip(cols, cards):
        with col:
            render_feature_card(
                icon=icon,
                title=title,
                description=description,
            )


def _explore() -> None:
    st.html(
        """
        <div class="eco-v2-section-title">
            <div class="k">Explore EcoShield</div>
            <h2>Guides, knowledge and AI-assisted support</h2>
            <p>
                Learn how to prepare devices securely and make responsible
                electronics lifecycle decisions.
            </p>
        </div>
        """
    )

    c1, c2, c3 = st.columns(3)

    with c1:
        render_feature_card(
            icon="🔐",
            title="Secure Data Guide",
            description=(
                "Review practical preparation steps before transferring, "
                "repairing, recycling, or disposing of a device."
            ),
        )
        if st.button(
            "Open Security Guide →",
            key="home_security_guide",
            use_container_width=True,
        ):
            force_navigate_to(
                PAGE_SECURE_DATA_GUIDE
            )

    with c2:
        render_feature_card(
            icon="📚",
            title="Knowledge + AI Advisor",
            description=(
                "Explore trusted cybersecurity and sustainability topics "
                "and use the EcoShield Advisor where available."
            ),
        )
        if st.button(
            "Open Knowledge Center →",
            key="home_knowledge_center",
            use_container_width=True,
        ):
            force_navigate_to(
                PAGE_KNOWLEDGE_CENTER
            )

    with c3:
        render_feature_card(
            icon="♻️",
            title="Sustainable Disposal",
            description=(
                "Understand the preferred lifecycle order: continue use, "
                "reuse, repair, donate or resell, then recycle responsibly."
            ),
        )
        if st.button(
            "Explore Lifecycle Options →",
            key="home_sustainable_guide",
            use_container_width=True,
        ):
            force_navigate_to(
                PAGE_SUSTAINABLE_DISPOSAL
            )


def _privacy() -> None:
    render_spacer("lg")

    render_notice(
        title="Privacy-first by design",
        message=(
            "EcoShield assesses device-security status without asking you "
            "to upload personal files, reveal passwords, or provide account "
            "credentials. The deterministic security assessment remains "
            "authoritative over optional AI enrichment."
        ),
        notice_type="success",
    )


def render() -> None:
    _hero()
    _why_ecoshield()
    _workflow()
    _explore()
    _privacy()
