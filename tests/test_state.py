"""
EcoShield AI
Application State Tests

Tests Streamlit session-state initialization, assessment
workflow state, reset boundaries, enrichment state,
defensive validation, and serialization.

The real Streamlit runtime is not required. Tests replace
st.session_state with an isolated dictionary.
"""

from __future__ import annotations

from dataclasses import dataclass

import pytest

import ui.state as state


@pytest.fixture
def isolated_session_state(monkeypatch):
    """
    Replace Streamlit session state with an isolated in-memory
    dictionary for deterministic testing.
    """

    session_state = {}

    monkeypatch.setattr(
        state.st,
        "session_state",
        session_state,
    )

    return session_state


@pytest.fixture
def initialized_state(isolated_session_state):
    state.initialize_session_state()

    return isolated_session_state


def test_default_assessment_payload_has_17_fields():
    assert len(
        state.DEFAULT_ASSESSMENT_PAYLOAD
    ) == 17


def test_default_session_state_has_28_keys():
    assert len(
        state.DEFAULT_SESSION_STATE
    ) == 28


def test_initialize_session_state_creates_all_defaults(
    isolated_session_state,
):
    state.initialize_session_state()

    for key in state.DEFAULT_SESSION_STATE:
        assert key in isolated_session_state

    assert (
        isolated_session_state[
            state.STATE_INITIALIZED
        ]
        is True
    )


def test_initialize_session_state_uses_independent_mutable_defaults(
    isolated_session_state,
):
    state.initialize_session_state()

    stored_payload = isolated_session_state[
        state.STATE_ASSESSMENT_PAYLOAD
    ]

    stored_sources = isolated_session_state[
        state.STATE_RAG_SOURCES
    ]

    assert (
        stored_payload
        is not state.DEFAULT_ASSESSMENT_PAYLOAD
    )

    assert (
        stored_sources
        is not state.DEFAULT_SESSION_STATE[
            state.STATE_RAG_SOURCES
        ]
    )


def test_initialize_session_state_preserves_valid_existing_values(
    isolated_session_state,
):
    isolated_session_state[
        state.STATE_THEME
    ] = "light"

    isolated_session_state[
        state.STATE_ASSESSMENT_STEP
    ] = 3

    state.initialize_session_state()

    assert (
        isolated_session_state[
            state.STATE_THEME
        ]
        == "light"
    )

    assert (
        isolated_session_state[
            state.STATE_ASSESSMENT_STEP
        ]
        == 3
    )


@pytest.mark.parametrize(
    ("raw_step", "expected"),
    (
        (True, state.ASSESSMENT_FIRST_STEP),
        ("invalid", state.ASSESSMENT_FIRST_STEP),
        (-100, state.ASSESSMENT_FIRST_STEP),
        (100, state.ASSESSMENT_FINAL_STEP),
        ("3", 3),
    ),
)
def test_state_initialization_repairs_assessment_step(
    isolated_session_state,
    raw_step,
    expected,
):
    isolated_session_state[
        state.STATE_ASSESSMENT_STEP
    ] = raw_step

    state.initialize_session_state()

    assert (
        isolated_session_state[
            state.STATE_ASSESSMENT_STEP
        ]
        == expected
    )


def test_state_initialization_repairs_assessment_payload(
    isolated_session_state,
):
    isolated_session_state[
        state.STATE_ASSESSMENT_PAYLOAD
    ] = {
        "device_type": "Laptop",
        "unknown_field": "remove-me",
    }

    state.initialize_session_state()

    payload = isolated_session_state[
        state.STATE_ASSESSMENT_PAYLOAD
    ]

    assert len(payload) == 17
    assert payload["device_type"] == "Laptop"
    assert "unknown_field" not in payload

    assert (
        payload["operating_system"]
        is None
    )


def test_state_initialization_repairs_invalid_boolean_state(
    isolated_session_state,
):
    isolated_session_state[
        state.STATE_ASSESSMENT_COMPLETED
    ] = "False"

    isolated_session_state[
        state.STATE_ASSESSMENT_AI_ENABLED
    ] = 1

    state.initialize_session_state()

    assert (
        isolated_session_state[
            state.STATE_ASSESSMENT_COMPLETED
        ]
        is False
    )

    assert (
        isolated_session_state[
            state.STATE_ASSESSMENT_AI_ENABLED
        ]
        is False
    )


