"""
EcoShield AI
Frontend / Backend Integration Tests

These tests protect the permanent integration boundary between
the Streamlit frontend and EcoShield's frozen backend service.

Covered contracts:
- runtime mode mapping
- service configuration mapping
- optional RAG / AI dependency construction
- successful result synchronization
- exactly-once backend execution
- frontend-safe validation failure handling
- frontend-safe setup failure handling
- unexpected backend failure handling
- deterministic fallback preservation
- user-query forwarding

No real RAG retrieval, LLM network request, or Streamlit
navigation is executed by this test module.
"""

from __future__ import annotations

from types import SimpleNamespace
from unittest.mock import Mock

import pytest

from config.config import RuntimeConfig

import src.services.frontend_integration as integration


# ============================================================
# RUNTIME CONFIGURATION HELPERS
# ============================================================


def _runtime_config(
    mode: str = "deterministic",
) -> RuntimeConfig:
    """
    Build a valid runtime configuration for integration tests.
    """

    return RuntimeConfig(
        assessment_mode=mode,
    )


# ============================================================
# SERVICE CONFIGURATION
# ============================================================


def test_deterministic_mode_builds_deterministic_service_config():
    runtime = _runtime_config(
        "deterministic"
    )

    config = integration._build_service_config(
        runtime
    )

    assert config.use_rag is False
    assert config.use_ai is False


def test_rag_mode_builds_rag_service_config():
    runtime = _runtime_config(
        "rag"
    )

    config = integration._build_service_config(
        runtime
    )

    assert config.use_rag is True
    assert config.use_ai is False


def test_ai_mode_builds_rag_and_ai_service_config():
    runtime = _runtime_config(
        "ai"
    )

    config = integration._build_service_config(
        runtime
    )

    assert config.use_rag is True
    assert config.use_ai is True


# ============================================================
# RUNTIME MODE STATUS
# ============================================================


@pytest.mark.parametrize(
    (
        "mode",
        "expected_label",
        "expected_rag",
        "expected_ai",
    ),
    (
        (
            "deterministic",
            "Deterministic",
            False,
            False,
        ),
        (
            "rag",
            "RAG-Grounded",
            True,
            False,
        ),
        (
            "ai",
            "RAG + AI",
            True,
            True,
        ),
    ),
)
def test_runtime_mode_status(
    monkeypatch,
    mode,
    expected_label,
    expected_rag,
    expected_ai,
):
    runtime = _runtime_config(
        mode
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        lambda: runtime,
    )

    status = (
        integration.get_runtime_mode_status()
    )

    assert status.mode == mode
    assert status.label == expected_label
    assert status.use_rag is expected_rag
    assert status.use_ai is expected_ai


# ============================================================
# OPTIONAL DEPENDENCY CONSTRUCTION
# ============================================================


def test_deterministic_mode_builds_no_rag_or_llm_dependencies(
    monkeypatch,
):
    runtime = _runtime_config(
        "deterministic"
    )

    retriever_builder = Mock()
    llm_builder = Mock()

    monkeypatch.setattr(
        integration,
        "build_retriever",
        retriever_builder,
    )

    monkeypatch.setattr(
        integration,
        "build_llm_client",
        llm_builder,
    )

    retriever = (
        integration._build_runtime_retriever(
            runtime
        )
    )

    llm_client = (
        integration._build_runtime_llm_client(
            runtime
        )
    )

    assert retriever is None
    assert llm_client is None

    retriever_builder.assert_not_called()
    llm_builder.assert_not_called()


def test_rag_mode_builds_retriever(
    monkeypatch,
):
    runtime = _runtime_config(
        "rag"
    )

    expected_retriever = object()

    retriever_builder = Mock(
        return_value=expected_retriever
    )

    monkeypatch.setattr(
        integration,
        "build_retriever",
        retriever_builder,
    )

    result = (
        integration._build_runtime_retriever(
            runtime
        )
    )

    assert result is expected_retriever

    retriever_builder.assert_called_once_with()


def test_ai_mode_builds_llm_client(
    monkeypatch,
):
    runtime = _runtime_config(
        "ai"
    )

    expected_client = object()

    llm_builder = Mock(
        return_value=expected_client
    )

    monkeypatch.setattr(
        integration,
        "build_llm_client",
        llm_builder,
    )

    result = (
        integration._build_runtime_llm_client(
            runtime
        )
    )

    assert result is expected_client

    llm_builder.assert_called_once()

    llm_config = (
        llm_builder.call_args.args[0]
    )

    assert (
        llm_config.model
        == runtime.llm_model
    )

    assert (
        llm_config.base_url
        == runtime.llm_base_url
    )

    assert (
        llm_config.temperature
        == runtime.llm_temperature
    )

    assert (
        llm_config.max_output_tokens
        == runtime.llm_max_output_tokens
    )

    assert (
        llm_config.timeout_seconds
        == runtime.llm_timeout_seconds
    )


