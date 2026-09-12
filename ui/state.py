"""
EcoShield AI
Streamlit Session State Management

This module provides centralized session-state management for
the EcoShield AI application.

Responsibilities:
- Initialize application session state
- Store device assessment form values
- Track multi-step assessment progress
- Store validation results
- Store cybersecurity risk assessments
- Store recommendation results
- Store future RAG and LLM outputs
- Manage navigation-related state
- Reset assessment workflows safely
- Provide small state access/update helpers

Business logic, validation, risk scoring, recommendation generation,
RAG retrieval, and LLM calls must NOT be implemented here.
"""

from __future__ import annotations

from copy import deepcopy
from typing import Any, Mapping

import streamlit as st


# ============================================================
# APPLICATION STATE KEYS
# ============================================================
STATE_THEME = "theme"

STATE_INITIALIZED = "_ecoshield_state_initialized"

STATE_CURRENT_PAGE = "current_page"

STATE_ASSESSMENT_STEP = "assessment_step"

STATE_ASSESSMENT_PAYLOAD = "assessment_payload"

STATE_VALIDATION_RESULT = "validation_result"

STATE_RISK_ASSESSMENT = "risk_assessment"

STATE_RECOMMENDATION_RESULT = "recommendation_result"

STATE_SUSTAINABILITY_RESULT = "sustainability_result"

STATE_ASSESSMENT_SERVICE_RESULT = "assessment_service_result"

STATE_ASSESSMENT_COMPLETED = "assessment_completed"

STATE_ASSESSMENT_RAG_ENABLED = "assessment_rag_enabled"

STATE_ASSESSMENT_AI_ENABLED = "assessment_ai_enabled"

STATE_ASSESSMENT_RAG_ATTEMPTED = "assessment_rag_attempted"

STATE_ASSESSMENT_AI_ATTEMPTED = "assessment_ai_attempted"

STATE_ASSESSMENT_RAG_SUCCEEDED = "assessment_rag_succeeded"

STATE_ASSESSMENT_AI_SUCCEEDED = "assessment_ai_succeeded"

STATE_ASSESSMENT_USED_FALLBACK = "assessment_used_fallback"

STATE_ASSESSMENT_RETRIEVED_CONTEXT = (
    "assessment_retrieved_context"
)

STATE_ASSESSMENT_AI_EXPLANATION = (
    "assessment_ai_explanation"
)

STATE_ASSESSMENT_WARNINGS = "assessment_warnings"

STATE_ASSESSMENT_ERRORS = "assessment_errors"

STATE_RAG_CONTEXT = "rag_context"

STATE_RAG_SOURCES = "rag_sources"

STATE_AI_RESPONSE = "ai_response"

STATE_LAST_QUESTION = "last_question"

STATE_KNOWLEDGE_QUERY = "knowledge_query"

STATE_ERROR_MESSAGE = "error_message"

STATE_SUCCESS_MESSAGE = "success_message"


# ============================================================
# ASSESSMENT CONFIGURATION
# ============================================================

ASSESSMENT_TOTAL_STEPS = 4

ASSESSMENT_FIRST_STEP = 1

ASSESSMENT_FINAL_STEP = ASSESSMENT_TOTAL_STEPS

# ============================================================
# DEFAULT DEVICE ASSESSMENT PAYLOAD
# ============================================================

DEFAULT_ASSESSMENT_PAYLOAD: dict[str, Any] = {
    "device_type": None,
    "operating_system": None,
    "device_age": None,
    "device_condition": None,
    "storage_type": None,
    "storage_capacity": None,
    "contains_personal_data": None,
    "contains_sensitive_data": None,
    "device_accessible": None,
    "can_power_on": None,
    "data_backed_up": None,
    "factory_reset_performed": None,
    "secure_erase_performed": None,
    "encryption_enabled": None,
    "accounts_signed_out": None,
    "sim_memory_card_removed": None,
    "intended_disposal_method": None,
}


# ============================================================
# DEFAULT APPLICATION STATE
# ============================================================

DEFAULT_SESSION_STATE: dict[str, Any] = {
    STATE_THEME: "dark",
    STATE_CURRENT_PAGE: "Home",
    STATE_ASSESSMENT_STEP: ASSESSMENT_FIRST_STEP,
    STATE_ASSESSMENT_PAYLOAD: DEFAULT_ASSESSMENT_PAYLOAD,
    STATE_VALIDATION_RESULT: None,
    STATE_RISK_ASSESSMENT: None,
    STATE_RECOMMENDATION_RESULT: None,
    STATE_SUSTAINABILITY_RESULT: None,
    STATE_ASSESSMENT_SERVICE_RESULT: None,
    STATE_ASSESSMENT_COMPLETED: False,

    STATE_ASSESSMENT_RAG_ENABLED: False,
    STATE_ASSESSMENT_AI_ENABLED: False,
    STATE_ASSESSMENT_RAG_ATTEMPTED: False,
    STATE_ASSESSMENT_AI_ATTEMPTED: False,
    STATE_ASSESSMENT_RAG_SUCCEEDED: False,
    STATE_ASSESSMENT_AI_SUCCEEDED: False,
    STATE_ASSESSMENT_USED_FALLBACK: False,
    STATE_ASSESSMENT_RETRIEVED_CONTEXT: (),
    STATE_ASSESSMENT_AI_EXPLANATION: None,
    STATE_ASSESSMENT_WARNINGS: (),
    STATE_ASSESSMENT_ERRORS: (),

    STATE_RAG_CONTEXT: None,
    STATE_RAG_SOURCES: [],
    STATE_AI_RESPONSE: None,
    STATE_LAST_QUESTION: None,
    STATE_KNOWLEDGE_QUERY: "",
    STATE_ERROR_MESSAGE: None,
    STATE_SUCCESS_MESSAGE: None,
}


