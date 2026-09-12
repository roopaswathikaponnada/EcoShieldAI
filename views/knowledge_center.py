"""
EcoShield AI
Knowledge Center

This module renders EcoShield's cybersecurity and
sustainability knowledge interface.

Responsibilities:
- Present trusted educational guidance
- Organize cybersecurity and sustainability topics
- Provide lightweight local topic discovery
- Provide the EcoShield AI Advisor frontend interface
- Connect Advisor requests through the service boundary
- Guide users toward device assessment when appropriate

Vector-store logic, embeddings, document loading,
retrieval algorithms, semantic validation, and direct
LLM execution must NOT be implemented in this module.
"""

from __future__ import annotations

import streamlit as st

from src.services.advisor_service import (
    AdvisorGenerationStatus,
    ask_advisor,
)

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

from ui.state import (
    get_advisor_result,
    get_last_question,
    get_rag_sources,
    get_recommendation_result,
    get_risk_assessment,
    set_advisor_result,
)

# ============================================================
# KNOWLEDGE CATEGORIES
# ============================================================

KNOWLEDGE_CATEGORIES = (
    (
        "🧹",
        "Secure Data Erasure",
        (
            "Understand factory resets, secure erasure, "
            "storage sanitization, and safe device preparation."
        ),
    ),
    (
        "🛡️",
        "Device Security",
        (
            "Learn how encryption, account protection, "
            "device access, and security controls reduce risk."
        ),
    ),
    (
        "🔐",
        "Privacy Protection",
        (
            "Understand how personal and sensitive information "
            "can remain exposed during device transfer."
        ),
    ),
    (
        "🔄",
        "Device Reuse",
        (
            "Learn how devices can be safely prepared for "
            "reuse, donation, resale, or reassignment."
        ),
    ),
    (
        "♻️",
        "E-Waste & Recycling",
        (
            "Understand responsible electronics recycling "
            "and why devices should not enter ordinary waste."
        ),
    ),
    (
        "🌱",
        "Sustainable Electronics",
        (
            "Explore repair, lifecycle extension, reuse, "
            "and environmentally responsible device decisions."
        ),
    ),
)


# ============================================================
# FEATURED GUIDANCE
# ============================================================

FEATURED_GUIDANCE = (
    (
        "Before selling a device",
        (
            "Back up important information, remove accounts, "
            "review encryption and sanitization status, remove "
            "removable media, and complete the appropriate reset."
        ),
    ),
    (
        "Before donating a device",
        (
            "Treat donation like any other ownership transfer. "
            "Personal information should be protected before the "
            "device reaches its next user."
        ),
    ),
    (
        "Before recycling a device",
        (
            "Protect stored information first and use an "
            "appropriate e-waste collection or recycling route."
        ),
    ),
)


# ============================================================
# SEARCH INTERFACE
# ============================================================

def _render_search() -> None:
    """
    Render lightweight local knowledge-topic discovery.

    This search matches the page's predefined educational
    categories only. Grounded RAG and AI questions are handled
    separately by the EcoShield Advisor through the service
    boundary below.
    """

    render_section_header(
        title="Search EcoShield Knowledge",
        description=(
            "Explore guidance about device security, privacy, "
            "data sanitization, reuse, repair, and recycling."
        ),
        icon="🔎",
    )

    query = st.text_input(
        "What would you like to learn about?",
        placeholder=(
            "Example: How should I prepare a laptop "
            "before selling it?"
        ),
        key="knowledge_search_query",
    )

    if query:

        normalized_query = (
            query.strip().lower()
        )

        matches = []

        for (
            icon,
            title,
            description,
        ) in KNOWLEDGE_CATEGORIES:

            searchable_text = (
                f"{title} {description}"
            ).lower()

            if any(
                word in searchable_text
                for word in normalized_query.split()
            ):
                matches.append(
                    (
                        icon,
                        title,
                        description,
                    )
                )

        if matches:

            st.caption(
                "Related EcoShield knowledge topics"
            )

            for (
                icon,
                title,
                description,
            ) in matches:

                render_feature_card(
                    icon=icon,
                    title=title,
                    description=description,
                )

        else:

            render_notice(
    title="No matching local topic",
    message=(
        "No predefined knowledge category matched this query. "
        "Try broader search terms, or use Ask EcoShield AI "
        "below for grounded cybersecurity and sustainability "
        "guidance."
    ),
    notice_type="info",
)


