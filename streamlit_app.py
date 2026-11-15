"""Streamlit Frontend for MediResearch AI — Multi-Agent Medical Researcher.

Permanent dark theme with clinical document/lab photo upload and evidence-based medical research guidance.
"""

import os
import sys
from pathlib import Path

# Ensure root directory is on Python path
BASE_DIR = Path(__file__).resolve().parent
if str(BASE_DIR) not in sys.path:
    sys.path.insert(0, str(BASE_DIR))

import streamlit as st
from app import config
from app.agents.medical_team import AGENT_NAMES, run_medical_workflow
from app.data.sample_documents import SAMPLE_MEDICAL_DOCUMENTS

# Page configuration
st.set_page_config(
    page_title="MediResearch AI — Multi-Agent Medical Researcher",
    page_icon="🩺",
    layout="wide",
    initial_sidebar_state="expanded",
)

# Sidebar: Branding, System Overview & Engine Status
with st.sidebar:
    st.title("🩺 MediResearch AI")
    st.caption("Multi-Agent Medical Researcher")
    st.markdown(
        "<div style='font-size: 0.85rem; color: #38bdf8; font-weight: 600; line-height: 1.4; margin-top: -4px; margin-bottom: 12px;'>"
        "GenAI Clinical Intelligence &bull; Multi-Agent System"
        "</div>",
        unsafe_allow_html=True,
    )
    st.divider()

    # Engine Status
    st.subheader("System Status")
    is_ready = config.is_provider_configured()
    active_model = config.get_active_model_name()
    if is_ready:
        st.success(f"● Connected: {active_model}")
        st.caption(f"Provider: `{config.MODEL_PROVIDER.upper()}`")
    else:
        st.error(f"● {config.MODEL_PROVIDER.capitalize()} API Key Missing")
        if config.MODEL_PROVIDER == "google":
            st.info("Please add `GEMINI_API_KEY` to `.env` (free from [Google AI Studio](https://aistudio.google.com/apikey)).")
        else:
            st.info("Please set `GROQ_API_KEY` in `.env`.")

    st.divider()

    # The 3 Agno Agents
    st.subheader("Collaborating Agno Medical Agents")
    st.markdown(
        """
        1. **Medical Query Analyzer**  
           *Classifies specialty, extracts patient vitals, eGFR, biomarkers, and frames clinical questions.*
        
        2. **Medical Research Agent**  
           *Investigates evidence-based clinical guidelines (ADA, ACC/AHA, IDSA, GOLD, KDIGO).*
        
        3. **Clinical Reviewer & Safety Auditor**  
           *Cross-examines drug-drug interactions, flags contraindications, and verifies clinical memo.*
        """
    )

    st.divider()

    # Grounding Library
    with st.expander("📚 Grounding Clinical Practice Guidelines", expanded=False):
        for doc in SAMPLE_MEDICAL_DOCUMENTS:
            st.markdown(f"**{doc['title']}**")
            st.caption(f"Specialty: {doc['category']}")
            st.caption(doc["summary"])
            st.markdown("---")


# Permanent Professional Dark Theme Stylesheet (Light mode disabled)
st.markdown(
    """
    <style>
    /* Hide only the hamburger menu and deploy toolbar; KEEP sidebar expand/collapse button visible */
    #MainMenu { display: none !important; }
    [data-testid="stToolbar"] { display: none !important; }
    footer { display: none !important; }

    /* Ensure sidebar open/close toggle buttons are always visible and styled */
    header {
        background: transparent !important;
    }
    [data-testid="collapsedControl"],
    [data-testid="stSidebarCollapseButton"] {
        visibility: visible !important;
        display: flex !important;
        color: #38bdf8 !important;
        z-index: 999999 !important;
    }

    .stApp {
        background-color: #0b1120;
        color: #f8fafc;
    }
    .medical-banner {
        background-color: rgba(14, 165, 233, 0.08);
        border: 1px solid rgba(14, 165, 233, 0.28);
        color: #bae6fd;
        padding: 12px 18px;
        border-radius: 8px;
        font-size: 0.88rem;
        margin-bottom: 20px;
        line-height: 1.5;
    }
    .academic-tag {
        display: inline-block;
        background-color: rgba(14, 165, 233, 0.12);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.3);
        padding: 4px 12px;
        border-radius: 4px;
        font-size: 0.82rem;
        font-weight: 600;
        margin-bottom: 12px;
    }
    .memo-card-header {
        background: #0f172a;
        border: 1px solid #1e293b;
        border-radius: 8px 8px 0 0;
        padding: 12px 18px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        border-bottom: 2px solid #0ea5e9;
    }
    .memo-tag {
        background-color: rgba(14, 165, 233, 0.15);
        color: #38bdf8;
        border: 1px solid rgba(14, 165, 233, 0.35);
        font-weight: 700;
        font-size: 0.75rem;
        padding: 2px 8px;
        border-radius: 4px;
        letter-spacing: 0.05em;
    }
    .audit-seal {
        background-color: rgba(16, 185, 129, 0.08);
        border: 1px solid rgba(16, 185, 129, 0.25);
        color: #34d399;
        padding: 10px 14px;
        border-radius: 6px;
        font-size: 0.84rem;
        font-weight: 600;
        margin-top: 18px;
        display: flex;
        align-items: center;
        gap: 8px;
    }
    .evidence-badge {
        background-color: rgba(139, 92, 246, 0.12);
        border: 1px solid rgba(139, 92, 246, 0.3);
        color: #ddd6fe;
        padding: 6px 12px;
        border-radius: 6px;
        font-size: 0.82rem;
        display: inline-flex;
        align-items: center;
        gap: 6px;
        margin-bottom: 12px;
    }
    .disclaimer-foot {
        color: #94a3b8;
        font-size: 0.78rem;
        line-height: 1.45;
        margin-top: 10px;
    }
    .source-chip {
        display: inline-block;
        background-color: #1e293b;
        border: 1px solid #334155;
        color: #38bdf8;
        font-size: 0.8rem;
        padding: 3px 8px;
        border-radius: 4px;
        margin-right: 6px;
        margin-bottom: 6px;
    }
    </style>
    """,
    unsafe_allow_html=True,
)