# ============================================================
# INTERNAL COPY HELPER
# ============================================================

def _copy_default(
    value: Any,
) -> Any:
    """
    Return a safe independent copy of a default state value.

    Deep copying prevents mutable values such as dictionaries
    and lists from being shared accidentally between state
    initialization operations.
    """

    return deepcopy(value)

# ============================================================
# INTERNAL BOOLEAN VALIDATION
# ============================================================

def _require_bool(
    value: Any,
    *,
    field_name: str,
) -> bool:
    """
    Require an actual boolean value.

    This prevents truthy values such as "False", 1, or non-empty
    containers from being silently interpreted as True.
    """

    if not isinstance(value, bool):
        raise TypeError(
            f"{field_name} must be a boolean."
        )

    return value

# ============================================================
# INTERNAL STATE REPAIR
# ============================================================

def _repair_session_state() -> None:
    """
    Repair structurally invalid EcoShield session-state values.

    Valid existing user/session values are preserved. Recovery
    only applies when a known state value cannot safely satisfy
    its expected structural contract.
    """

    # --------------------------------------------------------
    # Assessment step
    # --------------------------------------------------------

    raw_step = st.session_state.get(
        STATE_ASSESSMENT_STEP,
        ASSESSMENT_FIRST_STEP,
    )

    if isinstance(raw_step, bool):
        repaired_step = ASSESSMENT_FIRST_STEP

    else:
        try:
            repaired_step = int(raw_step)

        except (TypeError, ValueError):
            repaired_step = ASSESSMENT_FIRST_STEP

    repaired_step = max(
        ASSESSMENT_FIRST_STEP,
        min(
            repaired_step,
            ASSESSMENT_FINAL_STEP,
        ),
    )

    st.session_state[
        STATE_ASSESSMENT_STEP
    ] = repaired_step

    # --------------------------------------------------------
    # Assessment payload
    # --------------------------------------------------------

    raw_payload = st.session_state.get(
        STATE_ASSESSMENT_PAYLOAD
    )

    if isinstance(raw_payload, Mapping):

        repaired_payload = _copy_default(
            DEFAULT_ASSESSMENT_PAYLOAD
        )

        for field_name in DEFAULT_ASSESSMENT_PAYLOAD:

            if field_name in raw_payload:
                repaired_payload[field_name] = (
                    raw_payload[field_name]
                )

        st.session_state[
            STATE_ASSESSMENT_PAYLOAD
        ] = repaired_payload

    else:

        st.session_state[
            STATE_ASSESSMENT_PAYLOAD
        ] = _copy_default(
            DEFAULT_ASSESSMENT_PAYLOAD
        )

    # --------------------------------------------------------
    # Boolean assessment state
    # --------------------------------------------------------

    boolean_state_keys = (
        STATE_ASSESSMENT_COMPLETED,
        STATE_ASSESSMENT_RAG_ENABLED,
        STATE_ASSESSMENT_AI_ENABLED,
        STATE_ASSESSMENT_RAG_ATTEMPTED,
        STATE_ASSESSMENT_AI_ATTEMPTED,
        STATE_ASSESSMENT_RAG_SUCCEEDED,
        STATE_ASSESSMENT_AI_SUCCEEDED,
        STATE_ASSESSMENT_USED_FALLBACK,
    )

    for key in boolean_state_keys:

        if not isinstance(
            st.session_state.get(key),
            bool,
        ):
            st.session_state[key] = False

    # --------------------------------------------------------
    # Assessment tuple/container state
    # --------------------------------------------------------

    tuple_state_keys = (
        STATE_ASSESSMENT_RETRIEVED_CONTEXT,
        STATE_ASSESSMENT_WARNINGS,
        STATE_ASSESSMENT_ERRORS,
    )

    for key in tuple_state_keys:

        value = st.session_state.get(
            key,
            (),
        )

        if isinstance(
            value,
            (list, tuple),
        ):
            st.session_state[key] = tuple(value)

        else:
            st.session_state[key] = ()

    # --------------------------------------------------------
    # Assessment AI explanation
    # --------------------------------------------------------

    explanation = st.session_state.get(
        STATE_ASSESSMENT_AI_EXPLANATION
    )

    if (
        explanation is not None
        and not isinstance(explanation, str)
    ):
        st.session_state[
            STATE_ASSESSMENT_AI_EXPLANATION
        ] = None

    # --------------------------------------------------------
    # Generic RAG source container
    # --------------------------------------------------------

    rag_sources = st.session_state.get(
        STATE_RAG_SOURCES,
        [],
    )

    if isinstance(
        rag_sources,
        (list, tuple),
    ):
        st.session_state[
            STATE_RAG_SOURCES
        ] = list(rag_sources)

    else:
        st.session_state[
            STATE_RAG_SOURCES
        ] = []

    # --------------------------------------------------------
    # Knowledge query
    # --------------------------------------------------------

    if not isinstance(
        st.session_state.get(
            STATE_KNOWLEDGE_QUERY
        ),
        str,
    ):
        st.session_state[
            STATE_KNOWLEDGE_QUERY
        ] = ""

