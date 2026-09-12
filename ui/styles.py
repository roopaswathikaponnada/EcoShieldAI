"""
EcoShield AI
Global UI Styling

This module contains the reusable visual design system used
throughout the EcoShield AI Streamlit application.

Responsibilities:
- Apply global EcoShield styling
- Define cybersecurity + sustainability visual identity
- Style Streamlit-native controls consistently
- Provide reusable CSS classes for custom UI components
- Support responsive desktop/tablet/mobile layouts

Business logic must never be placed in this module.
"""

from __future__ import annotations

import streamlit as st


# ============================================================
# ECOSHIELD BRAND COLORS
# ============================================================

COLOR_PRIMARY = "#22C55E"

COLOR_PRIMARY_HOVER = "#16A34A"

COLOR_PRIMARY_SOFT = "rgba(34, 197, 94, 0.12)"

COLOR_PRIMARY_BORDER = "rgba(34, 197, 94, 0.28)"

COLOR_BACKGROUND = "#07131A"

COLOR_SURFACE = "#0D2028"

COLOR_SURFACE_ALT = "#102832"

COLOR_SURFACE_HOVER = "#15313C"

COLOR_BORDER = "#1E3A43"

COLOR_BORDER_SOFT = "rgba(148, 163, 184, 0.14)"

COLOR_TEXT = "#F1F5F9"

COLOR_TEXT_SECONDARY = "#94A3B8"

COLOR_TEXT_MUTED = "#64748B"

COLOR_SUCCESS = "#22C55E"

COLOR_WARNING = "#F59E0B"

COLOR_DANGER = "#EF4444"

COLOR_INFO = "#38BDF8"

COLOR_AI = "#14B8A6"


# ============================================================
# LAYOUT CONSTANTS
# ============================================================

CONTENT_MAX_WIDTH = "1380px"

CARD_RADIUS = "16px"

SMALL_RADIUS = "10px"

SECTION_GAP = "1.25rem"


# ============================================================
# GLOBAL CSS
# ============================================================