def test_state_initialization_repairs_tuple_state(
    isolated_session_state,
):
    isolated_session_state[
        state.STATE_ASSESSMENT_WARNINGS
    ] = ["warning-1", "warning-2"]

    isolated_session_state[
        state.STATE_ASSESSMENT_ERRORS
    ] = "invalid"

    state.initialize_session_state()

    assert (
        isolated_session_state[
            state.STATE_ASSESSMENT_WARNINGS
        ]
        == ("warning-1", "warning-2")
    )

    assert (
        isolated_session_state[
            state.STATE_ASSESSMENT_ERRORS
        ]
        == ()
    )


def test_state_initialization_repairs_generic_rag_sources(
    isolated_session_state,
):
    isolated_session_state[
        state.STATE_RAG_SOURCES
    ] = ("source-a", "source-b")

    state.initialize_session_state()

    assert (
        isolated_session_state[
            state.STATE_RAG_SOURCES
        ]
        == ["source-a", "source-b"]
    )


def test_state_initialization_repairs_invalid_knowledge_query(
    isolated_session_state,
):
    isolated_session_state[
        state.STATE_KNOWLEDGE_QUERY
    ] = 123

    state.initialize_session_state()

    assert (
        isolated_session_state[
            state.STATE_KNOWLEDGE_QUERY
        ]
        == ""
    )


def test_require_bool_accepts_actual_booleans():
    assert (
        state._require_bool(
            True,
            field_name="test",
        )
        is True
    )

    assert (
        state._require_bool(
            False,
            field_name="test",
        )
        is False
    )


@pytest.mark.parametrize(
    "value",
    (
        "True",
        "False",
        1,
        0,
        None,
        [],
        {},
    ),
)
def test_require_bool_rejects_non_boolean_values(value):
    with pytest.raises(TypeError):
        state._require_bool(
            value,
            field_name="test",
        )


def test_assessment_step_navigation_stays_within_bounds(
    initialized_state,
):
    state.set_assessment_step(
        state.ASSESSMENT_FIRST_STEP
    )

    assert (
        state.previous_assessment_step()
        == state.ASSESSMENT_FIRST_STEP
    )

    state.set_assessment_step(
        state.ASSESSMENT_FINAL_STEP
    )

    assert (
        state.next_assessment_step()
        == state.ASSESSMENT_FINAL_STEP
    )


def test_set_assessment_step_rejects_boolean(
    initialized_state,
):
    with pytest.raises(TypeError):
        state.set_assessment_step(True)


def test_set_assessment_step_rejects_out_of_range(
    initialized_state,
):
    with pytest.raises(ValueError):
        state.set_assessment_step(0)

    with pytest.raises(ValueError):
        state.set_assessment_step(
            state.ASSESSMENT_FINAL_STEP + 1
        )


def test_set_assessment_payload_rejects_unknown_fields(
    initialized_state,
):
    with pytest.raises(KeyError):
        state.set_assessment_payload(
            {
                "device_type": "Laptop",
                "unknown_field": "invalid",
            }
        )


def test_update_assessment_payload_rejects_unknown_fields(
    initialized_state,
):
    with pytest.raises(KeyError):
        state.update_assessment_payload(
            {
                "unknown_field": "invalid",
            }
        )


def test_set_assessment_field_rejects_unknown_field(
    initialized_state,
):
    with pytest.raises(KeyError):
        state.set_assessment_field(
            "unknown_field",
            "invalid",
        )


def test_assessment_input_change_invalidates_generated_results(
    initialized_state,
):
    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    risk = object()
    recommendation = object()
    service_result = object()

    state.set_validation_result(
        {"valid": True}
    )

    state.set_risk_assessment(risk)

    state.set_recommendation_result(
        recommendation
    )

    state.set_assessment_service_result(
        service_result
    )

    state.mark_assessment_completed(True)

    state.set_assessment_enrichment_state(
        rag_enabled=True,
        ai_enabled=True,
        rag_attempted=True,
        ai_attempted=True,
        rag_succeeded=True,
        ai_succeeded=True,
        retrieved_context=("evidence",),
        ai_explanation="Explanation",
    )

    state.set_assessment_field(
        "device_type",
        "Desktop",
    )

    assert (
        state.get_validation_result()
        is None
    )

    assert (
        state.get_risk_assessment()
        is None
    )

    assert (
        state.get_recommendation_result()
        is None
    )

    assert (
        state.get_assessment_service_result()
        is None
    )

    assert (
        state.is_assessment_completed()
        is False
    )

    status = (
        state.get_assessment_enrichment_status()
    )

    assert status["rag_enabled"] is False
    assert status["ai_enabled"] is False
    assert status["rag_attempted"] is False
    assert status["ai_attempted"] is False
    assert status["rag_succeeded"] is False
    assert status["ai_succeeded"] is False
    assert status["used_fallback"] is False

    assert (
        state.get_assessment_retrieved_context()
        == ()
    )

    assert (
        state.get_assessment_ai_explanation()
        is None
    )


