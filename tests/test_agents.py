"""Tests for Medical Agent Architecture and Clinical Knowledge Base Retrieval."""

from app.agents.medical_team import AGENT_NAMES, build_medical_team
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_medical_library,
)


def test_agent_names_list():
    """Verify exactly 3 designated medical agents are present."""
    assert len(AGENT_NAMES) == 3
    assert "Medical Query Analyzer" in AGENT_NAMES
    assert "Medical Research Agent" in AGENT_NAMES
    assert "Clinical Reviewer & Safety Auditor" in AGENT_NAMES


def test_build_medical_team():
    """Verify Agno Team composition and configuration."""
    team = build_medical_team(api_key="mock_test_key_xyz")
    assert team.name == "Medical Research Assistant Team"
    assert len(team.members) == 3

    member_names = [m.name for m in team.members]
    assert "Medical Query Analyzer" in member_names
    assert "Medical Research Agent" in member_names
    assert "Clinical Reviewer & Safety Auditor" in member_names

    # Check that Medical Research Agent has the search_medical_library tool
    research_agent = next(m for m in team.members if m.name == "Medical Research Agent")
    assert research_agent.tools is not None
    assert len(research_agent.tools) >= 1


def test_search_medical_library_diabetes():
    """Verify search tool returns ADA guidelines for diabetes and cardiorenal queries."""
    clear_consulted_sources()
    result = search_medical_library("diabetes metformin sglt2 ckd hba1c")
    assert "ADA Standards of Care" in result or "Type 2 Diabetes" in result
    sources = get_last_consulted_sources()
    assert any("Diabetes" in s for s in sources)


def test_search_medical_library_hypertension():
    """Verify search tool returns ACC/AHA hypertension guidelines."""
    clear_consulted_sources()
    result = search_medical_library("hypertension blood pressure lisinopril amlodipine")
    assert "Hypertension" in result
    sources = get_last_consulted_sources()
    assert any("Hypertension" in s for s in sources)


def test_search_medical_library_pneumonia():
    """Verify search tool returns IDSA/ATS guidelines for pneumonia."""
    clear_consulted_sources()
    result = search_medical_library("community acquired pneumonia curb-65 amoxicillin")
    assert "Pneumonia" in result
    sources = get_last_consulted_sources()
    assert any("Pneumonia" in s for s in sources)