# ============================================================
# RESULT STATE SYNCHRONIZATION
# ============================================================


def test_store_service_result_synchronizes_all_state(
    monkeypatch,
):
    risk = object()
    recommendation = object()
    sustainability = object()

    result = SimpleNamespace(
        risk=risk,
        recommendation=recommendation,
        sustainability=sustainability,
        rag_enabled=True,
        ai_enabled=True,
        rag_attempted=True,
        ai_attempted=True,
        rag_succeeded=True,
        ai_succeeded=True,
        used_fallback=False,
        retrieved_context=(
            "evidence-1",
            "evidence-2",
        ),
        ai_explanation="Grounded explanation.",
        warnings=(
            "warning-1",
        ),
        errors=(),
    )

    set_service = Mock()
    set_risk = Mock()
    set_recommendation = Mock()
    set_sustainability = Mock()
    set_enrichment = Mock()
    mark_completed = Mock()

    monkeypatch.setattr(
        integration,
        "set_assessment_service_result",
        set_service,
    )

    monkeypatch.setattr(
        integration,
        "set_risk_assessment",
        set_risk,
    )

    monkeypatch.setattr(
        integration,
        "set_recommendation_result",
        set_recommendation,
    )

    monkeypatch.setattr(
    integration,
    "set_sustainability_result",
    set_sustainability,
    )

    monkeypatch.setattr(
        integration,
        "set_assessment_enrichment_state",
        set_enrichment,
    )

    monkeypatch.setattr(
        integration,
        "mark_assessment_completed",
        mark_completed,
    )

    integration._store_service_result(
        result
    )

    set_service.assert_called_once_with(
        result
    )

    set_risk.assert_called_once_with(
        risk
    )

    set_recommendation.assert_called_once_with(
        recommendation
    )

    set_sustainability.assert_called_once_with(
    sustainability
    )

    set_enrichment.assert_called_once_with(
        rag_enabled=True,
        ai_enabled=True,
        rag_attempted=True,
        ai_attempted=True,
        rag_succeeded=True,
        ai_succeeded=True,
        used_fallback=False,
        retrieved_context=(
            "evidence-1",
            "evidence-2",
        ),
        ai_explanation="Grounded explanation.",
        warnings=(
            "warning-1",
        ),
        errors=(),
    )

    mark_completed.assert_called_once_with(
        True
    )


# ============================================================
# SUCCESSFUL SUBMISSION
# ============================================================


def test_submission_calls_backend_exactly_once(
    monkeypatch,
):
    runtime = _runtime_config(
        "deterministic"
    )

    backend_result = SimpleNamespace(
        used_fallback=False
    )

    backend = Mock(
        return_value=backend_result
    )

    store_result = Mock()

    monkeypatch.setattr(
        integration,
        "clear_assessment_results",
        Mock(),
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        lambda: runtime,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_retriever",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_llm_client",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "assess_device",
        backend,
    )

    monkeypatch.setattr(
        integration,
        "_store_service_result",
        store_result,
    )

    payload = {
        "device_type": "Laptop",
    }

    submission = (
        integration.submit_device_assessment(
            payload
        )
    )

    assert backend.call_count == 1

    backend.assert_called_once()

    call = backend.call_args

    assert call.args[0] is payload

    assert (
        call.kwargs["user_query"]
        is None
    )

    assert (
        call.kwargs["retriever"]
        is None
    )

    assert (
        call.kwargs["llm_client"]
        is None
    )

    store_result.assert_called_once_with(
        backend_result
    )

    assert submission.succeeded is True
    assert submission.assessment_completed is True
    assert submission.validation_failed is False
    assert submission.used_fallback is False


def test_submission_forwards_user_query(
    monkeypatch,
):
    runtime = _runtime_config(
        "deterministic"
    )

    backend_result = SimpleNamespace(
        used_fallback=False
    )

    backend = Mock(
        return_value=backend_result
    )

    monkeypatch.setattr(
        integration,
        "clear_assessment_results",
        Mock(),
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        lambda: runtime,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_retriever",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_llm_client",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "assess_device",
        backend,
    )

    monkeypatch.setattr(
        integration,
        "_store_service_result",
        Mock(),
    )

    user_query = (
        "How should I securely donate this device?"
    )

    integration.submit_device_assessment(
        {},
        user_query=user_query,
    )

    assert (
        backend.call_args.kwargs[
            "user_query"
        ]
        == user_query
    )


# ============================================================
# VALIDATION FAILURE
# ============================================================


