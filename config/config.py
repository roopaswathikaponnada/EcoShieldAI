"""
EcoShield AI
Application Configuration

Central configuration values used throughout the project.
"""

import os
from dataclasses import dataclass
from math import isfinite
from pathlib import Path

from dotenv import load_dotenv


# ============================================================
# PROJECT INFORMATION
# ============================================================

PROJECT_NAME = "EcoShield AI"

PROJECT_DESCRIPTION = (
    "AI-Powered Secure E-Waste Disposal Advisor"
)

PROJECT_VERSION = "1.0.0"


# ============================================================
# PROJECT ROOT
# ============================================================

PROJECT_ROOT = Path(__file__).resolve().parent.parent
load_dotenv(PROJECT_ROOT / ".env")

# ============================================================
# DIRECTORY PATHS
# ============================================================

CONFIG_DIR = PROJECT_ROOT / "config"

SRC_DIR = PROJECT_ROOT / "src"

TESTS_DIR = PROJECT_ROOT / "tests"

KNOWLEDGE_BASE_DIR = PROJECT_ROOT / "knowledge_base"

DOCS_DIR = PROJECT_ROOT / "docs"

RESULTS_DIR = PROJECT_ROOT / "results"


# ============================================================
# KNOWLEDGE BASE PATHS
# ============================================================

CYBERSECURITY_KB_DIR = (
    KNOWLEDGE_BASE_DIR / "cybersecurity"
)

SUSTAINABILITY_KB_DIR = (
    KNOWLEDGE_BASE_DIR / "sustainability"
)


# ============================================================
# DOCUMENTATION PATHS
# ============================================================

SCREENSHOTS_DIR = DOCS_DIR / "screenshots"

DIAGRAMS_DIR = DOCS_DIR / "diagrams"


# ============================================================
# APPLICATION SETTINGS
# ============================================================

PAGE_TITLE = "EcoShield AI"

PAGE_ICON = "♻️"

PAGE_LAYOUT = "wide"


# ============================================================
# SECURITY RISK LEVELS
# ============================================================

RISK_LOW = "Low"

RISK_MEDIUM = "Medium"

RISK_HIGH = "High"


# ============================================================
# DEVICE TYPES
# ============================================================

DEVICE_TYPES = [
    "Laptop",
    "Desktop",
    "Smartphone",
    "Tablet",
    "External Hard Drive",
    "USB Drive",
    "Other",
]


# ============================================================
# OPERATING SYSTEMS
# ============================================================

OPERATING_SYSTEMS = [
    "Windows",
    "macOS",
    "Linux",
    "Android",
    "iOS",
    "ChromeOS",
    "Other",
    "Not Applicable",
    "Unknown",
]


# ============================================================
# DEVICE AGE
# ============================================================

MIN_DEVICE_AGE = 0.0

MAX_DEVICE_AGE = 50.0


# ============================================================
# DEVICE CONDITIONS
# ============================================================

DEVICE_CONDITIONS = [
    "Working",
    "Partially Working",
    "Not Working",
    "Physically Damaged",
]


# ============================================================
# STORAGE TYPES
# ============================================================

STORAGE_TYPES = [
    "HDD",
    "SSD",
    "eMMC",
    "Flash Storage",
    "Hybrid",
    "Unknown",
    "Not Applicable",
]


# ============================================================
# STORAGE CAPACITY
# ============================================================

STORAGE_CAPACITY_UNITS = [
    "GB",
    "TB",
]

MAX_STORAGE_CAPACITY_GB = 1_000_000.0


# ============================================================
# PERSONAL DATA OPTIONS
# ============================================================

PERSONAL_DATA_OPTIONS = [
    "Yes",
    "No",
    "Unsure",
]


# ============================================================
# SENSITIVE DATA OPTIONS
# ============================================================

SENSITIVE_DATA_OPTIONS = [
    "Yes",
    "No",
    "Unsure",
]


# ============================================================
# DEVICE ACCESSIBILITY OPTIONS
# ============================================================

DEVICE_ACCESSIBLE_OPTIONS = [
    "Yes",
    "No",
]


# ============================================================
# POWER STATUS OPTIONS
# ============================================================

