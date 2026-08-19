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

STATE_INITIALIZED = "_ecoshield_state_initialized"

STATE_CURRENT_PAGE = "current_page"

STATE_ASSESSMENT_STEP = "assessment_step"

STATE_ASSESSMENT_PAYLOAD = "assessment_payload"

STATE_VALIDATION_RESULT = "validation_result"

STATE_RISK_ASSESSMENT = "risk_assessment"

STATE_RECOMMENDATION_RESULT = "recommendation_result"

STATE_ASSESSMENT_COMPLETED = "assessment_completed"

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
    STATE_CURRENT_PAGE: "Home",
    STATE_ASSESSMENT_STEP: ASSESSMENT_FIRST_STEP,
    STATE_ASSESSMENT_PAYLOAD: DEFAULT_ASSESSMENT_PAYLOAD,
    STATE_VALIDATION_RESULT: None,
    STATE_RISK_ASSESSMENT: None,
    STATE_RECOMMENDATION_RESULT: None,
    STATE_ASSESSMENT_COMPLETED: False,
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
# SESSION STATE INITIALIZATION
# ============================================================

def initialize_session_state() -> None:
    """
    Initialize all EcoShield session-state values.

    Existing state is preserved.

    This function is safe to call on every Streamlit rerun.
    """

    for key, default_value in DEFAULT_SESSION_STATE.items():

        if key not in st.session_state:

            st.session_state[key] = _copy_default(
                default_value
            )

    st.session_state[STATE_INITIALIZED] = True


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

    Only recognized EcoShield device-assessment fields are stored.
    Unknown fields are ignored.
    """

    if not isinstance(payload, Mapping):
        raise TypeError(
            "Assessment payload must be a dictionary-like mapping."
        )

    updated_payload = _copy_default(
        DEFAULT_ASSESSMENT_PAYLOAD
    )

    for field_name in DEFAULT_ASSESSMENT_PAYLOAD:

        if field_name in payload:

            updated_payload[field_name] = payload[
                field_name
            ]

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

    payload = get_assessment_payload()

    payload.update(
        values
    )

    st.session_state[
        STATE_ASSESSMENT_PAYLOAD
    ] = payload

    return dict(payload)


def set_assessment_field(
    field_name: str,
    value: Any,
) -> None:
    """
    Update one device-assessment field.
    """

    if field_name not in DEFAULT_ASSESSMENT_PAYLOAD:

        raise KeyError(
            f"Unknown assessment field: "
            f"'{field_name}'."
        )

    payload = get_assessment_payload()

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
# ASSESSMENT COMPLETION
# ============================================================

def mark_assessment_completed(
    completed: bool = True,
) -> None:
    """
    Set assessment completion status.
    """

    st.session_state[
        STATE_ASSESSMENT_COMPLETED
    ] = bool(completed)


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
# RAG STATE
# ============================================================

def set_rag_context(
    context: Any,
    sources: list[Any] | tuple[Any, ...] | None = None,
) -> None:
    """
    Store retrieved RAG context and optional source metadata.

    This function is intentionally generic so the future
    retriever can return structured document/chunk objects.
    """

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
        STATE_ASSESSMENT_COMPLETED
    ] = False

    clear_rag_state()

    st.session_state[
        STATE_AI_RESPONSE
    ] = None


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