# Session state for inquiry, image & answer persistence
if "question_text" not in st.session_state:
    st.session_state.question_text = ""
if "response_data" not in st.session_state:
    st.session_state.response_data = None
if "attached_doc_name" not in st.session_state:
    st.session_state.attached_doc_name = None

# Main Page Content
st.title("Evidence-Based Clinical Inquiry & Medical Advisory")
st.markdown(
    '<div class="academic-tag">MediResearch AI &bull; Autonomous Multi-Agent Medical Intelligence</div>',
    unsafe_allow_html=True,
)
st.markdown(
    '<div class="medical-banner">'
    '<strong>Clinical Research Notice:</strong> MediResearch AI is an evidence-based clinical research assistant designed for educational '
    'and research inquiries. It synthesizes findings from established practice guidelines (ADA, ACC/AHA, IDSA, GOLD, KDIGO). '
    'It does not provide individual medical diagnosis, prescribe treatments, or substitute professional physician consultations.'
    '</div>',
    unsafe_allow_html=True,
)

# Common Clinical Scenario Buttons
st.write("**Common Clinical & Pharmacotherapy Scenarios:**")
col1, col2 = st.columns(2)
with col1:
    if st.button("🩸 T2D & SGLT2i Cardiorenal Protection in CKD", use_container_width=True):
        st.session_state.question_text = (
            "What is the evidence-based first-line therapy for a 56-year-old patient with Type 2 Diabetes, "
            "hypertension, and CKD (eGFR 44 mL/min/1.73m², UACR 180 mg/g) to reduce cardiorenal progression, and what are the metformin renal limits?"
        )
    if st.button("🫀 Stage 2 Hypertension with Albuminuria: Regimens", use_container_width=True):
        st.session_state.question_text = (
            "What are the guideline-directed first-line antihypertensive classes for a patient with persistent microalbuminuria, "
            "and why must dual ACE inhibitor and ARB therapy be strictly avoided?"
        )

with col2:
    if st.button("🫁 Community-Acquired Pneumonia Outpatient Triage", use_container_width=True):
        st.session_state.question_text = (
            "What is the recommended outpatient empiric antimicrobial regimen for Community-Acquired Pneumonia (CAP) "
            "in a patient with chronic lung disease, and what are the safety considerations regarding fluoroquinolones?"
        )
    if st.button("💊 High-Risk Drug Interactions: SSRIs, Tramadol & Anticoagulants", use_container_width=True):
        st.session_state.question_text = (
            "What is the clinical mechanism, risk profile, and symptom presentation of combining an SSRI (such as Sertraline) "
            "with Tramadol or NSAIDs, and how should it be managed?"
        )

st.write("")

# Query Input Form with Media Upload
with st.form("inquiry_form"):
    user_query = st.text_area(
        "Enter clinical question, patient presentation, or pharmacotherapy scenario:",
        value=st.session_state.question_text,
        height=130,
        placeholder="E.g., What are the guideline-directed therapies for a 62-year-old with Type 2 Diabetes and heart failure with preserved ejection fraction?",
        max_chars=2000,
    )

    # Document Image Upload
    uploaded_image = st.file_uploader(
        "📷 Upload Lab Report / Prescription / Clinical Summary Photo (Optional):",
        type=["png", "jpg", "jpeg", "webp"],
        help="Attach a photo of laboratory results (eGFR, HbA1c, CBC, CMP), prescription list, ECG strip, or clinical discharge notes.",
    )

    if uploaded_image:
        st.caption(f"📎 Attached file: `{uploaded_image.name}` ({uploaded_image.size // 1024} KB)")

    btn_col1, btn_col2, _ = st.columns([1.5, 1, 4])
    with btn_col1:
        submitted = st.form_submit_button("Analyze Clinical Inquiry", type="primary", use_container_width=True)
    with btn_col2:
        cleared = st.form_submit_button("Clear", use_container_width=True)