# ============================================================
# SESSION STATE INITIALIZATION
# ============================================================

def initialize_session_state() -> None:
    """
    Initialize all EcoShield session-state values.

    Missing values are created from safe independent defaults.
    Valid existing session values are preserved, while known
    structurally invalid values are repaired safely.

    This function is safe to call on every Streamlit rerun.
    """

    for key, default_value in DEFAULT_SESSION_STATE.items():

        if key not in st.session_state:

            st.session_state[key] = _copy_default(
                default_value
            )

    _repair_session_state()

    st.session_state[
        STATE_INITIALIZED
    ] = True


# ============================================================
# INITIALIZATION CHECK
# ============================================================

def is_state_initialized() -> bool:
    """
    Return whether EcoShield session state has been initialized.
    """

    return bool(
        st.session_state.get(
            STATE_INITIALIZED,
            False,
        )
    )


# ============================================================
# GENERIC STATE ACCESS
# ============================================================

def get_state(
    key: str,
    default: Any = None,
) -> Any:
    """
    Safely retrieve a value from Streamlit session state.
    """

    return st.session_state.get(
        key,
        default,
    )


def set_state(
    key: str,
    value: Any,
) -> None:
    """
    Store a value in Streamlit session state.
    """

    st.session_state[key] = value


def clear_state(
    key: str,
) -> None:
    """
    Remove a state value when it exists.
    """

    if key in st.session_state:
        del st.session_state[key]

# ============================================================
# STATE SERIALIZATION
# ============================================================

def _serialize_state_value(
    value: Any,
) -> Any:
    """
    Convert a session-state value into a serialization-safe
    representation.

    Primitive values are preserved. Dictionaries and sequence
    containers are serialized recursively. Domain objects that
    expose a callable to_dict() method are serialized through
    that public boundary.

    Unknown opaque objects are converted to strings rather than
    exposing their internal implementation details.
    """

    if value is None or isinstance(
        value,
        (str, int, float, bool),
    ):
        return value

    if isinstance(value, Mapping):
        return {
            str(key): _serialize_state_value(item)
            for key, item in value.items()
        }

    if isinstance(value, (list, tuple, set)):
        return [
            _serialize_state_value(item)
            for item in value
        ]

    to_dict = getattr(
        value,
        "to_dict",
        None,
    )

    if callable(to_dict):

        try:
            serialized = to_dict()

        except Exception:
            return str(value)

        return _serialize_state_value(
            serialized
        )

    return str(value)        

def serialize_application_state() -> dict[str, Any]:
    """
    Return a serialization-safe snapshot of EcoShield-owned
    application/session state.

    Only keys owned by EcoShield are included. Unrelated
    Streamlit widget state is intentionally excluded.
    """

    serialized_state: dict[str, Any] = {}

    for key in DEFAULT_SESSION_STATE:

        value = st.session_state.get(
            key,
            _copy_default(
                DEFAULT_SESSION_STATE[key]
            ),
        )

        serialized_state[key] = (
            _serialize_state_value(value)
        )

    return serialized_state

def serialize_assessment_state() -> dict[str, Any]:
    """
    Return a serialization-safe snapshot of the current
    assessment workflow.

    Navigation, theme, flash messages, and standalone
    Knowledge Center state are intentionally excluded.
    """

    assessment_state = {
        "assessment_step": get_assessment_step(),
        "assessment_payload": get_assessment_payload(),
        "validation_result": get_validation_result(),
        "risk_assessment": get_risk_assessment(),
        "recommendation_result": get_recommendation_result(),
        "sustainability_result": (
            get_sustainability_result()
        ),   
        "assessment_service_result": (
            get_assessment_service_result()
        ),
        "assessment_completed": (
            is_assessment_completed()
        ),
        "enrichment": {
            **get_assessment_enrichment_status(),
            "retrieved_context": (
                get_assessment_retrieved_context()
            ),
            "ai_explanation": (
                get_assessment_ai_explanation()
            ),
            "warnings": get_assessment_warnings(),
            "errors": get_assessment_errors(),
        },
    }

    return _serialize_state_value(
        assessment_state
    )

# ============================================================
# THEME STATE
# ============================================================

THEME_LIGHT = "light"

THEME_DARK = "dark"

SUPPORTED_THEMES = (
    THEME_LIGHT,
    THEME_DARK,
)


def get_theme() -> str:
    """
    Return the currently selected EcoShield theme.
    """

    theme = str(
        st.session_state.get(
            STATE_THEME,
            THEME_DARK,
        )
    ).strip().lower()

    if theme not in SUPPORTED_THEMES:
        return THEME_DARK

    return theme


