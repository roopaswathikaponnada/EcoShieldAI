"""
EcoShield AI
Reusable UI Components

This module contains reusable presentation components used
throughout the EcoShield AI Streamlit frontend.

Responsibilities:
- Render branded headers and logos
- Render cards and feature blocks
- Render risk and readiness badges
- Render metric/stat cards
- Render recommendation cards
- Render empty states and notices
- Render source/evidence pills
- Render the common footer

Business logic must never be placed in this module.
"""

from __future__ import annotations

from html import escape
from textwrap import dedent
from typing import Iterable

import streamlit as st

# ============================================================
# SAFE HTML RENDERING
# ============================================================

def _render_html(
    html: str,
) -> None:
    """
    Render EcoShield custom HTML safely and consistently.

    dedent() removes Python indentation from triple-quoted
    templates so HTML is not interpreted as a Markdown
    code block.

    st.html() is used because these components contain HTML,
    not Markdown.
    """

    cleaned_html = dedent(
        html
    ).strip()

    if not cleaned_html:
        return

    st.html(
        cleaned_html
    )

# ============================================================
# BRAND COMPONENTS
# ============================================================

def render_brand(
    *,
    name: str = "EcoShield AI",
    tagline: str = "Secure Devices. Greener Tomorrow.",
    icon: str = "🛡️🌱",
) -> None:
    """
    Render the EcoShield brand block.

    Intended mainly for:
    - sidebar
    - landing page
    - compact page headers
    """

    safe_name = escape(name)
    safe_tagline = escape(tagline)
    safe_icon = escape(icon)

    _render_html(
        f"""
        <div class="eco-brand">
            <div class="eco-brand-icon">
                {safe_icon}
            </div>

            <div>
                <div class="eco-brand-name">
                    {safe_name}
                </div>

                <div class="eco-brand-tagline">
                    {safe_tagline}
                </div>
            </div>
        </div>
        """,
    )


# ============================================================
# PAGE HEADER
# ============================================================

def render_page_header(
    *,
    title: str,
    subtitle: str | None = None,
    kicker: str | None = None,
    icon: str | None = None,
) -> None:
    """
    Render a consistent EcoShield page header.
    """

    safe_title = escape(title)

    title_text = (
        f"{escape(icon)} {safe_title}"
        if icon
        else safe_title
    )

    kicker_html = ""

    if kicker:
        kicker_html = (
            f'<div class="eco-kicker">'
            f'{escape(kicker)}'
            f'</div>'
        )

    subtitle_html = ""

    if subtitle:
        subtitle_html = (
            f'<div class="eco-page-subtitle">'
            f'{escape(subtitle)}'
            f'</div>'
        )

    _render_html(
        f"""
        <div class="eco-page-header">
            {kicker_html}

            <h1 class="eco-page-title">
                {title_text}
            </h1>

            {subtitle_html}
        </div>
        """
    )


# ============================================================
# HERO COMPONENT
# ============================================================

def render_hero(
    *,
    title: str,
    accent_text: str | None = None,
    subtitle: str | None = None,
) -> None:
    """
    Render the main EcoShield hero section.

    Example:
        title="Secure Your Data."
        accent_text="Sustain Your Planet."
    """

    safe_title = escape(title)

    accent_html = ""

    if accent_text:
        accent_html = (
            '<br>'
            '<span class="eco-hero-title-accent">'
            f'{escape(accent_text)}'
            '</span>'
        )

    subtitle_html = ""

    if subtitle:
        subtitle_html = (
            '<div class="eco-hero-text">'
            f'{escape(subtitle)}'
            '</div>'
        )

    _render_html(
        f"""
        <section class="eco-hero">

            <h1 class="eco-hero-title">
                {safe_title}
                {accent_html}
            </h1>

            {subtitle_html}

        </section>
        """
    )


# ============================================================
# SECTION HEADER
# ============================================================