def test_same_assessment_field_value_preserves_generated_results(
    initialized_state,
):
    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    risk = object()

    state.set_risk_assessment(risk)
    state.mark_assessment_completed(True)

    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    assert (
        state.get_risk_assessment()
        is risk
    )

    assert (
        state.is_assessment_completed()
        is True
    )


def test_partial_payload_change_invalidates_results(
    initialized_state,
):
    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    risk = object()

    state.set_risk_assessment(risk)
    state.mark_assessment_completed(True)

    state.update_assessment_payload(
        {
            "operating_system": "Windows",
        }
    )

    assert (
        state.get_risk_assessment()
        is None
    )

    assert (
        state.is_assessment_completed()
        is False
    )


def test_same_partial_payload_values_preserve_results(
    initialized_state,
):
    state.update_assessment_payload(
        {
            "device_type": "Laptop",
            "operating_system": "Windows",
        }
    )

    risk = object()

    state.set_risk_assessment(risk)
    state.mark_assessment_completed(True)

    state.update_assessment_payload(
        {
            "device_type": "Laptop",
            "operating_system": "Windows",
        }
    )

    assert (
        state.get_risk_assessment()
        is risk
    )

    assert (
        state.is_assessment_completed()
        is True
    )


def test_complete_payload_change_invalidates_results(
    initialized_state,
):
    payload = state.get_assessment_payload()

    payload["device_type"] = "Laptop"

    state.set_assessment_payload(payload)

    risk = object()

    state.set_risk_assessment(risk)
    state.mark_assessment_completed(True)

    updated_payload = (
        state.get_assessment_payload()
    )

    updated_payload[
        "operating_system"
    ] = "Windows"

    state.set_assessment_payload(
        updated_payload
    )

    assert (
        state.get_risk_assessment()
        is None
    )

    assert (
        state.is_assessment_completed()
        is False
    )


def test_same_complete_payload_preserves_results(
    initialized_state,
):
    payload = state.get_assessment_payload()

    payload["device_type"] = "Laptop"

    state.set_assessment_payload(payload)

    risk = object()

    state.set_risk_assessment(risk)
    state.mark_assessment_completed(True)

    state.set_assessment_payload(
        state.get_assessment_payload()
    )

    assert (
        state.get_risk_assessment()
        is risk
    )

    assert (
        state.is_assessment_completed()
        is True
    )


def test_mark_assessment_completed_requires_boolean(
    initialized_state,
):
    state.mark_assessment_completed(True)

    assert (
        state.is_assessment_completed()
        is True
    )

    state.mark_assessment_completed(False)

    assert (
        state.is_assessment_completed()
        is False
    )

    with pytest.raises(TypeError):
        state.mark_assessment_completed(
            "False"
        )


@pytest.mark.parametrize(
    "field_name",
    (
        "rag_enabled",
        "ai_enabled",
        "rag_attempted",
        "ai_attempted",
        "rag_succeeded",
        "ai_succeeded",
        "used_fallback",
    ),
)
def test_enrichment_flags_require_actual_booleans(
    initialized_state,
    field_name,
):
    arguments = {
        "rag_enabled": False,
        "ai_enabled": False,
        "rag_attempted": False,
        "ai_attempted": False,
        "rag_succeeded": False,
        "ai_succeeded": False,
        "used_fallback": False,
    }

    arguments[field_name] = "False"

    with pytest.raises(TypeError):
        state.set_assessment_enrichment_state(
            **arguments
        )


def test_set_assessment_enrichment_state_round_trip(
    initialized_state,
):
    state.set_assessment_enrichment_state(
        rag_enabled=True,
        ai_enabled=True,
        rag_attempted=True,
        ai_attempted=True,
        rag_succeeded=True,
        ai_succeeded=False,
        used_fallback=True,
        retrieved_context=(
            "source-a",
            "source-b",
        ),
        ai_explanation="  Explanation  ",
        warnings=("warning",),
        errors=("error",),
    )

    status = (
        state.get_assessment_enrichment_status()
    )

    assert status == {
        "rag_enabled": True,
        "ai_enabled": True,
        "rag_attempted": True,
        "ai_attempted": True,
        "rag_succeeded": True,
        "ai_succeeded": False,
        "used_fallback": True,
    }

    assert (
        state.get_assessment_retrieved_context()
        == (
            "source-a",
            "source-b",
        )
    )

    assert (
        state.get_assessment_ai_explanation()
        == "Explanation"
    )

    assert (
        state.get_assessment_warnings()
        == ("warning",)
    )

    assert (
        state.get_assessment_errors()
        == ("error",)
    )


