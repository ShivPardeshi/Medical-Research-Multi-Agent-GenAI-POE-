# MediResearch AI — Multi-Agent Medical Researcher 🩺🔬

**MediResearch AI** is an advanced, evidence-based multi-agent clinical research assistant designed for biomedical intelligence, clinical inquiry triage, and pharmacotherapy safety analysis. Built using **FastAPI**, the **Agno framework** multi-agent teams, and dual LLM support (**Google Gemini 2.5 Flash** with high TPM multimodal image analysis and **Groq** fallback running fast open-weight models), it delivers peer-reviewed medical guidance through both a modern web application and an interactive Streamlit dashboard.

***

## 🏛️ Multi-Agent Architecture

MediResearch AI coordinates exactly **three collaborating clinical agents** via Agno's `Team` framework (`TeamMode.coordinate`):

```
                       +------------------------------+
                       |  Clinical Inquiry / Patient  |
                       |  Scenario (+ Lab/Doc Image)  |
                       +--------------+---------------+
                                      |
                                      v
             +------------------------------------------------+
             |         Agno Medical Research Team             |
             |                                                |
             |  1. Medical Query Analyzer                     |
             |     - Classifies clinical specialty domain     |
             |     - Extracts patient vitals, eGFR, biomarkers|
             |     - Formulates targeted PICO research issues |
             |                        |                       |
             |                        v                       |
             |  2. Medical Research Agent                     |
             |     - Invokes `search_medical_library` tool    |
             |     - Grounded in consensus practice guidelines|
             |       (ADA, ACC/AHA, IDSA, GOLD, KDIGO)        |
             |     - Cites first-line regimens & trial data   |
             |                        |                       |
             |                        v                       |
             |  3. Clinical Reviewer & Safety Auditor         |
             |     - Audits drug-drug interactions (CYP450)   |
             |     - Flags organ contraindications (eGFR, QT) |
             |     - Strips unverified medical hallucinations |
             |     - Synthesizes final structured memo        |
             +------------------------+-----------------------+
                                      |
                                      v
                      +-------------------------------+
                      | Verified Clinical Memorandum  |
                      | + Consulted Practice Sources  |
                      | + Mandatory Medical Disclaimer|
                      +-------------------------------+
```

### The 3 Multi-Agent Clinical Flow:

1. **Medical Query Analyzer**:

   * Deconstructs complex clinical scenarios into pathophysiological mechanisms.

   * Extracts essential patient biomarkers: age, blood pressure, eGFR, HbA1c, renal status, comorbidities, and concurrent medications.

   * Formulates targeted biomedical research questions for evidence retrieval.
2. **Medical Research Agent**:

   * Calls the `search_medical_library` tool to investigate peer-reviewed clinical practice guidelines (ADA Standards of Care, ACC/AHA Hypertension Guidelines, IDSA Pneumonia Guidelines, GOLD COPD Consensus, KDIGO CKD Guidelines).

   * Identifies evidence levels, standard first-line therapies, therapeutic drug classes, renal/hepatic dosing adjustments, and landmark clinical trial conclusions.
3. **Clinical Reviewer & Safety Auditor**:

   * Rigorously checks for severe drug-drug interactions (e.g. Serotonin Syndrome with SSRIs + Tramadol, fatal bleeding risks with Anticoagulants + NSAIDs, QTc prolongation).

   * Evaluates contraindications (e.g. pregnancy, renal impairment thresholds like metformin eGFR < 30 mL/min/1.73m², bilateral renal artery stenosis).

   * Authoritative synthesis: formats the verified response into executive summary, guideline-directed pharmacotherapy, applied clinical analysis, and safety audit warnings.

***

## 📁 Project Structure

```
MediResearch/
├── .env.example             # Template for API keys (Gemini / Groq)
├── .gitignore               # Prevents committing secrets or build caches
├── requirements.txt         # Project dependencies (FastAPI, Agno, Streamlit, etc.)
├── README.md                # Project documentation and multi-agent architecture guide
├── Dockerfile               # Multi-stage container definition
├── docker-compose.yml       # Orchestrates FastAPI (8000) & Streamlit (8501)
├── streamlit_app.py         # Streamlit interactive clinical dashboard with lab upload
├── app/
│   ├── __init__.py
│   ├── config.py            # Environment configuration, timeouts & medical disclaimer
│   ├── main.py              # FastAPI app (GET /, POST /ask, POST /research, GET /health)
│   ├── schemas.py           # Pydantic schemas for medical request & response validation
│   ├── agents/
│   │   ├── __init__.py
│   │   ├── medical_team.py  # Agno Team definition and multi-agent coordination
│   │   ├── legal_team.py    # Backward-compatibility alias module
│   │   └── tools.py         # Clinical guideline search tool & source tracker
│   ├── data/
│   │   ├── __init__.py
│   │   └── sample_documents.py # Grounding practice guidelines (ADA, ACC/AHA, IDSA, GOLD, KDIGO)
│   └── static/
│       ├── index.html       # Clean single-page clinical research interface
│       ├── style.css        # Modern design system & responsive styling
│       └── app.js           # Frontend client logic & 3-step pipeline simulation
└── tests/
    ├── __init__.py
    ├── test_health.py       # Tests for /health and / endpoints
    ├── test_validation.py   # Tests for input validation and error handling
    └── test_agents.py       # Tests for Agno medical agents, Team, and guideline search tool
```

