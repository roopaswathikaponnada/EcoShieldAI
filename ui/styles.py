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
        38px;

    height:
        38px;

    border-radius:
        11px;

    background:
        var(--eco-primary-soft);

    border:
        1px solid var(--eco-primary-border);

    color:
        var(--eco-primary);

    font-size:
        1.2rem;
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

def apply_global_styles() -> None:
    """
    Apply the EcoShield global stylesheet to the current
    Streamlit page.

    This function should be called once by the final app shell.
    Individual pages should not inject their own global CSS.
    """

    st.markdown(
        GLOBAL_CSS,
        unsafe_allow_html=True,
    )