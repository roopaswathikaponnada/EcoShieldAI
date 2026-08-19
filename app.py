"""
EcoShield AI
Main Streamlit Application

Current production stage:
- Device assessment form
- Input validation
- Deterministic cybersecurity risk assessment
- Security recommendations
- Sustainability recommendations

RAG and LLM enrichment will be integrated in later stages.
"""

from __future__ import annotations

import streamlit as st

from config.config import (
    ACCOUNT_SIGNOUT_OPTIONS,
    BACKUP_OPTIONS,
    DEVICE_ACCESSIBLE_OPTIONS,
    DEVICE_CONDITIONS,
    DEVICE_TYPES,
    DISPOSAL_METHODS,
    ENCRYPTION_OPTIONS,
    FACTORY_RESET_OPTIONS,
    OPERATING_SYSTEMS,
    PAGE_ICON,
    PAGE_LAYOUT,
    PAGE_TITLE,
    PERSONAL_DATA_OPTIONS,
    POWER_ON_OPTIONS,
    PROJECT_DESCRIPTION,
    PROJECT_NAME,
    PROJECT_VERSION,
    REMOVABLE_MEDIA_OPTIONS,
    SECURE_ERASE_OPTIONS,
    SENSITIVE_DATA_OPTIONS,
    STORAGE_CAPACITY_UNITS,
    STORAGE_TYPES,
)

from src.recommendation import (
    READINESS_CONDITIONAL,
    READINESS_NOT_READY,
    READINESS_READY,
    generate_recommendation,
)

from src.risk_engine import (
    CATEGORY_ACCESSIBILITY,
    CATEGORY_DATA_EXPOSURE,
    CATEGORY_MEDIA_BACKUP,
    CATEGORY_SANITIZATION,
    CATEGORY_TRANSFER,
    assess_device_risk,
)

from src.validators import (
    FIELD_ACCOUNTS_SIGNED_OUT,
    FIELD_DATA_BACKED_UP,
    FIELD_DEVICE_ACCESSIBLE,
    FIELD_DEVICE_AGE,
    FIELD_DEVICE_CONDITION,
    FIELD_DEVICE_TYPE,
    FIELD_DISPOSAL_METHOD,
    FIELD_ENCRYPTION,
    FIELD_FACTORY_RESET,
    FIELD_OPERATING_SYSTEM,
    FIELD_PERSONAL_DATA,
    FIELD_POWER_ON,
    FIELD_REMOVABLE_MEDIA_REMOVED,
    FIELD_SECURE_ERASE,
    FIELD_SENSITIVE_DATA,
    FIELD_STORAGE_CAPACITY,
    FIELD_STORAGE_TYPE,
    validate_device_input,
)


# ============================================================
# PAGE CONFIGURATION
# ============================================================

st.set_page_config(
    page_title=PAGE_TITLE,
    page_icon=PAGE_ICON,
    layout=PAGE_LAYOUT,
)


# ============================================================
# HELPER FUNCTIONS
# ============================================================

def _selectbox(
    label: str,
    options: list[str],
    *,
    key: str,
    help_text: str | None = None,
):
    """
    Create a required selectbox with no preselected answer.
    """

    return st.selectbox(
        label,
        options=options,
        index=None,
        placeholder="Select an option",
        key=key,
        help=help_text,
    )


def _readiness_message(
    readiness: str,
) -> tuple[str, str]:
    """
    Return user-facing readiness label and explanation.
    """

    if readiness == READINESS_NOT_READY:
        return (
            "Not Ready",
            (
                "Blocking security issues should be resolved "
                "before proceeding with the selected action."
            ),
        )

    if readiness == READINESS_CONDITIONAL:
        return (
            "Conditional",
            (
                "The action may proceed only after the "
                "highlighted conditions or uncertainties "
                "are reviewed."
            ),
        )

    return (
        "Ready",
        (
            "No blocking security condition has been "
            "identified for the selected action."
        ),
    )


def _display_validation_errors(
    errors: tuple[str, ...],
) -> None:
    """
    Display validation errors in a consistent format.
    """

    st.error(
        "Please correct the following assessment details "
        "before continuing:"
    )

    for error in errors:
        st.markdown(
            f"- {error}"
        )


def _display_validation_warnings(
    warnings: tuple[str, ...],
) -> None:
    """
    Display non-blocking validation observations.
    """

    if not warnings:
        return

    with st.expander(
        "Input observations",
        expanded=False,
    ):

        for warning in warnings:
            st.warning(
                warning
            )


