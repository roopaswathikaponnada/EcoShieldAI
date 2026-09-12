"""
EcoShield AI
Application Navigation

This module defines the permanent page-navigation structure for
the EcoShield AI Streamlit application.

Responsibilities:
- Define canonical page names
- Define sidebar navigation groups
- Render the EcoShield sidebar
- Track the current page through centralized session state
- Guard pages that require completed assessment data
- Provide safe navigation helpers
- Keep routing metadata separate from app.py and page modules

Business logic, validation, risk scoring, RAG retrieval, and LLM
calls must NOT be implemented in this module.
"""

from __future__ import annotations

from dataclasses import dataclass
from typing import Callable

import streamlit as st

from ui.components import (
    render_brand,
    render_empty_state,
)

from ui.state import (
    get_current_page,
    has_recommendation_result,
    has_risk_assessment,
    is_assessment_completed,
    set_current_page,
    get_theme,
    set_theme,
    THEME_DARK,
    THEME_LIGHT,
)


# ============================================================
# PAGE NAMES
# ============================================================

PAGE_HOME = "Home"

PAGE_ASSESSMENT = "Device Assessment"

PAGE_RISK_ANALYSIS = "Risk Analysis"

PAGE_AI_RECOMMENDATION = "AI Recommendation"

PAGE_SECURE_DATA_GUIDE = "Secure Data Guide"

PAGE_SUSTAINABLE_DISPOSAL = "Sustainable Disposal"

PAGE_KNOWLEDGE_CENTER = "Knowledge Center"

PAGE_IMPACT_DASHBOARD = "Impact Dashboard"

PAGE_ABOUT = "About EcoShield"


# ============================================================
# PAGE GROUP LABELS
# ============================================================

GROUP_PRIMARY = "Assessment"

GROUP_GUIDES = "Guides & Knowledge"

GROUP_PROJECT = "Project"


# ============================================================
# PAGE DEFINITION
# ============================================================

@dataclass(frozen=True)
class PageDefinition:
    """
    Metadata describing one EcoShield application page.

    Attributes
    ----------
    name:
        Canonical internal/display page name.

    icon:
        Sidebar display icon.

    group:
        Navigation group.

    requires_assessment:
        Whether a completed device assessment is required.

    requires_risk:
        Whether a risk assessment result is required.

    requires_recommendation:
        Whether a recommendation result is required.
    """

    name: str

    icon: str

    group: str

    requires_assessment: bool = False

    requires_risk: bool = False

    requires_recommendation: bool = False


# ============================================================
# CANONICAL PAGE REGISTRY
# ============================================================

PAGE_REGISTRY = (
    PageDefinition(
        name=PAGE_HOME,
        icon="🏠",
        group=GROUP_PRIMARY,
    ),

    PageDefinition(
        name=PAGE_ASSESSMENT,
        icon="🔍",
        group=GROUP_PRIMARY,
    ),

    PageDefinition(
        name=PAGE_RISK_ANALYSIS,
        icon="🛡️",
        group=GROUP_PRIMARY,
        requires_assessment=True,
        requires_risk=True,
    ),

    PageDefinition(
        name=PAGE_AI_RECOMMENDATION,
        icon="🤖",
        group=GROUP_PRIMARY,
        requires_assessment=True,
        requires_risk=True,
        requires_recommendation=True,
    ),

    PageDefinition(
        name=PAGE_SECURE_DATA_GUIDE,
        icon="🔐",
        group=GROUP_GUIDES,
    ),

    PageDefinition(
        name=PAGE_SUSTAINABLE_DISPOSAL,
        icon="♻️",
        group=GROUP_GUIDES,
    ),

    PageDefinition(
        name=PAGE_KNOWLEDGE_CENTER,
        icon="📚",
        group=GROUP_GUIDES,
    ),

    PageDefinition(
        name=PAGE_IMPACT_DASHBOARD,
        icon="🌍",
        group=GROUP_PROJECT,
    ),

    PageDefinition(
        name=PAGE_ABOUT,
        icon="ℹ️",
        group=GROUP_PROJECT,
    ),
)


# ============================================================
# PAGE LOOKUP TABLE
# ============================================================

PAGE_LOOKUP = {
    page.name: page
    for page in PAGE_REGISTRY
}


# ============================================================
# VALID PAGE NAMES
# ============================================================

VALID_PAGES = tuple(
    page.name
    for page in PAGE_REGISTRY
)


# ============================================================
# NAVIGATION GROUP ORDER
# ============================================================

NAVIGATION_GROUPS = (
    GROUP_PRIMARY,
    GROUP_GUIDES,
    GROUP_PROJECT,
)