POWER_ON_OPTIONS = [
    "Yes",
    "No",
]


# ============================================================
# DATA BACKUP OPTIONS
# ============================================================

BACKUP_OPTIONS = [
    "Yes",
    "No",
    "Not Required",
    "Unsure",
]


# ============================================================
# FACTORY RESET OPTIONS
# ============================================================

FACTORY_RESET_OPTIONS = [
    "Yes",
    "No",
    "Not Applicable",
    "Unsure",
]


# ============================================================
# SECURE ERASE OPTIONS
# ============================================================

SECURE_ERASE_OPTIONS = [
    "Yes",
    "No",
    "Not Applicable",
    "Unsure",
]


# ============================================================
# ENCRYPTION OPTIONS
# ============================================================

ENCRYPTION_OPTIONS = [
    "Yes",
    "No",
    "Unsure",
    "Not Applicable",
]


# ============================================================
# ACCOUNT SIGN-OUT OPTIONS
# ============================================================

ACCOUNT_SIGNOUT_OPTIONS = [
    "Yes",
    "No",
    "Not Applicable",
    "Unsure",
]


# ============================================================
# SIM / MEMORY CARD REMOVAL OPTIONS
# ============================================================

REMOVABLE_MEDIA_OPTIONS = [
    "Yes",
    "No",
    "Not Applicable",
    "Unsure",
]


# ============================================================
# INTENDED DISPOSAL METHODS
# ============================================================

DISPOSAL_METHODS = [
    "Sell",
    "Donate",
    "Reuse",
    "Recycle",
    "Dispose",
    "Repair",
    "Not Decided",
]


# ============================================================
# DEVICE GROUPS
# ============================================================

MOBILE_DEVICES = {
    "Smartphone",
    "Tablet",
}

COMPUTER_DEVICES = {
    "Laptop",
    "Desktop",
}

EXTERNAL_STORAGE_DEVICES = {
    "External Hard Drive",
    "USB Drive",
}

DEVICES_EXPECTED_TO_HAVE_STORAGE = {
    "Laptop",
    "Desktop",
    "Smartphone",
    "Tablet",
    "External Hard Drive",
    "USB Drive",
}


# ============================================================
# DISPOSAL BEHAVIOR GROUPS
# ============================================================

DEVICE_LEAVES_OWNER_ACTIONS = {
    "Sell",
    "Donate",
    "Recycle",
    "Dispose",
}

# ============================================================
# APPLICATION ENVIRONMENTS
# ============================================================

APP_ENV_DEVELOPMENT = "development"

APP_ENV_TESTING = "testing"

APP_ENV_PRODUCTION = "production"

SUPPORTED_APP_ENVIRONMENTS = (
    APP_ENV_DEVELOPMENT,
    APP_ENV_TESTING,
    APP_ENV_PRODUCTION,
)


# ============================================================
# ASSESSMENT MODES
# ============================================================

ASSESSMENT_MODE_DETERMINISTIC = "deterministic"

ASSESSMENT_MODE_RAG = "rag"

ASSESSMENT_MODE_AI = "ai"

SUPPORTED_ASSESSMENT_MODES = (
    ASSESSMENT_MODE_DETERMINISTIC,
    ASSESSMENT_MODE_RAG,
    ASSESSMENT_MODE_AI,
)


# ============================================================
# LLM PROVIDERS
# ============================================================

LLM_PROVIDER_OLLAMA = "ollama"

LLM_PROVIDER_OPENAI_COMPATIBLE = (
    "openai_compatible"
)

LLM_PROVIDER_IBM_GRANITE = (
    "ibm_granite"
)

SUPPORTED_LLM_PROVIDERS = (
    LLM_PROVIDER_OLLAMA,
    LLM_PROVIDER_OPENAI_COMPATIBLE,
    LLM_PROVIDER_IBM_GRANITE,
)


# ============================================================
# RUNTIME CONFIGURATION DEFAULTS
# ============================================================

DEFAULT_APP_ENV = APP_ENV_DEVELOPMENT

DEFAULT_ASSESSMENT_MODE = (
    ASSESSMENT_MODE_DETERMINISTIC
)