# ============================================================
# KNOWLEDGE CATEGORY CARDS
# ============================================================

def _render_categories() -> None:
    """
    Render the primary knowledge categories.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Explore Topics",
        description=(
            "Browse the core cybersecurity and sustainability "
            "areas covered by EcoShield."
        ),
        icon="📚",
    )

    rows = (
        KNOWLEDGE_CATEGORIES[:3],
        KNOWLEDGE_CATEGORIES[3:],
    )

    for row in rows:

        columns = st.columns(
            3
        )

        for (
            column,
            category,
        ) in zip(
            columns,
            row,
        ):

            icon, title, description = (
                category
            )

            with column:

                render_feature_card(
                    icon=icon,
                    title=title,
                    description=description,
                )

        render_spacer(
            "sm"
        )


# ============================================================
# FEATURED GUIDANCE
# ============================================================

def _render_featured_guidance() -> None:
    """
    Render commonly needed device-handling guidance.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Featured Guidance",
        description=(
            "Quick guidance for common electronic-device "
            "ownership transitions."
        ),
        icon="💡",
    )

    for title, description in (
        FEATURED_GUIDANCE
    ):

        with st.expander(
            title,
            expanded=False,
        ):

            st.write(
                description
            )


# ============================================================
# CYBERSECURITY KNOWLEDGE
# ============================================================

def _render_security_knowledge() -> None:
    """
    Render introductory cybersecurity knowledge.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Cybersecurity Knowledge",
        description=(
            "Understand the security controls that matter "
            "before a device changes ownership or leaves "
            "your control."
        ),
        icon="🛡️",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="🔒",
            title="Encryption",
            description=(
                "Encryption helps protect stored information "
                "when unauthorized users cannot unlock the device."
            ),
        )

    with col2:

        render_feature_card(
            icon="🧹",
            title="Data Sanitization",
            description=(
                "Appropriate sanitization reduces the chance "
                "that previous information remains recoverable."
            ),
        )

    with col3:

        render_feature_card(
            icon="👤",
            title="Account Removal",
            description=(
                "Signing out and removing linked accounts helps "
                "prevent unintended access after transfer."
            ),
        )


# ============================================================
# SUSTAINABILITY KNOWLEDGE
# ============================================================

def _render_sustainability_knowledge() -> None:
    """
    Render introductory sustainable-electronics knowledge.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Sustainability Knowledge",
        description=(
            "Understand how extending device life can reduce "
            "premature electronic waste."
        ),
        icon="🌱",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="🔧",
            title="Repair",
            description=(
                "Repairing a usable device can extend its "
                "service life and delay replacement."
            ),
        )

    with col2:

        render_feature_card(
            icon="🔄",
            title="Reuse",
            description=(
                "Safe reuse allows functional hardware to "
                "continue providing value."
            ),
        )

    with col3:

        render_feature_card(
            icon="♻️",
            title="Responsible Recycling",
            description=(
                "When reuse is no longer practical, appropriate "
                "e-waste recycling supports responsible "
                "end-of-life handling."
            ),
        )


# ============================================================
# ECOSHIELD AI ADVISOR
# ============================================================

def _should_generate_advisor_answer(
    question: str,
) -> bool:
    """
    Return whether the submitted question requires a new
    Advisor generation.

    A normal Streamlit rerun must not regenerate an answer that
    is already stored for the same submitted question.
    """

    normalized_question = question.strip()

    if not normalized_question:
        return False

    existing_result = get_advisor_result()

    if existing_result is None:
        return True

    last_question = get_last_question()

    if (
        isinstance(last_question, str)
        and last_question.strip() == normalized_question
    ):
        return False

    return True