def render_section_header(
    *,
    title: str,
    description: str | None = None,
    icon: str | None = None,
) -> None:
    """
    Render a consistent section heading.
    """

    title_text = escape(title)

    if icon:
        title_text = (
            f"{escape(icon)} {title_text}"
        )

    description_html = ""

    if description:
        description_html = (
            '<div class="eco-section-description">'
            f'{escape(description)}'
            '</div>'
        )

    _render_html(
        f"""
        <div class="eco-section-title">
            {title_text}
        </div>

        {description_html}
        """
    )


# ============================================================
# GENERAL CARD
# ============================================================

def render_card(
    *,
    title: str,
    description: str | None = None,
    icon: str | None = None,
) -> None:
    """
    Render a generic EcoShield content card.
    """

    icon_html = ""

    if icon:
        icon_html = (
            '<div class="eco-feature-icon">'
            f'{escape(icon)}'
            '</div>'
        )

    description_html = ""

    if description:
        description_html = (
            '<div class="eco-feature-description">'
            f'{escape(description)}'
            '</div>'
        )

    _render_html(
        f"""
        <div class="eco-card">

            {icon_html}

            <div class="eco-feature-title">
                {escape(title)}
            </div>

            {description_html}

        </div>
        """
    )


# ============================================================
# FEATURE CARD
# ============================================================

def render_feature_card(
    *,
    title: str,
    description: str,
    icon: str,
) -> None:
    """
    Render a branded feature card.
    """

    render_card(
        title=title,
        description=description,
        icon=icon,
    )


# ============================================================
# BADGE HELPERS
# ============================================================

def _normalize_css_token(
    value: str,
) -> str:
    """
    Convert a display value into a safe CSS token.
    """

    normalized = (
        value.strip()
        .lower()
        .replace(" ", "-")
        .replace("/", "-")
    )

    allowed = {
        "low",
        "medium",
        "high",
        "ready",
        "conditional",
        "not-ready",
        "ai",
    }

    if normalized not in allowed:
        return "ai"

    return normalized


def render_badge(
    *,
    label: str,
    kind: str,
) -> None:
    """
    Render a generic EcoShield badge.
    """

    css_token = (
        _normalize_css_token(
            kind
        )
    )

    _render_html(
        f"""
        <span
            class="
                eco-badge
                eco-badge-{css_token}
            "
        >
            {escape(label)}
        </span>
        """
    )


# ============================================================
# RISK BADGE
# ============================================================

def render_risk_badge(
    risk_level: str,
) -> None:
    """
    Render Low / Medium / High risk badge.
    """

    normalized = (
        risk_level.strip().lower()
    )

    if normalized == "low":
        label = "LOW RISK"

    elif normalized == "medium":
        label = "MEDIUM RISK"

    elif normalized == "high":
        label = "HIGH RISK"

    else:
        label = risk_level.upper()

    render_badge(
        label=label,
        kind=normalized,
    )


# ============================================================
# READINESS BADGE
# ============================================================

def render_readiness_badge(
    readiness: str,
) -> None:
    """
    Render Ready / Conditional / Not Ready badge.
    """

    render_badge(
        label=readiness.upper(),
        kind=readiness,
    )


# ============================================================
# AI BADGE
# ============================================================

def render_ai_badge(
    label: str = "AI ASSISTED",
) -> None:
    """
    Render the EcoShield AI badge.
    """

    render_badge(
        label=label,
        kind="ai",
    )


# ============================================================
# STAT CARD
# ============================================================

def render_stat_card(
    *,
    label: str,
    value: str | int | float,
) -> None:
    """
    Render a compact custom metric card.
    """

    _render_html(
        f"""
        <div class="eco-stat">

            <div class="eco-stat-label">
                {escape(str(label))}
            </div>

            <div class="eco-stat-value">
                {escape(str(value))}
            </div>

        </div>
        """
    )


# ============================================================
# RISK SCORE CARD
# ============================================================

