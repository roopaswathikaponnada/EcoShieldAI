"""
EcoShield AI
About Page

This module renders information about the EcoShield AI
project, its purpose, architecture, capabilities, privacy
principles, technology stack, and limitations.

Responsibilities:
- Explain the EcoShield AI project
- Present the problem and proposed solution
- Explain the security + sustainability approach
- Present the system architecture
- Describe privacy-by-design principles
- Present current and planned capabilities
- Explain project limitations transparently

Business logic, validation, risk scoring, RAG retrieval,
vector-store operations, and LLM calls must NOT be
implemented directly in this module.
"""

from __future__ import annotations

import streamlit as st

from config.config import (
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
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
    PAGE_KNOWLEDGE_CENTER,
    force_navigate_to,
)


# ============================================================
# PROJECT INTRODUCTION
# ============================================================

def _render_project_introduction() -> None:
    """
    Explain the purpose of EcoShield AI.
    """

    render_section_header(
        title="What is EcoShield AI?",
        description=(
            "A decision-support system combining cybersecurity "
            "and sustainable electronics lifecycle guidance."
        ),
        icon="🛡️",
    )

    st.markdown(
        """
        **EcoShield AI** helps users make safer decisions before
        selling, donating, reusing, repairing, recycling, or
        disposing of electronic devices.

        Electronic devices can contain personal information,
        account data, credentials, documents, photographs, and
        other sensitive information even when the owner no longer
        intends to use the device.

        At the same time, prematurely discarding functional
        electronics contributes to unnecessary electronic waste.

        EcoShield brings these two concerns together:

        **protect the data first, then make the most responsible
        lifecycle decision for the device.**
        """
    )


# ============================================================
# PROBLEM
# ============================================================

def _render_problem() -> None:
    """
    Present the problem addressed by EcoShield.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="The Problem",
        description=(
            "Device disposal is both a cybersecurity problem "
            "and a sustainability problem."
        ),
        icon="⚠️",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        render_feature_card(
            icon="🔐",
            title="Data Exposure Risk",
            description=(
                "Devices may still contain personal or sensitive "
                "information when they are sold, donated, recycled, "
                "or transferred to another person."
            ),
        )

    with col2:

        render_feature_card(
            icon="♻️",
            title="Electronic Waste",
            description=(
                "Devices that could potentially be reused, repaired, "
                "donated, or resold may instead be discarded "
                "prematurely."
            ),
        )


# ============================================================
# SOLUTION
# ============================================================

def _render_solution() -> None:
    """
    Explain the EcoShield approach.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="The EcoShield Approach",
        description=(
            "EcoShield evaluates security readiness before "
            "supporting the next device lifecycle decision."
        ),
        icon="🌱",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="🔍",
            title="Assess",
            description=(
                "Collect security-relevant information about "
                "the device without requesting passwords, "
                "personal files, or account credentials."
            ),
        )

    with col2:

        render_feature_card(
            icon="🛡️",
            title="Protect",
            description=(
                "Evaluate cybersecurity risk and identify "
                "unresolved actions such as account removal, "
                "backup, encryption, or data sanitization."
            ),
        )

    with col3:

        render_feature_card(
            icon="♻️",
            title="Act Responsibly",
            description=(
                "Recommend reuse, repair, donation, resale, "
                "or responsible recycling based on the device "
                "and its preparation status."
            ),
        )


# ============================================================
# HOW THE SYSTEM WORKS
# ============================================================