def test_validation_failure_is_frontend_safe(
    monkeypatch,
):
    runtime = _runtime_config(
        "deterministic"
    )

    backend = Mock(
        side_effect=ValueError(
            "Invalid assessment input."
        )
    )

    store_result = Mock()
    mark_completed = Mock()

    monkeypatch.setattr(
        integration,
        "clear_assessment_results",
        Mock(),
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        lambda: runtime,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_retriever",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_llm_client",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "assess_device",
        backend,
    )

    monkeypatch.setattr(
        integration,
        "_store_service_result",
        store_result,
    )

    monkeypatch.setattr(
        integration,
        "mark_assessment_completed",
        mark_completed,
    )

    submission = (
        integration.submit_device_assessment(
            {}
        )
    )

    assert backend.call_count == 1

    store_result.assert_not_called()

    mark_completed.assert_called_once_with(
        False
    )

    assert submission.succeeded is False
    assert submission.assessment_completed is False
    assert submission.validation_failed is True
    assert submission.used_fallback is False


# ============================================================
# UNEXPECTED BACKEND FAILURE
# ============================================================


def test_unexpected_backend_failure_is_frontend_safe(
    monkeypatch,
):
    runtime = _runtime_config(
        "deterministic"
    )

    backend = Mock(
        side_effect=RuntimeError(
            "Unexpected backend error."
        )
    )

    store_result = Mock()
    mark_completed = Mock()

    monkeypatch.setattr(
        integration,
        "clear_assessment_results",
        Mock(),
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        lambda: runtime,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_retriever",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_llm_client",
        lambda _runtime: None,
    )

    monkeypatch.setattr(
        integration,
        "assess_device",
        backend,
    )

    monkeypatch.setattr(
        integration,
        "_store_service_result",
        store_result,
    )

    monkeypatch.setattr(
        integration,
        "mark_assessment_completed",
        mark_completed,
    )

    submission = (
        integration.submit_device_assessment(
            {}
        )
    )

    assert backend.call_count == 1

    store_result.assert_not_called()

    mark_completed.assert_called_once_with(
        False
    )

    assert submission.succeeded is False
    assert submission.assessment_completed is False
    assert submission.validation_failed is False
    assert submission.used_fallback is False


# ============================================================
# SETUP FAILURE
# ============================================================


def test_setup_failure_prevents_backend_execution(
    monkeypatch,
):
    backend = Mock()
    store_result = Mock()
    mark_completed = Mock()

    def fail_configuration():
        raise RuntimeError(
            "Configuration unavailable."
        )

    monkeypatch.setattr(
        integration,
        "clear_assessment_results",
        Mock(),
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        fail_configuration,
    )

    monkeypatch.setattr(
        integration,
        "assess_device",
        backend,
    )

    monkeypatch.setattr(
        integration,
        "_store_service_result",
        store_result,
    )

    monkeypatch.setattr(
        integration,
        "mark_assessment_completed",
        mark_completed,
    )

    submission = (
        integration.submit_device_assessment(
            {}
        )
    )

    backend.assert_not_called()
    store_result.assert_not_called()

    mark_completed.assert_called_once_with(
        False
    )

    assert submission.succeeded is False
    assert submission.assessment_completed is False
    assert submission.validation_failed is False
    assert submission.used_fallback is False


# ============================================================
# SAFE FALLBACK
# ============================================================


def test_optional_enrichment_fallback_remains_successful(
    monkeypatch,
):
    runtime = _runtime_config(
        "ai"
    )

    backend_result = SimpleNamespace(
        used_fallback=True
    )

    backend = Mock(
        return_value=backend_result
    )

    store_result = Mock()

    retriever = object()
    llm_client = object()

    monkeypatch.setattr(
        integration,
        "clear_assessment_results",
        Mock(),
    )

    monkeypatch.setattr(
        integration,
        "load_runtime_config",
        lambda: runtime,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_retriever",
        lambda _runtime: retriever,
    )

    monkeypatch.setattr(
        integration,
        "_build_runtime_llm_client",
        lambda _runtime: llm_client,
    )

    monkeypatch.setattr(
        integration,
        "assess_device",
        backend,
    )

    monkeypatch.setattr(
        integration,
        "_store_service_result",
        store_result,
    )

    submission = (
        integration.submit_device_assessment(
            {}
        )
    )

    backend.assert_called_once()

    assert (
        backend.call_args.kwargs[
            "retriever"
        ]
        is retriever
    )

    assert (
        backend.call_args.kwargs[
            "llm_client"
        ]
        is llm_client
    )

    store_result.assert_called_once_with(
        backend_result
    )

    assert submission.succeeded is True
    assert submission.assessment_completed is True
    assert submission.validation_failed is False
    assert submission.used_fallback is True

    assert submission.message is not None

    assert (
        "deterministic"
        in submission.message.lower()
    )