def render_risk_score(
    *,
    score: int,
    risk_level: str,
) -> None:
    """
    Render the primary 0-100 risk score card.
    """

    # Keep score safely within the supported 0-100 range.
    safe_score = max(
        0,
        min(
            int(score),
            100,
        ),
    )

    # Normalize the risk level for CSS styling.
    normalized_risk = (
        risk_level
        .strip()
        .lower()
    )

    # Map risk levels to the semantic text colors
    # defined by the EcoShield global stylesheet.
    risk_color_class = {
        "low": "eco-text-success",
        "medium": "eco-text-warning",
        "high": "eco-text-danger",
    }.get(
        normalized_risk,
        "eco-text-secondary",
    )

    # Render the final risk score component.
    _render_html(
        f"""
        <div class="eco-risk-score">

            <div>

                <span class="eco-risk-number">
                    {safe_score}
                </span>

                <span class="eco-risk-denominator">
                    /100
                </span>

            </div>

            <div
                class="
                    eco-risk-label
                    {risk_color_class}
                "
            >
                {escape(risk_level.upper())} RISK
            </div>

        </div>
        """
    )
# ============================================================
# RECOMMENDATION CARD
# ============================================================

def render_recommendation_card(
    *,
    title: str,
    action: str,
    rationale: str | None = None,
    priority: str = "Medium",
    category: str | None = None,
) -> None:
    """
    Render a structured recommendation card.
    """

    normalized_priority = (
        priority.strip().lower()
    )

    allowed_priorities = {
        "critical",
        "high",
        "medium",
        "low",
    }

    if (
        normalized_priority
        not in allowed_priorities
    ):
        normalized_priority = "medium"

    category_html = ""

    if category:
        category_html = (
            '<div class="eco-text-secondary" '
            'style="font-size:0.76rem; '
            'margin-bottom:0.35rem;">'
            f'{escape(category)}'
            '</div>'
        )

    rationale_html = ""

    if rationale:
        rationale_html = (
            '<div class="eco-feature-description" '
            'style="margin-top:0.65rem;">'
            f'<strong>Why:</strong> '
            f'{escape(rationale)}'
            '</div>'
        )

    _render_html(
        f"""
        <div
            class="
                eco-recommendation
                eco-recommendation-{normalized_priority}
            "
        >

            {category_html}

            <div class="eco-feature-title">
                {escape(title)}
            </div>

            <div
                class="eco-feature-description"
                style="margin-top:0.45rem;"
            >
                <strong>Action:</strong>
                {escape(action)}
            </div>

            {rationale_html}

        </div>
        """
    )


# ============================================================
# PRIORITY BADGE
# ============================================================

def render_priority_badge(
    priority: str,
) -> None:
    """
    Render Critical / High / Medium / Low priority.
    """

    normalized = (
        priority.strip().lower()
    )

    if normalized == "critical":

        _render_html(
            """
            <span
                class="eco-badge eco-badge-high"
            >
                CRITICAL
            </span>
            """
        )

    elif normalized == "high":

        render_badge(
            label="HIGH",
            kind="high",
        )

    elif normalized == "medium":

        render_badge(
            label="MEDIUM",
            kind="medium",
        )

    else:

        render_badge(
            label="LOW",
            kind="low",
        )


# ============================================================
# STEP INDICATOR
# ============================================================

def render_step_indicator(
    *,
    current_step: int,
    total_steps: int,
    labels: Iterable[str] | None = None,
) -> None:
    """
    Render a compact multi-step assessment indicator.

    Parameters
    ----------
    current_step:
        1-based active step.

    total_steps:
        Total number of assessment steps.

    labels:
        Optional step names.
    """

    if total_steps <= 0:
        return

    current_step = max(
        1,
        min(
            current_step,
            total_steps,
        ),
    )

    label_list = (
        list(labels)
        if labels is not None
        else []
    )

    pills: list[str] = []

    for step in range(
        1,
        total_steps + 1,
    ):

        css_class = (
            "eco-step-pill"
        )

        if step < current_step:

            css_class += (
                " eco-step-complete"
            )

        elif step == current_step:

            css_class += (
                " eco-step-active"
            )

        if (
            step - 1
            < len(label_list)
        ):

            label = (
                f"{step}. "
                f"{escape(label_list[step - 1])}"
            )

        else:

            label = str(step)

        pills.append(
            f"""
            <span class="{css_class}">
                {label}
            </span>
            """
        )

    _render_html(
        f"""
        <div class="eco-step-row">
            {''.join(pills)}
        </div>
        """
    )

    progress = (
        current_step
        / total_steps
    )

    st.progress(
        progress
    )


