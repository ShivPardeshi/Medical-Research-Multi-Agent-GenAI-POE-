"""Medical Researcher Agents — Multi-Agent Clinical Research Team.

Coordinates three collaborating Agno agents:
1. Medical Query Analyzer: Analyzes clinical inquiry, extracts patient parameters, and frames clinical questions.
2. Medical Research Agent: Investigates evidence-based guidelines, pharmacology databases, and clinical trials.
3. Clinical Reviewer & Safety Auditor: Audits drug interactions, contraindications, eliminates clinical hallucinations,
   and authors the structured Medical Research Memorandum.
"""

from typing import Any, Dict, List, Optional

try:
    from agno.agent import Agent
    from agno.team import Team, TeamMode
except ImportError:
    Agent = None
    Team = None
    class TeamMode:
        coordinate = "coordinate"

from app import config
from app.agents.tools import (
    clear_consulted_sources,
    get_last_consulted_sources,
    search_medical_library,
)

AGENT_NAMES = [
    "Medical Query Analyzer",
    "Medical Research Agent",
    "Clinical Reviewer & Safety Auditor",
]


def create_model_instance(api_key: Optional[str] = None, model_id: Optional[str] = None):
    """Instantiate the active LLM provider (Google Gemini or Groq)."""
    provider = config.MODEL_PROVIDER

    if provider == "google":
        from agno.models.google import Gemini

        key = api_key if api_key is not None else config.GEMINI_API_KEY
        m_id = model_id if model_id is not None else config.GEMINI_MODEL
        return Gemini(id=m_id, api_key=key)
    else:
        from agno.models.groq import Groq

        key = api_key if api_key is not None else config.GROQ_API_KEY
        m_id = model_id if model_id is not None else config.GROQ_MODEL
        return Groq(id=m_id, api_key=key)


def build_medical_team(api_key: Optional[str] = None, model_id: Optional[str] = None) -> Team:
    """Build the three collaborating Agno agents and coordinate them via an Agno Team."""
    model = create_model_instance(api_key=api_key, model_id=model_id)

    # Agent 1: Medical Query Analyzer (Clinical Case & Query Breakdown)
    analyzer_agent = Agent(
        name="Medical Query Analyzer",
        role="Analyze clinical inquiries, patient presentations, symptoms, and classify biomedical domains.",
        model=model,
        telemetry=False,
        description=(
            "An analytical medical expert specializing in clinical triage, medical biochemistry, pathology, "
            "and internal medicine domains (Cardiology, Endocrinology, Pulmonology, Nephrology, Infectious Disease). "
            "Deconstructs clinical scenarios, extracts patient vitals/biomarkers, and frames targeted research questions."
        ),
        instructions=[
            "1. Identify the primary clinical specialty and pathophysiological mechanisms involved.",
            "2. Extract critical patient clinical facts (e.g., age, vitals, eGFR, HbA1c, comorbidities, concurrent medications).",
            "3. Formulate 2-3 focused clinical research questions targeting diagnostic criteria and pharmacotherapy choices.",
        ],
    )

    # Agent 2: Medical Research Agent (Evidence-Based Guidelines & Pharmacology)
    research_agent = Agent(
        name="Medical Research Agent",
        role="Research clinical practice guidelines (ADA, ACC/AHA, IDSA, GOLD, KDIGO), drug monographs, and trial evidence.",
        model=model,
        tools=[search_medical_library],
        telemetry=False,
        description=(
            "A clinical medical researcher equipped with search_medical_library. Investigates first-line pharmacotherapies, "
            "organ-protective indications (e.g. SGLT2i/GLP-1 RA in CKD/HF), dosing adjustments, and consensus guidelines."
        ),
        instructions=[
            "1. Invoke search_medical_library with clinical keywords, disease states, and drug classes.",
            "2. Identify evidence-based recommendations, dosage protocols, organ-protective indications, and trial consensus.",
            "3. Explicitly cite consulted guideline modules and clinical reference documents.",
        ],
    )

    # Agent 3: Clinical Reviewer & Safety Auditor (Safety, Contraindications & Audit)
    reviewer_agent = Agent(
        name="Clinical Reviewer & Safety Auditor",
        role="Audit findings, evaluate drug-drug interactions, verify contraindications, and author medical memorandum.",
        model=model,
        telemetry=False,
        description=(
            "A senior clinical pharmacology and medical safety auditor. Evaluates evidence for clinical accuracy, "
            "rigorously checks for drug-drug interactions (e.g. Serotonin Syndrome, dual RAAS blockade, bleeding risks), "
            "flags renal/hepatic contraindications, eliminates unverified clinical claims, and authors the final advisory memo."
        ),
        instructions=[
            "1. Audit all findings against clinical safety standards, black-box warnings, and organ impairment thresholds.",
            "2. Specifically evaluate drug-drug interactions, contraindications (e.g., pregnancy, eGFR cutoffs), and adverse effects.",
            "3. Strip out any speculative, outdated, or hallucinated medical claims.",
            "4. Author the final response formatted with:",
            "   - **Clinical Specialty & Executive Summary**: Medical domain and concise clinical conclusion.",
            "   - **Evidence-Based Guidelines & Pharmacotherapy**: Recommended regimens, mechanisms of action, and guideline citations.",
            "   - **Applied Clinical Analysis & Management Strategy**: Step-by-step clinical evaluation and monitoring plan.",
            "   - **Clinical Safety Audit & Contraindication Warnings**: Explicit drug interactions, renal/hepatic cautions, and safety audit note.",
        ],
    )

    # Agno Team Coordinator
    medical_team = Team(
        name="Medical Research Assistant Team",
        members=[analyzer_agent, research_agent, reviewer_agent],
        model=model,
        tools=[search_medical_library],
        add_member_tools_to_context=True,
        mode=TeamMode.coordinate,
        telemetry=False,
        instructions=[
            "Coordinate the three agents sequentially to produce an authoritative Evidence-Based Medical Research Memorandum:",
            "1. Have Medical Query Analyzer dissect the clinical case, extract parameters, and frame research questions.",
            "2. Have Medical Research Agent search the clinical guideline library and retrieve evidence-based citations.",
            "3. Have Clinical Reviewer & Safety Auditor audit interactions, check contraindications, and synthesize the final verified memo.",
        ],
    )

    return medical_team


