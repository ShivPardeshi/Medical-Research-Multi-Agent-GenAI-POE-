"""Legacy compatibility module forwarding to app.agents.medical_team."""

from app.agents.medical_team import (  # noqa: F401
    AGENT_NAMES,
    build_medical_team,
    build_medical_team as build_legal_team,
    create_model_instance,
    run_medical_workflow,
    run_medical_workflow as run_legal_workflow,
)
from app.agents.tools import (  # noqa: F401
    clear_consulted_sources,
    get_last_consulted_sources,
    search_medical_library,
    search_medical_library as search_legal_library,
)
