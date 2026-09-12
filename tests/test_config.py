"""
EcoShield AI
Configuration Tests

Tests centralized runtime configuration, environment parsing,
safe defaults, mode resolution, and defensive normalization.

These tests do not perform network calls or contact an LLM.
"""

from __future__ import annotations

import pytest

from config.config import (
    APP_ENV_DEVELOPMENT,
    APP_ENV_PRODUCTION,
    APP_ENV_TESTING,
    ASSESSMENT_MODE_AI,
    ASSESSMENT_MODE_DETERMINISTIC,
    ASSESSMENT_MODE_RAG,
    DEFAULT_APP_ENV,
    DEFAULT_ASSESSMENT_MODE,
    DEFAULT_LLM_MAX_OUTPUT_TOKENS,
    DEFAULT_LLM_MODEL,
    DEFAULT_LLM_PROVIDER,
    DEFAULT_LLM_TEMPERATURE,
    DEFAULT_LLM_TIMEOUT_SECONDS,
    DEFAULT_OLLAMA_BASE_URL,
    LLM_PROVIDER_IBM_GRANITE,
    LLM_PROVIDER_OLLAMA,
    LLM_PROVIDER_OPENAI_COMPATIBLE,
    MAX_LLM_MAX_OUTPUT_TOKENS,
    MAX_LLM_TEMPERATURE,
    MAX_LLM_TIMEOUT_SECONDS,
    MIN_LLM_MAX_OUTPUT_TOKENS,
    MIN_LLM_TEMPERATURE,
    MIN_LLM_TIMEOUT_SECONDS,
    RuntimeConfig,
    SUPPORTED_APP_ENVIRONMENTS,
    SUPPORTED_ASSESSMENT_MODES,
    SUPPORTED_LLM_PROVIDERS,
    _get_environment_float,
    _get_environment_int,
    _get_environment_value,
    _normalize_choice,
    _normalize_max_output_tokens,
    _normalize_temperature,
    _normalize_timeout_seconds,
    load_runtime_config,
)


RUNTIME_ENVIRONMENT_VARIABLES = (
    "APP_ENV",
    "ASSESSMENT_MODE",
    "LLM_PROVIDER",
    "LLM_MODEL",
    "LLM_BASE_URL",
    "LLM_API_KEY",
    "LLM_TEMPERATURE",
    "LLM_MAX_OUTPUT_TOKENS",
    "LLM_TIMEOUT_SECONDS",
    "LLM_PROJECT_ID",
)


@pytest.fixture
def clean_runtime_environment(monkeypatch):
    """
    Remove EcoShield runtime environment variables so tests are
    isolated from the developer machine.
    """

    for variable_name in RUNTIME_ENVIRONMENT_VARIABLES:
        monkeypatch.delenv(
            variable_name,
            raising=False,
        )


def test_supported_application_environments():
    assert SUPPORTED_APP_ENVIRONMENTS == (
        APP_ENV_DEVELOPMENT,
        APP_ENV_TESTING,
        APP_ENV_PRODUCTION,
    )


def test_supported_assessment_modes():
    assert SUPPORTED_ASSESSMENT_MODES == (
        ASSESSMENT_MODE_DETERMINISTIC,
        ASSESSMENT_MODE_RAG,
        ASSESSMENT_MODE_AI,
    )


def test_supported_llm_providers():
    assert SUPPORTED_LLM_PROVIDERS == (
        LLM_PROVIDER_OLLAMA,
        LLM_PROVIDER_OPENAI_COMPATIBLE,
        LLM_PROVIDER_IBM_GRANITE,
    )


def test_runtime_config_default_mode_is_deterministic():
    config = RuntimeConfig()

    assert (
        config.assessment_mode
        == DEFAULT_ASSESSMENT_MODE
    )
    assert config.use_rag is False
    assert config.use_ai is False


def test_runtime_config_rag_mode_enables_only_rag():
    config = RuntimeConfig(
        assessment_mode=ASSESSMENT_MODE_RAG
    )

    assert config.use_rag is True
    assert config.use_ai is False


def test_runtime_config_ai_mode_enables_rag_and_ai():
    config = RuntimeConfig(
        assessment_mode=ASSESSMENT_MODE_AI
    )

    assert config.use_rag is True
    assert config.use_ai is True


def test_environment_value_returns_default_when_missing(
    clean_runtime_environment,
):
    assert (
        _get_environment_value(
            "APP_ENV",
            DEFAULT_APP_ENV,
        )
        == DEFAULT_APP_ENV
    )


def test_environment_value_trims_whitespace(
    monkeypatch,
):
    monkeypatch.setenv(
        "APP_ENV",
        "  production  ",
    )

    assert (
        _get_environment_value("APP_ENV")
        == "production"
    )


def test_environment_value_uses_default_for_blank_value(
    monkeypatch,
):
    monkeypatch.setenv(
        "APP_ENV",
        "   ",
    )

    assert (
        _get_environment_value(
            "APP_ENV",
            DEFAULT_APP_ENV,
        )
        == DEFAULT_APP_ENV
    )