GLOBAL_CSS = f"""
<style>

/* ==========================================================
   ECOSHIELD DESIGN TOKENS
   ========================================================== */

:root {{
    --eco-primary: {COLOR_PRIMARY};
    --eco-primary-hover: {COLOR_PRIMARY_HOVER};
    --eco-primary-soft: {COLOR_PRIMARY_SOFT};
    --eco-primary-border: {COLOR_PRIMARY_BORDER};

    --eco-background: {COLOR_BACKGROUND};
    --eco-surface: {COLOR_SURFACE};
    --eco-surface-alt: {COLOR_SURFACE_ALT};
    --eco-surface-hover: {COLOR_SURFACE_HOVER};

    --eco-border: {COLOR_BORDER};
    --eco-border-soft: {COLOR_BORDER_SOFT};

    --eco-text: {COLOR_TEXT};
    --eco-text-secondary: {COLOR_TEXT_SECONDARY};
    --eco-text-muted: {COLOR_TEXT_MUTED};

    --eco-success: {COLOR_SUCCESS};
    --eco-warning: {COLOR_WARNING};
    --eco-danger: {COLOR_DANGER};
    --eco-info: {COLOR_INFO};
    --eco-ai: {COLOR_AI};

    --eco-card-radius: {CARD_RADIUS};
    --eco-small-radius: {SMALL_RADIUS};

    --eco-shadow:
        0 10px 30px rgba(0, 0, 0, 0.18);
}}


/* ==========================================================
   PAGE FOUNDATION
   ========================================================== */

html {{
    scroll-behavior: smooth;
}}

body {{
    -webkit-font-smoothing: antialiased;
    -moz-osx-font-smoothing: grayscale;
}}

[data-testid="stAppViewContainer"] {{
    background:
        radial-gradient(
            circle at 85% 5%,
            rgba(34, 197, 94, 0.06),
            transparent 24rem
        ),
        radial-gradient(
            circle at 5% 90%,
            rgba(20, 184, 166, 0.035),
            transparent 26rem
        ),
        var(--eco-background);
}}

[data-testid="stMain"] {{
    background: transparent;
}}

.block-container {{
    max-width: {CONTENT_MAX_WIDTH};
    padding-top: 2rem;
    padding-bottom: 3.5rem;
    padding-left: 2rem;
    padding-right: 2rem;
}}


/* ==========================================================
   TYPOGRAPHY
   ========================================================== */

h1,
h2,
h3,
h4,
h5,
h6 {{
    letter-spacing: -0.025em;
}}

h1 {{
    font-weight: 750;
    line-height: 1.08;
}}

h2 {{
    font-weight: 700;
}}

h3 {{
    font-weight: 650;
}}

p {{
    line-height: 1.65;
}}

a {{
    text-decoration: none;
}}

a:hover {{
    text-decoration: none;
}}


/* ==========================================================
   SIDEBAR
   ========================================================== */

[data-testid="stSidebar"] {{
    background:
        linear-gradient(
            180deg,
            #08171E 0%,
            #0A1C24 100%
        );

    border-right:
        1px solid var(--eco-border-soft);
}}

[data-testid="stSidebar"] > div:first-child {{
    padding-top: 1.25rem;
}}

[data-testid="stSidebar"] hr {{
    border-color: var(--eco-border-soft);
}}

[data-testid="stSidebar"] button {{
    transition:
        background-color 0.18s ease,
        border-color 0.18s ease,
        transform 0.18s ease;
}}


/* ==========================================================
   PRIMARY BUTTONS
   ========================================================== */

.stButton > button,
.stFormSubmitButton > button {{
    border-radius: 10px;

    font-weight: 650;

    transition:
        transform 0.16s ease,
        box-shadow 0.16s ease,
        background-color 0.16s ease,
        border-color 0.16s ease;
}}

.stButton > button[kind="primary"],
.stFormSubmitButton > button[kind="primary"] {{
    background:
        linear-gradient(
            135deg,
            var(--eco-primary),
            #16A34A
        );

    border:
        1px solid rgba(74, 222, 128, 0.45);

    color: #04130A;

    box-shadow:
        0 6px 18px rgba(34, 197, 94, 0.18);
}}

.stButton > button:hover,
.stFormSubmitButton > button:hover {{
    transform: translateY(-1px);
}}

.stButton > button[kind="primary"]:hover,
.stFormSubmitButton > button[kind="primary"]:hover {{
    box-shadow:
        0 8px 24px rgba(34, 197, 94, 0.24);
}}


/* ==========================================================
   FORM CONTROLS
   ========================================================== */

[data-testid="stSelectbox"],
[data-testid="stNumberInput"],
[data-testid="stTextInput"],
[data-testid="stTextArea"] {{
    margin-bottom: 0.15rem;
}}

[data-baseweb="select"] > div,
[data-testid="stNumberInput"] input,
[data-testid="stTextInput"] input,
[data-testid="stTextArea"] textarea {{
    border-radius: var(--eco-small-radius);
}}

[data-testid="stForm"] {{
    background:
        linear-gradient(
            180deg,
            rgba(13, 32, 40, 0.76),
            rgba(10, 27, 34, 0.72)
        );

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        var(--eco-card-radius);

    padding:
        1.35rem 1.35rem 1.5rem 1.35rem;

    box-shadow:
        0 14px 38px rgba(0, 0, 0, 0.12);
}}


/* ==========================================================
   METRIC CARDS
   ========================================================== */

[data-testid="stMetric"] {{
    background:
        linear-gradient(
            145deg,
            rgba(16, 40, 50, 0.92),
            rgba(11, 29, 36, 0.92)
        );

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        var(--eco-card-radius);

    padding:
        1rem 1.1rem;

    box-shadow:
        0 8px 24px rgba(0, 0, 0, 0.12);

    min-height:
        112px;
}}

[data-testid="stMetricLabel"] {{
    color:
        var(--eco-text-secondary);
}}

[data-testid="stMetricValue"] {{
    font-weight:
        750;
}}


/* ==========================================================
   PROGRESS BARS
   ========================================================== */

[data-testid="stProgress"] > div > div {{
    border-radius:
        999px;
}}

[data-testid="stProgress"] div[role="progressbar"] {{
    border-radius:
        999px;

    background:
        linear-gradient(
            90deg,
            #22C55E,
            #84CC16
        );
}}


/* ==========================================================
   TABS
   ========================================================== */

[data-baseweb="tab-list"] {{
    gap:
        0.5rem;

    border-bottom:
        1px solid var(--eco-border-soft);
}}

[data-baseweb="tab"] {{
    border-radius:
        10px 10px 0 0;

    padding-left:
        1rem;

    padding-right:
        1rem;

    font-weight:
        600;
}}

[data-baseweb="tab"][aria-selected="true"] {{
    color:
        var(--eco-primary);

    background:
        var(--eco-primary-soft);
}}


/* ==========================================================
   EXPANDERS
   ========================================================== */

[data-testid="stExpander"] {{
    border:
        1px solid var(--eco-border-soft);

    border-radius:
        12px;

    background:
        rgba(13, 32, 40, 0.58);

    overflow:
        hidden;
}}

[data-testid="stExpander"]:hover {{
    border-color:
        var(--eco-primary-border);
}}


/* ==========================================================
   ALERTS
   ========================================================== */

[data-testid="stAlert"] {{
    border-radius:
        12px;

    border-width:
        1px;

    box-shadow:
        none;
}}


/* ==========================================================
   DIVIDERS
   ========================================================== */

hr {{
    border:
        none;

    border-top:
        1px solid var(--eco-border-soft);

    margin:
        1.75rem 0;
}}


/* ==========================================================
   CUSTOM ECOSHIELD COMPONENTS
   ========================================================== */


/* ----------------------------------------------------------
   Brand / Logo
   ---------------------------------------------------------- */

.eco-brand {{
    display:
        flex;

    align-items:
        center;

    gap:
        0.7rem;

    margin-bottom:
        1.2rem;
}}

.eco-brand-icon {{
    display:
        flex;

    align-items:
        center;

    justify-content:
        center;

    width:
        44px;

    height:
        44px;

    border-radius:
        11px;

    background:
        var(--eco-primary-soft);

    border:
        1px solid var(--eco-primary-border);

    color:
        var(--eco-primary);

    font-size:
        1.3rem;
}}

.eco-brand-name {{
    font-size:
        1.05rem;

    font-weight:
        750;

    letter-spacing:
        -0.02em;

    color:
        var(--eco-text);
}}

.eco-brand-tagline {{
    font-size:
        0.72rem;

    color:
        var(--eco-text-secondary);
}}


/* ----------------------------------------------------------
   Page header
   ---------------------------------------------------------- */

.eco-page-header {{
    margin-bottom:
        1.6rem;
}}

.eco-kicker {{
    display:
        inline-flex;

    align-items:
        center;

    gap:
        0.4rem;

    margin-bottom:
        0.55rem;

    padding:
        0.28rem 0.62rem;

    border-radius:
        999px;

    background:
        var(--eco-primary-soft);

    border:
        1px solid var(--eco-primary-border);

    color:
        var(--eco-primary);

    font-size:
        0.74rem;

    font-weight:
        700;

    letter-spacing:
        0.055em;

    text-transform:
        uppercase;
}}

.eco-page-title {{
    margin:
        0;

    color:
        var(--eco-text);

    font-size:
        clamp(
            1.8rem,
            4vw,
            2.6rem
        );

    font-weight:
        780;

    line-height:
        1.12;
}}

.eco-page-subtitle {{
    max-width:
        760px;

    margin-top:
        0.6rem;

    color:
        var(--eco-text-secondary);

    font-size:
        0.98rem;

    line-height:
        1.65;
}}


/* ----------------------------------------------------------
   Hero
   ---------------------------------------------------------- */

.eco-hero {{
    position:
        relative;

    overflow:
        hidden;

    padding:
        clamp(
            2rem,
            6vw,
            4rem
        );

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        22px;

    background:
        linear-gradient(
            135deg,
            rgba(8, 30, 38, 0.98),
            rgba(8, 23, 30, 0.96)
        );

    box-shadow:
        var(--eco-shadow);
}}

.eco-hero::before {{
    content:
        "";

    position:
        absolute;

    width:
        420px;

    height:
        420px;

    top:
        -210px;

    right:
        -130px;

    border-radius:
        999px;

    background:
        radial-gradient(
            circle,
            rgba(34, 197, 94, 0.18),
            transparent 66%
        );

    pointer-events:
        none;
}}

.eco-hero-title {{
    position:
        relative;

    max-width:
        720px;

    margin:
        0;

    font-size:
        clamp(
            2.1rem,
            5vw,
            4rem
        );

    line-height:
        1.04;

    letter-spacing:
        -0.045em;

    font-weight:
        820;
}}

.eco-hero-title-accent {{
    color:
        var(--eco-primary);
}}

.eco-hero-text {{
    position:
        relative;

    max-width:
        650px;

    margin-top:
        1.15rem;

    color:
        var(--eco-text-secondary);

    font-size:
        1.02rem;

    line-height:
        1.72;
}}


/* ----------------------------------------------------------
   General card
   ---------------------------------------------------------- */

.eco-card {{
    height:
        100%;

    padding:
        1.15rem;

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        var(--eco-card-radius);

    background:
        linear-gradient(
            145deg,
            rgba(16, 40, 50, 0.9),
            rgba(10, 28, 35, 0.9)
        );

    box-shadow:
        0 8px 22px rgba(0, 0, 0, 0.1);

    transition:
        transform 0.18s ease,
        border-color 0.18s ease,
        background-color 0.18s ease;
}}

.eco-card:hover {{
    transform:
        translateY(-2px);

    border-color:
        var(--eco-primary-border);
}}


/* ----------------------------------------------------------
   Feature card
   ---------------------------------------------------------- */

.eco-feature-icon {{
    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    width:
        40px;

    height:
        40px;

    margin-bottom:
        0.85rem;

    border-radius:
        11px;

    color:
        var(--eco-primary);

    background:
        var(--eco-primary-soft);

    border:
        1px solid var(--eco-primary-border);
}}

.eco-feature-title {{
    color:
        var(--eco-text);

    font-size:
        1rem;

    font-weight:
        700;
}}

.eco-feature-description {{
    margin-top:
        0.4rem;

    color:
        var(--eco-text-secondary);

    font-size:
        0.88rem;

    line-height:
        1.55;
}}


/* ----------------------------------------------------------
   Section header
   ---------------------------------------------------------- */

.eco-section-title {{
    display:
        flex;

    align-items:
        center;

    gap:
        0.55rem;

    margin:
        0 0 0.9rem 0;

    font-size:
        1.22rem;

    font-weight:
        730;

    color:
        var(--eco-text);
}}

.eco-section-description {{
    margin-top:
        -0.45rem;

    margin-bottom:
        1rem;

    color:
        var(--eco-text-secondary);

    font-size:
        0.9rem;
}}


/* ----------------------------------------------------------
   Status badges
   ---------------------------------------------------------- */

.eco-badge {{
    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    padding:
        0.34rem 0.7rem;

    border-radius:
        999px;

    font-size:
        0.76rem;

    font-weight:
        750;

    letter-spacing:
        0.025em;
}}

.eco-badge-low,
.eco-badge-ready {{
    color:
        #86EFAC;

    background:
        rgba(34, 197, 94, 0.12);

    border:
        1px solid rgba(34, 197, 94, 0.3);
}}

.eco-badge-medium,
.eco-badge-conditional {{
    color:
        #FCD34D;

    background:
        rgba(245, 158, 11, 0.12);

    border:
        1px solid rgba(245, 158, 11, 0.3);
}}

.eco-badge-high,
.eco-badge-not-ready {{
    color:
        #FCA5A5;

    background:
        rgba(239, 68, 68, 0.12);

    border:
        1px solid rgba(239, 68, 68, 0.3);
}}

.eco-badge-ai {{
    color:
        #5EEAD4;

    background:
        rgba(20, 184, 166, 0.12);

    border:
        1px solid rgba(20, 184, 166, 0.28);
}}


/* ----------------------------------------------------------
   Risk Score
   ---------------------------------------------------------- */

.eco-risk-score {{
    display:
        flex;

    flex-direction:
        column;

    align-items:
        center;

    justify-content:
        center;

    min-height:
        220px;

    padding:
        1.4rem;

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        var(--eco-card-radius);

    background:
        linear-gradient(
            145deg,
            rgba(16, 40, 50, 0.96),
            rgba(9, 26, 33, 0.96)
        );
}}

.eco-risk-number {{
    font-size:
        clamp(
            2.8rem,
            7vw,
            4.5rem
        );

    font-weight:
        820;

    line-height:
        1;

    letter-spacing:
        -0.055em;
}}

.eco-risk-denominator {{
    margin-left:
        0.2rem;

    color:
        var(--eco-text-secondary);

    font-size:
        1rem;

    font-weight:
        500;
}}

.eco-risk-label {{
    margin-top:
        0.7rem;

    font-size:
        1rem;

    font-weight:
        760;

    letter-spacing:
        0.025em;
}}


/* ----------------------------------------------------------
   Metric / Stat card
   ---------------------------------------------------------- */

.eco-stat {{
    height:
        100%;

    padding:
        1rem;

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        14px;

    background:
        rgba(13, 32, 40, 0.72);
}}

.eco-stat-label {{
    color:
        var(--eco-text-secondary);

    font-size:
        0.78rem;

    font-weight:
        600;
}}

.eco-stat-value {{
    margin-top:
        0.35rem;

    color:
        var(--eco-text);

    font-size:
        1.38rem;

    font-weight:
        760;
}}


/* ----------------------------------------------------------
   Recommendation cards
   ---------------------------------------------------------- */

.eco-recommendation {{
    padding:
        1rem 1.05rem;

    margin-bottom:
        0.8rem;

    border:
        1px solid var(--eco-border-soft);

    border-radius:
        14px;

    background:
        rgba(13, 32, 40, 0.66);
}}

.eco-recommendation-critical {{
    border-left:
        4px solid var(--eco-danger);
}}

.eco-recommendation-high {{
    border-left:
        4px solid #FB923C;
}}

.eco-recommendation-medium {{
    border-left:
        4px solid var(--eco-warning);
}}

.eco-recommendation-low {{
    border-left:
        4px solid var(--eco-success);
}}


/* ----------------------------------------------------------
   Step indicator
   ---------------------------------------------------------- */

.eco-step-row {{
    display:
        flex;

    align-items:
        center;

    justify-content:
        space-between;

    gap:
        0.4rem;

    margin:
        0.75rem 0 1rem 0;
}}

.eco-step-pill {{
    display:
        inline-flex;

    align-items:
        center;

    justify-content:
        center;

    min-width:
        32px;

    height:
        32px;

    padding:
        0 0.6rem;

    border-radius:
        999px;

    border:
        1px solid var(--eco-border-soft);

    background:
        rgba(13, 32, 40, 0.7);

    color:
        var(--eco-text-secondary);

    font-size:
        0.78rem;

    font-weight:
        700;
}}

.eco-step-active {{
    color:
        #04130A;

    background:
        var(--eco-primary);

    border-color:
        var(--eco-primary);
}}

.eco-step-complete {{
    color:
        var(--eco-primary);

    border-color:
        var(--eco-primary-border);

    background:
        var(--eco-primary-soft);
}}


/* ----------------------------------------------------------
   Checklist
   ---------------------------------------------------------- */

.eco-check-item {{
    display:
        flex;

    align-items:
        flex-start;

    gap:
        0.65rem;

    padding:
        0.6rem 0;

    border-bottom:
        1px solid var(--eco-border-soft);
}}

.eco-check-item:last-child {{
    border-bottom:
        none;
}}


/* ----------------------------------------------------------
   Source / evidence pill
   ---------------------------------------------------------- */

.eco-source-pill {{
    display:
        inline-flex;

    align-items:
        center;

    margin:
        0.18rem;

    padding:
        0.3rem 0.6rem;

    border-radius:
        999px;

    color:
        #99F6E4;

    background:
        rgba(20, 184, 166, 0.1);

    border:
        1px solid rgba(20, 184, 166, 0.24);

    font-size:
        0.72rem;
}}


/* ----------------------------------------------------------
   Empty state
   ---------------------------------------------------------- */

.eco-empty-state {{
    display:
        flex;

    flex-direction:
        column;

    align-items:
        center;

    justify-content:
        center;

    min-height:
        250px;

    padding:
        2rem;

    text-align:
        center;

    border:
        1px dashed var(--eco-border);

    border-radius:
        var(--eco-card-radius);

    background:
        rgba(13, 32, 40, 0.35);
}}

.eco-empty-title {{
    margin-top:
        0.75rem;

    color:
        var(--eco-text);

    font-size:
        1.08rem;

    font-weight:
        720;
}}

.eco-empty-description {{
    max-width:
        500px;

    margin-top:
        0.35rem;

    color:
        var(--eco-text-secondary);

    font-size:
        0.88rem;
}}


/* ----------------------------------------------------------
   Footer
   ---------------------------------------------------------- */

.eco-footer {{
    margin-top:
        2rem;

    padding-top:
        1.2rem;

    border-top:
        1px solid var(--eco-border-soft);

    color:
        var(--eco-text-muted);

    font-size:
        0.78rem;

    text-align:
        center;
}}


/* ----------------------------------------------------------
   Utility classes
   ---------------------------------------------------------- */

.eco-text-primary {{
    color:
        var(--eco-primary);
}}

.eco-text-secondary {{
    color:
        var(--eco-text-secondary);
}}

.eco-text-danger {{
    color:
        var(--eco-danger);
}}

.eco-text-warning {{
    color:
        var(--eco-warning);
}}

.eco-text-success {{
    color:
        var(--eco-success);
}}

.eco-muted {{
    color:
        var(--eco-text-muted);
}}

.eco-no-margin {{
    margin:
        0;
}}

.eco-spacer-sm {{
    height:
        0.5rem;
}}

.eco-spacer-md {{
    height:
        1rem;
}}

.eco-spacer-lg {{
    height:
        1.75rem;
}}


/* ==========================================================
   RESPONSIVE DESIGN
   ========================================================== */

@media (
    max-width: 1100px
) {{

    .block-container {{
        padding-left:
            1.25rem;

        padding-right:
            1.25rem;
    }}

    .eco-hero {{
        padding:
            2rem;
    }}

}}


@media (
    max-width: 768px
) {{

    .block-container {{
        padding-top:
            1.25rem;

        padding-left:
            1rem;

        padding-right:
            1rem;

        padding-bottom:
            2.5rem;
    }}

    .eco-hero {{
        padding:
            1.5rem;

        border-radius:
            16px;
    }}

    .eco-hero-title {{
        font-size:
            2.25rem;
    }}

    .eco-page-title {{
        font-size:
            1.8rem;
    }}

    .eco-step-row {{
        flex-wrap:
            wrap;

        justify-content:
            flex-start;
    }}

    [data-testid="stMetric"] {{
        min-height:
            auto;
    }}

}}


@media (
    max-width: 480px
) {{

    .block-container {{
        padding-left:
            0.75rem;

        padding-right:
            0.75rem;
    }}

    .eco-hero {{
        padding:
            1.2rem;
    }}

    .eco-hero-title {{
        font-size:
            1.9rem;
    }}

    .eco-card {{
        padding:
            0.95rem;
    }}

}}


/* ==========================================================
   PRINT / REPORT FRIENDLINESS
   ========================================================== */

@media print {{

    [data-testid="stSidebar"] {{
        display:
            none;
    }}

    .block-container {{
        max-width:
            100%;

        padding:
            0;
    }}

    .eco-card,
    [data-testid="stMetric"] {{
        box-shadow:
            none;
    }}

}}

</style>
"""