DEFAULT_LLM_PROVIDER = LLM_PROVIDER_OLLAMA

DEFAULT_LLM_MODEL = "qwen2.5:3b"

DEFAULT_OLLAMA_BASE_URL = (
    "http://localhost:11434"
)

DEFAULT_LLM_TEMPERATURE = 0.2

DEFAULT_LLM_MAX_OUTPUT_TOKENS = 900

DEFAULT_LLM_TIMEOUT_SECONDS = 180.0

# ============================================================
# RUNTIME CONFIGURATION LIMITS
# ============================================================

MIN_LLM_TEMPERATURE = 0.0

MAX_LLM_TEMPERATURE = 2.0

MIN_LLM_MAX_OUTPUT_TOKENS = 1

MAX_LLM_MAX_OUTPUT_TOKENS = 16_384

MIN_LLM_TIMEOUT_SECONDS = 1.0

MAX_LLM_TIMEOUT_SECONDS = 300.0

# ============================================================
# RUNTIME CONFIGURATION MODEL
# ============================================================

@dataclass(frozen=True)
class RuntimeConfig:
    """
    Resolved EcoShield application runtime configuration.

    This object contains configuration only. It does not perform
    validation, risk scoring, retrieval, recommendation generation,
    or LLM calls.
    """

    app_env: str = DEFAULT_APP_ENV

    assessment_mode: str = (
        DEFAULT_ASSESSMENT_MODE
    )

    llm_provider: str = (
        DEFAULT_LLM_PROVIDER
    )

    llm_model: str = (
        DEFAULT_LLM_MODEL
    )

    llm_base_url: str | None = (
        DEFAULT_OLLAMA_BASE_URL
    )

    llm_api_key: str | None = None

    llm_temperature: float = (
        DEFAULT_LLM_TEMPERATURE
    )

    llm_max_output_tokens: int = (
        DEFAULT_LLM_MAX_OUTPUT_TOKENS
    )

    llm_timeout_seconds: float = (
        DEFAULT_LLM_TIMEOUT_SECONDS
    )

    llm_project_id: str | None = None

    @property
    def use_rag(self) -> bool:
        """
        Return whether retrieval is required by the selected mode.
        """

        return self.assessment_mode in {
            ASSESSMENT_MODE_RAG,
            ASSESSMENT_MODE_AI,
        }

    @property
    def use_ai(self) -> bool:
        """
        Return whether LLM enrichment is enabled.
        """

        return (
            self.assessment_mode
            == ASSESSMENT_MODE_AI
        )

# ============================================================
# ENVIRONMENT VALUE HELPERS
# ============================================================

def _get_environment_value(
    name: str,
    default: str | None = None,
) -> str | None:
    """
    Return a normalized environment-variable value.

    Missing or blank values resolve to the supplied default.
    """

    value = os.getenv(name)

    if value is None:
        return default

    normalized = value.strip()

    if not normalized:
        return default

    return normalized


def _get_environment_float(
    name: str,
    default: float,
) -> float:
    """
    Read an environment variable as a float.

    Invalid values currently fall back to the supplied default.
    Additional validation is handled by the configuration
    hardening layer.
    """

    value = _get_environment_value(name)

    if value is None:
        return default

    try:
        return float(value)

    except (TypeError, ValueError):
        return default


def _get_environment_int(
    name: str,
    default: int,
) -> int:
    """
    Read an environment variable as an integer.

    Invalid values currently fall back to the supplied default.
    Additional validation is handled by the configuration
    hardening layer.
    """

    value = _get_environment_value(name)

    if value is None:
        return default

    try:
        return int(value)

    except (TypeError, ValueError):
        return default

# ============================================================
# CONFIGURATION VALIDATION HELPERS
# ============================================================

def _normalize_choice(
    value: str,
    *,
    supported_values: tuple[str, ...],
    default: str,
) -> str:
    """
    Normalize a configuration choice.

    Unsupported or blank values resolve to a known safe default.
    """

    normalized = str(value).strip().lower()

    if normalized in supported_values:
        return normalized

    return default


