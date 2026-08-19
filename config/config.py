"""
EcoShield AI
Application Configuration

Central configuration values used throughout the project.
"""

from pathlib import Path


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