def _display_risk_overview(
    recommendation,
) -> None:
    """
    Display high-level risk and readiness information.
    """

    assessment = (
        recommendation.assessment
    )

    if assessment is None:
        return

    st.subheader(
        "Assessment Overview"
    )

    col1, col2, col3 = st.columns(
        3
    )

    with col1:
        st.metric(
            "Security Risk Score",
            f"{assessment.score}/100",
        )

    with col2:
        st.metric(
            "Risk Level",
            assessment.risk_level,
        )

    with col3:
        st.metric(
            "Disposal Readiness",
            recommendation.readiness,
        )

    readiness_label, readiness_text = (
        _readiness_message(
            recommendation.readiness
        )
    )

    if readiness_label == "Not Ready":
        st.error(
            f"**{readiness_label}:** "
            f"{readiness_text}"
        )

    elif readiness_label == "Conditional":
        st.warning(
            f"**{readiness_label}:** "
            f"{readiness_text}"
        )

    else:
        st.success(
            f"**{readiness_label}:** "
            f"{readiness_text}"
        )

    st.info(
        recommendation.summary
    )


def _display_category_scores(
    assessment,
) -> None:
    """
    Display deterministic risk-category breakdown.
    """

    st.subheader(
        "Risk Category Breakdown"
    )

    category_order = [
        CATEGORY_DATA_EXPOSURE,
        CATEGORY_SANITIZATION,
        CATEGORY_TRANSFER,
        CATEGORY_ACCESSIBILITY,
        CATEGORY_MEDIA_BACKUP,
    ]

    columns = st.columns(
        len(category_order)
    )

    for column, category in zip(
        columns,
        category_order,
    ):

        with column:

            st.metric(
                category,
                assessment.category_scores.get(
                    category,
                    0,
                ),
            )


def _display_risk_factors(
    assessment,
) -> None:
    """
    Display explainable risk factors.
    """

    st.subheader(
        "Why This Risk Score?"
    )

    if not assessment.factors:

        st.success(
            "No significant cybersecurity risk factors "
            "were identified."
        )

        return

    for factor in assessment.factors:

        st.markdown(
            f"**{factor.category} — "
            f"+{factor.points} points**"
        )

        st.write(
            factor.message
        )


def _display_security_actions(
    recommendation,
) -> None:
    """
    Display prioritized cybersecurity recommendations.
    """

    st.subheader(
        "Security Recommendations"
    )

    if not recommendation.security_actions:

        st.success(
            "No additional security actions are currently "
            "required by the deterministic assessment."
        )

        return

    for action in (
        recommendation.security_actions
    ):

        with st.expander(
            f"{action.priority} — "
            f"{action.title}",
            expanded=(
                action.priority
                in {
                    "Critical",
                    "High",
                }
            ),
        ):

            st.markdown(
                f"**Action:** {action.action}"
            )

            st.markdown(
                f"**Why:** {action.rationale}"
            )

            st.caption(
                f"Source: {action.source}"
            )


def _display_sustainability_actions(
    recommendation,
) -> None:
    """
    Display sustainability recommendations.
    """

    st.subheader(
        "Sustainability Recommendations"
    )

    if not (
        recommendation
        .sustainability_actions
    ):

        st.info(
            "No additional sustainability recommendation "
            "was generated for this assessment."
        )

        return

    for action in (
        recommendation
        .sustainability_actions
    ):

        with st.expander(
            action.title,
            expanded=True,
        ):

            st.markdown(
                f"**Action:** {action.action}"
            )

            st.markdown(
                f"**Why:** {action.rationale}"
            )


def _display_next_steps(
    recommendation,
) -> None:
    """
    Display ordered next actions.
    """

    if not recommendation.next_steps:
        return

    st.subheader(
        "Recommended Next Steps"
    )

    for index, step in enumerate(
        recommendation.next_steps,
        start=1,
    ):

        st.markdown(
            f"**{index}. {step}**"
        )


def _display_uncertainties(
    assessment,
) -> None:
    """
    Display unknown or unsure security-relevant values.
    """

    if not assessment.uncertainties:
        return

    st.subheader(
        "Information to Verify"
    )

    st.warning(
        "Some device information remains uncertain."
    )

    for uncertainty in (
        assessment.uncertainties
    ):

        st.markdown(
            f"- {uncertainty}"
        )


def _display_final_warnings(
    recommendation,
) -> None:
    """
    Display final decision-support notices.
    """

    if not recommendation.warnings:
        return

    with st.expander(
        "Important Notices",
        expanded=False,
    ):

        for warning in (
            recommendation.warnings
        ):

            st.write(
                f"• {warning}"
            )


# ============================================================
# APPLICATION HEADER
# ============================================================

st.title(
    f"{PAGE_ICON} {PROJECT_NAME}"
)

st.subheader(
    PROJECT_DESCRIPTION
)