def _render_system_flow() -> None:
    """
    Explain the high-level EcoShield processing pipeline.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="How EcoShield Works",
        description=(
            "The system separates validation, deterministic "
            "security analysis, recommendation logic, and "
            "AI knowledge enrichment."
        ),
        icon="⚙️",
    )

    st.markdown(
        """
        ### 1. Device Assessment
        The user provides device-condition and security-status
        information.

        ↓

        ### 2. Input Validation
        EcoShield checks whether the supplied information is
        complete, valid, and internally consistent.

        ↓

        ### 3. Security Risk Analysis
        The deterministic risk engine evaluates known security
        conditions and produces an explainable risk assessment.

        ↓

        ### 4. Recommendation Engine
        Security and sustainability actions are generated from
        the validated assessment.

        ↓

        ### 5. Knowledge Retrieval
        The RAG layer can retrieve relevant information from
        EcoShield's curated knowledge base.

        ↓

        ### 6. AI Guidance
        The language-model layer can use retrieved evidence and
        deterministic assessment results to produce clearer,
        contextual guidance.

        ↓

        ### 7. Responsible Action
        The user receives actionable guidance before transferring
        or disposing of the device.
        """
    )


# ============================================================
# ARCHITECTURE
# ============================================================

def _render_architecture() -> None:
    """
    Present the logical project architecture.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="System Architecture",
        description=(
            "EcoShield uses a modular architecture so that "
            "presentation, deterministic logic, retrieval, "
            "and AI responsibilities remain separated."
        ),
        icon="🏗️",
    )

    st.code(
        """
User
 │
 ▼
Streamlit Interface
 │
 ├── Device Assessment
 │
 ├── Risk Analysis
 │
 ├── AI Recommendation
 │
 ├── Security Guides
 │
 └── Knowledge Center
 │
 ▼
Input Validation
 │
 ▼
Deterministic Risk Engine
 │
 ▼
Recommendation Engine
 │
 ├───────────────┐
 │               │
 ▼               ▼
Knowledge Base   Assessment Context
 │               │
 ▼               │
RAG Retriever    │
 │               │
 └───────┬───────┘
         ▼
      LLM Layer
         │
         ▼
Grounded Guidance
        """.strip(),
        language="text",
    )


# ============================================================
# CORE CAPABILITIES
# ============================================================

def _render_capabilities() -> None:
    """
    Present major EcoShield capabilities.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Core Capabilities",
        description=(
            "EcoShield combines security assessment, "
            "decision support, education, and sustainability."
        ),
        icon="✨",
    )

    first_row = st.columns(
        3
    )

    with first_row[0]:

        render_feature_card(
            icon="✅",
            title="Input Validation",
            description=(
                "Checks device-assessment information before "
                "security analysis begins."
            ),
        )

    with first_row[1]:

        render_feature_card(
            icon="🛡️",
            title="Risk Assessment",
            description=(
                "Produces explainable cybersecurity risk scores "
                "from device security conditions."
            ),
        )

    with first_row[2]:

        render_feature_card(
            icon="📋",
            title="Action Guidance",
            description=(
                "Provides prioritized security preparation "
                "steps before device transfer or disposal."
            ),
        )

    render_spacer(
        "sm"
    )

    second_row = st.columns(
        3
    )

    with second_row[0]:

        render_feature_card(
            icon="🌱",
            title="Sustainability Guidance",
            description=(
                "Encourages reuse, repair, donation, resale, "
                "and responsible recycling when appropriate."
            ),
        )

    with second_row[1]:

        render_feature_card(
            icon="📚",
            title="Knowledge Retrieval",
            description=(
                "Uses curated cybersecurity and sustainability "
                "knowledge to support grounded guidance."
            ),
        )

    with second_row[2]:

        render_feature_card(
            icon="🤖",
            title="AI Assistance",
            description=(
                "Supports contextual explanation while keeping "
                "deterministic security decisions separate from "
                "generative AI."
            ),
        )


# ============================================================
# PRIVACY
# ============================================================

def _render_privacy() -> None:
    """
    Explain EcoShield privacy principles.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Privacy by Design",
        description=(
            "EcoShield is designed to evaluate device security "
            "without inspecting the user's private content."
        ),
        icon="🔒",
    )

    render_notice(
        title="Your device content is not required",
        message=(
            "EcoShield does not need passwords, account "
            "credentials, personal documents, photographs, "
            "messages, or the actual contents of the device "
            "to perform its assessment."
        ),
        notice_type="success",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="🚫",
            title="No Password Collection",
            description=(
                "Passwords and authentication secrets are "
                "not assessment inputs."
            ),
        )

    with col2:

        render_feature_card(
            icon="📁",
            title="No File Inspection",
            description=(
                "EcoShield evaluates security status rather "
                "than reading personal device files."
            ),
        )

    with col3:

        render_feature_card(
            icon="🧠",
            title="Minimal Assessment Data",
            description=(
                "Only information relevant to security readiness "
                "and lifecycle decisions is requested."
            ),
        )


# ============================================================
# TECHNOLOGY STACK
# ============================================================