def _render_ai_knowledge_assistant() -> None:
    """
    Render the EcoShield AI Advisor interface.

    The frontend calls only the Advisor service boundary.
    Retrieval, LLM generation, semantic validation, fallbacks,
    and deterministic authority remain backend responsibilities.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Ask EcoShield AI",
        description=(
            "Ask about device security, secure data handling, "
            "e-waste, sustainability, or your completed "
            "EcoShield assessment."
        ),
        icon="🤖",
    )

    question = st.text_area(
        "Your question",
        placeholder=(
            "Example: Is my device safe to sell now? "
            "Or: How should I securely erase an SSD?"
        ),
        height=110,
        key="knowledge_ai_question",
    )

    normalized_question = (
        question.strip()
        if isinstance(question, str)
        else ""
    )

    ask_clicked = st.button(
        "🤖 Ask EcoShield AI",
        key="knowledge_ai_button",
        type="primary",
        use_container_width=True,
        disabled=not bool(normalized_question),
    )

    if ask_clicked:

        should_generate = (
            _should_generate_advisor_answer(
                normalized_question
            )
        )

        if should_generate:

            assessment = (
                get_risk_assessment()
            )

            recommendation = (
                get_recommendation_result()
            )

            try:
                with st.spinner(
                    "EcoShield is retrieving grounded guidance..."
                ):
                    result = ask_advisor(
                        normalized_question,
                        assessment=assessment,
                        recommendation=recommendation,
                    )

                set_advisor_result(
                    question=normalized_question,
                    result=result,
                )

            except Exception:
                st.error(
                    "EcoShield could not process this question "
                    "because an unexpected Advisor error occurred."
                )

    result = get_advisor_result()


    if result is None:
        st.caption(
            "EcoShield answers are grounded in its curated "
            "cybersecurity and sustainability knowledge base."
        )
        return

    st.divider()

    st.markdown(
        "### EcoShield Answer"
    )

    status = getattr(
        result,
        "status",
        None,
    )

    if (
        status
        == AdvisorGenerationStatus.SUCCESS
    ):
        st.success(
            "Grounded EcoShield guidance generated successfully."
        )

    elif (
        status
        == AdvisorGenerationStatus.FALLBACK
    ):
        st.warning(
            "EcoShield used a safe fallback because the generated "
            "AI answer could not be fully accepted."
        )

    elif (
        status
        == AdvisorGenerationStatus.UNAVAILABLE
    ):
        st.info(
            "EcoShield could not provide a grounded answer for "
            "this request in the current context."
        )

    elif (
        status
        == AdvisorGenerationStatus.ERROR
    ):
        st.error(
            "EcoShield encountered an Advisor processing error."
        )

    answer = getattr(
        result,
        "answer",
        "",
    )

    if isinstance(answer, str) and answer.strip():
        st.markdown(
            answer
        )

    sources = get_rag_sources()

    if sources:

        st.markdown(
            "#### Grounded Sources"
        )

        for source in sources:
            st.markdown(
                f"- `{source}`"
            )

    warnings = getattr(
        result,
        "warnings",
        (),
    )

    if warnings:

        with st.expander(
            "Advisor notices"
        ):
            for warning in warnings:
                st.warning(
                    str(warning)
                )

    errors = getattr(
        result,
        "errors",
        (),
    )

    if errors:

        with st.expander(
            "Advisor status details"
        ):
            for error in errors:
                st.caption(
                    str(error)
                )

# ============================================================
# ASSESSMENT CTA
# ============================================================

def _render_assessment_cta() -> None:
    """
    Render assessment navigation CTA.
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
            "### Need guidance for a specific device?"
        )

        st.caption(
            "Run the EcoShield assessment to evaluate "
            "your device's actual security condition and "
            "recommended next steps."
        )

        if st.button(
            "🛡️ Assess My Device",
            key="knowledge_assessment_cta",
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
    Render the complete Knowledge Center page.
    """

    render_page_header(
        kicker="Cybersecurity + Sustainability",
        title="Knowledge Center",
        subtitle=(
            "Explore practical guidance for protecting "
            "device data, extending electronics lifecycles, "
            "and making responsible disposal decisions."
        ),
        icon="📚",
    )

    render_notice(
        title="Learn before you act",
        message=(
            "Different devices, storage technologies, and "
            "ownership-transfer situations can require "
            "different security precautions."
        ),
        notice_type="info",
    )

    render_spacer(
        "lg"
    )

    _render_search()

    _render_categories()

    _render_featured_guidance()

    _render_security_knowledge()

    _render_sustainability_knowledge()

    _render_ai_knowledge_assistant()

    _render_assessment_cta()