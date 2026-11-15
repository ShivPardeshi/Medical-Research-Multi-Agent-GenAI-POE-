"""MediResearch AI Agents Package."""

from app.agents.medical_team import (
    AGENT_NAMES,
    build_legal_team,
    build_medical_team,
    run_legal_workflow,
    run_medical_workflow,
)
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_legal_library,
    search_medical_library,
)

__all__ = [
    "AGENT_NAMES",
    "build_medical_team",
    "run_medical_workflow",
    "search_medical_library",
    "build_legal_team",
    "run_legal_workflow",
    "search_legal_library",
    "get_last_consulted_sources",
    "clear_consulted_sources",
]