def test_environment_float_parses_valid_value(
    monkeypatch,
):
    monkeypatch.setenv(
        "LLM_TEMPERATURE",
        "0.7",
    )

    assert (
        _get_environment_float(
            "LLM_TEMPERATURE",
            DEFAULT_LLM_TEMPERATURE,
        )
        == 0.7
    )


def test_environment_float_falls_back_for_invalid_value(
    monkeypatch,
):
    monkeypatch.setenv(
        "LLM_TEMPERATURE",
        "invalid",
    )

    assert (
        _get_environment_float(
            "LLM_TEMPERATURE",
            DEFAULT_LLM_TEMPERATURE,
        )
        == DEFAULT_LLM_TEMPERATURE
    )


def test_environment_int_parses_valid_value(
    monkeypatch,
):
    monkeypatch.setenv(
        "LLM_MAX_OUTPUT_TOKENS",
        "1200",
    )

    assert (
        _get_environment_int(
            "LLM_MAX_OUTPUT_TOKENS",
            DEFAULT_LLM_MAX_OUTPUT_TOKENS,
        )
        == 1200
    )


def test_environment_int_falls_back_for_invalid_value(
    monkeypatch,
):
    monkeypatch.setenv(
        "LLM_MAX_OUTPUT_TOKENS",
        "invalid",
    )

    assert (
        _get_environment_int(
            "LLM_MAX_OUTPUT_TOKENS",
            DEFAULT_LLM_MAX_OUTPUT_TOKENS,
        )
        == DEFAULT_LLM_MAX_OUTPUT_TOKENS
    )


def test_normalize_choice_accepts_supported_value():
    assert (
        _normalize_choice(
            " AI ",
            supported_values=SUPPORTED_ASSESSMENT_MODES,
            default=DEFAULT_ASSESSMENT_MODE,
        )
        == ASSESSMENT_MODE_AI
    )


def test_normalize_choice_rejects_unsupported_value():
    assert (
        _normalize_choice(
            "unsupported",
            supported_values=SUPPORTED_ASSESSMENT_MODES,
            default=DEFAULT_ASSESSMENT_MODE,
        )
        == DEFAULT_ASSESSMENT_MODE
    )


@pytest.mark.parametrize(
    "value",
    (
        MIN_LLM_TEMPERATURE,
        0.2,
        1.0,
        MAX_LLM_TEMPERATURE,
    ),
)
def test_temperature_accepts_valid_range(value):
    assert _normalize_temperature(value) == value