def set_theme(
    theme: str,
) -> None:
    """
    Set the EcoShield application theme.
    """

    if not isinstance(theme, str):
        raise TypeError(
            "Theme must be a string."
        )

    normalized = (
        theme.strip().lower()
    )

    if normalized not in SUPPORTED_THEMES:
        raise ValueError(
            "Theme must be either "
            "'light' or 'dark'."
        )

    st.session_state[
        STATE_THEME
    ] = normalized


def toggle_theme() -> str:
    """
    Toggle between light and dark themes.

    Returns
    -------
    str
        Newly selected theme.
    """

    current = get_theme()

    updated = (
        THEME_LIGHT
        if current == THEME_DARK
        else THEME_DARK
    )

    set_theme(
        updated
    )

    return updated
    
# ============================================================
# NAVIGATION STATE
# ============================================================

def get_current_page() -> str:
    """
    Return the currently selected EcoShield page.
    """

    return str(
        st.session_state.get(
            STATE_CURRENT_PAGE,
            "Home",
        )
    )


def set_current_page(
    page_name: str,
) -> None:
    """
    Set the currently selected EcoShield page.
    """

    if not isinstance(page_name, str):
        raise TypeError(
            "Page name must be a string."
        )

    normalized = page_name.strip()

    if not normalized:
        raise ValueError(
            "Page name cannot be empty."
        )

    st.session_state[
        STATE_CURRENT_PAGE
    ] = normalized


# ============================================================
# ASSESSMENT STEP STATE
# ============================================================

def get_assessment_step() -> int:
    """
    Return the current assessment step.
    """

    raw_step = st.session_state.get(
        STATE_ASSESSMENT_STEP,
        ASSESSMENT_FIRST_STEP,
    )

    try:
        step = int(raw_step)

    except (TypeError, ValueError):
        step = ASSESSMENT_FIRST_STEP

    return max(
        ASSESSMENT_FIRST_STEP,
        min(
            step,
            ASSESSMENT_FINAL_STEP,
        ),
    )


def set_assessment_step(
    step: int,
) -> None:
    """
    Set the active assessment step.

    Raises
    ------
    ValueError
        If the requested step is outside the assessment range.
    """

    if isinstance(step, bool) or not isinstance(step, int):
        raise TypeError(
            "Assessment step must be an integer."
        )

    if not (
        ASSESSMENT_FIRST_STEP
        <= step
        <= ASSESSMENT_FINAL_STEP
    ):
        raise ValueError(
            "Assessment step must be between "
            f"{ASSESSMENT_FIRST_STEP} and "
            f"{ASSESSMENT_FINAL_STEP}."
        )

    st.session_state[
        STATE_ASSESSMENT_STEP
    ] = step


def next_assessment_step() -> int:
    """
    Advance the assessment by one step.

    The step never exceeds the configured final step.

    Returns
    -------
    int
        Updated assessment step.
    """

    current = get_assessment_step()

    updated = min(
        current + 1,
        ASSESSMENT_FINAL_STEP,
    )

    st.session_state[
        STATE_ASSESSMENT_STEP
    ] = updated

    return updated


def previous_assessment_step() -> int:
    """
    Move the assessment back by one step.

    The step never goes below the first step.

    Returns
    -------
    int
        Updated assessment step.
    """

    current = get_assessment_step()

    updated = max(
        current - 1,
        ASSESSMENT_FIRST_STEP,
    )

    st.session_state[
        STATE_ASSESSMENT_STEP
    ] = updated

    return updated


# ============================================================
# ASSESSMENT PAYLOAD
# ============================================================

def get_assessment_payload() -> dict[str, Any]:
    """
    Return a copy of the current device assessment payload.

    A copy is returned so callers cannot accidentally mutate
    session state without using the provided update functions.
    """

    payload = st.session_state.get(
        STATE_ASSESSMENT_PAYLOAD,
        DEFAULT_ASSESSMENT_PAYLOAD,
    )

    if not isinstance(payload, Mapping):
        return _copy_default(
            DEFAULT_ASSESSMENT_PAYLOAD
        )

    return dict(payload)


def set_assessment_payload(
    payload: Mapping[str, Any],
) -> None:
    """
    Replace the complete assessment payload.

    Missing recognized fields are restored to their default
    values. Unknown field names are rejected so frontend/state
    contract mistakes are detected instead of silently ignored.
    """

    if not isinstance(payload, Mapping):
        raise TypeError(
            "Assessment payload must be a dictionary-like mapping."
        )

    unknown_fields = set(payload).difference(
        DEFAULT_ASSESSMENT_PAYLOAD
    )

    if unknown_fields:

        field_list = ", ".join(
            sorted(
                str(field)
                for field in unknown_fields
            )
        )

        raise KeyError(
            "Unknown assessment field(s): "
            f"{field_list}"
        )

    updated_payload = _copy_default(
        DEFAULT_ASSESSMENT_PAYLOAD
    )

    for field_name in DEFAULT_ASSESSMENT_PAYLOAD:

        if field_name in payload:

            updated_payload[field_name] = payload[
                field_name
            ]

    current_payload = get_assessment_payload()

    if current_payload != updated_payload:
        clear_assessment_results()

    st.session_state[
        STATE_ASSESSMENT_PAYLOAD
    ] = updated_payload