st.markdown(
    """
    Assess an electronic device before **selling, donating,
    reusing, repairing, recycling, or disposing of it**.

    EcoShield evaluates cybersecurity and privacy conditions,
    identifies unresolved preparation steps, and provides
    sustainability-oriented guidance.
    """
)


# ============================================================
# PRIVACY NOTICE
# ============================================================

st.info(
    "Privacy by design: EcoShield does not require passwords, "
    "personal files, account credentials, or the contents of "
    "your device. Only device-condition and security-status "
    "information is assessed."
)


# ============================================================
# BUILD INFORMATION
# ============================================================

with st.expander(
    "About This Build",
    expanded=False,
):

    st.write(
        f"**Version:** {PROJECT_VERSION}"
    )

    st.write(
        "**Frontend:** Streamlit"
    )

    st.write(
        "**Backend:** Python"
    )

    st.write(
        "**Current assessment:** "
        "Deterministic cybersecurity risk engine"
    )

    st.write(
        "**Current recommendation mode:** "
        "Rule-based security + sustainability guidance"
    )

    st.write(
        "**AI/RAG:** Scheduled for the next development stage"
    )


st.divider()


# ============================================================
# DEVICE ASSESSMENT FORM
# ============================================================

st.header(
    "Device Assessment"
)

st.caption(
    "Complete all required fields before selecting "
    "'Assess Device'."
)


