"""Configuration management for Medical Researcher Agents (MediResearch).

Supports both Google Gemini (recommended for multimodal lab/imaging analysis and high TPM) and Groq.
"""

import os
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

try:
    from dotenv import load_dotenv
    load_dotenv(BASE_DIR / ".env", override=True)
except ImportError:
    pass

# Provider selection: "google" or "groq"
GEMINI_API_KEY: str = os.getenv("GEMINI_API_KEY", "").strip()
GROQ_API_KEY: str = os.getenv("GROQ_API_KEY", "").strip()

# Default to google if GEMINI_API_KEY is provided, else fallback to groq
default_provider = "google" if GEMINI_API_KEY else "groq"
MODEL_PROVIDER: str = os.getenv("MODEL_PROVIDER", default_provider).strip().lower()

GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash").strip()
GROQ_MODEL: str = os.getenv("GROQ_MODEL", "llama-3.3-70b-versatile").strip()

HOST: str = os.getenv("HOST", "127.0.0.1").strip()
PORT: int = int(os.getenv("PORT", "8000").strip())
REQUEST_TIMEOUT: int = int(os.getenv("REQUEST_TIMEOUT", "90").strip())

MEDICAL_DISCLAIMER: str = (
    "Medical Disclaimer: MediResearch Agents provides evidence-based scientific and clinical research analysis "
    "for educational and informational purposes only. It does not provide medical diagnosis, clinical treatment advice, "
    "or establish a doctor-patient relationship. Healthcare providers should exercise independent clinical judgment, "
    "and patients must always consult a licensed physician or healthcare specialist for medical decisions."
)

# Backward-compatibility alias
LEGAL_DISCLAIMER: str = MEDICAL_DISCLAIMER


def is_provider_configured() -> bool:
    """Check if the active model provider has a valid API key configured."""
    dummy_values = {"", "your_groq_api_key_here", "your_gemini_api_key_here", "placeholder"}
    if MODEL_PROVIDER == "google":
        return bool(GEMINI_API_KEY and GEMINI_API_KEY not in dummy_values)
    return bool(GROQ_API_KEY and GROQ_API_KEY not in dummy_values)


def is_groq_configured() -> bool:
    """Backward compatibility helper for health checks."""
    return is_provider_configured()


def get_active_model_name() -> str:
    """Return the name of the currently active model."""
    if MODEL_PROVIDER == "google":
        return f"Google ({GEMINI_MODEL})"
    return f"Groq ({GROQ_MODEL})"