if cleared:
    st.session_state.question_text = ""
    st.session_state.response_data = None
    st.session_state.attached_doc_name = None
    st.rerun()

if submitted:
    cleaned_query = user_query.strip()
    if not cleaned_query and not uploaded_image:
        st.error("Please enter a clinical question or upload a medical document photo to analyze.")
    elif cleaned_query and len(cleaned_query) < 5 and not uploaded_image:
        st.error("Please enter a clinical question with at least 5 characters.")
    elif not config.is_provider_configured():
        st.error(f"API Key for {config.MODEL_PROVIDER.upper()} is not configured. Please add your key to `.env`.")
    else:
        if not cleaned_query and uploaded_image:
            cleaned_query = f"Examine this attached clinical document ({uploaded_image.name}), extract laboratory biomarkers and clinical data, and provide evidence-based medical analysis."

        st.session_state.question_text = cleaned_query
        st.session_state.attached_doc_name = uploaded_image.name if uploaded_image else None

        img_bytes = uploaded_image.getvalue() if uploaded_image else None
        img_name = uploaded_image.name if uploaded_image else None
        img_mime = uploaded_image.type if uploaded_image else None

        # Multi-agent coordination progress
        progress_placeholder = st.empty()
        with progress_placeholder.container():
            if img_bytes:
                st.info("Extracting clinical biomarkers & coordinating Agno Medical Team (Analyzer ➔ Researcher ➔ Safety Auditor)...")
            else:
                st.info("Coordinating Agno Medical Team (Analyzer ➔ Researcher ➔ Safety Auditor)...")

        try:
            with st.spinner("Multi-agent team investigating clinical guidelines and auditing pharmacology safety..."):
                result = run_medical_workflow(
                    cleaned_query,
                    image_bytes=img_bytes,
                    image_filename=img_name,
                    image_mime_type=img_mime,
                )
                st.session_state.response_data = result
        except Exception as e:
            st.error(f"Error during medical research reasoning: {str(e)}")
        finally:
            progress_placeholder.empty()


# Display Response
if st.session_state.response_data:
    resp = st.session_state.response_data
    answer_text = resp.get("answer", "")
    sources = resp.get("sources", [])

    st.write("---")

    # Medical Memorandum Card
    st.markdown(
        """
        <div class="memo-card-header">
            <div>
                <span class="memo-tag">CLINICAL RESEARCH MEMORANDUM</span>
                <span style="font-size: 0.85rem; font-weight: 600; margin-left: 10px;">Evidence-Based Advisory Findings</span>
            </div>
            <div style="font-size: 0.78rem; opacity: 0.8;">
                Team: Query Analyzer &bull; Evidence Researcher &bull; Safety Auditor
            </div>
        </div>
        """,
        unsafe_allow_html=True,
    )

    # Document Evidence Badge if image was analyzed
    if st.session_state.attached_doc_name:
        st.markdown(
            f'<div class="evidence-badge">📎 <strong>Analyzed Clinical Evidence:</strong> {st.session_state.attached_doc_name}</div>',
            unsafe_allow_html=True,
        )

    # Sources panel
    if sources:
        with st.expander(f"📚 Grounding Clinical Practice Guidelines Consulted ({len(sources)})", expanded=True):
            for s in sources:
                st.markdown(f"- **{s}**")

    # Answer Markdown
    st.markdown("### Clinical Analysis & Review")
    st.markdown(answer_text)

    # Verification seal
    st.markdown(
        """
        <div class="audit-seal">
            <span>✓</span>
            <span>Audited by Clinical Reviewer & Safety Auditor &bull; Grounded in evidence-based clinical practice guidelines</span>
        </div>
        <p class="disclaimer-foot">
            <strong>Disclaimer:</strong> MediResearch AI provides evidence-based scientific and clinical information for educational and 
            research purposes only. It does not provide medical diagnosis, clinical treatment advice, or establish a doctor-patient relationship. 
            Healthcare providers should exercise independent clinical judgment, and patients must always consult a licensed physician or specialist.
        </p>
        """,
        unsafe_allow_html=True,
    )

    # Download answer option
    evidence_note = f"\nEvidence: {st.session_state.attached_doc_name}\n" if st.session_state.attached_doc_name else ""
    st.download_button(
        label="Download Medical Research Memo (.txt)",
        data=(
            f"CLINICAL RESEARCH MEMORANDUM\n\nQuestion / Scenario:\n{st.session_state.question_text}\n"
            f"{evidence_note}\nAnswer:\n{answer_text}\n\nClinical Guidelines Consulted:\n"
            + "\n".join(sources)
            + f"\n\n{config.MEDICAL_DISCLAIMER}"
        ),
        file_name="clinical_research_memo.txt",
        mime="text/plain",
    )