def test_ai_explanation_rejects_non_string(
    initialized_state,
):
    with pytest.raises(TypeError):
        state.set_assessment_enrichment_state(
            ai_explanation=123
        )


def test_rag_context_accepts_list_and_tuple_sources(
    initialized_state,
):
    state.set_rag_context(
        {"query": "erase"},
        sources=("a", "b"),
    )

    assert (
        state.get_rag_context()
        == {"query": "erase"}
    )

    assert (
        state.get_rag_sources()
        == ["a", "b"]
    )


@pytest.mark.parametrize(
    "invalid_sources",
    (
        "source.md",
        123,
        {"source": "x"},
    ),
)
def test_rag_context_rejects_invalid_source_container(
    initialized_state,
    invalid_sources,
):
    with pytest.raises(TypeError):
        state.set_rag_context(
            {},
            sources=invalid_sources,
        )


def test_clear_assessment_results_preserves_payload_and_step(
    initialized_state,
):
    state.set_assessment_step(3)

    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    state.set_risk_assessment(object())

    state.set_recommendation_result(
        object()
    )

    state.mark_assessment_completed(True)

    state.clear_assessment_results()

    assert (
        state.get_assessment_step()
        == 3
    )

    assert (
        state.get_assessment_field(
            "device_type"
        )
        == "Laptop"
    )

    assert (
        state.get_risk_assessment()
        is None
    )

    assert (
        state.get_recommendation_result()
        is None
    )

    assert (
        state.is_assessment_completed()
        is False
    )


def test_reset_assessment_preserves_navigation_theme_and_knowledge(
    initialized_state,
):
    state.set_theme("light")
    state.set_current_page("Knowledge Center")

    state.set_knowledge_query(
        "secure erase"
    )

    state.set_rag_context(
        {"query": "secure erase"},
        sources=["source-a"],
    )

    state.set_ai_response(
        {"text": "Knowledge response"}
    )

    state.set_assessment_step(4)

    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    state.set_risk_assessment(object())
    state.mark_assessment_completed(True)

    state.set_error_message("Error")
    state.set_success_message("Success")

    state.reset_assessment()

    assert state.get_theme() == "light"

    assert (
        state.get_current_page()
        == "Knowledge Center"
    )

    assert (
        state.get_knowledge_query()
        == "secure erase"
    )

    assert (
        state.get_rag_context()
        == {"query": "secure erase"}
    )

    assert (
        state.get_ai_response()
        == {"text": "Knowledge response"}
    )

    assert (
        state.get_assessment_step()
        == state.ASSESSMENT_FIRST_STEP
    )

    assert (
        state.get_assessment_payload()
        == state.DEFAULT_ASSESSMENT_PAYLOAD
    )

    assert (
        state.get_risk_assessment()
        is None
    )

    assert (
        state.is_assessment_completed()
        is False
    )

    assert (
        initialized_state[
            state.STATE_ERROR_MESSAGE
        ]
        is None
    )

    assert (
        initialized_state[
            state.STATE_SUCCESS_MESSAGE
        ]
        is None
    )


def test_reset_knowledge_state_preserves_assessment(
    initialized_state,
):
    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    risk = object()

    state.set_risk_assessment(risk)
    state.mark_assessment_completed(True)

    state.set_knowledge_query(
        "recycling"
    )

    state.set_last_question(
        "Where can I recycle?"
    )

    state.set_rag_context(
        {"query": "recycling"},
        sources=["source"],
    )

    state.set_ai_response(
        {"text": "answer"}
    )

    state.reset_knowledge_state()

    assert (
        state.get_assessment_field(
            "device_type"
        )
        == "Laptop"
    )

    assert (
        state.get_risk_assessment()
        is risk
    )

    assert (
        state.is_assessment_completed()
        is True
    )

    assert state.get_knowledge_query() == ""
    assert state.get_last_question() is None
    assert state.get_rag_context() is None
    assert state.get_rag_sources() == []
    assert state.get_ai_response() is None