@pytest.mark.parametrize(
    "value",
    (
        -1.0,
        2.1,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_temperature_rejects_unsafe_values(value):
    assert (
        _normalize_temperature(value)
        == DEFAULT_LLM_TEMPERATURE
    )


@pytest.mark.parametrize(
    "value",
    (
        MIN_LLM_MAX_OUTPUT_TOKENS,
        900,
        MAX_LLM_MAX_OUTPUT_TOKENS,
    ),
)
def test_max_output_tokens_accepts_valid_range(value):
    assert (
        _normalize_max_output_tokens(value)
        == value
    )


@pytest.mark.parametrize(
    "value",
    (
        0,
        -1,
        MAX_LLM_MAX_OUTPUT_TOKENS + 1,
    ),
)
def test_max_output_tokens_rejects_unsafe_values(value):
    assert (
        _normalize_max_output_tokens(value)
        == DEFAULT_LLM_MAX_OUTPUT_TOKENS
    )


@pytest.mark.parametrize(
    "value",
    (
        MIN_LLM_TIMEOUT_SECONDS,
        60.0,
        MAX_LLM_TIMEOUT_SECONDS,
    ),
)
def test_timeout_accepts_valid_range(value):
    assert (
        _normalize_timeout_seconds(value)
        == value
    )


@pytest.mark.parametrize(
    "value",
    (
        0.0,
        -1.0,
        301.0,
        float("nan"),
        float("inf"),
        float("-inf"),
    ),
)
def test_timeout_rejects_unsafe_values(value):
    assert (
        _normalize_timeout_seconds(value)
        == DEFAULT_LLM_TIMEOUT_SECONDS
    )


def test_load_runtime_config_uses_safe_defaults(
    clean_runtime_environment,
):
    config = load_runtime_config()

    assert config.app_env == DEFAULT_APP_ENV

    assert (
        config.assessment_mode
        == DEFAULT_ASSESSMENT_MODE
    )

    assert (
        config.llm_provider
        == DEFAULT_LLM_PROVIDER
    )

    assert config.llm_model == DEFAULT_LLM_MODEL

    assert (
        config.llm_base_url
        == DEFAULT_OLLAMA_BASE_URL
    )

    assert config.llm_api_key is None

    assert (
        config.llm_temperature
        == DEFAULT_LLM_TEMPERATURE
    )

    assert (
        config.llm_max_output_tokens
        == DEFAULT_LLM_MAX_OUTPUT_TOKENS
    )

    assert (
        config.llm_timeout_seconds
        == DEFAULT_LLM_TIMEOUT_SECONDS
    )

    assert config.llm_project_id is None

    assert config.use_rag is False
    assert config.use_ai is False


def test_load_runtime_config_normalizes_choices(
    clean_runtime_environment,
    monkeypatch,
):
    monkeypatch.setenv(
        "APP_ENV",
        " PRODUCTION ",
    )

    monkeypatch.setenv(
        "ASSESSMENT_MODE",
        " AI ",
    )

    monkeypatch.setenv(
        "LLM_PROVIDER",
        " OPENAI_COMPATIBLE ",
    )

    config = load_runtime_config()

    assert config.app_env == APP_ENV_PRODUCTION

    assert (
        config.assessment_mode
        == ASSESSMENT_MODE_AI
    )

    assert (
        config.llm_provider
        == LLM_PROVIDER_OPENAI_COMPATIBLE
    )

    assert config.use_rag is True
    assert config.use_ai is True


def test_load_runtime_config_invalid_choices_use_defaults(
    clean_runtime_environment,
    monkeypatch,
):
    monkeypatch.setenv(
        "APP_ENV",
        "invalid-environment",
    )

    monkeypatch.setenv(
        "ASSESSMENT_MODE",
        "invalid-mode",
    )

    monkeypatch.setenv(
        "LLM_PROVIDER",
        "invalid-provider",
    )

    config = load_runtime_config()

    assert config.app_env == DEFAULT_APP_ENV

    assert (
        config.assessment_mode
        == DEFAULT_ASSESSMENT_MODE
    )

    assert (
        config.llm_provider
        == DEFAULT_LLM_PROVIDER
    )

    assert config.use_rag is False
    assert config.use_ai is False


def test_load_runtime_config_valid_custom_values(
    clean_runtime_environment,
    monkeypatch,
):
    monkeypatch.setenv(
        "APP_ENV",
        APP_ENV_TESTING,
    )

    monkeypatch.setenv(
        "ASSESSMENT_MODE",
        ASSESSMENT_MODE_RAG,
    )

    monkeypatch.setenv(
        "LLM_PROVIDER",
        LLM_PROVIDER_IBM_GRANITE,
    )

    monkeypatch.setenv(
        "LLM_MODEL",
        "granite-test-model",
    )

    monkeypatch.setenv(
        "LLM_BASE_URL",
        "https://example.test/api",
    )

    monkeypatch.setenv(
        "LLM_API_KEY",
        "test-key",
    )

    monkeypatch.setenv(
        "LLM_TEMPERATURE",
        "0.6",
    )

    monkeypatch.setenv(
        "LLM_MAX_OUTPUT_TOKENS",
        "1200",
    )

    monkeypatch.setenv(
        "LLM_TIMEOUT_SECONDS",
        "45",
    )

    monkeypatch.setenv(
        "LLM_PROJECT_ID",
        "project-test",
    )

    config = load_runtime_config()

    assert config.app_env == APP_ENV_TESTING

    assert (
        config.assessment_mode
        == ASSESSMENT_MODE_RAG
    )

    assert (
        config.llm_provider
        == LLM_PROVIDER_IBM_GRANITE
    )

    assert config.llm_model == "granite-test-model"

    assert (
        config.llm_base_url
        == "https://example.test/api"
    )

    assert config.llm_api_key == "test-key"

    assert config.llm_temperature == 0.6

    assert config.llm_max_output_tokens == 1200

    assert config.llm_timeout_seconds == 45.0

    assert config.llm_project_id == "project-test"

    assert config.use_rag is True
    assert config.use_ai is False


def test_non_ollama_provider_has_no_default_ollama_url(
    clean_runtime_environment,
    monkeypatch,
):
    monkeypatch.setenv(
        "LLM_PROVIDER",
        LLM_PROVIDER_OPENAI_COMPATIBLE,
    )

    config = load_runtime_config()

    assert config.llm_base_url is None


@pytest.mark.parametrize(
    (
        "environment_name",
        "environment_value",
        "expected",
    ),
    (
        (
            "LLM_TEMPERATURE",
            "nan",
            DEFAULT_LLM_TEMPERATURE,
        ),
        (
            "LLM_TEMPERATURE",
            "inf",
            DEFAULT_LLM_TEMPERATURE,
        ),
        (
            "LLM_TIMEOUT_SECONDS",
            "nan",
            DEFAULT_LLM_TIMEOUT_SECONDS,
        ),
        (
            "LLM_TIMEOUT_SECONDS",
            "inf",
            DEFAULT_LLM_TIMEOUT_SECONDS,
        ),
    ),
)
def test_load_runtime_config_rejects_non_finite_numbers(
    clean_runtime_environment,
    monkeypatch,
    environment_name,
    environment_value,
    expected,
):
    monkeypatch.setenv(
        environment_name,
        environment_value,
    )

    config = load_runtime_config()

    if environment_name == "LLM_TEMPERATURE":
        actual = config.llm_temperature
    else:
        actual = config.llm_timeout_seconds

    assert actual == expected