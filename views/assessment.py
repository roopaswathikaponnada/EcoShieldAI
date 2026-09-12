"""
EcoShield AI
Device Assessment Page

This module renders the permanent multi-step device assessment
workflow for EcoShield AI.

Responsibilities:
- Collect the canonical 17 device-assessment inputs
- Organize inputs into four user-friendly steps
- Preserve answers across Streamlit reruns
- Store assessment inputs through centralized application state
- Submit the canonical payload through the frontend integration layer
- Display frontend-safe submission feedback
- Navigate to Risk Analysis after successful assessment

Validation, risk scoring, recommendation generation, RAG retrieval,
and LLM enrichment are owned by EcoShield's backend service layers.
"""

from __future__ import annotations

from typing import Any

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
    PERSONAL_DATA_OPTIONS,
    POWER_ON_OPTIONS,
    REMOVABLE_MEDIA_OPTIONS,
    SECURE_ERASE_OPTIONS,
    SENSITIVE_DATA_OPTIONS,
    STORAGE_CAPACITY_UNITS,
    STORAGE_TYPES,
)

from src.services.frontend_integration import (
    submit_device_assessment,
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
)

from ui.components import (
    render_notice,
    render_page_header,
    render_section_header,
    render_spacer,
    render_step_indicator,
)

from ui.navigation import (
    PAGE_RISK_ANALYSIS,
    navigate_to,
)

from ui.state import (
    ASSESSMENT_FINAL_STEP,
    ASSESSMENT_TOTAL_STEPS,
    get_assessment_payload,
    get_assessment_step,
    next_assessment_step,
    previous_assessment_step,
    set_assessment_step,
    update_assessment_payload,
)

# ============================================================
# ASSESSMENT STEP LABELS
# ============================================================

ASSESSMENT_STEP_LABELS = (
    "Device Profile",
    "Data Sensitivity",
    "Security Preparation",
    "Intended Action",
)


# ============================================================
# WIDGET KEY PREFIX
# ============================================================

WIDGET_PREFIX = "assessment_ui_"


# ============================================================
# OPTION INDEX HELPER
# ============================================================

def _option_index(
    options: list[str],
    current_value: Any,
) -> int | None:
    """
    Return the index of a previously selected value.

    None is returned when no valid previous selection exists.
    """

    if current_value is None:
        return None

    try:
        return options.index(
            str(current_value)
        )

    except ValueError:
        return None


# ============================================================
# REQUIRED SELECTBOX
# ============================================================

def _required_selectbox(
    *,
    label: str,
    options: list[str],
    field_name: str,
    help_text: str | None = None,
) -> str | None:
    """
    Render a required selectbox while restoring any
    previously stored assessment value.
    """

    payload = (
        get_assessment_payload()
    )

    return st.selectbox(
        label,
        options=options,
        index=_option_index(
            options,
            payload.get(
                field_name
            ),
        ),
        placeholder="Select an option",
        key=(
            WIDGET_PREFIX
            + field_name
        ),
        help=help_text,
    )


# ============================================================
# STORAGE CAPACITY PARSING
# ============================================================

def _stored_capacity_parts() -> tuple[float, str]:
    """
    Convert the stored canonical storage-capacity value into
    number + unit values for the UI.

    Examples
    --------
    "512 GB" -> (512.0, "GB")
    "1 TB"   -> (1.0, "TB")
    None     -> (0.0, "GB")
    """

    payload = (
        get_assessment_payload()
    )

    value = payload.get(
        FIELD_STORAGE_CAPACITY
    )

    if value is None:
        return 0.0, "GB"

    normalized = (
        str(value)
        .strip()
        .upper()
    )

    if not normalized:
        return 0.0, "GB"

    parts = normalized.split()

    try:

        if len(parts) == 1:

            return (
                float(parts[0]),
                "GB",
            )

        number = float(
            parts[0]
        )

        unit = parts[1]

        if unit not in STORAGE_CAPACITY_UNITS:
            unit = "GB"

        return (
            number,
            unit,
        )

    except (
        TypeError,
        ValueError,
    ):

        return 0.0, "GB"


# ============================================================
# STEP 1 — DEVICE PROFILE
# ============================================================