def update_assessment_payload(
    values: Mapping[str, Any],
) -> dict[str, Any]:
    """
    Update selected fields in the assessment payload.

    Unknown field names are rejected to catch programming
    mistakes between the frontend and validation layer.

    Returns
    -------
    dict[str, Any]
        Updated assessment payload.
    """

    if not isinstance(values, Mapping):
        raise TypeError(
            "Assessment values must be a dictionary-like mapping."
        )

    unknown_fields = set(values).difference(
        DEFAULT_ASSESSMENT_PAYLOAD
    )

    if unknown_fields:

        field_list = ", ".join(
            sorted(
                str(field)
                for field in unknown_fields
            )
        )

        raise KeyError(
            "Unknown assessment field(s): "
            f"{field_list}"
        )

    current_payload = get_assessment_payload()

    updated_payload = dict(
        current_payload
    )

    updated_payload.update(
        values
    )

    if updated_payload != current_payload:
        clear_assessment_results()

    st.session_state[
        STATE_ASSESSMENT_PAYLOAD
    ] = updated_payload

    return dict(
        updated_payload
    )
    
def set_assessment_field(
    field_name: str,
    value: Any,
) -> None:
    """
    Update one device-assessment field.

    Changing an input invalidates any results generated from
    the previous assessment values.
    """

    if field_name not in DEFAULT_ASSESSMENT_PAYLOAD:

        raise KeyError(
            f"Unknown assessment field: "
            f"'{field_name}'."
        )

    payload = get_assessment_payload()

    if payload.get(field_name) != value:
        clear_assessment_results()

    payload[field_name] = value

    st.session_state[
        STATE_ASSESSMENT_PAYLOAD
    ] = payload

def get_assessment_field(
    field_name: str,
    default: Any = None,
) -> Any:
    """
    Return one device-assessment field.
    """

    if field_name not in DEFAULT_ASSESSMENT_PAYLOAD:

        raise KeyError(
            f"Unknown assessment field: "
            f"'{field_name}'."
        )

    return get_assessment_payload().get(
        field_name,
        default,
    )


# ============================================================
# VALIDATION RESULT
# ============================================================

def set_validation_result(
    result: Any,
) -> None:
    """
    Store the latest validators.py result.
    """

    st.session_state[
        STATE_VALIDATION_RESULT
    ] = result


def get_validation_result() -> Any:
    """
    Return the latest validation result.
    """

    return st.session_state.get(
        STATE_VALIDATION_RESULT
    )


# ============================================================
# RISK ASSESSMENT
# ============================================================

def set_risk_assessment(
    assessment: Any,
) -> None:
    """
    Store the latest risk_engine.py assessment.
    """

    st.session_state[
        STATE_RISK_ASSESSMENT
    ] = assessment


def get_risk_assessment() -> Any:
    """
    Return the latest risk assessment.
    """

    return st.session_state.get(
        STATE_RISK_ASSESSMENT
    )


def has_risk_assessment() -> bool:
    """
    Return whether a risk assessment currently exists.
    """

    return (
        get_risk_assessment()
        is not None
    )


# ============================================================
# RECOMMENDATION RESULT
# ============================================================

def set_recommendation_result(
    result: Any,
) -> None:
    """
    Store the latest recommendation.py result.
    """

    st.session_state[
        STATE_RECOMMENDATION_RESULT
    ] = result


def get_recommendation_result() -> Any:
    """
    Return the latest recommendation result.
    """

    return st.session_state.get(
        STATE_RECOMMENDATION_RESULT
    )


def has_recommendation_result() -> bool:
    """
    Return whether a recommendation currently exists.
    """

    return (
        get_recommendation_result()
        is not None
    )

# ============================================================
# SUSTAINABILITY RESULT
# ============================================================

def set_sustainability_result(
    result: Any,
) -> None:
    """
    Store the latest deterministic sustainability impact result.

    Sustainability calculation remains the responsibility of
    src.sustainability_engine. This state layer only stores the
    completed result.
    """

    st.session_state[
        STATE_SUSTAINABILITY_RESULT
    ] = result


def get_sustainability_result() -> Any:
    """
    Return the latest sustainability impact result.
    """

    return st.session_state.get(
        STATE_SUSTAINABILITY_RESULT
    )


def has_sustainability_result() -> bool:
    """
    Return whether a sustainability impact result currently exists.
    """

    return (
        get_sustainability_result()
        is not None
    )

# ============================================================
# ASSESSMENT SERVICE RESULT
# ============================================================

def set_assessment_service_result(
    result: Any,
) -> None:
    """
    Store the complete backend assessment-service result.

    The state layer only stores the result. Validation, risk
    scoring, recommendation generation, RAG retrieval, and AI
    generation remain the responsibility of backend modules.
    """

    st.session_state[
        STATE_ASSESSMENT_SERVICE_RESULT
    ] = result


def get_assessment_service_result() -> Any:
    """
    Return the latest complete backend assessment-service result.
    """

    return st.session_state.get(
        STATE_ASSESSMENT_SERVICE_RESULT
    )