# ============================================================
# PUBLIC STYLE APPLICATION
# ============================================================


def apply_global_styles(
    theme: str,
) -> None:
    """
    Apply the EcoShield global stylesheet and V2 visual layer.

    The V2 layer is fully theme-aware. It never forces the light
    palette after the user selects Dark mode.
    """

    normalized = (
        str(theme)
        .strip()
        .lower()
    )

    is_light = (
        normalized == "light"
    )

    if is_light:
        palette = {
            "background": "#F4F9F6",
            "surface": "#FFFFFF",
            "surface_alt": "#EEF8F2",
            "surface_hover": "#E6F4EB",
            "sidebar_top": "#FBFEFC",
            "sidebar_bottom": "#EEF8F2",
            "text": "#0B1F16",
"text_secondary": "#344B3D",
"text_muted": "#566C5F",
            "border": "#D6E6DB",
            "border_soft": "rgba(18, 74, 45, 0.10)",
            "shadow": "0 14px 38px rgba(17, 61, 36, 0.08)",
            "hero_start": "#063F35",
            "hero_mid": "#075D47",
            "hero_end": "#0B6B4E",
            "hero_text": "#FFFFFF",
            "hero_sub": "#D7F3E5",
            "input": "#FFFFFF",
            "topbar": "rgba(255,255,255,0.88)",
        }
    else:
        palette = {
            "background": "#061116",
            "surface": "#0C1B21",
            "surface_alt": "#10262C",
            "surface_hover": "#153138",
            "sidebar_top": "#08171C",
            "sidebar_bottom": "#0A2024",
            "text": "#F4F8F6",
            "text_secondary": "#B4C6BD",
            "text_muted": "#7F9A8E",
            "border": "#1D3B3D",
            "border_soft": "rgba(148, 184, 168, 0.12)",
            "shadow": "0 16px 44px rgba(0, 0, 0, 0.30)",
            "hero_start": "#032E2A",
            "hero_mid": "#06473A",
            "hero_end": "#07543F",
            "hero_text": "#FFFFFF",
            "hero_sub": "#CDEBDD",
            "input": "#0F2329",
            "topbar": "rgba(8,23,28,0.88)",
        }

    theme_css = f"""
    <style>
    :root {{
        --eco-primary: #17B978;
        --eco-primary-hover: #0E9F66;
        --eco-primary-soft: rgba(23, 185, 120, 0.12);
        --eco-primary-border: rgba(23, 185, 120, 0.26);
        --eco-ai: #16A6A0;
        --eco-success: #16A36A;
        --eco-warning: #E2A20A;
        --eco-danger: #E34B4B;
        --eco-info: #2C9CCE;

        --eco-background: {palette["background"]};
        --eco-surface: {palette["surface"]};
        --eco-surface-alt: {palette["surface_alt"]};
        --eco-surface-hover: {palette["surface_hover"]};
        --eco-border: {palette["border"]};
        --eco-border-soft: {palette["border_soft"]};
        --eco-text: {palette["text"]};
        --eco-text-secondary: {palette["text_secondary"]};
        --eco-text-muted: {palette["text_muted"]};
        --eco-shadow: {palette["shadow"]};
    }}

    html, body, [class*="css"] {{
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
            BlinkMacSystemFont, "Segoe UI", sans-serif;
    }}

    /* ==========================================================
       GLOBAL TYPOGRAPHY SYSTEM
       ========================================================== */

    html,
    body,
    [data-testid="stAppViewContainer"],
    [data-testid="stSidebar"],
    button,
    input,
    textarea,
    select,
    label,
    p,
    small {{
        font-family: Inter, ui-sans-serif, system-ui, -apple-system,
            BlinkMacSystemFont, "Segoe UI", sans-serif !important;
    }}

    /* Keep Streamlit / Material icons as icons, not text labels such as
       "keyboard_double_arrow_left". */
    .material-icons,
    .material-icons-outlined,
    .material-icons-round,
    .material-icons-sharp,
    .material-symbols-outlined,
    .material-symbols-rounded,
    .material-symbols-sharp,
    [class*="material-symbols"],
    [class*="material-icons"] {{
        font-family: "Material Symbols Rounded",
                     "Material Symbols Outlined",
                     "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        white-space: nowrap !important;
        word-wrap: normal !important;
        direction: ltr !important;
        -webkit-font-feature-settings: "liga" !important;
        -webkit-font-smoothing: antialiased !important;
        font-feature-settings: "liga" !important;
    }}

    /* Streamlit sidebar collapse / expand control */
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] i,
    [data-testid="stSidebarCollapsedControl"] span,
    [data-testid="stSidebarCollapsedControl"] i {{
        font-family: "Material Symbols Rounded",
                     "Material Symbols Outlined",
                     "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-feature-settings: "liga" !important;
        -webkit-font-feature-settings: "liga" !important;
    }}

    /* Main page headings */
    h1,
    .eco-page-title,
    .eco-v2-hero h1 {{
        font-weight: 800 !important;
        letter-spacing: -.035em;
    }}

    h2,
    .eco-section-title,
    .eco-v2-section-title h2 {{
        font-weight: 750 !important;
        letter-spacing: -.025em;
    }}

    h3,
    h4,
    .eco-card-title,
    .eco-feature-title,
    .eco-empty-title {{
        font-weight: 700 !important;
        letter-spacing: -.015em;
    }}

    h5,
    h6 {{
        font-weight: 700 !important;
    }}

    /* Normal body/context text */
    p,
    .eco-page-subtitle,
    .eco-section-description,
    .eco-card-description,
    .eco-feature-description,
    .eco-v2-section-title p,
    .eco-v2-mini span {{
        font-weight: 500 !important;
        line-height: 1.55;
    }}

    /* Form labels and field context */
    label,
    [data-testid="stWidgetLabel"] p,
    [data-testid="stWidgetLabel"] span {{
        font-weight: 600 !important;
        color: {palette["text"]} !important;
    }}

    /* Inputs/selects */
    input,
    textarea,
    div[data-baseweb="select"] span {{
        font-weight: 500 !important;
    }}

    /* Input and textarea placeholder contrast.
       Dark mode gets a brighter muted tone; Light mode keeps
       the existing theme-aware muted text colour. */
    input::placeholder,
    textarea::placeholder {{
        color: {"#9FB5AA" if not is_light else palette["text_muted"]} !important;
        opacity: 1 !important;
    }}

    /* Assessment help / tooltip icons
       Keep Light mode subtle, but make the icons clearly visible in Dark mode. */
    [data-testid="stWidgetLabel"] [data-testid="stTooltipIcon"],
    [data-testid="stWidgetLabel"] button[aria-label*="Help"],
    [data-testid="stWidgetLabel"] button[aria-label*="help"] {{
        color: {"#F4F8F6" if not is_light else palette["text_muted"]} !important;
        opacity: 1 !important;
    }}

    [data-testid="stWidgetLabel"] [data-testid="stTooltipIcon"] svg,
    [data-testid="stWidgetLabel"] button[aria-label*="Help"] svg,
    [data-testid="stWidgetLabel"] button[aria-label*="help"] svg {{
        color: {"#F4F8F6" if not is_light else palette["text_muted"]} !important;
        fill: currentColor !important;
        opacity: 1 !important;
    }}

    /* Buttons across the complete app */
    .stButton > button,
    .stFormSubmitButton > button,
    [data-testid="stSidebar"] .stButton > button {{
        font-weight: 700 !important;
        letter-spacing: -.01em;
    }}

    .stButton > button p,
    .stFormSubmitButton > button p,
    [data-testid="stSidebar"] .stButton > button p,
    .stButton > button span,
    .stFormSubmitButton > button span,
    [data-testid="stSidebar"] .stButton > button span {{
        font-weight: 700 !important;
    }}

    /* Tabs, expanders and navigation-like controls */
    [data-baseweb="tab"],
    [data-testid="stExpander"] summary,
    [data-testid="stExpander"] summary p {{
        font-weight: 650 !important;
    }}

    /* Metrics and statistical values */
    [data-testid="stMetricValue"],
    .eco-stat-value,
    .eco-risk-number,
    .eco-risk-label {{
        font-weight: 750 !important;
    }}

    [data-testid="stMetricLabel"],
    .eco-stat-label {{
        font-weight: 600 !important;
    }}

    /* Badges, kickers and eyebrow text */
    .eco-kicker,
    .eco-badge,
    .eco-v2-eyebrow,
    .eco-v2-section-title .k {{
        font-weight: 750 !important;
        letter-spacing: .055em;
    }}

    /* Sidebar hierarchy */
    .eco-brand-name {{
        font-weight: 800 !important;
    }}

    .eco-brand-tagline,
    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small,
    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        font-weight: 600 !important;
    }}

    /* Small helper text / captions */
    .stCaption,
    small,
    .eco-muted,
    .eco-footer {{
        font-weight: 500 !important;
    }}

    /* Strong and bold tags rendered from markdown/HTML */
    strong,
    b {{
        font-weight: 700 !important;
    }}

    [data-testid="stAppViewContainer"] {{
        background:
            radial-gradient(circle at 78% 0%, rgba(23,185,120,0.07), transparent 28rem),
            radial-gradient(circle at 8% 88%, rgba(22,166,160,0.05), transparent 24rem),
            {palette["background"]} !important;
        color: {palette["text"]};
    }}

    /* Keep Streamlit's header alive so the sidebar can be reopened,
       but make the bar visually transparent. */
    [data-testid="stHeader"],
    header[data-testid="stHeader"] {{
        background: transparent !important;
        border: none !important;
        box-shadow: none !important;
        backdrop-filter: none !important;
    }}

    [data-testid="stDecoration"] {{
        display: none !important;
    }}

    /* Always keep sidebar hide/show controls visible and clickable. */
    [data-testid="stSidebarCollapseButton"],
    [data-testid="stSidebarCollapsedControl"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 99999 !important;
    }}

    [data-testid="stSidebarCollapsedControl"] {{
        position: fixed !important;
        top: .75rem !important;
        left: .75rem !important;
    }}

    [data-testid="stSidebarCollapseButton"] button,
    [data-testid="stSidebarCollapsedControl"] button {{
        background: {palette["surface"]} !important;
        color: {palette["text"]} !important;
        border: 1px solid {palette["border"]} !important;
        border-radius: 10px !important;
        box-shadow: 0 5px 16px rgba(0,0,0,.10) !important;
    }}

    /* Wider, clearer sidebar */
    [data-testid="stSidebar"] {{
        width: 268px !important;
        min-width: 268px !important;
        max-width: 268px !important;
        background: linear-gradient(
            180deg,
            {palette["sidebar_top"]} 0%,
            {palette["sidebar_bottom"]} 100%
        ) !important;
        border-right: 1px solid {palette["border_soft"]};
    }}

    [data-testid="stSidebar"] > div:first-child {{
        width: 268px !important;
        padding-top: .85rem;
        padding-left: .9rem;
        padding-right: .9rem;
    }}

    [data-testid="stSidebar"] .stButton > button {{
        width: 100% !important;
        min-height: 2.9rem;
        padding: .55rem .8rem !important;
        border-radius: 11px !important;
        border: 1px solid transparent !important;
        font-size: .88rem !important;
        font-weight: 700 !important;
        letter-spacing: -.01em;
        line-height: 1.25 !important;
        transition: all .18s ease;
    }}

    [data-testid="stSidebar"] .stButton > button p,
    [data-testid="stSidebar"] .stButton > button span {{
        font-size: .88rem !important;
        font-weight: 700 !important;
        line-height: 1.25 !important;
    }}

    [data-testid="stSidebar"] .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #16B978, #119968) !important;
        color: white !important;
        box-shadow: 0 8px 18px rgba(22,185,120,.18);
    }}

    [data-testid="stSidebar"] [data-testid="stMarkdownContainer"] p {{
        color: {palette["text_secondary"]} !important;
    }}

    [data-testid="stSidebar"] hr {{
        margin: 1rem 0 !important;
        border-color: {palette["border"]} !important;
        opacity: .9;
    }}

    [data-testid="stSidebar"] .stButton > button[kind="secondary"] {{
        background: {palette["surface"]} !important;
        color: {palette["text"]} !important;
        border-color: {palette["border"]} !important;
        font-weight: 700 !important;
        box-shadow: 0 3px 10px rgba(17, 61, 36, 0.035);
    }}

    [data-testid="stSidebar"] .stButton > button[kind="secondary"]:hover {{
        background: {palette["surface_hover"]} !important;
        border-color: {palette["border"]} !important;
    }}

    [data-testid="stSidebar"] .stCaption,
    [data-testid="stSidebar"] small {{
        color: {palette["text_secondary"]} !important;
        font-size: .75rem !important;
        font-weight: 650 !important;
        line-height: 1.45 !important;
    }}

    /* Safe screen-fit layout:
       centered by width, normal vertical document flow. */
    .block-container,
    [data-testid="stMainBlockContainer"] {{
        width: min(92%, 1480px) !important;
        max-width: 1480px !important;
        margin-left: auto !important;
        margin-right: auto !important;
        padding-top: clamp(2.25rem, 5vh, 4rem) !important;
        padding-bottom: clamp(2rem, 5vh, 4rem) !important;
        padding-left: clamp(1rem, 1.8vw, 1.75rem) !important;
        padding-right: clamp(1rem, 1.8vw, 1.75rem) !important;
        box-sizing: border-box !important;
    }}

    [data-testid="stMain"] {{
        width: 100% !important;
        max-width: none !important;
    }}

    h1, h2, h3, h4, h5, h6,
    .stMarkdown, .stCaption, label,
    [data-testid="stMarkdownContainer"] {{
        color: {palette["text"]};
    }}

    p, small, .stCaption {{
    color: {palette["text_secondary"]};
    font-weight: 500;
}}

    .eco-brand {{
        padding: .4rem 0 .8rem 0;
    }}

    .eco-brand-icon {{
        background: linear-gradient(145deg, #17B978, #0B7D5C) !important;
        border: 0 !important;
        box-shadow: 0 8px 24px rgba(23,185,120,.18);
    }}

    .eco-brand-name {{
        color: {palette["text"]} !important;
        font-size: 1.22rem !important;
        font-weight: 850 !important;
        letter-spacing: -.025em;
        line-height: 1.15;
    }}

    .eco-brand-tagline {{
    color: {"#FFFFFF" if not is_light else palette["text_secondary"]} !important;
    font-size: .82rem !important;
    font-weight: 650 !important;
    line-height: 1.45;
    margin-top: .18rem;
}}

    .eco-v2-hero {{
        position: relative;
        overflow: hidden;
        border-radius: 22px;
        padding: clamp(1.6rem, 2.7vw, 2.8rem);
        min-height: 250px;
        background:
            radial-gradient(circle at 88% 18%, rgba(75,255,179,.22), transparent 18rem),
            radial-gradient(circle at 65% 88%, rgba(9,113,85,.42), transparent 19rem),
            linear-gradient(120deg,
                {palette["hero_start"]} 0%,
                {palette["hero_mid"]} 52%,
                {palette["hero_end"]} 100%);
        color: {palette["hero_text"]};
        box-shadow: 0 24px 60px rgba(3, 48, 38, .22);
        border: 1px solid rgba(255,255,255,.08);
    }}

    .eco-v2-hero:after {{
        content: "";
        position: absolute;
        width: 360px;
        height: 360px;
        right: -90px;
        bottom: -150px;
        border-radius: 50%;
        border: 1px solid rgba(255,255,255,.13);
        box-shadow:
            0 0 0 36px rgba(255,255,255,.025),
            0 0 0 72px rgba(255,255,255,.018);
    }}

    .eco-v2-eyebrow {{
        display: inline-flex;
        gap: .45rem;
        align-items: center;
        padding: .45rem .7rem;
        border-radius: 999px;
        background: rgba(255,255,255,.10);
        border: 1px solid rgba(255,255,255,.14);
        font-size: .76rem;
        font-weight: 750;
        letter-spacing: .08em;
        text-transform: uppercase;
        color: #DDF9EB;
    }}

    .eco-v2-hero h1 {{
        position: relative;
        z-index: 1;
        margin: 1rem 0 .8rem 0;
        max-width: 820px;
        font-size: clamp(2.15rem, 3.8vw, 4rem);
        line-height: .98;
        letter-spacing: -.055em;
        color: {palette["hero_text"]} !important;
    }}

    .eco-v2-hero h1 span {{
        color: #4AF0A0;
    }}

    .eco-v2-hero p {{
        position: relative;
        z-index: 1;
        max-width: 740px;
        margin: 0;
        color: {palette["hero_sub"]} !important;
        font-size: clamp(.96rem, 1.45vw, 1.12rem);
        line-height: 1.7;
    }}

    .eco-v2-feature-strip {{
        display: grid;
        grid-template-columns: repeat(4, 1fr);
        gap: .65rem;
        margin: .65rem 0 1rem 0;
    }}

    .eco-v2-mini {{
        display: flex;
        align-items: center;
        gap: .65rem;
        min-height: 62px;
        padding: .65rem .8rem;
        border-radius: 14px;
        background: {palette["surface"]};
        border: 1px solid {palette["border"]};
        box-shadow: {palette["shadow"]};
        color: {palette["text"]};
    }}

    .eco-v2-mini-icon {{
        width: 36px;
        height: 36px;
        flex: 0 0 36px;
        display: grid;
        place-items: center;
        border-radius: 11px;
        background: rgba(23,185,120,.11);
        border: 1px solid rgba(23,185,120,.20);
        font-size: 1rem;
    }}

    .eco-v2-mini strong {{
        display: block;
        color: {palette["text"]};
        font-size: .9rem;
        margin-bottom: .1rem;
    }}

    .eco-v2-mini span {{
    color: {palette["text_secondary"]};
    font-size: .76rem;
    line-height: 1.4;
    font-weight: 500;
}}

    .eco-v2-section-title {{
        margin: 1.25rem 0 .55rem;
    }}

    .eco-v2-section-title .k {{
        color: #16A36A;
        font-size: .76rem;
        font-weight: 800;
        letter-spacing: .08em;
        text-transform: uppercase;
    }}

    .eco-v2-section-title h2 {{
        margin: .28rem 0 .25rem;
        font-size: clamp(1.4rem, 2vw, 2rem);
        color: {palette["text"]} !important;
    }}

    .eco-v2-section-title p {{
        margin: 0;
        color: {palette["text_secondary"]} !important;
        max-width: 760px;
        font-weight: 500;
        line-height: 1.6;
    }}

    .eco-card,
    .eco-stat,
    .eco-risk-score,
    .eco-recommendation,
    [data-testid="stMetric"],
    [data-testid="stForm"] {{
        background: {palette["surface"]} !important;
        border: 1px solid {palette["border"]} !important;
        box-shadow: {palette["shadow"]} !important;
        border-radius: 16px !important;
    }}

    .eco-feature-card {{
        min-height: 145px;
        background: {palette["surface"]} !important;
        border: 1px solid {palette["border"]} !important;
        box-shadow: {palette["shadow"]} !important;
        border-radius: 17px !important;
        transition: transform .18s ease, box-shadow .18s ease;
    }}

    .eco-feature-card:hover {{
        transform: translateY(-2px);
    }}

    .eco-card p,
    .eco-feature-card p,
    .eco-recommendation p {{
        color: {palette["text_secondary"]} !important;
        font-weight: 500;
    }}

    .eco-card-title,
    .eco-stat-value,
    .eco-section-title,
    .eco-page-title {{
        color: {palette["text"]} !important;
    }}

    .eco-card-description,
.eco-feature-description,
.eco-stat-label,
.eco-section-description,
.eco-page-subtitle {{
    color: {palette["text_secondary"]} !important;
}}

.eco-card-description,
.eco-feature-description,
.eco-section-description,
.eco-page-subtitle {{
    font-weight: 500;
}}

    .stButton > button {{
        border-radius: 11px !important;
        min-height: 2.75rem;
        font-weight: 700 !important;
    }}

    .stButton > button[kind="primary"] {{
        background: linear-gradient(135deg, #17B978, #0F9F68) !important;
        color: white !important;
        border: 0 !important;
        box-shadow: 0 8px 18px rgba(23,185,120,.18);
    }}

    .stButton > button[kind="secondary"] {{
        background: {palette["surface"]} !important;
        color: {palette["text"]} !important;
        border: 1px solid {palette["border"]} !important;
    }}

    div[data-baseweb="select"] > div,
    .stTextInput input,
    .stNumberInput input,
    textarea {{
        background: {palette["input"]} !important;
        color: {palette["text"]} !important;
        border-color: {palette["border"]} !important;
        border-radius: 11px !important;
    }}

    div[data-baseweb="select"] span {{
        color: {palette["text"]} !important;
    }}

    hr {{
        border-color: {palette["border_soft"]} !important;
    }}

    [data-testid="stHorizontalBlock"] {{
        gap: .65rem !important;
    }}

    [data-testid="stColumn"] {{
        min-width: 0 !important;
    }}

    @media (max-width: 1200px) {{
        .block-container,
        [data-testid="stMainBlockContainer"] {{
            width: 94% !important;
            padding-top: 2rem !important;
            padding-bottom: 2.5rem !important;
        }}

        [data-testid="stSidebar"] {{
            width: 248px !important;
            min-width: 248px !important;
            max-width: 248px !important;
        }}

        [data-testid="stSidebar"] > div:first-child {{
            width: 248px !important;
        }}
    }}

    @media (max-width: 1050px) {{
        .eco-v2-feature-strip {{
            grid-template-columns: repeat(2, 1fr);
        }}
    }}

    @media (max-width: 700px) {{
        .eco-v2-hero {{
            min-height: 0;
            padding: 1.6rem;
            border-radius: 19px;
        }}

        .eco-v2-feature-strip {{
            grid-template-columns: 1fr;
        }}

        .block-container {{
            padding-left: .85rem !important;
            padding-right: .85rem !important;
        }}
    }}

    /* ==========================================================
       STREAMLIT SIDEBAR TOGGLE — CURRENT DOM FIX
       ========================================================== */

    /* Streamlit currently keeps the collapse/reopen control inside
       stSidebar, including while aria-expanded="false". */
    [data-testid="stSidebarCollapseButton"] {{
        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
        z-index: 2147483000 !important;
        margin: 0 !important;
    }}

    [data-testid="stSidebarCollapseButton"] button {{
        display: inline-flex !important;
        align-items: center !important;
        justify-content: center !important;

        width: 2.35rem !important;
        height: 2.35rem !important;
        min-width: 2.35rem !important;
        min-height: 2.35rem !important;
        padding: 0 !important;

        background: var(--eco-surface) !important;
        color: var(--eco-text) !important;
        border: 1px solid var(--eco-border) !important;
        border-radius: 10px !important;
        box-shadow: 0 7px 20px rgba(0, 0, 0, .16) !important;

        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;
    }}

    [data-testid="stSidebarCollapseButton"] button:hover {{
        background: var(--eco-surface-hover) !important;
        border-color: var(--eco-primary) !important;
    }}

    /* Strongly restore the Material icon itself. */
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebarCollapseButton"] i {{
        font-family: "Material Symbols Rounded",
                     "Material Symbols Outlined",
                     "Material Icons" !important;
        font-weight: normal !important;
        font-style: normal !important;
        font-size: 1.35rem !important;
        line-height: 1 !important;
        color: var(--eco-text) !important;
        opacity: 1 !important;
        visibility: visible !important;
        letter-spacing: normal !important;
        text-transform: none !important;
        font-feature-settings: "liga" !important;
        -webkit-font-feature-settings: "liga" !important;
    }}

    /* When sidebar is OPEN: pin the collapse button at its top-right. */
    [data-testid="stSidebar"][aria-expanded="true"]
    [data-testid="stSidebarHeader"] {{
        position: sticky !important;
        top: 0 !important;
        z-index: 100000 !important;
    }}

    [data-testid="stSidebar"][aria-expanded="true"]
    [data-testid="stSidebarCollapseButton"] {{
        position: absolute !important;
        top: .65rem !important;
        right: .65rem !important;
        left: auto !important;
    }}

    /* When sidebar is CLOSED: keep the same native toggle visible
       as a floating reopen button at the top-left of the viewport. */
    [data-testid="stSidebar"][aria-expanded="false"]
    [data-testid="stSidebarCollapseButton"] {{
        position: fixed !important;
        top: .75rem !important;
        left: .75rem !important;
        right: auto !important;

        display: flex !important;
        visibility: visible !important;
        opacity: 1 !important;
        pointer-events: auto !important;

        transform: translateX(0) !important;
        z-index: 2147483000 !important;
    }}

    [data-testid="stSidebar"][aria-expanded="false"]
    [data-testid="stSidebarCollapseButton"] button {{
        background: #17B978 !important;
        color: #FFFFFF !important;
        border-color: rgba(255,255,255,.32) !important;
        box-shadow: 0 8px 24px rgba(0,0,0,.24) !important;
    }}

    [data-testid="stSidebar"][aria-expanded="false"]
    [data-testid="stSidebarCollapseButton"] span,
    [data-testid="stSidebar"][aria-expanded="false"]
    [data-testid="stSidebarCollapseButton"] i {{
        color: #FFFFFF !important;
    }}


    /* ==========================================================
       EXPANDER / DETECTED SECURITY ISSUES
       ========================================================== */

    [data-testid="stExpander"] {{
        background: {palette["surface"]} !important;
        border: 1px solid {palette["border"]} !important;
        border-radius: 12px !important;
        overflow: hidden !important;
    }}

    [data-testid="stExpander"] summary {{
        background: {palette["surface"]} !important;
        color: {palette["text"]} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stExpander"] summary:hover {{
        background: {palette["surface_hover"]} !important;
        color: {palette["text"]} !important;
    }}

    [data-testid="stExpander"] summary p,
    [data-testid="stExpander"] summary span {{
        color: {palette["text"]} !important;
        font-weight: 700 !important;
    }}

    [data-testid="stExpander"] summary:hover p,
    [data-testid="stExpander"] summary:hover span {{
        color: {palette["text"]} !important;
    }}

    [data-testid="stExpander"] summary svg,
    [data-testid="stExpander"] summary:hover svg {{
        color: {palette["text"]} !important;
        fill: {palette["text"]} !important;
    }}

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] {{
        background: {palette["surface"]} !important;
        color: {palette["text_secondary"]} !important;
    }}

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] p {{
        color: {palette["text_secondary"]} !important;
        font-weight: 500 !important;
    }}

    [data-testid="stExpander"] [data-testid="stExpanderDetails"] strong {{
    color: {palette["text"]} !important;
    font-weight: 700 !important;
}}


/* ==========================================================
   STATIC SIDEBAR — DISABLE HIDE / SHOW TOGGLE
   ========================================================== */

[data-testid="stSidebarCollapseButton"],
[data-testid="stSidebarCollapsedControl"] {{
    display: none !important;
    visibility: hidden !important;
    opacity: 0 !important;
    pointer-events: none !important;
}}

/* Keep sidebar permanently visible */
[data-testid="stSidebar"] {{
    transform: none !important;
    visibility: visible !important;
    opacity: 1 !important;
}}


</style>
"""

    # Keep the original reusable class definitions.
    st.html(
        GLOBAL_CSS
    )

    # Apply a complete theme-specific layer last.
    st.html(
        theme_css

        
    )