def _render_step_device_profile() -> dict[str, Any]:
    """
    Render Step 1: Device Profile.
    """

    render_section_header(
        title="Device Profile",
        description=(
            "Tell EcoShield what kind of device you are "
            "assessing and provide its basic hardware details."
        ),
        icon="🖥️",
    )

    payload = (
        get_assessment_payload()
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        device_type = (
            _required_selectbox(
                label="Device Type",
                options=DEVICE_TYPES,
                field_name=FIELD_DEVICE_TYPE,
                help_text=(
                    "Select the type of electronic device you are "
                    "assessing, such as a laptop, smartphone, "
                    "tablet, or desktop."
                ),
            )
        )

        operating_system = (
            _required_selectbox(
                label="Operating System",
                options=OPERATING_SYSTEMS,
                field_name=FIELD_OPERATING_SYSTEM,
                help_text=(
                    "Select the operating system currently installed "
                    "on the device."
                ),
            )
        )

        stored_age = payload.get(
            FIELD_DEVICE_AGE
        )

        device_age = st.number_input(
            "Device Age (Years)",
            min_value=0.0,
            max_value=50.0,
            value=(
                float(stored_age)
                if isinstance(
                    stored_age,
                    (int, float),
                )
                else 0.0
            ),
            step=0.5,
            key=(
                WIDGET_PREFIX
                + FIELD_DEVICE_AGE
            ),
            help=(
                "Enter the approximate age of the "
                "device in years."
            ),
        )

    with col2:

        device_condition = (
            _required_selectbox(
                label="Device Condition",
                options=DEVICE_CONDITIONS,
                field_name=FIELD_DEVICE_CONDITION,
                help_text=(
                    "Select the device's current physical and working "
                    "condition."
                ),
            )
        )

        storage_type = (
            _required_selectbox(
                label="Storage Type",
                options=STORAGE_TYPES,
                field_name=FIELD_STORAGE_TYPE,
                help_text=(
                    "Select the main storage technology used by the "
                    "device, such as SSD, HDD, or flash storage."
                ),
            )
        )

        stored_capacity, stored_unit = (
            _stored_capacity_parts()
        )

        capacity_col, unit_col = st.columns(
            [2, 1]
        )

        with capacity_col:

            storage_capacity = (
                st.number_input(
                    "Storage Capacity",
                    min_value=0.0,
                    value=stored_capacity,
                    step=1.0,
                    key=(
                        WIDGET_PREFIX
                        + "storage_capacity_value"
                    ),
                    help=(
                        "Use 0 only when storage type "
                        "is Not Applicable."
                    ),
                )
            )

        with unit_col:

            storage_unit = st.selectbox(
                "Unit",
                options=(
                    STORAGE_CAPACITY_UNITS
                ),
                index=(
                    STORAGE_CAPACITY_UNITS.index(
                        stored_unit
                    )
                    if stored_unit
                    in STORAGE_CAPACITY_UNITS
                    else 0
                ),
                key=(
                    WIDGET_PREFIX
                    + "storage_capacity_unit"
                ),
            )

    if storage_type == "Not Applicable":

        formatted_capacity = "0"

    else:

        formatted_capacity = (
            f"{storage_capacity:g} "
            f"{storage_unit}"
        )

    return {
        FIELD_DEVICE_TYPE:
            device_type,

        FIELD_OPERATING_SYSTEM:
            operating_system,

        FIELD_DEVICE_AGE:
            device_age,

        FIELD_DEVICE_CONDITION:
            device_condition,

        FIELD_STORAGE_TYPE:
            storage_type,

        FIELD_STORAGE_CAPACITY:
            formatted_capacity,
    }


# ============================================================
# STEP 2 — DATA SENSITIVITY
# ============================================================

def _render_step_data_sensitivity() -> dict[str, Any]:
    """
    Render Step 2: Data Sensitivity.
    """

    render_section_header(
        title="Data Sensitivity",
        description=(
            "Describe whether data may remain on the device "
            "and whether the device can currently be accessed."
        ),
        icon="🔐",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        personal_data = (
            _required_selectbox(
                label="Contains Personal Data?",
                options=PERSONAL_DATA_OPTIONS,
                field_name=FIELD_PERSONAL_DATA,
                help_text=(
                    "Examples include personal documents, "
                    "photos, messages, browser data, or "
                    "saved application information."
                ),
            )
        )

        device_accessible = (
            _required_selectbox(
                label="Device Accessible?",
                options=DEVICE_ACCESSIBLE_OPTIONS,
                field_name=FIELD_DEVICE_ACCESSIBLE,
                help_text=(
                    "Select Yes if you can currently unlock and access "
                    "the device and its stored data."
                ),
            )
        )

    with col2:

        sensitive_data = (
            _required_selectbox(
                label="Contains Sensitive Data?",
                options=SENSITIVE_DATA_OPTIONS,
                field_name=FIELD_SENSITIVE_DATA,
                help_text=(
                    "Examples include financial, academic, "
                    "business, identity, confidential, or "
                    "security-sensitive information."
                ),
            )
        )

        can_power_on = (
            _required_selectbox(
                label="Can Device Power On?",
                options=POWER_ON_OPTIONS,
                field_name=FIELD_POWER_ON,
                help_text=(
                    "Select Yes if the device can currently switch on "
                    "and operate enough to access its settings or storage."
                ),
            )
        )

    return {
        FIELD_PERSONAL_DATA:
            personal_data,

        FIELD_SENSITIVE_DATA:
            sensitive_data,

        FIELD_DEVICE_ACCESSIBLE:
            device_accessible,

        FIELD_POWER_ON:
            can_power_on,
    }


# ============================================================
# STEP 3 — SECURITY PREPARATION
# ============================================================

def _render_step_security_preparation() -> dict[str, Any]:
    """
    Render Step 3: Security Preparation.
    """

    render_section_header(
        title="Security Preparation",
        description=(
            "Tell EcoShield which data-protection and "
            "device-preparation actions have already been "
            "completed."
        ),
        icon="🛡️",
    )

    col1, col2 = st.columns(
        2
    )

    with col1:

        data_backed_up = (
            _required_selectbox(
                label="Data Backed Up?",
                options=BACKUP_OPTIONS,
                field_name=FIELD_DATA_BACKED_UP,
                help_text=(
                    "Select Yes if important files have already been safely "
                    "copied to another device, drive, or trusted cloud storage."
                ),
            )
        )

        factory_reset = (
            _required_selectbox(
                label="Factory Reset Performed?",
                options=FACTORY_RESET_OPTIONS,
                field_name=FIELD_FACTORY_RESET,
                help_text=(
                    "Select Yes if the device has already been restored to "
                    "factory settings and user data has been removed."
                ),
            )
        )

        secure_erase = (
            _required_selectbox(
                label="Secure Erase Performed?",
                options=SECURE_ERASE_OPTIONS,
                field_name=FIELD_SECURE_ERASE,
                help_text=(
                    "Select Yes only if an appropriate secure data-erasure "
                    "or storage-sanitization process has been performed."
                ),
            )
        )

    with col2:

        encryption_enabled = (
            _required_selectbox(
                label="Encryption Enabled?",
                options=ENCRYPTION_OPTIONS,
                field_name=FIELD_ENCRYPTION,
                help_text=(
                    "Select Yes if the device or its storage is protected "
                    "using device or disk encryption."
                ),
            )
        )

        accounts_signed_out = (
            _required_selectbox(
                label="Accounts Signed Out?",
                options=ACCOUNT_SIGNOUT_OPTIONS,
                field_name=FIELD_ACCOUNTS_SIGNED_OUT,
                help_text=(
                    "Select Yes if personal accounts such as Google, Apple, "
                    "Microsoft, email, or other services have been signed out."
                ),
            )
        )

        removable_media_removed = (
            _required_selectbox(
                label="SIM / Memory Card Removed?",
                options=REMOVABLE_MEDIA_OPTIONS,
                field_name=FIELD_REMOVABLE_MEDIA_REMOVED,
                help_text=(
                    "Select Yes if removable SIM cards and external memory "
                    "cards have been removed from the device."
                ),
            )
        )

    return {
        FIELD_DATA_BACKED_UP:
            data_backed_up,

        FIELD_FACTORY_RESET:
            factory_reset,

        FIELD_SECURE_ERASE:
            secure_erase,

        FIELD_ENCRYPTION:
            encryption_enabled,

        FIELD_ACCOUNTS_SIGNED_OUT:
            accounts_signed_out,

        FIELD_REMOVABLE_MEDIA_REMOVED:
            removable_media_removed,
    }


# ============================================================
# STEP 4 — INTENDED ACTION
# ============================================================

def _render_step_intended_action() -> dict[str, Any]:
    """
    Render Step 4: Intended Action.
    """

    render_section_header(
        title="Intended Device Action",
        description=(
            "Choose what you currently plan to do with "
            "the device. EcoShield will evaluate the "
            "security implications of that decision."
        ),
        icon="♻️",
    )

    disposal_method = (
        _required_selectbox(
            label="Intended Disposal Method",
            options=DISPOSAL_METHODS,
            field_name=FIELD_DISPOSAL_METHOD,
            help_text=(
                "Choose Sell, Donate, Reuse, Recycle, "
                "Dispose, Repair, or Not Decided."
            ),
        )
    )

    render_spacer(
        "sm"
    )

    render_notice(
        title="Before EcoShield analyzes the device",
        message=(
            "Your assessment uses only the security-status "
            "information entered in this form. EcoShield does "
            "not require passwords, personal files, account "
            "credentials, or device contents."
        ),
        notice_type="info",
    )

    return {
        FIELD_DISPOSAL_METHOD:
            disposal_method,
    }


# ============================================================
# CURRENT STEP RENDERER
# ============================================================

def _render_current_step(
    step: int,
) -> dict[str, Any]:
    """
    Render and return values for the active assessment step.
    """

    if step == 1:

        return (
            _render_step_device_profile()
        )

    if step == 2:

        return (
            _render_step_data_sensitivity()
        )

    if step == 3:

        return (
            _render_step_security_preparation()
        )

    return (
        _render_step_intended_action()
    )


# ============================================================
# CURRENT STEP COMPLETENESS
# ============================================================

def _step_is_complete(
    values: dict[str, Any],
) -> bool:
    """
    Perform lightweight UI completeness checking.

    Full correctness and cross-field validation remain the
    responsibility of src/validators.py.
    """

    for value in values.values():

        if value is None:
            return False

        if (
            isinstance(
                value,
                str,
            )
            and not value.strip()
        ):
            return False

    return True

# ============================================================
# FINAL ASSESSMENT PROCESSING
# ============================================================


def _process_assessment() -> None:
    """
    Submit the canonical assessment payload through EcoShield's
    unified frontend/backend integration boundary.

    Backend validation, deterministic risk calculation,
    recommendation generation, and optional RAG / AI enrichment
    are owned by the backend service and integration adapter.
    """

    payload = (
        get_assessment_payload()
    )

    try:

        with st.spinner(
            "EcoShield is analyzing your device..."
        ):

            submission = (
                submit_device_assessment(
                    payload
                )
            )

    except Exception as exc:

        render_notice(
            title="Assessment could not be completed",
            message=(
                "EcoShield encountered an unexpected "
                "integration error. Please try again."
            ),
            notice_type="error",
        )

        print(
            "[EcoShield] Unexpected frontend submission error: "
            f"{type(exc).__name__}: {exc}"
        )

        return

    if not submission.succeeded:

        render_notice(
            title="Assessment could not be completed",
            message=(
                submission.message
                or (
                    "Review the entered device information "
                    "and try again."
                )
            ),
            notice_type=(
                "warning"
                if submission.validation_failed
                else "error"
            ),
        )

        return

    if submission.used_fallback:

        render_notice(
            title="Assessment completed with safe fallback",
            message=(
                submission.message
                or (
                    "EcoShield completed the deterministic "
                    "assessment successfully."
                )
            ),
            notice_type="warning",
        )

    navigate_to(
        PAGE_RISK_ANALYSIS
    )

# ============================================================
# ASSESSMENT NAVIGATION
# ============================================================

def _render_step_navigation(
    *,
    step: int,
    current_values: dict[str, Any],
) -> None:
    """
    Render Previous / Continue / Analyze controls.
    """

    st.divider()

    if step == 1:

        left, right = st.columns(
            [2, 1]
        )

        with right:

            continue_clicked = (
                st.button(
                    "Continue →",
                    key=(
                        WIDGET_PREFIX
                        + "continue_step_1"
                    ),
                    type="primary",
                    use_container_width=True,
                )
            )

        if continue_clicked:

            if not _step_is_complete(
                current_values
            ):

                render_notice(
                    title="Complete this step",
                    message=(
                        "Please answer all fields in "
                        "Device Profile before continuing."
                    ),
                    notice_type="warning",
                )

                return

            update_assessment_payload(
                current_values
            )

            next_assessment_step()

            st.rerun()

        return

    if step < ASSESSMENT_FINAL_STEP:

        left, right = st.columns(
            2
        )

        with left:

            previous_clicked = (
                st.button(
                    "← Previous",
                    key=(
                        WIDGET_PREFIX
                        + f"previous_step_{step}"
                    ),
                    use_container_width=True,
                )
            )

        with right:

            continue_clicked = (
                st.button(
                    "Continue →",
                    key=(
                        WIDGET_PREFIX
                        + f"continue_step_{step}"
                    ),
                    type="primary",
                    use_container_width=True,
                )
            )

        if previous_clicked:

            update_assessment_payload(
                current_values
            )

            previous_assessment_step()

            st.rerun()

        if continue_clicked:

            if not _step_is_complete(
                current_values
            ):

                render_notice(
                    title="Complete this step",
                    message=(
                        "Please answer all fields before "
                        "continuing."
                    ),
                    notice_type="warning",
                )

                return

            update_assessment_payload(
                current_values
            )

            next_assessment_step()

            st.rerun()

        return

    # --------------------------------------------------------
    # Final step
    # --------------------------------------------------------

    left, right = st.columns(
        2
    )

    with left:

        previous_clicked = (
            st.button(
                "← Previous",
                key=(
                    WIDGET_PREFIX
                    + "previous_final"
                ),
                use_container_width=True,
            )
        )

    with right:

        analyze_clicked = (
            st.button(
                "🛡️ Analyze Device Risk",
                key=(
                    WIDGET_PREFIX
                    + "analyze"
                ),
                type="primary",
                use_container_width=True,
            )
        )

    if previous_clicked:

        update_assessment_payload(
            current_values
        )

        previous_assessment_step()

        st.rerun()

    if analyze_clicked:

        if not _step_is_complete(
            current_values
        ):

            render_notice(
                title="Choose an intended action",
                message=(
                    "Select the intended disposal method "
                    "before running the EcoShield assessment."
                ),
                notice_type="warning",
            )

            return

        update_assessment_payload(
            current_values
        )

        _process_assessment()


# ============================================================
# START-OVER CONTROL
# ============================================================

def _render_restart_control() -> None:
    """
    Allow the user to restart only the step workflow.

    Existing answers are intentionally retained until the
    user changes them.
    """

    if get_assessment_step() == 1:
        return

    if st.button(
        "↺ Return to Step 1",
        key=(
            WIDGET_PREFIX
            + "return_step_1"
        ),
    ):

        set_assessment_step(
            1
        )

        st.rerun()


# ============================================================
# PUBLIC PAGE RENDERER
# ============================================================

def render() -> None:
    """
    Render the complete EcoShield Device Assessment page.

    app.py discovers this function dynamically.
    """

    render_page_header(
        kicker="Security + Sustainability Assessment",
        title="Device Assessment",
        subtitle=(
            "Answer 17 structured questions about your "
            "device. EcoShield will validate the information, "
            "calculate a deterministic cybersecurity risk "
            "score, and generate recommended next actions."
        ),
        icon="🔍",
    )

    current_step = (
        get_assessment_step()
    )

    render_step_indicator(
        current_step=current_step,
        total_steps=ASSESSMENT_TOTAL_STEPS,
        labels=ASSESSMENT_STEP_LABELS,
    )

    st.caption(
        f"Step {current_step} of "
        f"{ASSESSMENT_TOTAL_STEPS}"
    )

    render_spacer(
        "md"
    )

    current_values = (
        _render_current_step(
            current_step
        )
    )

    _render_step_navigation(
        step=current_step,
        current_values=current_values,
    )

    render_spacer(
        "sm"
    )

    _render_restart_control()