def test_reset_application_state_resets_owned_keys_only(
    initialized_state,
):
    initialized_state[
        "unrelated_widget_key"
    ] = "keep-me"

    state.set_theme("light")

    state.set_current_page(
        "Knowledge Center"
    )

    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    state.mark_assessment_completed(True)

    state.reset_application_state()

    for (
        key,
        default_value,
    ) in state.DEFAULT_SESSION_STATE.items():

        assert (
            initialized_state[key]
            == default_value
        )

    assert (
        initialized_state[
            "unrelated_widget_key"
        ]
        == "keep-me"
    )

    assert (
        initialized_state[
            state.STATE_INITIALIZED
        ]
        is True
    )


def test_theme_validation(
    initialized_state,
):
    state.set_theme(" LIGHT ")

    assert state.get_theme() == "light"

    with pytest.raises(ValueError):
        state.set_theme("blue")

    with pytest.raises(TypeError):
        state.set_theme(123)


def test_current_page_rejects_invalid_values(
    initialized_state,
):
    state.set_current_page(
        " Device Assessment "
    )

    assert (
        state.get_current_page()
        == "Device Assessment"
    )

    with pytest.raises(ValueError):
        state.set_current_page("   ")

    with pytest.raises(TypeError):
        state.set_current_page(123)


def test_flash_messages_are_pop_once(
    initialized_state,
):
    state.set_error_message(
        "  Something failed  "
    )

    state.set_success_message(
        "  Completed  "
    )

    assert (
        state.pop_error_message()
        == "Something failed"
    )

    assert (
        state.pop_error_message()
        is None
    )

    assert (
        state.pop_success_message()
        == "Completed"
    )

    assert (
        state.pop_success_message()
        is None
    )


def test_serialize_state_value_handles_nested_containers():
    value = {
        "tuple": (1, 2),
        "list": [True, None],
        "mapping": {
            "name": "EcoShield"
        },
    }

    serialized = (
        state._serialize_state_value(value)
    )

    assert serialized == {
        "tuple": [1, 2],
        "list": [True, None],
        "mapping": {
            "name": "EcoShield"
        },
    }


@dataclass
class FakeDomainObject:
    score: int

    def to_dict(self):
        return {
            "score": self.score,
            "actions": (
                "erase",
                "sign-out",
            ),
        }


def test_serialize_state_value_uses_to_dict():
    serialized = state._serialize_state_value(
        FakeDomainObject(score=73)
    )

    assert serialized == {
        "score": 73,
        "actions": [
            "erase",
            "sign-out",
        ],
    }


class BrokenDomainObject:
    def to_dict(self):
        raise RuntimeError("broken")

    def __str__(self):
        return "safe-fallback"


def test_serialize_state_value_handles_broken_to_dict():
    assert (
        state._serialize_state_value(
            BrokenDomainObject()
        )
        == "safe-fallback"
    )


def test_serialize_application_state_exports_only_owned_keys(
    initialized_state,
):
    initialized_state[
        "unrelated_widget_key"
    ] = "private-widget-state"

    serialized = (
        state.serialize_application_state()
    )

    assert (
        set(serialized)
        == set(state.DEFAULT_SESSION_STATE)
    )

    assert (
        "unrelated_widget_key"
        not in serialized
    )


def test_serialize_assessment_state_excludes_unrelated_state(
    initialized_state,
):
    state.set_theme("light")

    state.set_current_page(
        "Knowledge Center"
    )

    state.set_knowledge_query(
        "recycle laptop"
    )

    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    serialized = (
        state.serialize_assessment_state()
    )

    assert "assessment_step" in serialized

    assert (
        "assessment_payload"
        in serialized
    )

    assert (
        "assessment_completed"
        in serialized
    )

    assert "enrichment" in serialized

    assert "theme" not in serialized
    assert "current_page" not in serialized
    assert "knowledge_query" not in serialized


def test_assessment_payload_getter_returns_copy(
    initialized_state,
):
    state.set_assessment_field(
        "device_type",
        "Laptop",
    )

    payload = state.get_assessment_payload()

    payload["device_type"] = "Desktop"

    assert (
        state.get_assessment_field(
            "device_type"
        )
        == "Laptop"
    )


def test_rag_sources_getter_returns_copy(
    initialized_state,
):
    state.set_rag_context(
        {},
        sources=["source-a"],
    )

    sources = state.get_rag_sources()

    sources.append("source-b")

    assert (
        state.get_rag_sources()
        == ["source-a"]
    )