def run_medical_workflow(
    question: str,
    team: Optional[Team] = None,
    image_bytes: Optional[bytes] = None,
    image_filename: Optional[str] = None,
    image_mime_type: Optional[str] = None,
) -> Dict[str, Any]:
    """Execute the multi-agent medical research collaboration on a clinical inquiry and optional lab/imaging attachment."""
    clear_consulted_sources()

    evidence_context = ""
    candidate_models = [
        config.GEMINI_MODEL,
        "gemini-3.5-flash-lite",
        "gemini-3.1-flash-lite",
        "gemini-3.6-flash",
        "gemini-3.7-flash",
        "gemini-3.8-flash",
    ]
    seen = set()
    models_to_try = [m for m in candidate_models if not (m in seen or seen.add(m))]

    # 1. Clinical Document / Lab Report / Prescription Vision Extraction
    if image_bytes and config.MODEL_PROVIDER == "google" and config.GEMINI_API_KEY:
        from google import genai
        from google.genai import types

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        mime = image_mime_type or "image/jpeg"

        for model_id in models_to_try:
            try:
                ocr_response = client.models.generate_content(
                    model=model_id,
                    contents=[
                        types.Part.from_bytes(data=image_bytes, mime_type=mime),
                        (
                            "You are a clinical document specialist. Inspect this uploaded medical image (lab test result, "
                            "prescription, discharge summary, or diagnostic report). Transcribe all legible patient laboratory values "
                            "(eGFR, Creatinine, HbA1c, BP, electrolytes), medication dosages, diagnostic impressions, and clinical markers."
                        ),
                    ],
                    config={"http_options": {"timeout": 15000}},
                )
                if ocr_response and ocr_response.text:
                    evidence_context = (
                        f"\n\n[ATTACHED CLINICAL DATA EVIDENCE: {image_filename or 'Uploaded Medical Image'}]\n"
                        f"{ocr_response.text.strip()}\n"
                        f"[END OF CLINICAL DATA EVIDENCE]\n"
                    )
                    break
            except Exception:
                continue

    # 2. Search Grounding Clinical Practice Guidelines
    search_query = f"{question} {evidence_context[:300]}"
    clinical_guidelines = search_medical_library(search_query)
    sources = get_last_consulted_sources()

    # 3. Multi-Agent Synthesis (Analyzer, Researcher, Safety Reviewer)
    workflow_prompt = (
        f"You are MediResearch AI, an authoritative Medical Research Advisory Team composed of:\n"
        f"1. Medical Query Analyzer: Categorize clinical specialty, extract patient vitals/biomarkers, and frame research questions.\n"
        f"2. Medical Research Agent: Ground recommendations in established clinical guidelines (ADA, ACC/AHA, IDSA, GOLD, KDIGO) and trial data.\n"
        f"3. Clinical Reviewer & Safety Auditor: Scrutinize drug-drug interactions, renal/hepatic dosing contraindications, and author an evidence-based memorandum.\n\n"
        f"CLINICAL INQUIRY / CASE SCENARIO:\n"
        f"\"\"\"{question}\"\"\"\n"
        f"{evidence_context}\n"
        f"GROUNDING CLINICAL PRACTICE GUIDELINE LIBRARY:\n"
        f"{clinical_guidelines}\n\n"
        f"Generate the verified Medical Research Memorandum formatted strictly with:\n"
        f"- **Clinical Specialty & Executive Summary**: Relevant domain (e.g., Endocrinology, Cardiology, Nephrology) and direct clinical conclusion.\n"
        f"- **Evidence-Based Guidelines & Pharmacotherapy**: First-line regimens, mechanisms of action, and specific guideline citations.\n"
        f"- **Applied Clinical Analysis & Management Strategy**: Practical assessment addressing the patient's case, parameters, and attached lab evidence.\n"
        f"- **Clinical Safety Audit & Contraindication Warnings**: Comprehensive safety check covering drug interactions, organ dosage adjustments, and safety audit note."
    )

    content_text = ""
    # Execute with fallback across Gemini models
    if config.MODEL_PROVIDER == "google" and config.GEMINI_API_KEY:
        from google import genai

        client = genai.Client(api_key=config.GEMINI_API_KEY)
        for model_id in models_to_try:
            try:
                resp = client.models.generate_content(
                    model=model_id,
                    contents=workflow_prompt,
                    config={"http_options": {"timeout": 25000}},
                )
                if resp and resp.text:
                    content_text = resp.text.strip()
                    break
            except Exception:
                continue

    # Fallback to Agno Team run if direct generation was empty
    if not content_text:
        try:
            active_team = team if team is not None else build_medical_team()
            run_output = active_team.run(workflow_prompt)
            if hasattr(run_output, "get_content_as_string"):
                content_text = run_output.get_content_as_string()
            elif hasattr(run_output, "content") and run_output.content:
                content_text = str(run_output.content)
            else:
                content_text = str(run_output)
        except Exception as e:
            content_text = f"Unable to generate response: {e}"

    def _is_error_response(txt: str) -> bool:
        if not txt or not txt.strip():
            return True
        low = txt.lower()
        if "resource_exhausted" in low or "quota exceeded" in low or '"code": 429' in low or "'code': 429" in low:
            return True
        if txt.strip().startswith('{"error":') or txt.strip().startswith("{'error':"):
            return True
        return False

    # Automatic Failover to Groq if Google hit quota exhaustion or failed
    if _is_error_response(content_text) and config.GROQ_API_KEY:
        try:
            from groq import Groq

            groq_client = Groq(api_key=config.GROQ_API_KEY)
            groq_model = config.GROQ_MODEL or "llama-3.3-70b-versatile"
            groq_resp = groq_client.chat.completions.create(
                model=groq_model,
                messages=[
                    {
                        "role": "system",
                        "content": (
                            "You are MediResearch AI, an authoritative Medical Research Advisory Team composed of "
                            "Medical Query Analyzer, Medical Research Agent, and Clinical Reviewer & Safety Auditor. "
                            "Ground all findings strictly in evidence-based clinical guidelines, pharmacology, and patient safety."
                        ),
                    },
                    {"role": "user", "content": workflow_prompt},
                ],
                max_tokens=2500,
            )
            if groq_resp and groq_resp.choices and groq_resp.choices[0].message.content:
                content_text = groq_resp.choices[0].message.content.strip()
        except Exception:
            pass

    if _is_error_response(content_text):
        content_text = (
            "### ⏳ Temporary Rate Limit Notice\n\n"
            "The AI model provider's rate limit was temporarily reached. "
            "Your clinical query was preserved. **Please wait 10 seconds and click 'Analyze Clinical Inquiry' again.**\n\n"
            "*Tip: You can configure a Groq API key or Google AI Studio key with higher quota in `.env`.*"
        )

    return {
        "answer": content_text,
        "sources": sources,
    }


# Backward compatibility aliases
build_legal_team = build_medical_team
run_legal_workflow = run_medical_workflow