def _normalize_temperature(
    value: float,
) -> float:
    """
    Return a safe finite LLM temperature.
    """

    if not isfinite(value):
        return DEFAULT_LLM_TEMPERATURE

    if (
        MIN_LLM_TEMPERATURE
        <= value
        <= MAX_LLM_TEMPERATURE
    ):
        return value

    return DEFAULT_LLM_TEMPERATURE


def _normalize_max_output_tokens(
    value: int,
) -> int:
    """
    Return a safe maximum output-token value.
    """

    if (
        MIN_LLM_MAX_OUTPUT_TOKENS
        <= value
        <= MAX_LLM_MAX_OUTPUT_TOKENS
    ):
        return value

    return DEFAULT_LLM_MAX_OUTPUT_TOKENS


def _normalize_timeout_seconds(
    value: float,
) -> float:
    """
    Return a safe finite provider timeout.
    """

    if not isfinite(value):
        return DEFAULT_LLM_TIMEOUT_SECONDS

    if (
        MIN_LLM_TIMEOUT_SECONDS
        <= value
        <= MAX_LLM_TIMEOUT_SECONDS
    ):
        return value

    return DEFAULT_LLM_TIMEOUT_SECONDS    

# ============================================================
# RUNTIME CONFIGURATION LOADER
# ============================================================

def load_runtime_config() -> RuntimeConfig:
    """
    Resolve EcoShield runtime configuration from environment
    variables while preserving safe application defaults.

    Environment variables are read when this function is called,
    rather than when config.py is imported.
    """

    app_env = _normalize_choice(
        (
            _get_environment_value(
                "APP_ENV",
                DEFAULT_APP_ENV,
            )
            or DEFAULT_APP_ENV
        ),
        supported_values=SUPPORTED_APP_ENVIRONMENTS,
        default=DEFAULT_APP_ENV,
    )

    assessment_mode = _normalize_choice(
        (
            _get_environment_value(
                "ASSESSMENT_MODE",
                DEFAULT_ASSESSMENT_MODE,
            )
            or DEFAULT_ASSESSMENT_MODE
        ),
        supported_values=SUPPORTED_ASSESSMENT_MODES,
        default=DEFAULT_ASSESSMENT_MODE,
    )

    llm_provider = _normalize_choice(
        (
            _get_environment_value(
                "LLM_PROVIDER",
                DEFAULT_LLM_PROVIDER,
            )
            or DEFAULT_LLM_PROVIDER
        ),
        supported_values=SUPPORTED_LLM_PROVIDERS,
        default=DEFAULT_LLM_PROVIDER,
    )

    llm_model = (
        _get_environment_value(
            "LLM_MODEL",
            DEFAULT_LLM_MODEL,
        )
        or DEFAULT_LLM_MODEL
    )

    llm_base_url = _get_environment_value(
        "LLM_BASE_URL",
        (
            DEFAULT_OLLAMA_BASE_URL
            if llm_provider == LLM_PROVIDER_OLLAMA
            else None
        ),
    )

    llm_api_key = _get_environment_value(
        "LLM_API_KEY"
    )

    llm_temperature = _normalize_temperature(
        _get_environment_float(
            "LLM_TEMPERATURE",
            DEFAULT_LLM_TEMPERATURE,
        )
    )

    llm_max_output_tokens = (
        _normalize_max_output_tokens(
            _get_environment_int(
                "LLM_MAX_OUTPUT_TOKENS",
                DEFAULT_LLM_MAX_OUTPUT_TOKENS,
            )
        )
    )

    llm_timeout_seconds = (
        _normalize_timeout_seconds(
            _get_environment_float(
                "LLM_TIMEOUT_SECONDS",
                DEFAULT_LLM_TIMEOUT_SECONDS,
            )
        )
    )

    llm_project_id = _get_environment_value(
        "LLM_PROJECT_ID"
    )

    return RuntimeConfig(
        app_env=app_env,
        assessment_mode=assessment_mode,
        llm_provider=llm_provider,
        llm_model=llm_model,
        llm_base_url=llm_base_url,
        llm_api_key=llm_api_key,
        llm_temperature=llm_temperature,
        llm_max_output_tokens=(
            llm_max_output_tokens
        ),
        llm_timeout_seconds=(
            llm_timeout_seconds
        ),
        llm_project_id=llm_project_id,
    )