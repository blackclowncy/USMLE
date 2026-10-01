# MedPulse USMLE Q-Bank - Tactile Neumorphic Suite

An authentic, offline-first USMLE Step 1 examination and learning platform engineered with a **Warm Neumorphism** tactile design system.

## 📖 Question Bank Architecture (12,000 Questions across 80 Chapters)

The question bank is organized under **USMLE Step 1** across 4 major disciplines:

### 1. Pathology (`step 1-Pathology/` - 14 Chapters, 2,100 Questions)
- `Ch01_Cellular_Adaptations_and_Reversible_Injury/` (150 Qs)
- `Ch02_Cell_Death_Necrosis_and_Apoptosis/` (150 Qs)
- `Ch03_Cellular_Accumulations_and_Amyloidosis/` (150 Qs)
- `Ch04_Acute_Inflammation_and_Leukocyte_Dynamics/` (150 Qs)
- `Ch05_Inflammatory_Mediators_and_Microbial_Killing/` (150 Qs)
- `Ch06_Chronic_and_Granulomatous_Inflammation/` (150 Qs)
- `Ch07_Tissue_Repair_and_Wound_Healing/` (150 Qs)
- `Ch08_Hemodynamic_Disorders_Thrombosis_and_Embolism/` (150 Qs)
- `Ch09_Infarction_and_Shock/` (150 Qs)
- `Ch10_Principles_of_Neoplasia_and_Carcinogenesis/` (150 Qs)
- `Ch11_Cancer_Genetics_Oncogenes_and_TSGs/` (150 Qs)
- `Ch12_Clinical_Oncology_Staging_and_Tumor_Markers/` (150 Qs)
- `Ch13_Paraneoplastic_Syndromes/` (150 Qs)
- `Ch14_Cellular_Aging_and_Systemic_Changes/` (150 Qs)

### 2. Pharmacology (`step 1-Pharmacology/` - 9 Chapters, 1,350 Questions)
- `Ch01_General_Principles_Pharmacokinetics_and_Pharmacodynamics/` (150 Qs)
- `Ch02_Autonomic_Pharmacology/` (150 Qs)
- `Ch03_Cardiovascular_and_Renal_Pharmacology/` (150 Qs)
- `Ch04_Central_Nervous_System_Pharmacology_and_Psychopharmacology/` (150 Qs)
- `Ch05_Antimicrobial_Pharmacology/` (150 Qs)
- `Ch06_Inflammatory_Autacoid_Pulmonary_and_GI_Pharmacology/` (150 Qs)
- `Ch07_Hematologic_Pharmacology_Anticoagulants_and_Antiplatelets/` (150 Qs)
- `Ch08_Endocrine_and_Metabolic_Pharmacology/` (150 Qs)
- `Ch09_Anticancer_Immunosuppressant_and_Toxicology/` (150 Qs)

### 3. Biochemistry & Medical Genetics (`step 1-Biochemistry and Medical Genetics QA/` - 23 Chapters, 3,450 Questions)
- `Ch01_Nucleic_Acid_Structure_and_Organization/` to `Ch18_Purine_and_Pyrimidine_Metabolism/` (18 Chapters, 2,700 Qs)
- `Ch19_Medical_Genetics_Single_Gene_Disorders/` to `Ch23_Medical_Genetics_Genetic_Diagnosis/` (5 Chapters, 750 Qs)

### 4. Physiology (`step 1-Physiology/` - 34 Chapters, 5,100 Questions)
- **Cellular & Neuromuscular** (Ch01 - Ch06, 900 Qs): Fluids, RMP & Ion Equilibrium, Action Potentials & Synapses, Cardiac Action Potentials, Excitation-Contraction Coupling, Skeletal Muscle Mechanics.
- **Cardiovascular & Hemodynamics** (Ch07 - Ch11, 750 Qs): Hemodynamics, Cardiac Muscle Mechanics, CV Regulation & Guyton Curves, Local Blood Flow Regulation, Cardiac Cycle & Valvular Disease.
- **Respiratory Physiology** (Ch12 - Ch15, 600 Qs): Lung Mechanics, Alveolar-Blood Gas Exchange, O2/CO2 Transport & Ventilatory Control, V/Q Matching & Hypoxemia.
- **Renal Physiology & Acid-Base** (Ch16 - Ch20, 750 Qs): Renal Structure & GFR, Solute Transport, GFR Estimation & Clearance, Regional Nephron Transport, Acid-Base Regulation & Disorders.
- **Endocrine Physiology** (Ch21 - Ch29, 1,350 Qs): General Endocrine Principles, Anterior Pituitary, Posterior Pituitary, Adrenal Cortex, Adrenal Medulla, Endocrine Pancreas, Calcium/Phosphate Control, Thyroid, GH/Puberty.
- **Reproductive Physiology** (Ch30 - Ch31, 300 Qs): Male Reproductive Physiology, Female Reproductive Physiology.
- **Gastrointestinal Physiology** (Ch32 - Ch34, 450 Qs): GI Overview & Motility, GI Secretions, GI Digestion & Absorption.

---

## 🎨 UI/UX Features ([DESIGN.md](DESIGN.md))
- **Warm Neumorphism Style**: Sculpted bone-clay tactile surfaces (`#ebe7df`) with unified 315° directional light vector.
- **Multi-Discipline Switching**: Instantly switch between Pathology, Pharmacology, Biochemistry & Genetics, and Physiology.
- **USMLE Test Blocks**: Filter questions by 50-question examination blocks (`Block 1`, `Block 2`, `Block 3`) or full chapter mode (`All 150`).
- **Real-Time Question Navigator**: Dynamic 50/150 question grid tracking Correct (Emerald), Incorrect (Coral), Flagged (Gold Star), and Unanswered states.
- **4-Tier In-Depth Explanations**:
  - Educational Objective / USMLE High-Yield Takeaway
  - Clinical Vignette Breakdown & Key Clues (题干与题眼拆解)
  - Physiological/Pathophysiological Deep-Dive (机制深度剖析)
  - Full Distractor Analysis (全干扰项逐一深度纠错剖析)
- **Clinical Exam Tools**: Interactive Countdown & Stopwatch timer, Tutor Mode / Timed Exam mode, Normal Labs reference drawer, and persistent progress saving in LocalStorage.

---

## 🚀 Quick Start
Double-click `launch.bat` or open `index.html` directly in any web browser (no local server or internet connection required).