def has_assessment_service_result() -> bool:
    """
    Return whether a complete backend assessment-service result
    currently exists.
    """

    return (
        get_assessment_service_result()
        is not None
    )

# ============================================================
# ASSESSMENT COMPLETION
# ============================================================

def mark_assessment_completed(
    completed: bool = True,
) -> None:
    """
    Set assessment completion status.

    Only actual boolean values are accepted.
    """

    st.session_state[
        STATE_ASSESSMENT_COMPLETED
    ] = _require_bool(
        completed,
        field_name="completed",
    )


def is_assessment_completed() -> bool:
    """
    Return whether the current assessment has completed.
    """

    return bool(
        st.session_state.get(
            STATE_ASSESSMENT_COMPLETED,
            False,
        )
    )

# ============================================================
# ASSESSMENT ENRICHMENT STATE
# ============================================================

def set_assessment_enrichment_state(
    *,
    rag_enabled: bool = False,
    ai_enabled: bool = False,
    rag_attempted: bool = False,
    ai_attempted: bool = False,
    rag_succeeded: bool = False,
    ai_succeeded: bool = False,
    used_fallback: bool = False,
    retrieved_context: (
        list[Any] | tuple[Any, ...] | None
    ) = None,
    ai_explanation: str | None = None,
    warnings: (
        list[str] | tuple[str, ...] | None
    ) = None,
    errors: (
        list[str] | tuple[str, ...] | None
    ) = None,
) -> None:
    """
    Store assessment-specific RAG and AI enrichment state.

    These values describe optional backend enrichment only.
    They do not determine the authoritative risk score,
    readiness, or deterministic recommendations.
    """

    st.session_state[
    STATE_ASSESSMENT_RAG_ENABLED
] = _require_bool(
    rag_enabled,
    field_name="rag_enabled",
)

    st.session_state[
    STATE_ASSESSMENT_AI_ENABLED
] = _require_bool(
    ai_enabled,
    field_name="ai_enabled",
)

    st.session_state[
    STATE_ASSESSMENT_RAG_ATTEMPTED
] = _require_bool(
    rag_attempted,
    field_name="rag_attempted",
)

    st.session_state[
    STATE_ASSESSMENT_AI_ATTEMPTED
] = _require_bool(
    ai_attempted,
    field_name="ai_attempted",
)

    st.session_state[
    STATE_ASSESSMENT_RAG_SUCCEEDED
] = _require_bool(
    rag_succeeded,
    field_name="rag_succeeded",
)

    st.session_state[
    STATE_ASSESSMENT_AI_SUCCEEDED
] = _require_bool(
    ai_succeeded,
    field_name="ai_succeeded",
)

    st.session_state[
    STATE_ASSESSMENT_USED_FALLBACK
] = _require_bool(
    used_fallback,
    field_name="used_fallback",
)

    st.session_state[
        STATE_ASSESSMENT_RETRIEVED_CONTEXT
    ] = tuple(
        retrieved_context or ()
    )

    if ai_explanation is not None:
        if not isinstance(ai_explanation, str):
            raise TypeError(
                "AI explanation must be a string or None."
            )

        normalized_explanation = (
            ai_explanation.strip()
        )

        ai_explanation = (
            normalized_explanation
            if normalized_explanation
            else None
        )

    st.session_state[
        STATE_ASSESSMENT_AI_EXPLANATION
    ] = ai_explanation

    st.session_state[
        STATE_ASSESSMENT_WARNINGS
    ] = tuple(
        warnings or ()
    )

    st.session_state[
        STATE_ASSESSMENT_ERRORS
    ] = tuple(
        errors or ()
    )


def get_assessment_retrieved_context() -> tuple[Any, ...]:
    """
    Return assessment-specific retrieved evidence/context.
    """

    value = st.session_state.get(
        STATE_ASSESSMENT_RETRIEVED_CONTEXT,
        (),
    )

    if not isinstance(
        value,
        (list, tuple),
    ):
        return ()

    return tuple(value)


def get_assessment_ai_explanation() -> str | None:
    """
    Return the assessment-specific AI explanation.
    """

    value = st.session_state.get(
        STATE_ASSESSMENT_AI_EXPLANATION
    )

    if value is None:
        return None

    return str(value)


def get_assessment_warnings() -> tuple[str, ...]:
    """
    Return warnings produced by assessment orchestration.
    """

    value = st.session_state.get(
        STATE_ASSESSMENT_WARNINGS,
        (),
    )

    if not isinstance(
        value,
        (list, tuple),
    ):
        return ()

    return tuple(
        str(item)
        for item in value
    )


def get_assessment_errors() -> tuple[str, ...]:
    """
    Return non-fatal orchestration error codes/messages.
    """

    value = st.session_state.get(
        STATE_ASSESSMENT_ERRORS,
        (),
    )

    if not isinstance(
        value,
        (list, tuple),
    ):
        return ()

    return tuple(
        str(item)
        for item in value
    )