***

## 🚀 Getting Started

### 1. Prerequisites

* Python 3.10, 3.11, 3.12, 3.13, or 3.14 (or `uv` package manager)

* An API Key:

  * **Google Gemini API Key** (Recommended, free from [Google AI Studio](https://aistudio.google.com/apikey))

  * **Groq API Key** (Free from [Groq Console](https://console.groq.com/keys))

### 2. Environment Setup

Create a `.env` file in the project root:

```bash
cp .env.example .env
```

Populate your key:

```env
MODEL_PROVIDER=google
GEMINI_API_KEY=your_gemini_api_key_here
GEMINI_MODEL=gemini-2.5-flash

# Optional Groq fallback
GROQ_API_KEY=your_groq_api_key_here
GROQ_MODEL=llama-3.3-70b-versatile
```

### 3. Install Dependencies

Using `uv` (recommended for ultra-fast setup):

```bash
uv venv
source .venv/bin/activate
uv pip install -r requirements.txt
```

Or using standard `pip`:

```bash
python3 -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```

***

## 🖥️ Running the Application

### Option A: FastAPI Backend with Integrated Single-Page UI

```bash
uvicorn app.main:app --host 127.0.0.1 --port 8000 --reload
```

Open <http://localhost:8000> in your browser.

### Option B: Streamlit Interactive Clinical Dashboard

```bash
streamlit run streamlit_app.py --server.port 8501
```

Open <http://localhost:8501> in your browser. Features multimodal photo upload for lab reports, prescriptions, and ECG notes.

### Option C: Docker Compose

```bash
docker compose up --build
```

* FastAPI + Web UI: <http://localhost:8000>

* Streamlit UI: <http://localhost:8501>

***

## 🧪 Running Automated Tests

Run the test suite with `pytest`:

```bash
pytest -v
```

All test cases verify:

* Presence of all 3 medical agents: `Medical Query Analyzer`, `Medical Research Agent`, `Clinical Reviewer & Safety Auditor`

* Full functionality of `search_medical_library` across Diabetes, Hypertension, and Pneumonia modules

* Health check endpoint `/health` and root HTML delivery

* Pydantic schema validation (empty queries, short strings, whitespace rejection)

* Mocked multi-agent execution and disclaimer delivery

***

## 📋 API Reference

### `GET /health`

Returns system status, active LLM model, and participating agents:

```json
{
  "status": "healthy",
  "app_name": "MediResearch AI — Multi-Agent Medical Researcher",
  "groq_configured": true,
  "model": "Google (gemini-2.5-flash)",
  "agents": [
    "Medical Query Analyzer",
    "Medical Research Agent",
    "Clinical Reviewer & Safety Auditor"
  ]
}
```

### `POST /ask` or `POST /research`

Submits a clinical inquiry to the 3-agent pipeline:
**Request Body**:

```json
{
  "question": "What is the recommended first-line therapy for a 56-year-old patient with Type 2 Diabetes and CKD (eGFR 44 mL/min/1.73m²) to reduce cardiorenal progression?"
}
```

**Response**:

```json
{
  "status": "success",
  "question": "What is the recommended first-line therapy for a 56-year-old patient with Type 2 Diabetes and CKD (eGFR 44 mL/min/1.73m²) to reduce cardiorenal progression?",
  "answer": "...",
  "category": "Endocrinology & Metabolic Disease",
  "sources": [
    "Type 2 Diabetes Mellitus: ADA Standards of Care & Cardiorenal Protection",
    "Chronic Kidney Disease (CKD): KDIGO 2024 Evaluation & Management"
  ],
  "disclaimer": "Medical Disclaimer: MediResearch Agents provides evidence-based scientific and clinical research analysis for educational and informational purposes only..."
}
```

***

## ⚖️ Clinical Disclaimer

> **IMPORTANT:** MediResearch AI is an evidence-based clinical intelligence and research assistant designed for educational and informational analysis. It does not provide medical diagnoses, formulate definitive treatment plans, or establish a physician-patient relationship. Healthcare professionals must exercise independent clinical discretion, and patients must always consult a licensed medical practitioner for personalized healthcare guidance.