# ============================================================
# CHECKLIST ITEM
# ============================================================

def render_checklist_item(
    *,
    text: str,
    completed: bool,
) -> None:
    """
    Render a checklist item.
    """

    icon = (
        "✅"
        if completed
        else "⬜"
    )

    _render_html(
        f"""
        <div class="eco-check-item">

            <span>
                {icon}
            </span>

            <span>
                {escape(text)}
            </span>

        </div>
        """
    )


# ============================================================
# SOURCE / EVIDENCE PILLS
# ============================================================

def render_source_pills(
    sources: Iterable[str],
) -> None:
    """
    Render RAG/source references as compact pills.
    """

    source_list = [
        source
        for source in sources
        if str(source).strip()
    ]

    if not source_list:
        return

    unique_sources = (
        dict.fromkeys(
            source_list
        )
    )

    pills = "".join(
        (
            '<span class="eco-source-pill">'
            f'{escape(str(source))}'
            '</span>'
        )
        for source in unique_sources
    )

    _render_html(
        f"""
        <div>
            {pills}
        </div>
        """
    )


# ============================================================
# EMPTY STATE
# ============================================================

def render_empty_state(
    *,
    title: str,
    description: str,
    icon: str = "🛡️",
) -> None:
    """
    Render a consistent empty/protected-page state.
    """

    _render_html(
        f"""
        <div class="eco-empty-state">

            <div
                class="eco-feature-icon"
                style="margin-bottom:0;"
            >
                {escape(icon)}
            </div>

            <div class="eco-empty-title">
                {escape(title)}
            </div>

            <div class="eco-empty-description">
                {escape(description)}
            </div>

        </div>
        """
    )


# ============================================================
# NOTICE COMPONENT
# ============================================================

def render_notice(
    *,
    title: str,
    message: str,
    notice_type: str = "info",
) -> None:
    """
    Render a native Streamlit semantic notice.

    Supported types:
    - success
    - warning
    - error
    - info
    """

    text = (
        f"**{title}**\n\n"
        f"{message}"
    )

    normalized = (
        notice_type
        .strip()
        .lower()
    )

    if normalized == "success":

        st.success(
            text
        )

    elif normalized == "warning":

        st.warning(
            text
        )

    elif normalized == "error":

        st.error(
            text
        )

    else:

        st.info(
            text
        )


# ============================================================
# DIVIDER / SPACING HELPERS
# ============================================================

def render_spacer(
    size: str = "md",
) -> None:
    """
    Render a predefined vertical spacer.

    Supported:
    - sm
    - md
    - lg
    """

    allowed = {
        "sm",
        "md",
        "lg",
    }

    normalized = (
        size.strip().lower()
    )

    if normalized not in allowed:
        normalized = "md"

    _render_html(
        f"""
        <div
            class="eco-spacer-{normalized}"
        ></div>
        """
    )


# ============================================================
# FOOTER
# ============================================================

def render_footer(
    *,
    project_name: str = "EcoShield AI",
    version: str | None = None,
) -> None:
    """
    Render the shared application footer.
    """

    version_text = ""

    if version:
        version_text = (
            f" • v{escape(version)}"
        )

    _render_html(
        f"""
        <div class="eco-footer">

            {escape(project_name)}
            {version_text}

            <br>

            Secure data handling •
            Responsible electronics lifecycle •
            Privacy by design

        </div>
        """
    )