# ============================================================
# PAGE ACCESS CHECK
# ============================================================

def can_access_page(
    page_name: str,
) -> bool:
    """
    Return whether the current session can access a page.

    Public informational pages are always available.

    Risk and recommendation pages require the corresponding
    assessment results.
    """

    page = PAGE_LOOKUP.get(
        page_name
    )

    if page is None:
        return False

    if (
        page.requires_assessment
        and not is_assessment_completed()
    ):
        return False

    if (
        page.requires_risk
        and not has_risk_assessment()
    ):
        return False

    if (
        page.requires_recommendation
        and not has_recommendation_result()
    ):
        return False

    return True


# ============================================================
# PAGE ACCESS REASON
# ============================================================

def get_access_message(
    page_name: str,
) -> tuple[str, str]:
    """
    Return a user-facing title and description explaining
    why a protected page cannot currently be accessed.
    """

    page = PAGE_LOOKUP.get(
        page_name
    )

    if page is None:

        return (
            "Page unavailable",
            (
                "The requested EcoShield page does not "
                "exist."
            ),
        )

    if (
        page.requires_assessment
        and not is_assessment_completed()
    ):

        return (
            "Complete a device assessment first",
            (
                "This page depends on an EcoShield device "
                "assessment. Complete the assessment to "
                "generate the required results."
            ),
        )

    if (
        page.requires_risk
        and not has_risk_assessment()
    ):

        return (
            "Risk analysis is not available yet",
            (
                "A valid cybersecurity risk assessment "
                "must be generated before this page can "
                "be displayed."
            ),
        )

    if (
        page.requires_recommendation
        and not has_recommendation_result()
    ):

        return (
            "Recommendation is not available yet",
            (
                "Complete a valid device assessment so "
                "EcoShield can generate its security and "
                "sustainability recommendations."
            ),
        )

    return (
        "Page available",
        "",
    )


# ============================================================
# SAFE PAGE NORMALIZATION
# ============================================================

def normalize_page_name(
    page_name: str | None,
) -> str:
    """
    Return a safe canonical page name.

    Unknown or empty values fall back to Home.
    """

    if not isinstance(
        page_name,
        str,
    ):

        return PAGE_HOME

    normalized = (
        page_name.strip()
    )

    if normalized not in PAGE_LOOKUP:
        return PAGE_HOME

    return normalized


# ============================================================
# NAVIGATE
# ============================================================

def navigate_to(
    page_name: str,
    *,
    rerun: bool = True,
) -> bool:
    """
    Navigate to an EcoShield page.

    Protected pages are not entered unless their required
    session data exists.

    Parameters
    ----------
    page_name:
        Target canonical page name.

    rerun:
        Whether Streamlit should rerun immediately after
        navigation.

    Returns
    -------
    bool
        True when navigation succeeded.
        False when the target page is unavailable.
    """

    normalized = normalize_page_name(
        page_name
    )

    if not can_access_page(
        normalized
    ):

        return False

    set_current_page(
        normalized
    )

    if rerun:
        st.rerun()

    return True


# ============================================================
# FORCE NAVIGATION
# ============================================================

def force_navigate_to(
    page_name: str,
    *,
    rerun: bool = True,
) -> None:
    """
    Navigate without page-access checks.

    This is intended only for safe public destinations such
    as Home or Device Assessment.

    Use navigate_to() for protected pages.
    """

    normalized = normalize_page_name(
        page_name
    )

    set_current_page(
        normalized
    )

    if rerun:
        st.rerun()


# ============================================================
# CURRENT PAGE VALIDATION
# ============================================================

def ensure_valid_current_page() -> str:
    """
    Validate the currently stored page.

    Invalid values are reset to Home.

    Protected pages that lose their required session data are
    redirected to Device Assessment.
    """

    current = normalize_page_name(
        get_current_page()
    )

    if current not in PAGE_LOOKUP:

        set_current_page(
            PAGE_HOME
        )

        return PAGE_HOME

    if not can_access_page(
        current
    ):

        if current in {
            PAGE_RISK_ANALYSIS,
            PAGE_AI_RECOMMENDATION,
        }:

            set_current_page(
                PAGE_ASSESSMENT
            )

            return PAGE_ASSESSMENT

        set_current_page(
            PAGE_HOME
        )

        return PAGE_HOME

    if current != get_current_page():

        set_current_page(
            current
        )

    return current


# ============================================================
# SIDEBAR PAGE BUTTON
# ============================================================