def get_assessment_enrichment_status() -> dict[str, bool]:
    """
    Return assessment RAG/AI execution status.
    """

    return {
        "rag_enabled": bool(
            st.session_state.get(
                STATE_ASSESSMENT_RAG_ENABLED,
                False,
            )
        ),
        "ai_enabled": bool(
            st.session_state.get(
                STATE_ASSESSMENT_AI_ENABLED,
                False,
            )
        ),
        "rag_attempted": bool(
            st.session_state.get(
                STATE_ASSESSMENT_RAG_ATTEMPTED,
                False,
            )
        ),
        "ai_attempted": bool(
            st.session_state.get(
                STATE_ASSESSMENT_AI_ATTEMPTED,
                False,
            )
        ),
        "rag_succeeded": bool(
            st.session_state.get(
                STATE_ASSESSMENT_RAG_SUCCEEDED,
                False,
            )
        ),
        "ai_succeeded": bool(
            st.session_state.get(
                STATE_ASSESSMENT_AI_SUCCEEDED,
                False,
            )
        ),
        "used_fallback": bool(
            st.session_state.get(
                STATE_ASSESSMENT_USED_FALLBACK,
                False,
            )
        ),
    }


def clear_assessment_enrichment_state() -> None:
    """
    Clear assessment-specific RAG/AI enrichment state.
    """

    st.session_state[
        STATE_ASSESSMENT_RAG_ENABLED
    ] = False

    st.session_state[
        STATE_ASSESSMENT_AI_ENABLED
    ] = False

    st.session_state[
        STATE_ASSESSMENT_RAG_ATTEMPTED
    ] = False

    st.session_state[
        STATE_ASSESSMENT_AI_ATTEMPTED
    ] = False

    st.session_state[
        STATE_ASSESSMENT_RAG_SUCCEEDED
    ] = False

    st.session_state[
        STATE_ASSESSMENT_AI_SUCCEEDED
    ] = False

    st.session_state[
        STATE_ASSESSMENT_USED_FALLBACK
    ] = False

    st.session_state[
        STATE_ASSESSMENT_RETRIEVED_CONTEXT
    ] = ()

    st.session_state[
        STATE_ASSESSMENT_AI_EXPLANATION
    ] = None

    st.session_state[
        STATE_ASSESSMENT_WARNINGS
    ] = ()

    st.session_state[
        STATE_ASSESSMENT_ERRORS
    ] = ()


# ============================================================
# RAG STATE
# ============================================================

def set_rag_context(
    context: Any,
    sources: list[Any] | tuple[Any, ...] | None = None,
) -> None:
    """
    Store retrieved RAG context and optional source metadata.

    Source metadata must be supplied as a list, tuple, or None.
    """

    if (
        sources is not None
        and not isinstance(
            sources,
            (list, tuple),
        )
    ):
        raise TypeError(
            "RAG sources must be a list, tuple, or None."
        )

    st.session_state[
        STATE_RAG_CONTEXT
    ] = context

    if sources is not None:

        st.session_state[
            STATE_RAG_SOURCES
        ] = list(sources)


def get_rag_context() -> Any:
    """
    Return the latest retrieved RAG context.
    """

    return st.session_state.get(
        STATE_RAG_CONTEXT
    )


def get_rag_sources() -> list[Any]:
    """
    Return a copy of current RAG source metadata.
    """

    sources = st.session_state.get(
        STATE_RAG_SOURCES,
        [],
    )

    if not isinstance(
        sources,
        (list, tuple),
    ):
        return []

    return list(sources)


def clear_rag_state() -> None:
    """
    Clear all retrieved RAG information.
    """

    st.session_state[
        STATE_RAG_CONTEXT
    ] = None

    st.session_state[
        STATE_RAG_SOURCES
    ] = []


# ============================================================
# AI / KNOWLEDGE CENTER STATE
# ============================================================

def set_ai_response(
    response: Any,
) -> None:
    """
    Store the latest LLM response.
    """

    st.session_state[
        STATE_AI_RESPONSE
    ] = response


def get_ai_response() -> Any:
    """
    Return the latest LLM response.
    """

    return st.session_state.get(
        STATE_AI_RESPONSE
    )


def set_last_question(
    question: str | None,
) -> None:
    """
    Store the latest Knowledge Center / AI question.
    """

    if question is None:

        st.session_state[
            STATE_LAST_QUESTION
        ] = None

        return

    if not isinstance(question, str):
        raise TypeError(
            "Question must be a string or None."
        )

    normalized = question.strip()

    st.session_state[
        STATE_LAST_QUESTION
    ] = (
        normalized
        if normalized
        else None
    )


def get_last_question() -> str | None:
    """
    Return the most recent AI question.
    """

    value = st.session_state.get(
        STATE_LAST_QUESTION
    )

    if value is None:
        return None

    return str(value)

