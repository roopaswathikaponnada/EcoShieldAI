"""
EcoShield AI
Main Streamlit Application Shell

This module is the permanent application entry point for
EcoShield AI.

Responsibilities:
- Configure the Streamlit application
- Initialize centralized session state
- Apply the global EcoShield visual system
- Render permanent sidebar navigation
- Dynamically load and render application views
- Display shared flash messages
- Render the global footer
- Fail gracefully when a page is unavailable

Business logic must NOT be implemented here.

Validation belongs to:
    src/validators.py

Cybersecurity risk scoring belongs to:
    src/risk_engine.py

Deterministic recommendations belong to:
    src/recommendation.py

RAG belongs to:
    src/rag/*

LLM integration belongs to:
    src/ai/*
"""

from __future__ import annotations

import importlib
from collections.abc import Callable
from types import ModuleType

import streamlit as st
from config.config import (
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
    PROJECT_NAME,
    PROJECT_VERSION,
)

from ui.components import (
    render_empty_state,
    render_footer,
    render_notice,
)

from ui.navigation import (
    PAGE_ABOUT,
    PAGE_AI_RECOMMENDATION,
    PAGE_ASSESSMENT,
    PAGE_HOME,
    PAGE_IMPACT_DASHBOARD,
    PAGE_KNOWLEDGE_CENTER,
    PAGE_RISK_ANALYSIS,
    PAGE_SECURE_DATA_GUIDE,
    PAGE_SUSTAINABLE_DISPOSAL,
    render_sidebar_navigation,
)

from ui.state import (
    get_theme,
    initialize_session_state,
    pop_error_message,
    pop_success_message,
)

from ui.styles import (
    apply_global_styles,
)


# ============================================================
# STREAMLIT PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
    initial_sidebar_state="expanded",
)


# ============================================================
# PAGE MODULE REGISTRY
# ============================================================

PAGE_MODULES: dict[str, str] = {
    PAGE_HOME: "views.home",
    PAGE_ASSESSMENT: "views.assessment",
    PAGE_RISK_ANALYSIS: "views.risk_analysis",
    PAGE_AI_RECOMMENDATION: "views.ai_recommendation",
    PAGE_SECURE_DATA_GUIDE: "views.secure_data_guide",
    PAGE_SUSTAINABLE_DISPOSAL: "views.sustainable_disposal",
    PAGE_KNOWLEDGE_CENTER: "views.knowledge_center",
    PAGE_IMPACT_DASHBOARD: "views.impact_dashboard",
    PAGE_ABOUT: "views.about",
}


# ============================================================
# VIEW CONTRACT
# ============================================================

VIEW_RENDER_FUNCTION = "render"


# ============================================================
# PAGE MODULE LOADER
# ============================================================

def _load_page_module(
    module_path: str,
) -> ModuleType | None:
    """
    Dynamically import an EcoShield view module.

    Parameters
    ----------
    module_path:
        Python import path such as ``views.home``.

    Returns
    -------
    ModuleType | None
        Imported module when available.

        None when the module cannot currently be loaded.

    Notes
    -----
    Individual view modules are loaded lazily so unfinished
    pages do not prevent the entire application from starting.
    """

    try:

        return importlib.import_module(
            module_path
        )

    except (
        ImportError,
        ModuleNotFoundError,
    ):

        return None


# ============================================================
# PAGE RENDERER RESOLUTION
# ============================================================

def _get_page_renderer(
    page_name: str,
) -> Callable[[], None] | None:
    """
    Resolve the render() function for a page.

    Every final file inside views/ follows one permanent
    convention:

        def render() -> None:
            ...

    This allows app.py to remain unchanged as pages are
    implemented one by one.
    """

    module_path = PAGE_MODULES.get(
        page_name
    )

    if module_path is None:
        return None

    module = _load_page_module(
        module_path
    )

    if module is None:
        return None

    renderer = getattr(
        module,
        VIEW_RENDER_FUNCTION,
        None,
    )

    if not callable(renderer):
        return None

    return renderer


# ============================================================
# UNAVAILABLE PAGE FALLBACK
# ============================================================

def _render_unavailable_page(
    page_name: str,
) -> None:
    """
    Render a clean fallback while a view has not yet been built.
    """

    render_empty_state(
        title=f"{page_name} is being prepared",
        description=(
            "This EcoShield page is part of the final "
            "application architecture but its view has not "
            "yet been implemented in the current build."
        ),
        icon="🛠️",
    )

    st.info(
        "The application shell is working correctly. "
        "This page will become available automatically once "
        "its view module defines a render() function."
    )


# ============================================================
# FLASH MESSAGES
# ============================================================

def _render_flash_messages() -> None:
    """
    Display temporary cross-page success and error messages.

    Messages are automatically cleared after rendering.
    """

    error_message = (
        pop_error_message()
    )

    if error_message:

        render_notice(
            title="EcoShield could not complete the action",
            message=error_message,
            notice_type="error",
        )

    success_message = (
        pop_success_message()
    )

    if success_message:

        render_notice(
            title="Success",
            message=success_message,
            notice_type="success",
        )


# ============================================================
# CURRENT PAGE RENDERING
# ============================================================

def _render_current_page(
    page_name: str,
) -> None:
    """
    Render the currently selected EcoShield view.
    """

    renderer = _get_page_renderer(
        page_name
    )

    if renderer is None:

        _render_unavailable_page(
            page_name
        )

        return

    try:

        renderer()

    except Exception as exc:

        # ----------------------------------------------------
        # Keep the application shell alive even when an
        # individual page encounters an unexpected error.
        #
        # Detailed traceback is intentionally not exposed
        # directly to end users in production UI.
        # ----------------------------------------------------

        render_notice(
            title="Page could not be displayed",
            message=(
                "EcoShield encountered an unexpected error "
                "while loading this page. Please return to "
                "another page or try again."
            ),
            notice_type="error",
        )

        # Development-safe logging to the terminal.
        # No user secrets or device contents should be logged.
        print(
            f"[EcoShield] Error rendering "
            f"'{page_name}': "
            f"{type(exc).__name__}: {exc}"
        )


# ============================================================
# APPLICATION BOOTSTRAP
# ============================================================

def main() -> None:
    """
    Start the EcoShield AI Streamlit application.
    """

    # --------------------------------------------------------
    # 1. Initialize application state
    # --------------------------------------------------------

    initialize_session_state()

    # --------------------------------------------------------
    # 2. Apply global cybersecurity + sustainability styling
    # --------------------------------------------------------

    apply_global_styles(
        get_theme()
    )

    # --------------------------------------------------------
    # 3. Render permanent sidebar and determine active page
    # --------------------------------------------------------

    current_page = (
        render_sidebar_navigation()
    )

    # --------------------------------------------------------
    # 4. Render cross-page notifications
    # --------------------------------------------------------

    _render_flash_messages()

    # --------------------------------------------------------
    # 5. Render selected application page
    # --------------------------------------------------------

    _render_current_page(
        current_page
    )

    # --------------------------------------------------------
    # 6. Shared application footer
    # --------------------------------------------------------

    render_footer(
        project_name=PROJECT_NAME,
        version=PROJECT_VERSION,
    )


# ============================================================
# APPLICATION ENTRY POINT
# ============================================================

if __name__ == "__main__":
    main()