def _render_technology_stack() -> None:
    """
    Present the technology architecture without exposing
    implementation secrets.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Technology Stack",
        description=(
            "EcoShield is built as a modular Python application."
        ),
        icon="💻",
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:

        render_feature_card(
            icon="🎨",
            title="Streamlit",
            description=(
                "Interactive application interface, navigation, "
                "forms, dashboards, and visualization."
            ),
        )

    with col2:

        render_feature_card(
            icon="🐍",
            title="Python",
            description=(
                "Validation, risk assessment, recommendation "
                "logic, retrieval, and application services."
            ),
        )

    with col3:

        render_feature_card(
            icon="🧠",
            title="RAG + LLM",
            description=(
                "Evidence retrieval and contextual AI guidance "
                "using the EcoShield knowledge base."
            ),
        )


# ============================================================
# DESIGN PRINCIPLES
# ============================================================

def _render_design_principles() -> None:
    """
    Present engineering principles followed by EcoShield.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Design Principles",
        description=(
            "The system is designed around explainability, "
            "privacy, modularity, and responsible AI."
        ),
        icon="🎯",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        st.markdown(
            """
            **🛡️ Security First**

            Security issues should be resolved before a device
            changes ownership.

            **🔎 Explainable Decisions**

            Risk scores should be traceable to identifiable
            assessment conditions.

            **🔐 Privacy by Design**

            Collect only the information required to make the
            assessment.
            """
        )

    with col2:

        st.markdown(
            """
            **🌱 Sustainability Aware**

            Reuse and lifecycle extension should be considered
            before unnecessary disposal.

            **🤖 Responsible AI**

            Generative AI should explain and enrich guidance,
            not silently replace deterministic security rules.

            **🧩 Modular Architecture**

            Frontend, risk logic, retrieval, and AI services
            remain separated for easier testing and maintenance.
            """
        )


# ============================================================
# LIMITATIONS
# ============================================================

def _render_limitations() -> None:
    """
    Transparently communicate project limitations.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Important Limitations",
        description=(
            "EcoShield is a decision-support system and should "
            "not be represented as a forensic data-destruction "
            "verification tool."
        ),
        icon="ℹ️",
    )

    render_notice(
        title="Decision support, not device forensics",
        message=(
            "EcoShield evaluates information supplied by the "
            "user. It does not directly inspect storage media, "
            "verify that deleted information is unrecoverable, "
            "or certify that a device has been professionally "
            "sanitized."
        ),
        notice_type="warning",
    )

    st.markdown(
        """
        EcoShield's recommendations depend on the accuracy of the
        information entered during assessment.

        Device-specific sanitization procedures can differ by
        operating system, storage technology, hardware condition,
        and manufacturer.

        Professional or organizational environments may also
        require additional policies, compliance procedures, or
        certified destruction methods.
        """
    )


# ============================================================
# PROJECT INFORMATION
# ============================================================

def _render_project_information() -> None:
    """
    Display project metadata.
    """

    render_spacer(
        "lg"
    )

    render_section_header(
        title="Project Information",
        icon="📌",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        st.markdown(
            f"""
            **Project**

            {PROJECT_NAME}

            **Version**

            {PROJECT_VERSION}
            """
        )

    with col2:

        st.markdown(
            f"""
            **Purpose**

            {PROJECT_DESCRIPTION}

            **Application Type**

            Cybersecurity + Sustainability Decision Support
            """
        )


# ============================================================
# FINAL CTA
# ============================================================

def _render_final_actions() -> None:
    """
    Render final navigation actions.
    """

    render_spacer(
        "lg"
    )

    st.divider()

    st.markdown(
        """
        ### Ready to use EcoShield?

        Assess a device or explore the EcoShield Knowledge Center.
        """
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        if st.button(
            "🛡️ Assess My Device",
            key="about_assessment",
            type="primary",
            use_container_width=True,
        ):

            force_navigate_to(
                PAGE_ASSESSMENT
            )

    with col2:

        if st.button(
            "📚 Explore Knowledge Center",
            key="about_knowledge",
            use_container_width=True,
        ):

            force_navigate_to(
                PAGE_KNOWLEDGE_CENTER
            )


# ============================================================
# PUBLIC PAGE RENDERER
# ============================================================

def render() -> None:
    """
    Render the complete About EcoShield page.
    """

    render_page_header(
        kicker="About the Project",
        title="About EcoShield AI",
        subtitle=(
            "A cybersecurity and sustainability decision-support "
            "system for safer electronic-device reuse, transfer, "
            "recycling, and disposal."
        ),
        icon="🛡️🌱",
    )

    _render_project_introduction()

    _render_problem()

    _render_solution()

    _render_system_flow()

    _render_architecture()

    _render_capabilities()

    _render_privacy()

    _render_technology_stack()

    _render_design_principles()

    _render_limitations()

    _render_project_information()

    _render_final_actions()