def _render_page_button(
    page: PageDefinition,
    current_page: str,
) -> None:
    """
    Render one sidebar navigation button.
    """

    is_active = (
        page.name == current_page
    )

    accessible = can_access_page(
        page.name
    )

    label = (
        f"{page.icon}  {page.name}"
    )

    button_type = (
        "primary"
        if is_active
        else "secondary"
    )

    clicked = st.button(
        label,
        key=(
            "nav_"
            + page.name
            .lower()
            .replace(" ", "_")
        ),
        use_container_width=True,
        type=button_type,
        disabled=not accessible,
    )

    if clicked:

        set_current_page(
            page.name
        )

        st.rerun()


# ============================================================
# SIDEBAR NAVIGATION
# ============================================================

def render_sidebar_navigation() -> str:
    """
    Render the permanent EcoShield sidebar.
    """

    current_page = (
        ensure_valid_current_page()
    )

    with st.sidebar:

        render_brand(
            name="EcoShield AI",
            tagline=(
                "Secure Devices. "
                "Greener Tomorrow."
            ),
            icon="🛡️",
        )

        # --------------------------------------------------------
        # Theme switcher
        # --------------------------------------------------------

        current_theme = (
            get_theme()
        )

        theme_col1, theme_col2 = (
            st.columns(2)
        )

        with theme_col1:

            light_clicked = st.button(
                "☀️ Light",
                key="theme_light",
                use_container_width=True,
                type=(
                    "primary"
                    if current_theme
                    == THEME_LIGHT
                    else "secondary"
                ),
            )

        with theme_col2:

            dark_clicked = st.button(
                "🌙 Dark",
                key="theme_dark",
                use_container_width=True,
                type=(
                    "primary"
                    if current_theme
                    == THEME_DARK
                    else "secondary"
                ),
            )

        if light_clicked:

            set_theme(
                THEME_LIGHT
            )

            st.rerun()

        if dark_clicked:

            set_theme(
                THEME_DARK
            )

            st.rerun()

        st.caption(
            "AI-powered e-waste security & "
            "sustainability advisor"
        )

        st.divider()

        for group in NAVIGATION_GROUPS:

            if group == GROUP_PRIMARY:

                label = (
                    "ASSESSMENT"
                )

            elif group == GROUP_GUIDES:

                label = (
                    "GUIDES & KNOWLEDGE"
                )

            else:

                label = (
                    "PROJECT"
                )

            st.caption(
                label
            )

            for page in PAGE_REGISTRY:

                if page.group != group:
                    continue

                _render_page_button(
                    page,
                    current_page,
                )

            st.divider()

        # ----------------------------------------------------
        # Privacy / mode information
        # ----------------------------------------------------

        st.caption(
            "PRIVACY"
        )

        st.markdown(
            """
            EcoShield evaluates device-security status
            without requiring passwords or personal files.
            """
        )

        st.caption(
            "Current mode: "
            "Deterministic Risk Assessment"
        )

    return current_page


# ============================================================
# PROTECTED PAGE EMPTY STATE
# ============================================================

def render_protected_page(
    page_name: str,
    *,
    redirect_page: str = PAGE_ASSESSMENT,
    redirect_label: str = "Start Device Assessment",
) -> bool:
    """
    Guard a protected page at render time.

    Usage
    -----
    if not render_protected_page(PAGE_RISK_ANALYSIS):
        return

    Returns
    -------
    bool
        True if access is allowed.
        False if an empty-state guard was displayed.
    """

    normalized = normalize_page_name(
        page_name
    )

    if can_access_page(
        normalized
    ):
        return True

    title, description = (
        get_access_message(
            normalized
        )
    )

    render_empty_state(
        title=title,
        description=description,
        icon="🛡️",
    )

    st.write("")

    col1, col2, col3 = st.columns(
        [1, 2, 1]
    )

    with col2:

        if st.button(
            redirect_label,
            key=(
                "protected_redirect_"
                + normalized
                .lower()
                .replace(" ", "_")
            ),
            use_container_width=True,
            type="primary",
        ):

            force_navigate_to(
                redirect_page
            )

    return False


# ============================================================
# PAGE ROUTER HELPER
# ============================================================

def render_page(
    page_renderers: dict[
        str,
        Callable[[], None],
    ],
) -> None:
    """
    Render the current page using a supplied renderer mapping.

    app.py will eventually pass:

        {
            PAGE_HOME: render_home,
            PAGE_ASSESSMENT: render_assessment,
            ...
        }

    Missing renderers fail gracefully rather than crashing the
    entire application.
    """

    current_page = (
        ensure_valid_current_page()
    )

    renderer = page_renderers.get(
        current_page
    )

    if renderer is None:

        render_empty_state(
            title="Page is being prepared",
            description=(
                "This EcoShield page is not available "
                "in the current build."
            ),
            icon="🛠️",
        )

        return

    renderer()