with st.form(
    "device_assessment_form",
    clear_on_submit=False,
):

    # ========================================================
    # SECTION 1 — DEVICE INFORMATION
    # ========================================================

    st.subheader(
        "1. Device Information"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        device_type = _selectbox(
            "Device Type",
            DEVICE_TYPES,
            key="device_type",
        )

        operating_system = (
            _selectbox(
                "Operating System",
                OPERATING_SYSTEMS,
                key="operating_system",
            )
        )

    with col2:

        device_age = st.number_input(
            "Device Age (Years)",
            min_value=0.0,
            max_value=50.0,
            value=0.0,
            step=0.5,
            help=(
                "Enter the approximate age of the "
                "device in years."
            ),
        )

        device_condition = (
            _selectbox(
                "Device Condition",
                DEVICE_CONDITIONS,
                key="device_condition",
            )
        )


    # ========================================================
    # SECTION 2 — STORAGE INFORMATION
    # ========================================================

    st.subheader(
        "2. Storage Information"
    )

    col1, col2, col3 = st.columns(
        [2, 2, 1]
    )

    with col1:

        storage_type = (
            _selectbox(
                "Storage Type",
                STORAGE_TYPES,
                key="storage_type",
            )
        )

    with col2:

        storage_capacity = (
            st.number_input(
                "Storage Capacity",
                min_value=0.0,
                value=0.0,
                step=1.0,
                help=(
                    "Enter 0 only when storage is "
                    "Not Applicable."
                ),
            )
        )

    with col3:

        storage_unit = (
            st.selectbox(
                "Unit",
                STORAGE_CAPACITY_UNITS,
                index=0,
            )
        )


    # ========================================================
    # SECTION 3 — DATA SENSITIVITY
    # ========================================================

    st.subheader(
        "3. Data Sensitivity"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        personal_data = (
            _selectbox(
                "Contains Personal Data?",
                PERSONAL_DATA_OPTIONS,
                key="personal_data",
            )
        )

    with col2:

        sensitive_data = (
            _selectbox(
                "Contains Sensitive Data?",
                SENSITIVE_DATA_OPTIONS,
                key="sensitive_data",
            )
        )


    # ========================================================
    # SECTION 4 — DEVICE ACCESS
    # ========================================================

    st.subheader(
        "4. Device Accessibility"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        device_accessible = (
            _selectbox(
                "Device Accessible?",
                DEVICE_ACCESSIBLE_OPTIONS,
                key="device_accessible",
            )
        )

    with col2:

        can_power_on = (
            _selectbox(
                "Can Device Power On?",
                POWER_ON_OPTIONS,
                key="can_power_on",
            )
        )


    # ========================================================
    # SECTION 5 — DATA PREPARATION
    # ========================================================

    st.subheader(
        "5. Data & Security Preparation"
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        data_backed_up = (
            _selectbox(
                "Data Backed Up?",
                BACKUP_OPTIONS,
                key="data_backed_up",
            )
        )

        factory_reset = (
            _selectbox(
                "Factory Reset Performed?",
                FACTORY_RESET_OPTIONS,
                key="factory_reset",
            )
        )

        secure_erase = (
            _selectbox(
                "Secure Erase Performed?",
                SECURE_ERASE_OPTIONS,
                key="secure_erase",
            )
        )

    with col2:

        encryption_enabled = (
            _selectbox(
                "Encryption Enabled?",
                ENCRYPTION_OPTIONS,
                key="encryption_enabled",
            )
        )

        accounts_signed_out = (
            _selectbox(
                "Accounts Signed Out?",
                ACCOUNT_SIGNOUT_OPTIONS,
                key="accounts_signed_out",
            )
        )

        removable_media_removed = (
            _selectbox(
                "SIM / Memory Card Removed?",
                REMOVABLE_MEDIA_OPTIONS,
                key="removable_media_removed",
            )
        )


    # ========================================================
    # SECTION 6 — INTENDED ACTION
    # ========================================================

    st.subheader(
        "6. Intended Device Action"
    )

    disposal_method = (
        _selectbox(
            "Intended Disposal Method",
            DISPOSAL_METHODS,
            key="disposal_method",
            help_text=(
                "Choose what you currently plan "
                "to do with the device."
            ),
        )
    )


    # ========================================================
    # SUBMIT
    # ========================================================

    st.divider()

    submitted = (
        st.form_submit_button(
            "Assess Device",
            use_container_width=True,
        )
    )


# ============================================================
# ASSESSMENT PROCESSING
# ============================================================

if submitted:

    # --------------------------------------------------------
    # Build canonical validator payload
    # --------------------------------------------------------

    if (
        storage_type
        == "Not Applicable"
    ):

        formatted_capacity = "0"

    else:

        formatted_capacity = (
            f"{storage_capacity} "
            f"{storage_unit}"
        )

    payload = {
        FIELD_DEVICE_TYPE: device_type,
        FIELD_OPERATING_SYSTEM: (
            operating_system
        ),
        FIELD_DEVICE_AGE: device_age,
        FIELD_DEVICE_CONDITION: (
            device_condition
        ),
        FIELD_STORAGE_TYPE: storage_type,
        FIELD_STORAGE_CAPACITY: (
            formatted_capacity
        ),
        FIELD_PERSONAL_DATA: (
            personal_data
        ),
        FIELD_SENSITIVE_DATA: (
            sensitive_data
        ),
        FIELD_DEVICE_ACCESSIBLE: (
            device_accessible
        ),
        FIELD_POWER_ON: can_power_on,
        FIELD_DATA_BACKED_UP: (
            data_backed_up
        ),
        FIELD_FACTORY_RESET: (
            factory_reset
        ),
        FIELD_SECURE_ERASE: (
            secure_erase
        ),
        FIELD_ENCRYPTION: (
            encryption_enabled
        ),
        FIELD_ACCOUNTS_SIGNED_OUT: (
            accounts_signed_out
        ),
        FIELD_REMOVABLE_MEDIA_REMOVED: (
            removable_media_removed
        ),
        FIELD_DISPOSAL_METHOD: (
            disposal_method
        ),
    }


    # --------------------------------------------------------
    # Validation
    # --------------------------------------------------------

    validation = (
        validate_device_input(
            payload
        )
    )

    st.divider()

    if not validation.is_valid:

        _display_validation_errors(
            validation.errors
        )

        _display_validation_warnings(
            validation.warnings
        )

    else:

        _display_validation_warnings(
            validation.warnings
        )

        # ----------------------------------------------------
        # Risk assessment + recommendation
        # ----------------------------------------------------

        try:

            assessment = (
                assess_device_risk(
                    validation.data
                )
            )

            recommendation = (
                generate_recommendation(
                    assessment
                )
            )

        except (
            TypeError,
            ValueError,
        ) as exc:

            st.error(
                "EcoShield could not complete the "
                "assessment."
            )

            st.exception(
                exc
            )

        else:

            # ------------------------------------------------
            # Results
            # ------------------------------------------------

            st.header(
                "EcoShield Results"
            )

            _display_risk_overview(
                recommendation
            )

            st.divider()

            _display_category_scores(
                assessment
            )

            st.divider()

            tab1, tab2, tab3 = st.tabs(
                [
                    "Risk Factors",
                    "Security Actions",
                    "Sustainability",
                ]
            )

            with tab1:

                _display_risk_factors(
                    assessment
                )

                _display_uncertainties(
                    assessment
                )

            with tab2:

                _display_security_actions(
                    recommendation
                )

            with tab3:

                _display_sustainability_actions(
                    recommendation
                )

            st.divider()

            _display_next_steps(
                recommendation
            )

            _display_final_warnings(
                recommendation
            )


# ============================================================
# FOOTER
# ============================================================

st.divider()

st.caption(
    "EcoShield AI • Decision-support prototype for secure "
    "and sustainable electronic-device handling."
)