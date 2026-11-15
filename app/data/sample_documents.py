"""Medical Knowledge Base & Clinical Practice Guidelines.

Contains curated evidence-based reference guidelines, clinical pharmacology monographs,
and diagnostic frameworks used by the Medical Evidence Researcher and Clinical Reviewer.
"""

from typing import Any, Dict, List

SAMPLE_MEDICAL_DOCUMENTS: List[Dict[str, Any]] = [
    {
        "id": "MED-GUIDE-DM2-001",
        "title": "Type 2 Diabetes Mellitus: ADA Standards of Care & Cardiorenal Protection",
        "category": "Endocrinology & Metabolic Disease",
        "keywords": [
            "diabetes", "type 2 diabetes", "t2d", "metformin", "sglt2", "sglt2 inhibitor",
            "glp-1", "semaglutide", "empagliflozin", "dapagliflozin", "hba1c", "ckd",
            "heart failure", "ascvd", "lactic acidosis", "hypoglycemia", "insulin"
        ],
        "summary": "First-line pharmacotherapy, organ protection (heart failure, CKD, ASCVD), and renal dosing thresholds.",
        "content": (
            "1. First-Line Pharmacotherapy (ADA Standards of Care 2024):\n"
            "   - Metformin combined with comprehensive lifestyle modification remains foundational first-line therapy.\n"
            "   - Renal Dosing: Check eGFR before initiation. Contraindicated if eGFR < 30 mL/min/1.73m². "
            "Reduce maximum dose to 1000 mg/day if eGFR 30-44 mL/min/1.73m² due to risk of lactic acidosis. "
            "Temporarily withhold prior to iodinated radiocontrast procedures.\n"
            "2. Cardiorenal Protection Independent of Baseline HbA1c:\n"
            "   - Heart Failure (HFrEF/HFpEF) or CKD (eGFR 20-60 or UACR > 30 mg/g): Prioritize SGLT2 inhibitors "
            "   (Empagliflozin, Dapagliflozin) to reduce HF hospitalization and slow CKD progression.\n"
            "   - Established Atherosclerotic Cardiovascular Disease (ASCVD) or High Risk: Prioritize GLP-1 Receptor Agonists "
            "   with proven CVD benefit (Semaglutide, Dulaglutide, Liraglutide) or SGLT2 inhibitors.\n"
            "3. Glycemic Targets:\n"
            "   - General non-pregnant adult target: HbA1c < 7.0% (53 mmol/mol).\n"
            "   - Stringent target (< 6.5%) for younger patients with short disease duration and low hypoglycemia risk.\n"
            "   - Relaxed target (< 8.0%) for frail elderly, extensive vascular complications, or severe hypoglycemia history.\n"
            "4. Safety Warnings & Adverse Profiles:\n"
            "   - SGLT2i: Risk of mycotic genital infections, euglycemic DKA, volume depletion, and Fournier's gangrene.\n"
            "   - GLP-1 RA: Gastrointestinal upset, contraindicated in personal/family history of Medullary Thyroid Carcinoma or MEN-2."
        )
    },
    {
        "id": "MED-GUIDE-HTN-002",
        "title": "Hypertension Clinical Practice Guidelines: ACC/AHA & ESC Framework",
        "category": "Cardiology & Vascular Medicine",
        "keywords": [
            "hypertension", "blood pressure", "acc/aha", "ace inhibitor", "arb", "lisinopril",
            "losartan", "amlodipine", "calcium channel blocker", "hydrochlorothiazide",
            "chlorthalidone", "hyperkalemia", "angioedema", "renal artery stenosis", "stage 2 htn"
        ],
        "summary": "Diagnostic staging, first-line antihypertensive classes, combination regimens, and contraindications.",
        "content": (
            "1. Blood Pressure Staging (ACC/AHA Guidelines):\n"
            "   - Normal: SBP < 120 and DBP < 80 mmHg.\n"
            "   - Elevated: SBP 120-129 and DBP < 80 mmHg.\n"
            "   - Stage 1 HTN: SBP 130-139 or DBP 80-89 mmHg (Treat with lifestyle + medication if 10-yr ASCVD risk >= 10%).\n"
            "   - Stage 2 HTN: SBP >= 140 or DBP >= 90 mmHg (Initiate 2 first-line agents of different classes if BP > 20/10 mmHg over goal).\n"
            "2. First-Line Antihypertensive Drug Classes:\n"
            "   - Thiazide/Thiazide-like Diuretics (Chlorthalidone, Hydrochlorothiazide, Indapamide).\n"
            "   - Angiotensin-Converting Enzyme (ACE) Inhibitors (e.g., Lisinopril, Enalapril) or "
            "   Angiotensin Receptor Blockers (ARBs, e.g., Losartan, Valsartan).\n"
            "   - Dihydropyridine Calcium Channel Blockers (CCBs, e.g., Amlodipine, Nifedipine ER).\n"
            "3. Special Clinical Situations:\n"
            "   - CKD with Albuminuria / Diabetes: ACEi or ARB is preferred first-line for renal hemodynamics and antiproteinuric effects.\n"
            "   - Black Patient Population (without CKD): CCBs and thiazide diuretics show superior initial BP reduction.\n"
            "   - Post-Myocardial Infarction / Heart Failure: Beta-blockers (Carvedilol, Metoprolol succinate) + ACEi/ARB.\n"
            "4. Absolute Contraindications & Safety Alerts:\n"
            "   - Pregnancy: ACE inhibitors, ARBs, and Direct Renin Inhibitors are strictly teratogenic (contraindicated).\n"
            "   - Bilateral Renal Artery Stenosis: ACEi/ARB may precipitate acute renal failure.\n"
            "   - NEVER combine ACE inhibitor + ARB concurrently (causes hyperkalemia, syncope, acute kidney injury without benefit)."
        )
    },
    {
        "id": "MED-GUIDE-PNEUMO-003",
        "title": "Community-Acquired Pneumonia (CAP): IDSA/ATS Evidence-Based Management",
        "category": "Infectious Disease & Pulmonology",
        "keywords": [
            "pneumonia", "cap", "curb-65", "amoxicillin", "azithromycin", "doxycycline",
            "augmentin", "levofloxacin", "moxifloxacin", "respiratory infection",
            "antibiotic stewardship", "fever", "cough", "infiltrate"
        ],
        "summary": "Outpatient vs inpatient triage, empiric antimicrobial regimens, severity scores, and fluoroquinolone stewardship.",
        "content": (
            "1. Triage & Severity Stratification:\n"
            "   - Utilize CURB-65 criteria (Confusion, Urea > 7 mmol/L, Resp Rate >= 30, BP SBP < 90 or DBP <= 60, Age >= 65).\n"
            "   - Score 0-1: Low risk, outpatient management appropriate.\n"
            "   - Score 2: Moderate risk, consider short inpatient stay or closely monitored outpatient care.\n"
            "   - Score >= 3: High risk, mandatory inpatient admission; evaluate for ICU if severe (shock or mechanical ventilation).\n"
            "2. Outpatient Empiric Antimicrobial Regimens:\n"
            "   - Healthy Outpatients (no comorbidities/risk factors for resistant pathogens):\n"
            "     * Amoxicillin 1g TID, OR Doxycycline 100mg BID, OR Macrolide (Azithromycin 500mg day 1 then 250mg daily) "
            "       only in areas with pneumococcal macrolide resistance < 25%.\n"
            "   - Outpatients with Comorbidities (COPD, DM, CKD, CHF, malignancy, alcoholism):\n"
            "     * Combination Therapy: Amoxicillin/clavulanate (875/125mg BID or 2000/125mg BID) or Cefuroxime/Cefpodoxime "
            "       PLUS Macrolide or Doxycycline.\n"
            "     * Monotherapy: Respiratory Fluoroquinolone (Levofloxacin 750mg daily or Moxifloxacin 400mg daily).\n"
            "3. Antimicrobial Stewardship & Precautions:\n"
            "   - Fluoroquinolone Warnings: Reserve fluoroquinolones when alternative options exist due to risks of tendinitis/tendon rupture, "
            "     QTc prolongation, aortic dissection, and C. difficile colitis.\n"
            "   - Duration: Minimum 5 days; patient must be afebrile for 48-72 hours with clinical stability before discontinuation."
        )
    },
    {
        "id": "MED-GUIDE-COPD-004",
        "title": "Chronic Obstructive Pulmonary Disease: GOLD 2024 Consensus Guidelines",
        "category": "Pulmonology & Respiratory Medicine",
        "keywords": [
            "copd", "gold guidelines", "bronchodilator", "tiotropium", "lama", "laba",
            "formoterol", "salmeterol", "inhaled corticosteroid", "ics", "eosinophils",
            "dyspnea", "exacerbation", "spirometry", "fev1"
        ],
        "summary": "GOLD classification, initial pharmacological therapy (LAMA/LABA vs ICS), and exacerbation prevention.",
        "content": (
            "1. Diagnosis & Severity Assessment:\n"
            "   - Spirometric confirmation: Post-bronchodilator FEV1/FVC < 0.70 confirms persistent airflow limitation.\n"
            "   - GOLD 2024 Group ABE Classification:\n"
            "     * Group A (0-1 moderate exacerbation, low symptoms mMRC 0-1, CAT < 10): Single bronchodilator (LABA or LAMA).\n"
            "     * Group B (0-1 moderate exacerbation, high symptoms mMRC >= 2, CAT >= 10): Dual bronchodilator (LABA + LAMA).\n"
            "     * Group E (>= 2 moderate exacerbations or >= 1 exacerbation leading to hospitalization): LABA + LAMA combination.\n"
            "2. Inhaled Corticosteroid (ICS) Positioning:\n"
            "   - ICS should NOT be used as monotherapy in COPD.\n"
            "   - Add ICS to LABA+LAMA (Triple Therapy) ONLY IF:\n"
            "     * Blood eosinophil count >= 300 cells/µL, OR\n"
            "     * Blood eosinophils >= 100 cells/µL with history of >= 2 moderate exacerbations or 1 hospitalization.\n"
            "   - ICS Avoidance / Warnings: Avoid if blood eosinophils < 100 cells/µL or recurrent pneumonia episodes.\n"
            "3. Non-Pharmacological Cornerstones:\n"
            "   - Smoking cessation counseling and pharmacotherapy (Varenicline, Bupropion, NRT).\n"
            "   - Vaccines: Annual Influenza, Pneumococcal conjugate (PCV20 or PCV15+PPSV23), COVID-19, and RSV (age >= 60)."
        )
    },
    {
        "id": "MED-GUIDE-PHARM-005",
        "title": "Clinical Pharmacology: High-Risk Drug Interactions & Safety Alerts",
        "category": "Pharmacology & Medication Safety",
        "keywords": [
            "drug interaction", "pharmacology", "serotonin syndrome", "ssri", "nsaid",
            "anticoagulant", "warfarin", "apixaban", "rivaroxaban", "bleeding", "qt prolongation",
            "cyp450", "potassium", "spironolactone", "tramadol"
        ],
        "summary": "Critical pharmacodynamic & pharmacokinetic interactions, QTc prolongation, and bleeding risks.",
        "content": (
            "1. Serotonin Syndrome (Severe / Life-Threatening):\n"
            "   - Mechanism: Additive serotonergic neurotransmission in CNS.\n"
            "   - Risky Combinations: Concomitant SSRIs/SNRIs (Sertraline, Fluoxetine, Venlafaxine) with Tramadol, "
            "     Linezolid (MAOI properties), Triptans, St. John's Wort, or Dextromethorphan.\n"
            "   - Symptoms: Hyperthermia, agitation, hyperreflexia, clonus, diaphoresis, tremors.\n"
            "2. Major Hemorrhagic / GI Bleeding Hazards:\n"
            "   - Oral Anticoagulants (DOACs like Apixaban, Rivaroxaban; or Warfarin) + Nonsteroidal Anti-inflammatory Drugs (NSAIDs):\n"
            "     Synergistic inhibition of platelet aggregation and gastric mucosal erosion leads to 3- to 5-fold surge in fatal GI bleeds.\n"
            "   - Co-prescription of SSRIs + NSAIDs also significantly elevates bleeding via platelet serotonin depletion.\n"
            "3. QTc Prolongation & Torsades de Pointes (TdP):\n"
            "   - Additive prolongation of myocardial ventricular repolarization.\n"
            "   - Offenders: Macrolides (Azithromycin, Clarithromycin), Fluoroquinolones (Levofloxacin), Ondansetron, "
            "     Antipsychotics (Haloperidol, Quetiapine), and Class III antiarrhythmics (Amiodarone, Sotalol).\n"
            "   - Monitoring: Baseline ECG, serum potassium and magnesium correction required.\n"
            "4. Renin-Angiotensin System & Hyperkalemia Hazard:\n"
            "   - Triple whammy: ACEi/ARB + Diuretic + NSAID precipitously induces acute prerenal azotemia.\n"
            "   - ACEi/ARB + Potassium-sparing diuretics (Spironolactone, Eplerenone, Amiloride) requires serial electrolyte tracking."
        )
    },
    {
        "id": "MED-GUIDE-CKD-006",
        "title": "Chronic Kidney Disease (CKD): KDIGO 2024 Evaluation & Management",
        "category": "Nephrology & Renal Medicine",
        "keywords": [
            "ckd", "kdigo", "egfr", "albuminuria", "proteinuria", "creatinine", "nephrotoxic",
            "nsaids", "gabapentin", "doac", "hyperkalemia", "anemia of ckd", "renin angiotensin"
        ],
        "summary": "Staging (G1-G5, A1-A3), nephrotoxic drug avoidance, and renal dosing adjustments.",
        "content": (
            "1. Definition & Staging (KDIGO Guidelines):\n"
            "   - Abnormalities of kidney structure or function persisting for > 3 months.\n"
            "   - eGFR Staging: G1 (>=90), G2 (60-89), G3a (45-59), G3b (30-44), G4 (15-29), G5 (<15 or dialysis).\n"
            "   - Albuminuria Staging (UACR): A1 (<30 mg/g normal), A2 (30-300 microalbuminuria), A3 (>300 severely increased).\n"
            "2. Renoprotective Interventions:\n"
            "   - ACEi or ARB titrated to maximum tolerated dose for patients with hypertension and UACR >= 30 mg/g.\n"
            "   - SGLT2 Inhibitor (Dapagliflozin or Empagliflozin) for patients with eGFR >= 20 mL/min/1.73m² and persistent albuminuria.\n"
            "   - Non-steroidal mineralocorticoid receptor antagonist (Finerenone) in T2D with CKD to reduce CVD and progression.\n"
            "3. Drug Dosing & Nephrotoxic Safeguards:\n"
            "   - Absolute Avoidance: Chronic systemic NSAIDs (accelerate interstitial fibrosis and cause acute hemodynamic decline).\n"
            "   - Dose Reductions: Gabapentin/Pregabalin (renally cleared, risk of severe neurotoxicity/myoclonus), "
            "     DOACs (reduce or avoid in eGFR < 15-30), Low Molecular Weight Heparins (monitor anti-Xa or switch to unfractionated heparin).\n"
            "   - Contrast-Induced Nephropathy: Hydrate with isotonic saline; avoid routine sodium bicarbonate or N-acetylcysteine."
        )
    }
]

# Backward compatibility alias
SAMPLE_LEGAL_DOCUMENTS = SAMPLE_MEDICAL_DOCUMENTS