def set_advisor_result(
    *,
    question: str,
    result: Any,
) -> None:
    """
    Store the latest EcoShield Advisor interaction using the
    existing centralized Knowledge Center / RAG / AI state.

    This helper performs state synchronization only.
    It does not execute retrieval, LLM generation, risk scoring,
    recommendation generation, or Advisor orchestration.
    """

    if not isinstance(question, str):
        raise TypeError(
            "Advisor question must be a string."
        )

    normalized_question = question.strip()

    if not normalized_question:
        raise ValueError(
            "Advisor question cannot be empty."
        )

    if result is None:
        raise ValueError(
            "Advisor result cannot be None."
        )

    # Store the normalized question.
    set_last_question(
        normalized_question
    )

    # Store the complete AdvisorResult object.
    set_ai_response(
        result
    )

    # Store retrieval context and source metadata when available.
    retrieval = getattr(
        result,
        "retrieval",
        None,
    )

    if retrieval is None:
        clear_rag_state()
        return

    evidence = getattr(
        retrieval,
        "evidence",
        (),
    )

    sources: list[str] = []

    for item in evidence:
        source_name = getattr(
            item,
            "source_name",
            None,
        )

        if (
            isinstance(source_name, str)
            and source_name.strip()
            and source_name not in sources
        ):
            sources.append(
                source_name
            )

    set_rag_context(
        retrieval,
        sources=sources,
    )

def get_advisor_result() -> Any:
    """
    Return the latest stored EcoShield Advisor result.

    Advisor results reuse the existing centralized AI-response
    state rather than introducing a duplicate session-state key.
    """

    return get_ai_response()  

def clear_advisor_state() -> None:
    """
    Clear the latest EcoShield Advisor interaction.

    Existing centralized Knowledge Center / RAG / AI state is
    reused so no duplicate Advisor-specific session keys exist.
    """

    set_last_question(
        None
    )

    set_ai_response(
        None
    )

    clear_rag_state()  

def set_knowledge_query(
    query: str,
) -> None:
    """
    Store the current Knowledge Center search query.
    """

    if not isinstance(query, str):
        raise TypeError(
            "Knowledge query must be a string."
        )

    st.session_state[
        STATE_KNOWLEDGE_QUERY
    ] = query.strip()


def get_knowledge_query() -> str:
    """
    Return the current Knowledge Center search query.
    """

    return str(
        st.session_state.get(
            STATE_KNOWLEDGE_QUERY,
            "",
        )
    )


# ============================================================
# FLASH MESSAGE STATE
# ============================================================

def set_error_message(
    message: str | None,
) -> None:
    """
    Store a temporary application error message.
    """

    st.session_state[
        STATE_ERROR_MESSAGE
    ] = (
        message.strip()
        if isinstance(message, str)
        and message.strip()
        else None
    )


def pop_error_message() -> str | None:
    """
    Return and clear the current error message.
    """

    return st.session_state.pop(
        STATE_ERROR_MESSAGE,
        None,
    )


def set_success_message(
    message: str | None,
) -> None:
    """
    Store a temporary application success message.
    """

    st.session_state[
        STATE_SUCCESS_MESSAGE
    ] = (
        message.strip()
        if isinstance(message, str)
        and message.strip()
        else None
    )


def pop_success_message() -> str | None:
    """
    Return and clear the current success message.
    """

    return st.session_state.pop(
        STATE_SUCCESS_MESSAGE,
        None,
    )


# ============================================================
# CLEAR GENERATED RESULTS
# ============================================================

def clear_assessment_results() -> None:
    """
    Clear results derived from the current assessment.

    Device form values and assessment step are preserved.

    Use this when the user edits assessment inputs after a
    previous analysis.
    """

    st.session_state[
        STATE_VALIDATION_RESULT
    ] = None

    st.session_state[
    STATE_RISK_ASSESSMENT
    ] = None

    st.session_state[
    STATE_RECOMMENDATION_RESULT
     ] = None

    st.session_state[
    STATE_SUSTAINABILITY_RESULT
    ] = None

    st.session_state[
    STATE_ASSESSMENT_SERVICE_RESULT
    ] = None

    st.session_state[
    STATE_ASSESSMENT_COMPLETED
    ] = False

    clear_assessment_enrichment_state()


# ============================================================
# RESET ASSESSMENT
# ============================================================

def reset_assessment() -> None:
    """
    Reset the complete device-assessment workflow.

    Application-level navigation and Knowledge Center state
    are preserved.
    """

    st.session_state[
        STATE_ASSESSMENT_STEP
    ] = ASSESSMENT_FIRST_STEP

    st.session_state[
        STATE_ASSESSMENT_PAYLOAD
    ] = _copy_default(
        DEFAULT_ASSESSMENT_PAYLOAD
    )

    clear_assessment_results()

    st.session_state[
        STATE_ERROR_MESSAGE
    ] = None

    st.session_state[
        STATE_SUCCESS_MESSAGE
    ] = None
# ============================================================
# RESET AI / KNOWLEDGE WORKFLOW
# ============================================================

def reset_knowledge_state() -> None:
    """
    Clear Knowledge Center and standalone AI interaction state.
    """

    st.session_state[
        STATE_KNOWLEDGE_QUERY
    ] = ""

    st.session_state[
        STATE_LAST_QUESTION
    ] = None

    st.session_state[
        STATE_AI_RESPONSE
    ] = None

    clear_rag_state()


# ============================================================
# COMPLETE APPLICATION RESET
# ============================================================

def reset_application_state() -> None:
    """
    Reset all EcoShield-owned state to application defaults.

    Streamlit state belonging to unrelated widgets/components
    is not deliberately removed.
    """

    for key, default_value in DEFAULT_SESSION_STATE.items():

        st.session_state[key] = _copy_default(
            default_value
        )

    st.session_state[
        STATE_INITIALIZED
    ] = True