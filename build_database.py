import os
import re
import json
import sys

def convert_markdown_to_html(md_text, edu_fallback=None):
    if not md_text:
        return ""
    
    # Extract Educational Objective if present to render as a distinct callout card
    edu_match = re.search(r'#{4,5}\s*(?:\d+\.\s*)?Educational Objective[^:]*:\s*(.*)', md_text, re.DOTALL | re.IGNORECASE)
    edu_html = ""
    body_text = md_text
    
    edu_content = None
    if edu_match:
        edu_content = edu_match.group(1).strip()
        body_text = md_text[:edu_match.start()].strip()
    elif edu_fallback:
        edu_content = edu_fallback.strip()
    
    if edu_content:
        clean_edu = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-[#181d24] font-bold">\1</strong>', edu_content)
        clean_edu = re.sub(r'\*(.*?)\*', r'<em class="italic text-[#4a453c]">\1</em>', clean_edu)
        edu_html = (
            f'<div class="exp-edu-card">'
            f'<div class="exp-edu-title">'
            f'<span class="material-symbols-outlined text-[20px]">school</span>'
            f'<span>Educational Objective / USMLE High-Yield Takeaway</span>'
            f'</div>'
            f'<p class="exp-edu-text">{clean_edu}</p>'
            f'</div>'
        )

    # Format Distractor Analysis header (English only)
    body_text = re.sub(
        r'#{4,5}\s*(?:\d+\.\s*)?(?:Comprehensive\s+)?Distractor Analysis[^:]*:?', 
        r'<div class="exp-section-title"><span class="material-symbols-outlined text-[18px]">rule</span><span>Distractor Analysis</span></div>', 
        body_text, 
        flags=re.IGNORECASE
    )
    
    # Format Explanation header (English only)
    body_text = re.sub(
        r'#{4,5}\s*(?:High-Yield Mechanism[^:\n\r]*|High-Yield Pathophysiological Explanation|Detailed Explanations?|Explanation):?',
        r'<div class="exp-mech-title"><span class="material-symbols-outlined text-[18px]">auto_stories</span><span>Explanation &amp; Mechanism Breakdown</span></div>',
        body_text,
        flags=re.IGNORECASE
    )

    # Format Section headers
    body_text = re.sub(
        r'#####\s*(\d+\.\s*[^\n\r]+)',
        r'<div class="exp-heading"><span class="exp-heading-dot"></span><span>\1</span></div>',
        body_text
    )

    # Replace bold & italic
    body_text = re.sub(r'\*\*(.*?)\*\*', r'<strong class="text-[#181d24] font-bold">\1</strong>', body_text)
    body_text = re.sub(r'\*(.*?)\*', r'<em class="italic text-[#4a453c]">\1</em>', body_text)

    # Process lines: bullets and paragraphs
    lines = body_text.split('\n')
    formatted_lines = []
    
    for line in lines:
        s = line.strip()
        if not s:
            continue
        if s.startswith('- ') or s.startswith('* '):
            item_text = s[2:]
            # Check if option letter like (A): or **(A)**:
            opt_tag_m = re.match(r'^(?:\(|<strong>\()?([A-E])(?:\)|<\/strong>\))?:?\s*(.*)', item_text)
            if opt_tag_m and len(opt_tag_m.group(1)) == 1:
                letter = opt_tag_m.group(1)
                rest = opt_tag_m.group(2)
                formatted_lines.append(
                    f'<div class="exp-opt-box"><span class="exp-badge">{letter}</span><div class="exp-text">{rest}</div></div>'
                )
            else:
                formatted_lines.append(
                    f'<div class="exp-bullet-row"><span class="exp-bullet-dot">•</span><div class="exp-text">{item_text}</div></div>'
                )
        elif s.startswith('<div') or s.startswith('</div') or s.startswith('<h') or s.startswith('</h'):
            formatted_lines.append(s)
        else:
            formatted_lines.append(f'<p class="exp-p">{s}</p>')

    res = "".join(formatted_lines) + edu_html
    return res

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
SYSTEMIC_PATHOLOGY_DIR = os.path.join(BASE_DIR, 'Systemic Pathology QA')
ADV_PHARM_DIR = os.path.join(BASE_DIR, 'Advanced Clinical Pharmacology and Toxicology QA')
METABOLIC_GENETICS_DIR = os.path.join(BASE_DIR, 'Metabolic Genetics and Clinical Nutrition QA')
EXERCISE_PHYSIOLOGY_DIR = os.path.join(BASE_DIR, 'Exercise and Environmental Physiology QA')
PHARYNGEAL_EMBRYOLOGY_DIR = os.path.join(BASE_DIR, 'Pharyngeal Embryology and Clinical Teratology QA')

def sanitize_chapters(chapters):
    return [{k: v for k, v in ch.items() if k not in ('baseDir', 'sourceDir')} for ch in chapters]

PATHOLOGY_CHAPTERS = [
    {
        "id": "Ch01_Cellular_Adaptations_and_Reversible_Injury",
        "name": "Ch01 Cellular Adaptations and Reversible Injury",
        "dirName": "Ch01_Cellular_Adaptations_and_Reversible_Injury",
        "totalQuestions": 150,
        "status": "active",
        "description": "Cellular adaptations (hypertrophy, hyperplasia, atrophy, metaplasia) and reversible cell injury."
    },
    {
        "id": "Ch02_Cell_Death_Necrosis_and_Apoptosis",
        "name": "Ch02 Cell Death Necrosis and Apoptosis",
        "dirName": "Ch02_Cell_Death_Necrosis_and_Apoptosis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Mechanisms of necrosis, apoptosis, subcellular responses to injury, and ischemic cell death."
    },
    {
        "id": "Ch03_Cellular_Accumulations_and_Amyloidosis",
        "name": "Ch03 Cellular Accumulations and Amyloidosis",
        "dirName": "Ch03_Cellular_Accumulations_and_Amyloidosis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Intracellular accumulations (steatosis, pigments, calcification) and systemic amyloidosis."
    },
    {
        "id": "Ch04_Acute_Inflammation_and_Leukocyte_Dynamics",
        "name": "Ch04 Acute Inflammation and Leukocyte Dynamics",
        "dirName": "Ch04_Acute_Inflammation_and_Leukocyte_Dynamics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Vascular events, leukocyte adhesion cascade, transmigration, and chemotaxis."
    },
    {
        "id": "Ch05_Inflammatory_Mediators_and_Microbial_Killing",
        "name": "Ch05 Inflammatory Mediators and Microbial Killing",
        "dirName": "Ch05_Inflammatory_Mediators_and_Microbial_Killing",
        "totalQuestions": 150,
        "status": "active",
        "description": "Chemical mediators (histamine, prostaglandins, leukotrienes, cytokines) and phagocytosis."
    },
    {
        "id": "Ch06_Chronic_and_Granulomatous_Inflammation",
        "name": "Ch06 Chronic and Granulomatous Inflammation",
        "dirName": "Ch06_Chronic_and_Granulomatous_Inflammation",
        "totalQuestions": 150,
        "status": "active",
        "description": "Macrophage activation, granuloma formation, tuberculosis, sarcoidosis, and chronic inflammatory states."
    },
    {
        "id": "Ch07_Tissue_Repair_and_Wound_Healing",
        "name": "Ch07 Tissue Repair and Wound Healing",
        "dirName": "Ch07_Tissue_Repair_and_Wound_Healing",
        "totalQuestions": 150,
        "status": "active",
        "description": "Regeneration vs repair, granulation tissue, ECM deposition, collagen synthesis, and scar remodeling."
    },
    {
        "id": "Ch08_Hemodynamic_Disorders_Thrombosis_and_Embolism",
        "name": "Ch08 Hemodynamic Disorders Thrombosis and Embolism",
        "dirName": "Ch08_Hemodynamic_Disorders_Thrombosis_and_Embolism",
        "totalQuestions": 150,
        "status": "active",
        "description": "Thrombosis, Virchow triad, embolism, and hypercoagulable states."
    },
    {
        "id": "Ch09_Infarction_and_Shock",
        "name": "Ch09 Infarction and Shock",
        "dirName": "Ch09_Infarction_and_Shock",
        "totalQuestions": 150,
        "status": "active",
        "description": "Pathology of infarction, ischemic reperfusion injury, and stages of shock."
    },
    {
        "id": "Ch10_Principles_of_Neoplasia_and_Carcinogenesis",
        "name": "Ch10 Principles of Neoplasia and Carcinogenesis",
        "dirName": "Ch10_Principles_of_Neoplasia_and_Carcinogenesis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Benign vs malignant neoplasms, nomenclature, differentiation, anaplasia, invasion, metastasis, and carcinogenesis."
    },
    {
        "id": "Ch11_Cancer_Genetics_Oncogenes_and_TSGs",
        "name": "Ch11 Cancer Genetics Oncogenes and TSGs",
        "dirName": "Ch11_Cancer_Genetics_Oncogenes_and_TSGs",
        "totalQuestions": 150,
        "status": "active",
        "description": "Proto-oncogenes, tumor suppressor genes (p53, Rb), Knudson two-hit hypothesis, and familial cancer syndromes."
    },
    {
        "id": "Ch12_Clinical_Oncology_Staging_and_Tumor_Markers",
        "name": "Ch12 Clinical Oncology Staging and Tumor Markers",
        "dirName": "Ch12_Clinical_Oncology_Staging_and_Tumor_Markers",
        "totalQuestions": 150,
        "status": "active",
        "description": "TNM staging, histological grading, serum tumor markers, invasion-metastasis cascade, and immunohistochemistry."
    },
    {
        "id": "Ch13_Paraneoplastic_Syndromes",
        "name": "Ch13 Paraneoplastic Syndromes",
        "dirName": "Ch13_Paraneoplastic_Syndromes",
        "totalQuestions": 150,
        "status": "active",
        "description": "Endocrinopathies, neuromyopathies, dermatologic, and hematologic paraneoplastic syndromes."
    },
    {
        "id": "Ch14_Cellular_Aging_and_Systemic_Changes",
        "name": "Ch14 Cellular Aging and Systemic Changes",
        "dirName": "Ch14_Cellular_Aging_and_Systemic_Changes",
        "totalQuestions": 150,
        "status": "active",
        "description": "Telomere biology, cellular senescence, DNA damage accumulation, progeroid syndromes, and systemic physiological decline."
    },
    {
        "id": "Ch15_Skin_Pathology",
        "name": "Ch15 Systemic: Skin Pathology",
        "dirName": "Ch01_Skin_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Inflammatory dermatoses (eczema, psoriasis, lichen planus, erythema multiforme, Stevens-Johnson/TEN), blistering diseases (pemphigus vulgaris, bullous pemphigoid, dermatitis herpetiformis), and skin neoplasms (basal cell carcinoma, squamous cell carcinoma, melanoma, dysplastic nevus, seborrheic keratosis, actinic keratosis)."
    },
    {
        "id": "Ch16_RBC_Pathology_and_Anemias",
        "name": "Ch16 Systemic: RBC Pathology & Anemias",
        "dirName": "Ch02_RBC_Pathology_and_Anemias",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Microcytic anemias (iron deficiency, anemia of chronic disease, alpha/beta thalassemia, sideroblastic anemia), normocytic anemias (hereditary spherocytosis, PNH, sickle cell, G6PD deficiency, autoimmune hemolytic anemia, microangiopathic hemolytic anemia/TTP/HUS), macrocytic anemias (B12 and folate deficiency), and aplastic anemia."
    },
    {
        "id": "Ch17_Vascular_Pathology_and_Vasculitides",
        "name": "Ch17 Systemic: Vascular Pathology & Vasculitides",
        "dirName": "Ch03_Vascular_Pathology_and_Vasculitides",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Large-vessel vasculitis (giant cell/temporal arteritis, Takayasu arteritis), medium-vessel vasculitis (polyarteritis nodosa, Kawasaki disease, Buerger disease), small-vessel vasculitis (granulomatosis with polyangiitis/Wegener, microscopic polyangiitis, eosinophilic granulomatosis with polyangiitis/Churg-Strauss, Henoch-Schonlein purpura/IgA vasculitis), atherosclerosis, and aneurysms/dissections."
    },
    {
        "id": "Ch18_Cardiac_Pathology",
        "name": "Ch18 Systemic: Cardiac Pathology",
        "dirName": "Ch04_Cardiac_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Ischemic heart disease (angina, myocardial infarction timeline, histological progression, complications), heart failure (systolic vs diastolic, left vs right), valvular diseases (rheumatic fever, infective endocarditis, nonbacterial thrombotic endocarditis, carcinoid heart disease), cardiomyopathies (dilated, hypertrophic, restrictive), myocarditis, and cardiac tumors (myxoma, rhabdomyoma)."
    },
    {
        "id": "Ch19_Pulmonary_Pathology",
        "name": "Ch19 Systemic: Pulmonary Pathology",
        "dirName": "Ch05_Pulmonary_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Obstructive lung diseases (COPD/emphysema, chronic bronchitis, asthma, bronchiectasis), restrictive lung diseases (idiopathic pulmonary fibrosis, sarcoidosis, pneumoconioses/asbestosis/silicosis/coal workers, hypersensitivity pneumonitis), ARDS/diffuse alveolar damage, pulmonary hypertension, and lung cancer (adenocarcinoma, squamous cell, small cell, large cell, mesothelioma)."
    },
    {
        "id": "Ch20_Renal_Pathology",
        "name": "Ch20 Systemic: Renal Pathology",
        "dirName": "Ch06_Renal_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Glomerulonephritis and nephrotic syndromes (minimal change disease, FSGS, membranous nephropathy, amyloidosis, diabetic nephropathy), nephritic syndromes (post-streptococcal GN, rapidly progressive GN, IgA nephropathy/Berger, Alport syndrome, membranoproliferative GN), acute tubular necrosis (ATN), acute interstitial nephritis (AIN), renal papillary necrosis, polycystic kidney disease, and renal cell carcinoma."
    },
    {
        "id": "Ch21_GI_Tract_Pathology",
        "name": "Ch21 Systemic: GI Tract Pathology",
        "dirName": "Ch07_GI_Tract_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Esophageal pathology (GERD, Barrett esophagus, esophageal adenocarcinoma and squamous cell carcinoma, Mallory-Weiss, Boerhaave, achalasia), gastric pathology (acute/chronic gastritis, H. pylori, autoimmune gastritis, peptic ulcer disease, gastric adenocarcinoma, MALT lymphoma), intestinal pathology (celiac disease, Crohn disease vs ulcerative colitis, appendicitis, diverticular disease, Hirschsprung, bowel ischemia), and colonic polyps/colorectal carcinoma (APC/KRAS/p53 and microsatellite instability pathways)."
    },
    {
        "id": "Ch22_Pancreatic_Pathology",
        "name": "Ch22 Systemic: Pancreatic Pathology",
        "dirName": "Ch08_Pancreatic_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Acute pancreatitis (gallstones, alcohol, hypertriglyceridemia, enzymatic fat necrosis, pseudocyst), chronic pancreatitis (pancreatic calcifications, exocrine insufficiency), pancreatic cystic neoplasms, and pancreatic ductal adenocarcinoma (head of pancreas, painless jaundice, Courvoisier sign, Trousseau syndrome)."
    },
    {
        "id": "Ch23_Gallbladder_and_Biliary_Tract_Pathology",
        "name": "Ch23 Systemic: Gallbladder & Biliary Tract Pathology",
        "dirName": "Ch09_Gallbladder_and_Biliary_Tract_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Cholelithiasis (cholesterol vs pigment stones), acute and chronic cholecystitis (acalculous cholecystitis, porcelain gallbladder), choledocholithiasis, ascending cholangitis (Charcot triad, Reynolds pentad), primary biliary cholangitis (anti-mitochondrial antibodies), primary sclerosing cholangitis (onion-skinning, p-ANCA, ulcerative colitis association), and cholangiocarcinoma."
    },
    {
        "id": "Ch24_Liver_Pathology",
        "name": "Ch24 Systemic: Liver Pathology",
        "dirName": "Ch10_Liver_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Viral hepatitis (HAV, HBV, HCV, HDV, HEV morphology and serology), autoimmune hepatitis, alcoholic liver disease (steatosis, alcoholic hepatitis, Mallory-Denk bodies, cirrhosis), nonalcoholic fatty liver disease (NAFLD/NASH), hemochromatosis (HFE mutation, Prussian blue), Wilson disease (ATP7B, copper overload, Kayser-Fleischer rings), alpha-1 antitrypsin deficiency (PAS-positive diastase-resistant globules), hepatic adenoma, and hepatocellular carcinoma."
    },
    {
        "id": "Ch25_Central_Nervous_System_Pathology",
        "name": "Ch25 Systemic: Central Nervous System Pathology",
        "dirName": "Ch11_Central_Nervous_System_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Cerebrovascular diseases (ischemic stroke timeline, intracerebral hemorrhage, subarachnoid hemorrhage, saccular aneurysms), CNS infections (bacterial, viral, fungal, tuberculous meningitis, encephalitis), neurodegenerative disorders (Alzheimer disease, frontotemporal lobar degeneration, Parkinson disease, Huntington disease, ALS, prion disease), demyelinating diseases (multiple sclerosis), and CNS tumors (glioblastoma, meningioma, oligodendroglioma, schwannoma, pilocytic astrocytoma, medulloblastoma, ependymoma, craniopharyngioma)."
    },
    {
        "id": "Ch26_Hematopoietic_Pathology_Leukemias_and_Lymphomas",
        "name": "Ch26 Systemic: Hematopoietic Pathology (Leukemias & Lymphomas)",
        "dirName": "Ch12_Hematopoietic_Pathology_Leukemias_and_Lymphomas",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Acute leukemias (ALL vs AML, Auer rods, t(15;17) APL), myeloproliferative neoplasms (CML, polycythemia vera, essential thrombocythemia, primary myelofibrosis, JAK2/BCR-ABL1), myelodysplastic syndromes, Hodgkin lymphoma (Reed-Sternberg cells, classical subtypes), Non-Hodgkin lymphomas (diffuse large B-cell, follicular, Burkitt, mantle cell, marginal zone, adult T-cell, mycosis fungoides), and plasma cell dyscrasias (multiple myeloma, MGUS, Waldenstrom macroglobulinemia)."
    },
    {
        "id": "Ch27_Female_Genital_Pathology",
        "name": "Ch27 Systemic: Female Genital Pathology",
        "dirName": "Ch13_Female_Genital_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Vulvar and vaginal pathology (lichen sclerosus, lichen simplex chronicus, VIN/squamous carcinoma, extramammary Paget disease, clear cell adenocarcinoma), cervical pathology (HPV 16/18, CIN, cervical cancer, screening), uterine pathology (endometritis, adenomyosis, endometriosis, endometrial hyperplasia, endometrial carcinoma, leiomyoma, leiomyosarcoma), ovarian pathology (surface epithelial tumors, germ cell tumors/teratoma, sex cord-stromal tumors/granulosa cell tumor, Krukenberg tumor), and gestational pathology (hydatidiform mole, choriocarcinoma, preeclampsia)."
    },
    {
        "id": "Ch28_Breast_Pathology",
        "name": "Ch28 Systemic: Breast Pathology",
        "dirName": "Ch14_Breast_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Benign breast conditions (fibrocystic changes, fibroadenoma, phyllodes tumor, intraductal papilloma, acute mastitis, fat necrosis), noninvasive carcinoma (ductal carcinoma in situ/DCIS, lobular carcinoma in situ/LCIS, Paget disease of breast), invasive breast carcinoma (invasive ductal carcinoma, invasive lobular carcinoma, medullary, inflammatory breast cancer), and molecular subtypes (ER/PR+, HER2+, triple-negative, BRCA1/BRCA2)."
    },
    {
        "id": "Ch29_Male_Genital_Pathology",
        "name": "Ch29 Systemic: Male Genital Pathology",
        "dirName": "Ch15_Male_Genital_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Penile pathology (hypospadias, epispadias, phimosis, condyloma acuminatum, Bowen disease, erythroplasia of Queyrat, squamous cell carcinoma), testicular pathology (cryptorchidism, orchitis, testicular torsion, hydrocele/varicocele/spermatocele), testicular germ cell tumors (seminoma, embryonal carcinoma, yolk sac tumor/Schiller-Duval, choriocarcinoma, teratoma), testicular non-germ cell tumors (Leydig cell, Sertoli cell), and prostate pathology (acute/chronic prostatitis, benign prostatic hyperplasia, prostate adenocarcinoma, Gleason scoring, PSA)."
    },
    {
        "id": "Ch30_Endocrine_Pathology",
        "name": "Ch30 Systemic: Endocrine Pathology",
        "dirName": "Ch16_Endocrine_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Pituitary disorders (pituitary adenomas, prolactinoma, acromegaly, Cushing disease, hypopituitarism, Sheehan syndrome), thyroid disorders (hyperthyroidism/Graves, hypothyroidism/Hashimoto, subacute thyroiditis, Riedel thyroiditis, thyroid nodules, papillary/follicular/medullary/anaplastic carcinoma), parathyroid disorders (primary/secondary/tertiary hyperparathyroidism, hypoparathyroidism, pseudohypoparathyroidism), and adrenal disorders (Cushing syndrome, primary aldosteronism/Conn, adrenal insufficiency/Addison, congenital adrenal hyperplasia, pheochromocytoma, neuroblastoma)."
    },
    {
        "id": "Ch31_Bone_Pathology",
        "name": "Ch31 Systemic: Bone Pathology",
        "dirName": "Ch17_Bone_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Metabolic bone disorders (osteoporosis, osteomalacia/rickets, Paget disease of bone/osteitis deformans, renal osteodystrophy), osteomyelitis (Staph aureus, Salmonella in sickle cell, Pott disease), avascular necrosis, bone tumors (osteochondroma, osteoma, osteoid osteoma/osteoblastoma, giant cell tumor, osteosarcoma, chondrosarcoma, Ewing sarcoma), and skeletal dysplasias (achondroplasia, osteogenesis imperfecta)."
    },
    {
        "id": "Ch32_Joint_and_Soft_Tissue_Pathology",
        "name": "Ch32 Systemic: Joint & Soft Tissue Pathology",
        "dirName": "Ch18_Joint_and_Soft_Tissue_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Arthritides: osteoarthritis (Heberden/Bouchard nodes), rheumatoid arthritis (pannus, HLA-DR4, anti-CCP, subcutaneous nodules), seronegative spondyloarthropathies (ankylosing spondylitis, reactive arthritis, psoriatic arthritis, IBD-associated, HLA-B27), crystal arthropathies (gout/monosodium urate, pseudogout/calcium pyrophosphate), infectious/septic arthritis, and soft tissue tumors (lipoma/liposarcoma, rhabdomyoma/rhabdomyosarcoma, synovial sarcoma)."
    },
    {
        "id": "Ch33_Peripheral_Nerve_and_Muscle_Pathology",
        "name": "Ch33 Systemic: Peripheral Nerve & Muscle Pathology",
        "dirName": "Ch19_Peripheral_Nerve_and_Muscle_Pathology",
        "baseDir": SYSTEMIC_PATHOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Peripheral neuropathies (diabetic neuropathy, Guillain-Barre syndrome, Charcot-Marie-Tooth disease, toxic neuropathies), neuromuscular junction disorders (myasthenia gravis vs Lambert-Eaton syndrome, botulism), inflammatory myopathies (polymyositis, dermatomyositis, inclusion body myositis), muscular dystrophies (Duchenne vs Becker, dystrophin mutations), and rhabdomyolysis."
    }
]

PHARMACOLOGY_CHAPTERS = [
    {
        "id": "Ch01_General_Principles_Pharmacokinetics_and_Pharmacodynamics",
        "name": "Ch01 General Principles: Pharmacokinetics & Pharmacodynamics",
        "dirName": "Ch01_General_Principles_Pharmacokinetics_and_Pharmacodynamics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Pharmacokinetics (pKa, Henderson-Hasselbalch, bioavailability, Vd, clearance, half-life) and pharmacodynamics (receptors, dose-response, agonism, antagonism)."
    },
    {
        "id": "Ch02_Autonomic_Pharmacology",
        "name": "Ch02 Autonomic Pharmacology: Cholinergic & Adrenergic Systems",
        "dirName": "Ch02_Autonomic_Pharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Cholinergic and adrenergic neurotransmission, receptor subtypes (alpha, beta, muscarinic, nicotinic), direct and indirect agonists, antagonists, and autonomic toxidromes."
    },
    {
        "id": "Ch03_Cardiovascular_and_Renal_Pharmacology",
        "name": "Ch03 Cardiovascular and Renal Pharmacology",
        "dirName": "Ch03_Cardiovascular_and_Renal_Pharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Antihypertensives, diuretics, antiarrhythmics (Classes I-IV), heart failure therapeutics (RAAS inhibitors, inotropes, beta-blockers), antianginals, and lipid-lowering agents."
    },
    {
        "id": "Ch04_Central_Nervous_System_Pharmacology_and_Psychopharmacology",
        "name": "Ch04 CNS Pharmacology & Psychopharmacology",
        "dirName": "Ch04_Central_Nervous_System_Pharmacology_and_Psychopharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Sedative-hypnotics, anxiolytics, antidepressants, antipsychotics, mood stabilizers, antiepileptics, neurodegenerative therapeutics, and anesthetics."
    },
    {
        "id": "Ch05_Antimicrobial_Pharmacology",
        "name": "Ch05 Antimicrobial Pharmacology",
        "dirName": "Ch05_Antimicrobial_Pharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Bacterial cell wall synthesis inhibitors, ribosomal protein synthesis inhibitors, fluoroquinolones, antimetabolites, antimycobacterials, antifungals, and antivirals/HIV ART."
    },
    {
        "id": "Ch06_Inflammatory_Autacoid_Pulmonary_and_GI_Pharmacology",
        "name": "Ch06 Inflammatory, Autacoid, Pulmonary & GI Pharmacology",
        "dirName": "Ch06_Inflammatory_Autacoid_Pulmonary_and_GI_Pharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "NSAIDs, acetaminophen, gout agents, eicosanoids, antihistamines, asthma/COPD bronchodilators, and gastrointestinal therapeutics."
    },
    {
        "id": "Ch07_Hematologic_Pharmacology_Anticoagulants_and_Antiplatelets",
        "name": "Ch07 Hematologic Pharmacology: Anticoagulants, Antiplatelets & Thrombolytics",
        "dirName": "Ch07_Hematologic_Pharmacology_Anticoagulants_and_Antiplatelets",
        "totalQuestions": 150,
        "status": "active",
        "description": "Parenteral anticoagulants, oral anticoagulants (warfarin, DOACs), antiplatelet therapies, thrombolytics, reversal agents, and hematopoietic growth factors."
    },
    {
        "id": "Ch08_Endocrine_and_Metabolic_Pharmacology",
        "name": "Ch08 Endocrine and Metabolic Pharmacology",
        "dirName": "Ch08_Endocrine_and_Metabolic_Pharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Insulins and oral hypoglycemic agents, thyroid/antithyroid drugs, corticosteroids, sex steroids/modulators, bone mineral homeostasis, and hypothalamic/pituitary analogs."
    },
    {
        "id": "Ch09_Anticancer_Immunosuppressant_and_Toxicology",
        "name": "Ch09 Anticancer Drugs, Immunosuppressants & Clinical Toxicology",
        "dirName": "Ch09_Anticancer_Immunosuppressant_and_Toxicology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Cytotoxic antineoplastics, targeted small molecule inhibitors, immunosuppressive pharmacotherapy, heavy metal chelators, and acute clinical antidotes."
    },
    {
        "id": "Ch10_Clinical_Toxicology_and_Antidotes",
        "name": "Ch10 Clinical Toxicology and Specific Antidotes",
        "dirName": "Ch01_Clinical_Toxicology_and_Antidotes",
        "baseDir": ADV_PHARM_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Clinical toxic syndromes (cholinergic, anticholinergic, sympathomimetic, opioid, sedative-hypnotic), acute poisoning management, specific antidotes (naloxone, flumazenil, N-acetylcysteine, atropine/pralidoxime, digibind, deferoxamine, dimercaprol, calcium disodium EDTA, methylene blue, sodium thiosulfate/nitrites, fomepizole, glucagon, physostigmine), and toxic alcohols (methanol, ethylene glycol)."
    },
    {
        "id": "Ch11_CYP450_Interactions_and_Pharmacogenomics",
        "name": "Ch11 CYP450 Drug Interactions & Pharmacogenomics",
        "dirName": "Ch02_CYP450_Interactions_and_Pharmacogenomics",
        "baseDir": ADV_PHARM_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Cytochrome P450 enzyme inducers and inhibitors (CYP3A4, CYP2D6, CYP2C9, CYP2C19, CYP1A2), clinically significant drug-drug interactions, pharmacogenomic variants (slow vs fast acetylators/NAT2, CYP2D6 poor/ultrarapid metabolizers, TPMT deficiency and thiopurines, VKORC1/CYP2C9 polymorphisms and warfarin dosing, HLA-B*5701 and abacavir, HLA-B*1502 and carbamazepine)."
    },
    {
        "id": "Ch12_Chemotherapy_Immunosuppressant_Toxicities_and_Rescue",
        "name": "Ch12 Chemotherapy & Immunosuppressant Toxicities and Rescue",
        "dirName": "Ch03_Chemotherapy_Immunosuppressant_Toxicities_and_Rescue",
        "baseDir": ADV_PHARM_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Chemotherapy drug-specific organ toxicities and rescue strategies (doxorubicin cardiotoxicity and dexrazoxane, cyclophosphamide/ifosfamide hemorrhagic cystitis and mesna, methotrexate myelosuppression and leucovorin rescue, cisplatin nephro/ototoxicity and amifostine, bleomycin pulmonary fibrosis, vincristine peripheral neuropathy), and immunosuppressant toxicities (calcineurin inhibitors/cyclosporine/tacrolimus nephrotoxicity, mTOR inhibitors, antimetabolites)."
    }
]

BIOCHEMISTRY_CHAPTERS = [
    {
        "id": "Ch01_Nucleic_Acid_Structure_and_Organization",
        "name": "Ch01 Nucleic Acid Structure and Organization",
        "dirName": "Ch01_Nucleic_Acid_Structure_and_Organization",
        "totalQuestions": 150,
        "status": "active",
        "description": "Nucleic acid structure, nucleotide bases, B-DNA double helix, nucleosome octamers, histone modifications, and euchromatin vs. heterochromatin."
    },
    {
        "id": "Ch02_DNA_Replication_and_Repair",
        "name": "Ch02 DNA Replication and Repair",
        "dirName": "Ch02_DNA_Replication_and_Repair",
        "totalQuestions": 150,
        "status": "active",
        "description": "DNA replication machinery, telomerase, mismatch repair, base excision repair, nucleotide excision repair (xeroderma pigmentosum), and double-strand break repair."
    },
    {
        "id": "Ch03_Transcription_and_RNA_Processing",
        "name": "Ch03 Transcription and RNA Processing",
        "dirName": "Ch03_Transcription_and_RNA_Processing",
        "totalQuestions": 150,
        "status": "active",
        "description": "RNA polymerases (I, II, III), promoter elements, mRNA 5' capping, polyadenylation, spliceosome dynamics, alternative splicing, and transcriptional toxins."
    },
    {
        "id": "Ch04_Genetic_Code_Mutations_and_Translation",
        "name": "Ch04 Genetic Code, Mutations, and Translation",
        "dirName": "Ch04_Genetic_Code_Mutations_and_Translation",
        "totalQuestions": 150,
        "status": "active",
        "description": "Genetic code properties, point mutations (missense, nonsense, frameshift), tRNA aminoacylation, translation initiation/elongation, and ribosomal toxin/antibiotic targets."
    },
    {
        "id": "Ch05_Regulation_of_Eukaryotic_Gene_Expression",
        "name": "Ch05 Regulation of Eukaryotic Gene Expression",
        "dirName": "Ch05_Regulation_of_Eukaryotic_Gene_Expression",
        "totalQuestions": 150,
        "status": "active",
        "description": "Cis-acting elements (enhancers/silencers), trans-acting transcription factor domains, CpG island methylation, genomic imprinting (Prader-Willi and Angelman syndromes), and microRNAs."
    },
    {
        "id": "Ch06_Genetic_Strategies_in_Therapeutics",
        "name": "Ch06 Genetic Strategies in Therapeutics",
        "dirName": "Ch06_Genetic_Strategies_in_Therapeutics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Recombinant DNA molecular tools, restriction endonucleases, plasmids, cDNA libraries, CRISPR-Cas9 genome editing, and gene replacement therapies."
    },
    {
        "id": "Ch07_Techniques_of_Genetic_Analysis",
        "name": "Ch07 Techniques of Genetic Analysis",
        "dirName": "Ch07_Techniques_of_Genetic_Analysis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Blotting techniques (Southern, Northern, Western), PCR, Sanger vs Next-Generation Sequencing, microarrays, ELISA, flow cytometry, and FISH."
    },
    {
        "id": "Ch08_Amino_Acids_Proteins_and_Enzymes",
        "name": "Ch08 Amino Acids, Proteins, and Enzymes",
        "dirName": "Ch08_Amino_Acids_Proteins_and_Enzymes",
        "totalQuestions": 150,
        "status": "active",
        "description": "Amino acid classification and charge titration (pKa/pI), primary to quaternary protein structure, enzyme kinetics (Michaelis-Menten, Lineweaver-Burk), and enzyme inhibition."
    },
    {
        "id": "Ch09_Hormones_and_Signal_Transduction",
        "name": "Ch09 Hormones and Signal Transduction",
        "dirName": "Ch09_Hormones_and_Signal_Transduction",
        "totalQuestions": 150,
        "status": "active",
        "description": "Transmembrane receptors and second messenger pathways: Gs/Gi-cAMP-PKA, Gq-IP3/DAG/calcium, receptor tyrosine kinases (MAPK, PI3K/Akt), and intracellular nuclear receptors."
    },
    {
        "id": "Ch10_Vitamins_Water_and_Fat_Soluble",
        "name": "Ch10 Vitamins: Water- and Fat-Soluble",
        "dirName": "Ch10_Vitamins_Water_and_Fat_Soluble",
        "totalQuestions": 150,
        "status": "active",
        "description": "Water-soluble vitamins (B-complex and vitamin C) and fat-soluble vitamins (A, D, E, K), biochemical coenzyme functions, and deficiency/toxicity manifestations."
    },
    {
        "id": "Ch11_Energy_Metabolism_and_Fuel_Homeostasis",
        "name": "Ch11 Energy Metabolism and Fuel Homeostasis",
        "dirName": "Ch11_Energy_Metabolism_and_Fuel_Homeostasis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Thermodynamics and high-energy phosphates, metabolic adaptations across the fed, fasting, and starved states, and hormonal counter-regulation."
    },
    {
        "id": "Ch12_Glycolysis_and_Pyruvate_Dehydrogenase",
        "name": "Ch12 Glycolysis and Pyruvate Dehydrogenase",
        "dirName": "Ch12_Glycolysis_and_Pyruvate_Dehydrogenase",
        "totalQuestions": 150,
        "status": "active",
        "description": "Glycolytic enzymatic steps, regulatory checkpoints (hexokinase, PFK-1, pyruvate kinase), 2,3-BPG shunt, pyruvate dehydrogenase complex, and lactic acidosis."
    },
    {
        "id": "Ch13_Citric_Acid_Cycle_and_Oxidative_Phosphorylation",
        "name": "Ch13 Citric Acid Cycle and Oxidative Phosphorylation",
        "dirName": "Ch13_Citric_Acid_Cycle_and_Oxidative_Phosphorylation",
        "totalQuestions": 150,
        "status": "active",
        "description": "Mitochondrial TCA cycle reactions, electron transport chain complexes (I-IV), ATP synthase, uncouplers, and ETC inhibitors."
    },
    {
        "id": "Ch14_Glycogen_Gluconeogenesis_and_HMP_Shunt",
        "name": "Ch14 Glycogen, Gluconeogenesis, and Hexose Monophosphate Shunt",
        "dirName": "Ch14_Glycogen_Gluconeogenesis_and_HMP_Shunt",
        "totalQuestions": 150,
        "status": "active",
        "description": "Glycogen synthesis and degradation, glycogen storage diseases (types I-V), gluconeogenic substrate flows, and the pentose phosphate pathway (G6PD deficiency)."
    },
    {
        "id": "Ch15_Lipid_Synthesis_and_Storage",
        "name": "Ch15 Lipid Synthesis and Storage",
        "dirName": "Ch15_Lipid_Synthesis_and_Storage",
        "totalQuestions": 150,
        "status": "active",
        "description": "De novo fatty acid synthesis, triglyceride storage, cholesterol biosynthesis (HMG-CoA reductase), and lipoprotein metabolism (chylomicrons, VLDL, LDL, HDL, hyperlipidemias)."
    },
    {
        "id": "Ch16_Lipid_Mobilization_and_Catabolism",
        "name": "Ch16 Lipid Mobilization and Catabolism",
        "dirName": "Ch16_Lipid_Mobilization_and_Catabolism",
        "totalQuestions": 150,
        "status": "active",
        "description": "Hormone-sensitive lipase, carnitine shuttle, beta-oxidation, systemic carnitine deficiency, MCAD deficiency, ketone body metabolism, and lysosomal sphingolipidoses."
    },
    {
        "id": "Ch17_Amino_Acid_Metabolism",
        "name": "Ch17 Amino Acid Metabolism",
        "dirName": "Ch17_Amino_Acid_Metabolism",
        "totalQuestions": 150,
        "status": "active",
        "description": "Transamination and oxidative deamination, urea cycle disorders, branched-chain amino acid catabolism (MSUD), phenylketonuria (PKU), alkaptonuria, and homocystinuria."
    },
    {
        "id": "Ch18_Purine_and_Pyrimidine_Metabolism",
        "name": "Ch18 Purine and Pyrimidine Metabolism",
        "dirName": "Ch18_Purine_and_Pyrimidine_Metabolism",
        "totalQuestions": 150,
        "status": "active",
        "description": "De novo purine and pyrimidine biosynthesis, purine salvage pathways (HGPRT/Lesch-Nyhan syndrome, ADA/SCID), gout, orotic aciduria, and antimetabolite chemotherapeutic targets."
    },
    {
        "id": "Ch19_Medical_Genetics_Single_Gene_Disorders",
        "name": "Ch19 Single-Gene Disorders and Non-Mendelian Inheritance",
        "dirName": "Ch19_Medical_Genetics_Single_Gene_Disorders",
        "totalQuestions": 150,
        "status": "active",
        "description": "Mendelian inheritance patterns (autosomal dominant, autosomal recessive, X-linked), incomplete penetrance, variable expressivity, pleiotropy, anticipation, and mosaicism."
    },
    {
        "id": "Ch20_Medical_Genetics_Population_Genetics",
        "name": "Ch20 Population Genetics and Hardy-Weinberg Equilibrium",
        "dirName": "Ch20_Medical_Genetics_Population_Genetics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Hardy-Weinberg equilibrium, carrier frequency calculations, genetic drift, founder effect, natural selection, and balanced polymorphism."
    },
    {
        "id": "Ch21_Medical_Genetics_Cytogenetics",
        "name": "Ch21 Cytogenetics and Chromosomal Disorders",
        "dirName": "Ch21_Medical_Genetics_Cytogenetics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Chromosomal aneuploidies (trisomies 21, 18, 13), sex chromosome aneuploidies (Turner and Klinefelter syndromes), microdeletion syndromes (Cri-du-chat, DiGeorge, Williams), and translocations."
    },
    {
        "id": "Ch22_Medical_Genetics_Recombination_Frequency",
        "name": "Ch22 Recombination Frequency and Genetic Linkage",
        "dirName": "Ch22_Medical_Genetics_Recombination_Frequency",
        "totalQuestions": 150,
        "status": "active",
        "description": "Meiotic crossing-over, genetic recombination frequency, genetic linkage maps (centimorgans), haplotype analysis, and LOD score computation."
    },
    {
        "id": "Ch23_Medical_Genetics_Genetic_Diagnosis",
        "name": "Ch23 Genetic Diagnosis and Molecular Testing Strategies",
        "dirName": "Ch23_Medical_Genetics_Genetic_Diagnosis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Direct genetic testing (ASO, multiplex PCR, direct sequencing) vs indirect linkage diagnosis (RFLP, STR markers), carrier screening, and prenatal diagnostic testing."
    },
    {
        "id": "Ch24_Lysosomal_Storage_and_Peroxisomal_Diseases",
        "name": "Ch24 Lysosomal Storage and Peroxisomal Diseases",
        "dirName": "Ch01_Lysosomal_Storage_and_Peroxisomal_Diseases",
        "baseDir": METABOLIC_GENETICS_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Lysosomal storage diseases: sphingolipidoses (Gaucher disease/glucocerebrosidase, Niemann-Pick/sphingomyelinase, Tay-Sachs/hexosaminidase A, Fabry disease/alpha-galactosidase A, Krabbe disease/galactocerebrosidase, metachromatic leukodystrophy/arylsulfatase A), mucopolysaccharidoses (Hurler vs Hunter syndrome), I-cell disease (phosphotransferase deficiency), and peroxisomal disorders (Zellweger syndrome, X-linked adrenoleukodystrophy, Refsum disease)."
    },
    {
        "id": "Ch25_Micronutrients_Trace_Minerals_and_Nutritional_Syndromes",
        "name": "Ch25 Micronutrients, Trace Minerals & Nutritional Syndromes",
        "dirName": "Ch02_Micronutrients_Trace_Minerals_and_Nutritional_Syndromes",
        "baseDir": METABOLIC_GENETICS_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Fat-soluble vitamins (A, D, E, K deficiencies and toxicities), water-soluble vitamins (thiamine/B1/beriberi/Wernicke-Korsakoff, riboflavin/B2/cheilosis, niacin/B3/pellagra, pantothenic acid/B5, pyridoxine/B6/isoniazid neuropathy, biotin/B7, folate/B9 vs cobalamin/B12, vitamin C/scurvy), trace elements (zinc/acrodermatitis enteropathica, copper/Menkes vs Wilson, iron, selenium, iodine), and severe protein-energy malnutrition (marasmus vs kwashiorkor)."
    }
]

PHYSIOLOGY_CHAPTERS = [
    {
        "id": "Ch01_Fluid_Distribution_and_Edema",
        "name": "Ch01 Fluid Distribution and Edema",
        "dirName": "Ch01_Fluid_Distribution_and_Edema",
        "totalQuestions": 150,
        "status": "active",
        "description": "Fluid compartments, dilution methods, 60-40-20 rule, Darrow-Yannet diagrams, Starling forces, and edema pathophysiology."
    },
    {
        "id": "Ch02_Ionic_Equilibrium_and_RMP",
        "name": "Ch02 Ionic Equilibrium and Resting Membrane Potential",
        "dirName": "Ch02_Ionic_Equilibrium_and_RMP",
        "totalQuestions": 150,
        "status": "active",
        "description": "Nernst equation, Goldman-Hodgkin-Katz equation, electrochemical equilibrium, resting membrane potential, and ion channelopathies."
    },
    {
        "id": "Ch03_Neuron_AP_and_Synaptic_Transmission",
        "name": "Ch03 Neuron Action Potential and Synaptic Transmission",
        "dirName": "Ch03_Neuron_AP_and_Synaptic_Transmission",
        "totalQuestions": 150,
        "status": "active",
        "description": "Voltage-gated sodium/potassium dynamics, electrotonic conduction, myelination, demyelinating pathologies, and neurotransmitter release."
    },
    {
        "id": "Ch04_Electrical_Activity_of_the_Heart",
        "name": "Ch04 Electrical Activity of the Heart",
        "dirName": "Ch04_Electrical_Activity_of_the_Heart",
        "totalQuestions": 150,
        "status": "active",
        "description": "Cardiac action potential phases (fast vs slow response), pacemaker automaticity, refractory periods, ECG leads, and arrhythmogenesis."
    },
    {
        "id": "Ch05_Excitation_Contraction_Coupling",
        "name": "Ch05 Excitation-Contraction Coupling",
        "dirName": "Ch05_Excitation_Contraction_Coupling",
        "totalQuestions": 150,
        "status": "active",
        "description": "DHPR/RyR1 dynamics, calcium-induced calcium release, cross-bridge cycling, smooth muscle calmodulin/MLCK cascade, and malignant hyperthermia."
    },
    {
        "id": "Ch06_Skeletal_Muscle_Mechanics",
        "name": "Ch06 Skeletal Muscle Mechanics",
        "dirName": "Ch06_Skeletal_Muscle_Mechanics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Isometric vs isotonic contraction, length-tension relationship, force-velocity curves, Type I (slow-twitch) vs Type II (fast-twitch) motor units."
    },
    {
        "id": "Ch07_Hemodynamics_and_Vascular_Principles",
        "name": "Ch07 Hemodynamics and Vascular Principles",
        "dirName": "Ch07_Hemodynamics_and_Vascular_Principles",
        "totalQuestions": 150,
        "status": "active",
        "description": "Poiseuille law, vascular resistance (series vs parallel), laminar vs turbulent flow, Reynolds number, and arterial compliance."
    },
    {
        "id": "Ch08_Cardiac_Muscle_Mechanics",
        "name": "Ch08 Cardiac Muscle Mechanics",
        "dirName": "Ch08_Cardiac_Muscle_Mechanics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Frank-Starling law, preload, afterload, inotropy, pressure-volume loops, ejection fraction, and myocardial oxygen consumption (MVO2)."
    },
    {
        "id": "Ch09_CV_Regulation_and_Cardiac_Output",
        "name": "Ch09 Cardiovascular Regulation and Cardiac Output",
        "dirName": "Ch09_CV_Regulation_and_Cardiac_Output",
        "totalQuestions": 150,
        "status": "active",
        "description": "Guyton vascular function curves, cardiac function curves, baroreceptor reflex, Valsalva maneuver, orthostatic reflexes, and RAAS activation."
    },
    {
        "id": "Ch10_Regulation_of_Blood_Flow",
        "name": "Ch10 Regulation of Blood Flow",
        "dirName": "Ch10_Regulation_of_Blood_Flow",
        "totalQuestions": 150,
        "status": "active",
        "description": "Local autoregulation (myogenic & metabolic), coronary, cerebral, renal, pulmonary, and cutaneous microcirculation, and exercise hemodynamics."
    },
    {
        "id": "Ch11_Cardiac_Cycle_and_Valvular_Heart_Disease",
        "name": "Ch11 Cardiac Cycle and Valvular Heart Disease",
        "dirName": "Ch11_Cardiac_Cycle_and_Valvular_Heart_Disease",
        "totalQuestions": 150,
        "status": "active",
        "description": "Wiggers diagram, jugular venous pulse (JVP) waves, heart sounds (S1-S4, clicks, snaps), and valvular murmurs with dynamic maneuvers."
    },
    {
        "id": "Ch12_Lung_Mechanics",
        "name": "Ch12 Lung Mechanics",
        "dirName": "Ch12_Lung_Mechanics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Lung & chest wall compliance, intrapleural pressure, surfactant & Laplace law, airway resistance, dynamic airway compression, and work of breathing."
    },
    {
        "id": "Ch13_Alveolar_Blood_Gas_Exchange",
        "name": "Ch13 Alveolar-Blood Gas Exchange",
        "dirName": "Ch13_Alveolar_Blood_Gas_Exchange",
        "totalQuestions": 150,
        "status": "active",
        "description": "Fick law of diffusion, alveolar-capillary barrier, diffusing capacity (DLCO), diffusion-limited vs perfusion-limited gas exchange."
    },
    {
        "id": "Ch14_O2_CO2_Transport_and_Ventilation_Regulation",
        "name": "Ch14 O2 and CO2 Transport and Ventilation Regulation",
        "dirName": "Ch14_O2_CO2_Transport_and_Ventilation_Regulation",
        "totalQuestions": 150,
        "status": "active",
        "description": "Oxygen-hemoglobin dissociation curve, Bohr & Haldane effects, 2,3-BPG, CO poisoning, methemoglobinemia, central/peripheral chemoreceptors, and respiratory pacemakers."
    },
    {
        "id": "Ch15_V_Q_Matching_and_Hypoxemia",
        "name": "Ch15 Ventilation-Perfusion Matching and Hypoxemia",
        "dirName": "Ch15_V_Q_Matching_and_Hypoxemia",
        "totalQuestions": 150,
        "status": "active",
        "description": "V/Q ratio regional distribution, physiological shunt vs dead space, alveolar gas equation, A-a gradient calculation, and differential diagnosis of hypoxemia."
    },
    {
        "id": "Ch16_Renal_Structure_and_GFR",
        "name": "Ch16 Renal Structure and Glomerular Filtration",
        "dirName": "Ch16_Renal_Structure_and_GFR",
        "totalQuestions": 150,
        "status": "active",
        "description": "Glomerular filtration barrier charge/size selectivity, net filtration pressure, Starling forces, afferent/efferent arteriolar resistance, and GFR autoregulation."
    },
    {
        "id": "Ch17_Solute_Transport_Reabsorption_Secretion",
        "name": "Ch17 Solute Transport: Reabsorption and Secretion",
        "dirName": "Ch17_Solute_Transport_Reabsorption_Secretion",
        "totalQuestions": 150,
        "status": "active",
        "description": "Proximal tubular transport, primary vs secondary active transport, glucose titration curve, transport maximum (Tm), splay, and organic ion secretion."
    },
    {
        "id": "Ch18_Clinical_Estimation_of_GFR_and_Clearance",
        "name": "Ch18 Clinical Estimation of GFR and Clearance",
        "dirName": "Ch18_Clinical_Estimation_of_GFR_and_Clearance",
        "totalQuestions": 150,
        "status": "active",
        "description": "Renal clearance formulas, inulin & creatinine clearance, PAH clearance for effective RPF, filtration fraction, and free water clearance."
    },
    {
        "id": "Ch19_Regional_Transport_along_Nephron",
        "name": "Ch19 Regional Transport along the Nephron",
        "dirName": "Ch19_Regional_Transport_along_Nephron",
        "totalQuestions": 150,
        "status": "active",
        "description": "NKCC2 in thick ascending limb, NCCT in DCT, ENaC & ROMK in principal cells, intercalated cells, countercurrent multiplication, and diuretic pharmacology."
    },
    {
        "id": "Ch20_Acid_Base_Regulation_and_Disorders",
        "name": "Ch20 Acid-Base Regulation and Disorders",
        "dirName": "Ch20_Acid_Base_Regulation_and_Disorders",
        "totalQuestions": 150,
        "status": "active",
        "description": "Bicarbonate/ammonium renal handling, Davenport diagrams, anion gap metabolic acidosis (GOLDMARK), Winter formula compensation, and mixed acid-base disorders."
    },
    {
        "id": "Ch21_General_Endocrine_Principles",
        "name": "Ch21 General Endocrine Principles",
        "dirName": "Ch21_General_Endocrine_Principles",
        "totalQuestions": 150,
        "status": "active",
        "description": "Peptide vs steroid vs amine hormones, second messenger pathways (cAMP/PKA, IP3/DAG/Ca2+, cGMP, JAK-STAT), and negative/positive feedback regulation."
    },
    {
        "id": "Ch22_Hypothalamic_Anterior_Pituitary_System",
        "name": "Ch22 Hypothalamic-Anterior Pituitary System",
        "dirName": "Ch22_Hypothalamic_Anterior_Pituitary_System",
        "totalQuestions": 150,
        "status": "active",
        "description": "Hypophyseal portal system, trophic hormone axes (TRH-TSH, CRH-ACTH, GnRH-LH/FSH), prolactin regulation, dopamine inhibition, and pituitary adenomas."
    },
    {
        "id": "Ch23_Posterior_Pituitary",
        "name": "Ch23 Posterior Pituitary",
        "dirName": "Ch23_Posterior_Pituitary",
        "totalQuestions": 150,
        "status": "active",
        "description": "Supraoptic and paraventricular nuclei, ADH (V1/V2 receptors), oxytocin, plasma osmolality vs volume regulation, diabetes insipidus, and SIADH."
    },
    {
        "id": "Ch24_Adrenal_Cortex",
        "name": "Ch24 Adrenal Cortex",
        "dirName": "Ch24_Adrenal_Cortex",
        "totalQuestions": 150,
        "status": "active",
        "description": "Adrenal zonation (GFR - salt, sugar, sex), steroidogenic enzyme pathways, congenital adrenal hyperplasias (21, 11-beta, 17-alpha deficiencies), Cushing syndrome, and Addison disease."
    },
    {
        "id": "Ch25_Adrenal_Medulla_and_Catecholamines",
        "name": "Ch25 Adrenal Medulla and Catecholamines",
        "dirName": "Ch25_Adrenal_Medulla_and_Catecholamines",
        "totalQuestions": 150,
        "status": "active",
        "description": "Chromaffin cells, PNMT cortisol induction, catecholamine synthesis/degradation (MAO/COMT to VMA/metanephrines), pheochromocytoma, and adrenergic receptor physiology."
    },
    {
        "id": "Ch26_Endocrine_Pancreas_and_Glucose_Homeostasis",
        "name": "Ch26 Endocrine Pancreas and Glucose Homeostasis",
        "dirName": "Ch26_Endocrine_Pancreas_and_Glucose_Homeostasis",
        "totalQuestions": 150,
        "status": "active",
        "description": "Beta cell SUR1/K-ATP channel insulin exocytosis, GLUT-4 translocation, glucagon counter-regulation, somatostatin, somatostatinoma, and insulinoma."
    },
    {
        "id": "Ch27_Calcium_and_Phosphate_Hormonal_Control",
        "name": "Ch27 Calcium and Phosphate Hormonal Control",
        "dirName": "Ch27_Calcium_and_Phosphate_Hormonal_Control",
        "totalQuestions": 150,
        "status": "active",
        "description": "Parathyroid hormone (PTH), 1,25-(OH)2D3 activation, calcitonin, FGF23/Klotho axis, CaSR signaling, hypercalcemia vs hypocalcemia, and metabolic bone disorders."
    },
    {
        "id": "Ch28_Thyroid_Hormone_Physiology",
        "name": "Ch28 Thyroid Hormone Physiology",
        "dirName": "Ch28_Thyroid_Hormone_Physiology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Iodide trapping, thyroid peroxidase (organification & coupling), TBG binding, peripheral 5'-deiodinase (T4 to T3 conversion), and metabolic rate actions."
    },
    {
        "id": "Ch29_Growth_GH_and_Puberty",
        "name": "Ch29 Growth Hormone, IGF-1, and Puberty",
        "dirName": "Ch29_Growth_GH_and_Puberty",
        "totalQuestions": 150,
        "status": "active",
        "description": "GHRH and somatostatin regulation, pulsatile GH secretion, hepatic IGF-1 generation, epiphyseal plate growth, Tanner staging, and pubertal endocrine transitions."
    },
    {
        "id": "Ch30_Male_Reproductive_Physiology",
        "name": "Ch30 Male Reproductive Physiology",
        "dirName": "Ch30_Male_Reproductive_Physiology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Hypothalamic-pituitary-gonadal axis, LH stimulation of Leydig cells (testosterone), FSH stimulation of Sertoli cells (spermatogenesis & inhibin B), and DHT 5-alpha reductase."
    },
    {
        "id": "Ch31_Female_Reproductive_Physiology",
        "name": "Ch31 Female Reproductive Physiology",
        "dirName": "Ch31_Female_Reproductive_Physiology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Two-cell two-gonadotropin model (theca LH & granulosa FSH), follicular/luteal phases, LH surge positive feedback, endometrial cycle, and pregnancy hCG."
    },
    {
        "id": "Ch32_Gastrointestinal_Overview_and_Motility",
        "name": "Ch32 Gastrointestinal Overview and Motility",
        "dirName": "Ch32_Gastrointestinal_Overview_and_Motility",
        "totalQuestions": 150,
        "status": "active",
        "description": "Interstitial cells of Cajal, slow waves, enteric nervous system (Auerbach & Meissner plexuses), esophageal peristalsis, lower esophageal sphincter, and migrating motor complex (MMC)."
    },
    {
        "id": "Ch33_Gastrointestinal_Secretions",
        "name": "Ch33 Gastrointestinal Secretions",
        "dirName": "Ch33_Gastrointestinal_Secretions",
        "totalQuestions": 150,
        "status": "active",
        "description": "Gastric parietal cell H+/K+-ATPase (gastrin, histamine, ACh stimulation), somatostatin inhibition, pancreatic acinar vs ductal HCO3- secretion, and bile acid enterohepatic circulation."
    },
    {
        "id": "Ch34_Gastrointestinal_Digestion_and_Absorption",
        "name": "Ch34 Gastrointestinal Digestion and Absorption",
        "dirName": "Ch34_Gastrointestinal_Digestion_and_Absorption",
        "totalQuestions": 150,
        "status": "active",
        "description": "Luminal & brush border carbohydrate digestion (SGLT1, GLUT5, GLUT2), protein digestion & peptide transport, lipid micelle absorption & chylomicron formation, and vitamin/mineral uptake."
    },
    {
        "id": "Ch35_Exercise_Physiology_and_Extreme_Environment_Acclimatization",
        "name": "Ch35 Exercise Physiology & Environmental Acclimatization",
        "dirName": "Ch01_Exercise_Physiology_and_Extreme_Environment_Acclimatization",
        "baseDir": EXERCISE_PHYSIOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Acute and chronic physiological adaptations to exercise (VO2 max, cardiac output, arteriovenous oxygen difference, sympathetic activation, glycogen depletion, lactic acidosis, ventilation changes), high-altitude acclimatization (hypoxic pulmonary vasoconstriction, acute mountain sickness, erythropoietin production, 2,3-BPG elevation, respiratory alkalosis), hyperbaric physiology (decompression sickness, nitrogen narcosis), and thermoregulation (heat exhaustion vs heat stroke, hypothermia, frostbite)."
    }
]

ANATOMY_CHAPTERS = [
    {
        "id": "Ch01_Gonad_Development",
        "name": "Ch01 Early Embryology: Gonad Development",
        "dirName": "Ch01_Gonad_Development",
        "totalQuestions": 150,
        "status": "active",
        "description": "Sex determination, SRY/TDF, mesonephric vs paramesonephric duct differentiation, external genitalia development, and disorders of sex development."
    },
    {
        "id": "Ch02_First_8_Weeks_of_Development",
        "name": "Ch02 Early Embryology: First 8 Weeks of Development",
        "dirName": "Ch02_First_8_Weeks_of_Development",
        "totalQuestions": 150,
        "status": "active",
        "description": "Fertilization, blastocyst implantation, gastrulation, notochord induction, trilaminar germ disc derivatives, fetal membranes, and teratogen critical windows."
    },
    {
        "id": "Ch03_Histology_Epithelia",
        "name": "Ch03 Histology: Epithelia and Cellular Junctions",
        "dirName": "Ch03_Histology_Epithelia",
        "totalQuestions": 150,
        "status": "active",
        "description": "Simple, stratified, transitional, and pseudostratified epithelia, metaplasia (Barrett esophagus), tight junctions, desmosomes, hemidesmosomes, basement membrane collagen IV, and ciliary axonemes."
    },
    {
        "id": "Ch04_Back_and_Autonomic_Nervous_System",
        "name": "Ch04 Gross Anatomy: Vertebral Column, Back and ANS",
        "dirName": "Ch04_Back_and_Autonomic_Nervous_System",
        "totalQuestions": 150,
        "status": "active",
        "description": "Vertebral column osteology, herniated intervertebral discs (L4-L5 vs L5-S1), lumbar puncture layers (L3-L5), deep back musculature, suboccipital triangle, sympathetic trunk (Horner syndrome), parasympathetics, and visceral referred pain mechanisms."
    },
    {
        "id": "Ch05_Thorax",
        "name": "Ch05 Gross Anatomy: Thorax",
        "dirName": "Ch05_Thorax",
        "totalQuestions": 150,
        "status": "active",
        "description": "Thoracic wall intercostal neurovascular bundles (VAN), thoracentesis safety margins, carina (T4/T5), foreign body aspiration anatomy, mediastinal masses (4 Ts), pericardial sinuses, coronary artery dominance, and conduction system."
    },
    {
        "id": "Ch06_Abdomen_Pelvis_and_Perineum",
        "name": "Ch06 Gross Anatomy: Abdomen, Pelvis, and Perineum",
        "dirName": "Ch06_Abdomen_Pelvis_and_Perineum",
        "totalQuestions": 150,
        "status": "active",
        "description": "Rectus sheath arcuate line, direct vs indirect inguinal hernia (Hesselbach triangle, inferior epigastric vessels), retroperitoneal organs (SAD PUCKER), celiac trunk, SMA/IMA territories, mesenteric ischemia, portal hypertension portocaval anastomoses, ureter course, and pectinate line landmarks."
    },
    {
        "id": "Ch07_Upper_Limb",
        "name": "Ch07 Gross Anatomy: Upper Limb",
        "dirName": "Ch07_Upper_Limb",
        "totalQuestions": 150,
        "status": "active",
        "description": "Brachial plexus (roots, trunks, cords, branches), Erb-Duchenne palsy (waiter's tip), Klumpke palsy, rotator cuff muscles (SITS), radial nerve injury (wrist drop), median nerve entrapment (carpal tunnel, pope's blessing), ulnar nerve injury (claw hand), and scaphoid fracture avascular necrosis."
    },
    {
        "id": "Ch08_Lower_Limb",
        "name": "Ch08 Gross Anatomy: Lower Limb",
        "dirName": "Ch08_Lower_Limb",
        "totalQuestions": 150,
        "status": "active",
        "description": "Femoral nerve, obturator nerve, superior gluteal nerve (Trendelenburg sign), inferior gluteal nerve, sciatic nerve, femoral triangle (NAVEL), knee ligament and meniscal tears (unhappy triad), and common fibular/peroneal nerve injury (foot drop)."
    },
    {
        "id": "Ch09_Head_and_Neck",
        "name": "Ch09 Gross Anatomy: Head and Neck",
        "dirName": "Ch09_Head_and_Neck",
        "totalQuestions": 150,
        "status": "active",
        "description": "Skull base foramina and cranial nerve exits (CN I-XII), cavernous sinus thrombosis, cervical triangles, fascial planes and mediastinitis spread, thyroid neurovascular relations (superior/recurrent laryngeal nerves), pharyngeal arch/pouch/cleft derivatives, extraocular muscles, and salivary gland autonomic innervation."
    },
    {
        "id": "Ch10_Nervous_System_Organization_and_Development",
        "name": "Ch10 Neuroscience: Nervous System Organization & Development",
        "dirName": "Ch10_Nervous_System_Organization_and_Development",
        "totalQuestions": 150,
        "status": "active",
        "description": "Neural tube induction and neurulation, neural tube defects (anencephaly, spina bifida, maternal folate), primary and secondary brain vesicles, Chiari malformations, Dandy-Walker malformation, neural crest cell migration, and neurocristopathies (Hirschsprung disease, neurofibromatosis)."
    },
    {
        "id": "Ch11_Histology_of_the_Nervous_System",
        "name": "Ch11 Neuroscience: Histology of the Nervous System",
        "dirName": "Ch11_Histology_of_the_Nervous_System",
        "totalQuestions": 150,
        "status": "active",
        "description": "Neuronal cytoskeleton, anterograde and retrograde axonal transport (rabies, tetanus toxin), astrocytes and glial scarring, oligodendrocytes (multiple sclerosis), microglial response, blood-brain barrier (BBB) ultrastructure, and peripheral nerve Wallerian degeneration."
    },
    {
        "id": "Ch12_Ventricular_System",
        "name": "Ch12 Neuroscience: Ventricular System and CSF Dynamics",
        "dirName": "Ch12_Ventricular_System",
        "totalQuestions": 150,
        "status": "active",
        "description": "Ventricular system communications (foramina of Monro, Luschka, Magendie), choroid plexus CSF production, arachnoid granulations, lumbar puncture CSF interpretation, communicating vs non-communicating hydrocephalus, normal pressure hydrocephalus (NPH), pseudotumor cerebri, and brain herniation syndromes."
    },
    {
        "id": "Ch13_The_Spinal_Cord",
        "name": "Ch13 Neuroscience: The Spinal Cord",
        "dirName": "Ch13_The_Spinal_Cord",
        "totalQuestions": 150,
        "status": "active",
        "description": "Spinal cord gross anatomy, conus medullaris, cauda equina, Rexed laminae, anterior spinal artery territory (artery of Adamkiewicz), dorsal column-medial lemniscal system, spinothalamic tract, corticospinal tract, Brown-Séquard syndrome, syringomyelia, tabes dorsalis, and amyotrophic lateral sclerosis (ALS)."
    },
    {
        "id": "Ch14_The_Brain_Stem",
        "name": "Ch14 Neuroscience: The Brain Stem",
        "dirName": "Ch14_The_Brain_Stem",
        "totalQuestions": 150,
        "status": "active",
        "description": "Medulla, pons, and midbrain internal architecture, cranial nerve nuclei, lateral medullary (Wallenberg / PICA) syndrome, medial medullary syndrome, medial pontine syndrome, locked-in syndrome, Weber syndrome, Parinaud syndrome, and internuclear ophthalmoplegia (INO / MLF lesion)."
    },
    {
        "id": "Ch15_The_Cerebellum",
        "name": "Ch15 Neuroscience: The Cerebellum",
        "dirName": "Ch15_The_Cerebellum",
        "totalQuestions": 150,
        "status": "active",
        "description": "Vestibulocerebellum, spinocerebellum, and cerebrocerebellum functional topography, deep cerebellar nuclei (dentate, emboliform, globose, fastigial), Purkinje cell GABAergic output, climbing vs mossy fibers, cerebellar ataxia (hemispheric vs vermian), and pediatric posterior fossa tumors."
    },
    {
        "id": "Ch16_Basal_Ganglia",
        "name": "Ch16 Neuroscience: Basal Ganglia",
        "dirName": "Ch16_Basal_Ganglia",
        "totalQuestions": 150,
        "status": "active",
        "description": "Corpus striatum (caudate & putamen), globus pallidus, subthalamic nucleus, substantia nigra, direct pathway (motor facilitation) vs indirect pathway (motor inhibition), Parkinson disease (loss of dopaminergic neurons in SNc, Lewy bodies), Huntington disease (caudate atrophy, CAG repeats), hemiballismus, and Wilson disease."
    },
    {
        "id": "Ch17_Visual_Pathways",
        "name": "Ch17 Neuroscience: Visual Pathways",
        "dirName": "Ch17_Visual_Pathways",
        "totalQuestions": 150,
        "status": "active",
        "description": "Optical refraction, retinal phototransduction cascade, optic chiasm lesions (bitemporal hemianopia), lateral geniculate nucleus (LGN), Meyer loop (temporal lobe / upper quadrantanopia) vs Baum loop (parietal lobe / lower quadrantanopia), primary visual cortex (macular sparing), pupillary light reflex, and afferent pupillary defect (Marcus Gunn pupil)."
    },
    {
        "id": "Ch18_Diencephalon",
        "name": "Ch18 Neuroscience: Diencephalon",
        "dirName": "Ch18_Diencephalon",
        "totalQuestions": 150,
        "status": "active",
        "description": "Thalamic sensory relay nuclei (VPL, VPM, LGN, MGN) and motor relay nuclei (VL, VA), hypothalamic nuclei (SCN circadian rhythm, SON/PVN neuroendocrine, anterior cooling, posterior heating, hunger and satiety centers), pineal gland, and craniopharyngioma."
    },
    {
        "id": "Ch19_Cerebral_Cortex",
        "name": "Ch19 Neuroscience: Cerebral Cortex",
        "dirName": "Ch19_Cerebral_Cortex",
        "totalQuestions": 150,
        "status": "active",
        "description": "Cerebral lobes, Brodmann cytoarchitectonic areas (motor area 4, premotor 6, FEF 8, Broca 44/45, somatosensory 3,1,2, primary visual 17, Wernicke 22, angular gyrus 39), internal capsule stroke syndromes, aphasia differentiation (Broca vs Wernicke vs conduction vs transcortical), circle of Willis aneurysms, and ACA/MCA/PCA ischemic stroke patterns."
    },
    {
        "id": "Ch20_Limbic_System",
        "name": "Ch20 Neuroscience: Limbic System",
        "dirName": "Ch20_Limbic_System",
        "totalQuestions": 150,
        "status": "active",
        "description": "Limbic lobe components, hippocampal long-term potentiation (LTP), Papez circuit, declarative vs non-declarative memory systems, amygdala fear conditioning and emotion regulation, Klüver-Bucy syndrome, Wernicke-Korsakoff syndrome (mammillary body atrophy), and mesial temporal sclerosis epilepsy."
    },
    {
        "id": "Ch21_Pharyngeal_Apparatus_Craniofacial_Defects_and_Teratology",
        "name": "Ch21 Pharyngeal Apparatus, Craniofacial Defects & Teratology",
        "dirName": "Ch01_Pharyngeal_Apparatus_Craniofacial_Defects_and_Teratology",
        "baseDir": PHARYNGEAL_EMBRYOLOGY_DIR,
        "totalQuestions": 150,
        "status": "active",
        "description": "Embryological pharyngeal apparatus derivatives: pharyngeal arches 1-6 (skeletal structures, muscles, cranial nerves CN V, VII, IX, X), pharyngeal pouches 1-4 (middle ear, palatine tonsils, inferior/superior parathyroids, thymus), pharyngeal clefts/grooves (external auditory meatus, branchial cleft cyst), thyroid and tongue development, craniofacial malformations (cleft lip and palate, Treacher Collins syndrome, Pierre Robin sequence), and clinical teratogens (isotretinoin, thalidomide, ACE inhibitors, lithium, alcohol/fetal alcohol syndrome, maternal diabetes)."
    }
]

BEHAVIORAL_CHAPTERS = [
    {
        "id": "Ch01_Epidemiology",
        "name": "Ch01 Behavioral: Epidemiology",
        "dirName": "Ch01_Epidemiology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Epidemiological study designs (cohort, case-control, cross-sectional, RCT), incidence vs prevalence, odds ratio, relative risk, attributable risk, selection and measurement bias, and confounding."
    },
    {
        "id": "Ch02_Biostatistics",
        "name": "Ch02 Behavioral: Biostatistics",
        "dirName": "Ch02_Biostatistics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Measures of central tendency and dispersion, normal distribution (68-95-99.7 rule), hypothesis testing (Type I/II error, statistical power, p-values), confidence intervals, t-test, ANOVA, chi-square, sensitivity, specificity, PPV, NPV, likelihood ratios, and ROC curves."
    },
    {
        "id": "Ch03_Developmental_Life_Cycle",
        "name": "Ch03 Behavioral: Developmental Life Cycle",
        "dirName": "Ch03_Developmental_Life_Cycle",
        "totalQuestions": 150,
        "status": "active",
        "description": "Erikson psychosocial stages, Piaget cognitive development, Freud psychosexual stages, motor, social, and language milestones across infancy, toddlerhood, preschool, school age, adolescence, and senescence."
    },
    {
        "id": "Ch04_Theories_of_Learning_and_Behavioral_Modification",
        "name": "Ch04 Behavioral: Theories of Learning & Behavioral Modification",
        "dirName": "Ch04_Theories_of_Learning_and_Behavioral_Modification",
        "totalQuestions": 150,
        "status": "active",
        "description": "Classical conditioning, operant conditioning (positive/negative reinforcement, punishment, reinforcement schedules), systematic desensitization, cognitive behavioral therapy (CBT), extinction, and token economy."
    },
    {
        "id": "Ch05_Defense_Mechanisms",
        "name": "Ch05 Behavioral: Defense Mechanisms",
        "dirName": "Ch05_Defense_Mechanisms",
        "totalQuestions": 150,
        "status": "active",
        "description": "Mature defense mechanisms (sublimation, altruism, suppression, humor) vs immature/neurotic defenses (projection, displacement, reaction formation, splitting, repression, rationalization, denial, acting out)."
    },
    {
        "id": "Ch06_Psychological_Health_and_Testing",
        "name": "Ch06 Behavioral: Psychological Health & Testing",
        "dirName": "Ch06_Psychological_Health_and_Testing",
        "totalQuestions": 150,
        "status": "active",
        "description": "Intelligence testing (WAIS, WISC), projective tests (Rorschach, TAT), objective personality inventories (MMPI), neuropsychological assessment, stress response (allostatic load), and illness behavior."
    },
    {
        "id": "Ch07_Substance_Use_Disorders",
        "name": "Ch07 Behavioral: Substance Use Disorders",
        "dirName": "Ch07_Substance_Use_Disorders",
        "totalQuestions": 150,
        "status": "active",
        "description": "DSM-5 criteria for substance use disorders, alcohol intoxication, withdrawal and delirium tremens, opioid overdose and withdrawal, sedative-hypnotics, stimulants (cocaine, amphetamines), cannabis, hallucinogens, and medication-assisted therapy."
    },
    {
        "id": "Ch08_Sleep_and_Sleep_Disorders",
        "name": "Ch08 Behavioral: Sleep & Sleep Disorders",
        "dirName": "Ch08_Sleep_and_Sleep_Disorders",
        "totalQuestions": 150,
        "status": "active",
        "description": "Sleep architecture (NREM stages N1-N3, REM sleep, EEG waveforms), circadian rhythm regulation (SCN, melatonin), insomnia, narcolepsy (hypocretin/orexin deficiency), obstructive sleep apnea, parasomnias (night terrors, sleepwalking), and REM sleep behavior disorder."
    },
    {
        "id": "Ch09_Psychiatric_DSM_5_Disorders",
        "name": "Ch09 Behavioral: Psychiatric DSM-5 Disorders",
        "dirName": "Ch09_Psychiatric_DSM_5_Disorders",
        "totalQuestions": 150,
        "status": "active",
        "description": "Depressive disorders, bipolar and related disorders, anxiety disorders (GAD, panic disorder, phobias), OCD, trauma/stressor disorders (PTSD, acute stress disorder), psychotic disorders (schizophrenia, schizoaffective), somatic symptom disorders, eating disorders, and personality disorders (Clusters A, B, C)."
    },
    {
        "id": "Ch10_Psychopharmacology",
        "name": "Ch10 Behavioral: Psychopharmacology",
        "dirName": "Ch10_Psychopharmacology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Antidepressants (SSRIs, SNRIs, TCAs, MAOIs, bupropion, mirtazapine), mood stabilizers (lithium, valproate, lamotrigine), antipsychotics (first and second generation, EPS, NMS, metabolic syndrome), anxiolytics, and psychostimulants."
    },
    {
        "id": "Ch11_Brain_Function_and_Neurocognitive_Disorders",
        "name": "Ch11 Behavioral: Brain Function & Neurocognitive Disorders",
        "dirName": "Ch11_Brain_Function_and_Neurocognitive_Disorders",
        "totalQuestions": 150,
        "status": "active",
        "description": "Delirium vs major/mild neurocognitive disorders (Alzheimer disease, frontotemporal dementia, Lewy body dementia, vascular dementia, prion disease), pseudodementia, and focal cerebral lesions."
    },
    {
        "id": "Ch12_Ethics_Law_and_Physician_Behavior",
        "name": "Ch12 Behavioral: Ethics, Law & Physician Behavior",
        "dirName": "Ch12_Ethics_Law_and_Physician_Behavior",
        "totalQuestions": 150,
        "status": "active",
        "description": "Core biomedical ethics (autonomy, beneficence, non-maleficence, justice), informed consent, decision-making capacity, surrogate decision-makers, advance directives, confidentiality, HIPAA, exceptions (duty to warn/Tarasoff, mandatory reporting), and physician boundaries."
    },
    {
        "id": "Ch13_Health_Care_Delivery_Systems",
        "name": "Ch13 Behavioral: Health Care Delivery Systems",
        "dirName": "Ch13_Health_Care_Delivery_Systems",
        "totalQuestions": 150,
        "status": "active",
        "description": "Healthcare financing and reimbursement models (Medicare, Medicaid, HMO, PPO, ACO), insurance concepts (deductible, copay, coinsurance), healthcare disparities, quality indicators, and global health systems."
    },
    {
        "id": "Ch14_Basic_Science_of_Patient_Safety",
        "name": "Ch14 Behavioral: Basic Science of Patient Safety",
        "dirName": "Ch14_Basic_Science_of_Patient_Safety",
        "totalQuestions": 150,
        "status": "active",
        "description": "Root cause analysis (RCA), failure mode and effects analysis (FMEA), Swiss cheese model of accident causation, active vs latent errors, handoff communication protocols (SBAR), checklist implementation, and culture of safety."
    }
]

MICROBIOLOGY_CHAPTERS = [
    {
        "id": "Ch01_The_Immune_System",
        "name": "Ch01 Immunology: The Immune System Architecture",
        "dirName": "Ch01_The_Immune_System",
        "totalQuestions": 150,
        "status": "active",
        "description": "Primary lymphoid organs (bone marrow, thymus) and secondary lymphoid tissues (lymph nodes, spleen, MALT), leukocyte adhesion cascade (selectins, integrins), and lymphocyte homing (HEVs, CCR7, S1P/S1PR1)."
    },
    {
        "id": "Ch02_Ontogeny_of_the_Immune_Cells",
        "name": "Ch02 Immunology: Ontogeny of the Immune Cells",
        "dirName": "Ch02_Ontogeny_of_the_Immune_Cells",
        "totalQuestions": 150,
        "status": "active",
        "description": "Hematopoiesis, myeloid and lymphoid lineage commitment, hematopoietic stem cell (HSC) markers (CD34), common lymphoid progenitor (CLP), and development of dendritic cells and tissue macrophages."
    },
    {
        "id": "Ch03_Lymphocyte_Development_and_Selection",
        "name": "Ch03 Immunology: Lymphocyte Development & Selection",
        "dirName": "Ch03_Lymphocyte_Development_and_Selection",
        "totalQuestions": 150,
        "status": "active",
        "description": "T-cell thymic ontogeny (double negative, double positive, positive selection in cortex, negative selection in medulla, AIRE and APS-1), B-cell maturation (pro-B, pre-B, heavy/light chain V(D)J recombination, RAG1/RAG2, TdT), central and peripheral tolerance."
    },
    {
        "id": "Ch04_Innate_Immune_Response",
        "name": "Ch04 Immunology: Innate Immune Response",
        "dirName": "Ch04_Innate_Immune_Response",
        "totalQuestions": 150,
        "status": "active",
        "description": "Pattern recognition receptors (PRRs, TLRs, NLRs, inflammasome/caspase-1, IL-1beta/IL-18), pathogen-associated molecular patterns (PAMPs), phagocytosis, oxidative burst (NADPH oxidase, MPO), natural killer (NK) cells (KIR/KAR, perforin/granzyme), and type I interferons (IFN-alpha/beta)."
    },
    {
        "id": "Ch05_Innate_Immune_Response_Meets_Adaptive",
        "name": "Ch05 Immunology: Innate Meets Adaptive Immunity",
        "dirName": "Ch05_Innate_Immune_Response_Meets_Adaptive",
        "totalQuestions": 150,
        "status": "active",
        "description": "Antigen processing and presentation (MHC Class I via proteasome/TAP, MHC Class II via endosome/invariant chain), cross-presentation, and dendritic cell activation/migration to regional lymph nodes."
    },
    {
        "id": "Ch06_B_and_T_Lymphocyte_Activation",
        "name": "Ch06 Immunology: B & T Lymphocyte Activation",
        "dirName": "Ch06_B_and_T_Lymphocyte_Activation",
        "totalQuestions": 150,
        "status": "active",
        "description": "Signal 1 (TCR-MHC/peptide, BCR-antigen), Signal 2 costimulation (CD28-CD80/86, CD40-CD40L), checkpoint receptors (CTLA-4, PD-1), Signal 3 cytokine polarizing signals, clonal expansion, and immunological memory."
    },
    {
        "id": "Ch07_Humoral_Immunity",
        "name": "Ch07 Immunology: Humoral Immunity",
        "dirName": "Ch07_Humoral_Immunity",
        "totalQuestions": 150,
        "status": "active",
        "description": "Antibody structure and isotypes (IgM, IgD, IgG, IgA, IgE), somatic hypermutation and affinity maturation in germinal centers, class switch recombination (AID, CD40-CD40L interaction, Hyper-IgM syndrome), and complement pathways (classical, alternative, lectin, MAC)."
    },
    {
        "id": "Ch08_Cell_Mediated_Immunity",
        "name": "Ch08 Immunology: Cell-Mediated Immunity",
        "dirName": "Ch08_Cell_Mediated_Immunity",
        "totalQuestions": 150,
        "status": "active",
        "description": "CD4+ T-cell helper subsets (Th1: IFN-gamma/IL-12, Th2: IL-4/IL-5/IL-13, Th17: IL-17/IL-23, Treg: FOXP3/IL-10/TGF-beta), CD8+ cytotoxic T lymphocyte killing (perforin/granzyme, Fas/FasL), and delayed-type hypersensitivity."
    },
    {
        "id": "Ch09_Immunodiagnostics",
        "name": "Ch09 Immunology: Immunodiagnostics",
        "dirName": "Ch09_Immunodiagnostics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Enzyme-linked immunosorbent assay (ELISA), Western blot, flow cytometry and immunophenotyping (CD markers), direct/indirect immunofluorescence, agglutination tests, and serum protein electrophoresis (SPEP/UPEP)."
    },
    {
        "id": "Ch10_Immunizations",
        "name": "Ch10 Immunology: Immunizations",
        "dirName": "Ch10_Immunizations",
        "totalQuestions": 150,
        "status": "active",
        "description": "Active vs passive immunity, vaccine types (live attenuated, inactivated/killed, toxoid, subunit, conjugate vaccines, mRNA vaccines), adjuvants, herd immunity, and contraindications (pregnancy, severe immunocompromise)."
    },
    {
        "id": "Ch11_Primary_Immunodeficiencies",
        "name": "Ch11 Immunology: Primary Immunodeficiencies",
        "dirName": "Ch11_Primary_Immunodeficiencies",
        "totalQuestions": 150,
        "status": "active",
        "description": "Severe combined immunodeficiency (SCID: IL2RG, ADA), X-linked agammaglobulinemia (Bruton tyrosine kinase), Hyper-IgM syndrome, Common variable immunodeficiency (CVID), DiGeorge syndrome, Wiskott-Aldrich syndrome, Ataxia-telangiectasia, Chronic granulomatous disease, Chédiak-Higashi syndrome, and Leukocyte adhesion deficiency (LAD)."
    },
    {
        "id": "Ch12_Hypersensitivity_and_Autoimmune_Disease",
        "name": "Ch12 Immunology: Hypersensitivity & Autoimmunity",
        "dirName": "Ch12_Hypersensitivity_and_Autoimmune_Disease",
        "totalQuestions": 150,
        "status": "active",
        "description": "Gell and Coombs hypersensitivity reactions (Type I IgE-mediated, Type II cytotoxic antibody-mediated, Type III immune complex-mediated, Type IV delayed-type cell-mediated), autoimmunity mechanisms, HLA associations, and autoantibodies (ANA, anti-dsDNA, anti-Ro/La, anti-CCP, ANCA)."
    },
    {
        "id": "Ch13_Transplantation",
        "name": "Ch13 Immunology: Transplantation Immunology",
        "dirName": "Ch13_Transplantation",
        "totalQuestions": 150,
        "status": "active",
        "description": "Allorecognition (direct vs indirect pathways), hyperacute graft rejection (preformed antibodies, fibrinoid necrosis), acute graft rejection (cell-mediated vs humoral/C4d), chronic graft rejection (accelerated arteriosclerosis, fibrosis), and graft-versus-host disease (GVHD)."
    },
    {
        "id": "Ch14_General_Microbiology",
        "name": "Ch14 Microbiology: General Microbiology",
        "dirName": "Ch14_General_Microbiology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Bacterial cell structure (peptidoglycan, lipopolysaccharide/endotoxin, capsule, flagella, pili/fimbriae), Gram stain physiology, bacterial spores (Bacillus, Clostridium), bacterial growth kinetics, exotoxins (A-B toxins, superantigens), and sterilization/disinfection."
    },
    {
        "id": "Ch15_Medically_Relevant_Bacteria",
        "name": "Ch15 Microbiology: Medically Relevant Bacteria",
        "dirName": "Ch15_Medically_Relevant_Bacteria",
        "totalQuestions": 150,
        "status": "active",
        "description": "Gram-positive cocci (Staphylococcus, Streptococcus, Enterococcus), Gram-positive rods (Bacillus, Clostridium, Listeria, Corynebacterium), Gram-negative cocci (Neisseria), Gram-negative rods (Enterobacteriaceae, Pseudomonas, Haemophilus, Legionella), acid-fast bacilli (Mycobacterium), spirochetes (Treponema, Borrelia), and zoonoses."
    },
    {
        "id": "Ch16_Bacterial_Genetics",
        "name": "Ch16 Microbiology: Bacterial Genetics",
        "dirName": "Ch16_Bacterial_Genetics",
        "totalQuestions": 150,
        "status": "active",
        "description": "Horizontal gene transfer (transformation, conjugation, F plasmid, Hfr, generalized and specialized transduction), transposons, plasmid-mediated antibiotic resistance, beta-lactamase (ESBL, carbapenemase), and vancomycin resistance (vanA)."
    },
    {
        "id": "Ch17_Medically_Relevant_Viruses",
        "name": "Ch17 Microbiology: Medically Relevant Viruses",
        "dirName": "Ch17_Medically_Relevant_Viruses",
        "totalQuestions": 150,
        "status": "active",
        "description": "DNA viruses (Pox, Herpes, Adeno, Papilloma, Polyoma, Parvo, Hepadna), RNA viruses (Picorna, Calici, Flavi, Toga, Corona, Retro, Orthomyxo, Paramyxo, Rhabdo, Filo, Bunya, Arena, Reo), viral replication cycle, oncogenic viruses (EBV, HPV, HBV, HCV, HTLV-1), and viral hepatitis."
    },
    {
        "id": "Ch18_Medically_Relevant_Fungi",
        "name": "Ch18 Microbiology: Medically Relevant Fungi",
        "dirName": "Ch18_Medically_Relevant_Fungi",
        "totalQuestions": 150,
        "status": "active",
        "description": "Systemic dimorphic mycoses (Histoplasma, Blastomyces, Coccidioides, Paracoccidioides), opportunistic fungi (Candida, Aspergillus, Cryptococcus, Mucor/Rhizopus, Pneumocystis jirovecii), and superficial/cutaneous mycoses (dermatophytes, Malassezia furfur)."
    },
    {
        "id": "Ch19_Medical_Parasitology",
        "name": "Ch19 Microbiology: Medical Parasitology",
        "dirName": "Ch19_Medical_Parasitology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Protozoa (Entamoeba, Giardia, Cryptosporidium, Toxoplasma, Trichomonas, Trypanosoma, Leishmania, Plasmodium, Babesia), Nematodes (roundworms, pinworm, hookworm, Ascaris, Strongyloides, Trichinella), Cestodes (tapeworms, Taenia, Echinococcus), and Trematodes (flukes, Schistosoma, Clonorchis)."
    },
    {
        "id": "Ch20_Clinical_Infectious_Disease",
        "name": "Ch20 Microbiology: Clinical Infectious Disease",
        "dirName": "Ch20_Clinical_Infectious_Disease",
        "totalQuestions": 150,
        "status": "active",
        "description": "Syndromic infectious diseases: meningitis and encephalitis, pneumonia (typical vs atypical), infective endocarditis (Duke criteria), urinary tract infections, osteomyelitis and septic arthritis, sexually transmitted infections, and healthcare-associated infections."
    },
    {
        "id": "Ch21_Comparative_Microbiology",
        "name": "Ch21 Microbiology: Comparative Microbiology",
        "dirName": "Ch21_Comparative_Microbiology",
        "totalQuestions": 150,
        "status": "active",
        "description": "Diagnostic algorithms, catalase test, coagulase test, hemolysis patterns (alpha, beta, gamma), optochin and bacitracin susceptibility, lactose fermentation on MacConkey agar, oxidase test, urease test, and differential laboratory identification schemes."
    }
]

def parse_discipline(discipline_name, base_dir, chapters_metadata, start_id):
    questions = []
    current_global_id = start_id

    for chap in chapters_metadata:
        ch_dir = os.path.join(chap.get("baseDir", base_dir), chap["dirName"])
        blocks = [f for f in os.listdir(ch_dir) if f.startswith('Block') and f.endswith('.md')]
        blocks.sort()

        chap_q_count = 0
        for b in blocks:
            b_path = os.path.join(ch_dir, b)
            b_num_match = re.search(r'Block(\d+)', b)
            b_name = f"Block {b_num_match.group(1)}" if b_num_match else b.split('_')[0]

            with open(b_path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            q_raw_blocks = re.split(r'\n(?=### Question \d+:)', content)[1:]

            for idx, qb in enumerate(q_raw_blocks):
                title_m = re.search(r'### Question (\d+):\s*(.*)', qb)
                diff_m = re.search(r'-\s*\*\*Difficulty\*\*:\s*(.*)', qb)
                core_m = re.search(r'-\s*\*\*Core Concept[^:]*\*\*:\s*(.*)', qb)

                # Answer (handles (A), A, **([A])**, ** (A), etc.)
                ans_m = re.search(r'####\s*Correct Answer:?\s*[\s\*\[\(]*([A-E])(?:\s|[\*\]\)\.:]|$)', qb, re.IGNORECASE)

                # Restrict options search to text preceding the answer line
                opts_section = qb[:ans_m.start()] if ans_m else qb

                # Vignette (handles #### Clinical Vignette: and - **Clinical Vignette**:)
                vig_m = re.search(r'(?:####\s*Clinical Vignette:?|- \*\*Clinical Vignette\*\*:?)\s*(.*?)(?=\n\s*[-*]?\s*\([A-E]\)|\Z)', opts_section, re.DOTALL)
                vig_text = vig_m.group(1).strip() if vig_m else ''

                # Options (handles (A) and - (A) and * (A))
                opt_pat = re.compile(r'^\s*[-*]?\s*\(([A-E])\)\s+(.*?)(?=\n\s*[-*]?\s*\([A-E]\)|\n\s*####|\Z)', re.DOTALL | re.MULTILINE)
                opts = opt_pat.findall(opts_section)
                options = [o[1].strip().replace('\n', ' ') for o in opts]

                if len(options) < 4:
                    opts_alt = re.findall(r'^\s*[-*]?\s*\(([A-E])\)\s+([^\n\r]+)', opts_section, re.MULTILINE)
                    options = [o[1].strip() for o in opts_alt]

                # Explanation text
                exp_m = re.search(r'####\s*(?:High-Yield Mechanism[^:\n\r]*|High-Yield Pathophysiological Explanation|Detailed Explanations?|Explanation):?\s*(.*)', qb, re.DOTALL)
                exp_text = exp_m.group(1).strip() if exp_m else ''

                # Educational objective
                edu_m = re.search(r'#{4,5}\s*(?:\d+\.\s*)?Educational Objective[^:]*:\s*(.*)', qb, re.DOTALL)
                edu_text = edu_m.group(1).strip() if edu_m else ''
                if not edu_text and core_m:
                    edu_text = core_m.group(1).strip()

                # Split vignette into stem and leadQuestion
                sentences = re.split(r'(?<=[.?!])\s+(?=[A-Z])', vig_text)
                if len(sentences) > 1 and sentences[-1].strip().endswith('?'):
                    lead_q = sentences[-1].strip()
                    stem = ' '.join(sentences[:-1]).strip()
                else:
                    lead_q = 'Which of the following is the most likely diagnosis or underlying mechanism?'
                    stem = vig_text

                # Render formatted explanation HTML
                exp_html = convert_markdown_to_html(exp_text, edu_fallback=edu_text)

                questions.append({
                    'id': current_global_id,
                    'discipline': discipline_name,
                    'disciplineId': discipline_name.lower(),
                    'qNum': int(title_m.group(1)) if title_m else chap_q_count + 1,
                    'title': title_m.group(2).strip() if title_m else f'Question {chap_q_count + 1}',
                    'chapter': chap["id"],
                    'chapterName': chap["name"],
                    'block': b_name,
                    'difficulty': diff_m.group(1).strip() if diff_m else 'Medium',
                    'subtag': core_m.group(1).strip()[:100] if core_m else chap["name"],
                    'stem': stem,
                    'leadQuestion': lead_q,
                    'options': options,
                    'correct': ans_m.group(1).upper() if ans_m else 'A',
                    'explanation': exp_html,
                    'rawObjective': edu_text[:350],
                    'flagged': False,
                    'answered': False
                })

                current_global_id += 1
                chap_q_count += 1

        chap["totalQuestions"] = chap_q_count
        print(f"[{discipline_name}] Loaded {chap['id']}: {chap_q_count} questions")

    return questions, current_global_id

def build_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    pathology_dir = os.path.join(current_dir, 'step 1-Pathology')
    pharmacology_dir = os.path.join(current_dir, 'step 1-Pharmacology')
    biochemistry_dir = os.path.join(current_dir, 'step 1-Biochemistry and Medical Genetics QA')
    physiology_dir = os.path.join(current_dir, 'step 1-Physiology')
    anatomy_dir = os.path.join(current_dir, 'step 1-Anatomy')
    behavioral_dir = os.path.join(current_dir, 'step 1-Behavioral Science and Social Sciences QA')
    microbiology_dir = os.path.join(current_dir, 'step 1-Immunology and Microbiology QA')
    output_js_path = os.path.join(current_dir, 'questions_data.js')

    print("=== Building USMLE Step 1 Comprehensive Question Database ===")
    print("Parsing Step 1 Pathology...")
    pathology_questions, next_id = parse_discipline("Pathology", pathology_dir, PATHOLOGY_CHAPTERS, 1)
    print(f" -> Pathology Complete: {len(pathology_questions)} questions loaded.\n")

    print("Parsing Step 1 Pharmacology...")
    pharmacology_questions, next_id2 = parse_discipline("Pharmacology", pharmacology_dir, PHARMACOLOGY_CHAPTERS, next_id)
    print(f" -> Pharmacology Complete: {len(pharmacology_questions)} questions loaded.\n")

    print("Parsing Step 1 Biochemistry & Genetics...")
    biochemistry_questions, next_id3 = parse_discipline("Biochemistry", biochemistry_dir, BIOCHEMISTRY_CHAPTERS, next_id2)
    print(f" -> Biochemistry Complete: {len(biochemistry_questions)} questions loaded.\n")

    print("Parsing Step 1 Physiology...")
    physiology_questions, next_id4 = parse_discipline("Physiology", physiology_dir, PHYSIOLOGY_CHAPTERS, next_id3)
    print(f" -> Physiology Complete: {len(physiology_questions)} questions loaded.\n")

    print("Parsing Step 1 Anatomy & Embryology...")
    anatomy_questions, next_id5 = parse_discipline("Anatomy", anatomy_dir, ANATOMY_CHAPTERS, next_id4)
    print(f" -> Anatomy Complete: {len(anatomy_questions)} questions loaded.\n")

    print("Parsing Step 1 Behavioral Science & Social Sciences...")
    behavioral_questions, next_id6 = parse_discipline("Behavioral", behavioral_dir, BEHAVIORAL_CHAPTERS, next_id5)
    print(f" -> Behavioral Complete: {len(behavioral_questions)} questions loaded.\n")

    print("Parsing Step 1 Microbiology & Immunology...")
    microbiology_questions, final_id = parse_discipline("Microbiology", microbiology_dir, MICROBIOLOGY_CHAPTERS, next_id6)
    print(f" -> Microbiology Complete: {len(microbiology_questions)} questions loaded.\n")

    all_questions = pathology_questions + pharmacology_questions + biochemistry_questions + physiology_questions + anatomy_questions + behavioral_questions + microbiology_questions
    print(f"Total Questions Compiled: {len(all_questions)}")

    disciplines_metadata = [
        {
            "id": "Pathology",
            "name": "Pathology",
            "step": 1,
            "count": len(pathology_questions),
            "status": "active",
            "description": "Comprehensive general and systemic pathology (33 chapters)"
        },
        {
            "id": "Pharmacology",
            "name": "Pharmacology",
            "step": 1,
            "count": len(pharmacology_questions),
            "status": "active",
            "description": "Comprehensive preclinical pharmacology, clinical toxicology, and pharmacogenomics (12 chapters)"
        },
        {
            "id": "Biochemistry",
            "name": "Biochemistry & Genetics",
            "step": 1,
            "count": len(biochemistry_questions),
            "status": "active",
            "description": "Comprehensive biochemistry, metabolism, molecular biology, medical genetics, and clinical nutrition (25 chapters)"
        },
        {
            "id": "Physiology",
            "name": "Physiology",
            "step": 1,
            "count": len(physiology_questions),
            "status": "active",
            "description": "Comprehensive cellular, neuromuscular, organ system, and environmental physiology (35 chapters)"
        },
        {
            "id": "Anatomy",
            "name": "Anatomy & Embryology",
            "step": 1,
            "count": len(anatomy_questions),
            "status": "active",
            "description": "Comprehensive gross anatomy, embryology, teratology, histology, and neuroscience (21 chapters)"
        },
        {
            "id": "Behavioral",
            "name": "Behavioral Science & Social Sciences",
            "step": 1,
            "count": len(behavioral_questions),
            "status": "active",
            "description": "Comprehensive behavioral science, epidemiology, biostatistics, psychiatry, ethics, and patient safety (14 chapters)"
        },
        {
            "id": "Microbiology",
            "name": "Microbiology & Immunology",
            "step": 1,
            "count": len(microbiology_questions),
            "status": "active",
            "description": "Comprehensive basic immunology, immunopathology, bacteriology, virology, mycology, and parasitology (21 chapters)"
        }
    ]

    # Write questions_data.js (Manifest)
    with open(output_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 Comprehensive Question Bank Manifest\n")
        out_f.write("// Contains metadata for Pathology (4,950 Qs), Pharmacology (1,800 Qs), Biochemistry & Genetics (3,750 Qs), Physiology (5,250 Qs), Anatomy & Embryology (3,150 Qs), Behavioral Science & Psychiatry (2,100 Qs), and Microbiology & Immunology (3,150 Qs) - Total 24,150 Qs across 161 Chapters\n\n")
        out_f.write("window.USMLE_QUESTIONS = window.USMLE_QUESTIONS || [];\n\n")
        out_f.write("window.USMLE_DISCIPLINES = ")
        json.dump(disciplines_metadata, out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n")

    # Write questions_data_pathology.js
    path_js_path = os.path.join(current_dir, 'questions_data_pathology.js')
    with open(path_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Pathology Question Bank (4,950 Questions)\n\n")
        out_f.write("window.USMLE_PATHOLOGY_CHAPTERS = ")
        json.dump(sanitize_chapters(PATHOLOGY_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(pathology_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    # Write questions_data_pharmacology.js
    pharm_js_path = os.path.join(current_dir, 'questions_data_pharmacology.js')
    with open(pharm_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Pharmacology Question Bank (1,800 Questions)\n\n")
        out_f.write("window.USMLE_PHARMACOLOGY_CHAPTERS = ")
        json.dump(sanitize_chapters(PHARMACOLOGY_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(pharmacology_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    # Write questions_data_biochemistry.js
    bio_js_path = os.path.join(current_dir, 'questions_data_biochemistry.js')
    with open(bio_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Biochemistry & Genetics Question Bank (3,750 Questions)\n\n")
        out_f.write("window.USMLE_BIOCHEMISTRY_CHAPTERS = ")
        json.dump(sanitize_chapters(BIOCHEMISTRY_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(biochemistry_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    # Write questions_data_physiology.js
    phys_js_path = os.path.join(current_dir, 'questions_data_physiology.js')
    with open(phys_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Physiology Question Bank (5,250 Questions)\n\n")
        out_f.write("window.USMLE_PHYSIOLOGY_CHAPTERS = ")
        json.dump(sanitize_chapters(PHYSIOLOGY_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(physiology_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    # Write questions_data_anatomy.js
    anat_js_path = os.path.join(current_dir, 'questions_data_anatomy.js')
    with open(anat_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Anatomy & Embryology Question Bank (3,150 Questions)\n\n")
        out_f.write("window.USMLE_ANATOMY_CHAPTERS = ")
        json.dump(sanitize_chapters(ANATOMY_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(anatomy_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    # Write questions_data_behavioral.js
    beh_js_path = os.path.join(current_dir, 'questions_data_behavioral.js')
    with open(beh_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Behavioral Science & Social Sciences Question Bank (2,100 Questions)\n\n")
        out_f.write("window.USMLE_BEHAVIORAL_CHAPTERS = ")
        json.dump(sanitize_chapters(BEHAVIORAL_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(behavioral_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    # Write questions_data_microbiology.js
    micro_js_path = os.path.join(current_dir, 'questions_data_microbiology.js')
    with open(micro_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 - Microbiology & Immunology Question Bank (3,150 Questions)\n\n")
        out_f.write("window.USMLE_MICROBIOLOGY_CHAPTERS = ")
        json.dump(sanitize_chapters(MICROBIOLOGY_CHAPTERS), out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat(")
        json.dump(microbiology_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(");\n")

    all_files = [output_js_path, path_js_path, pharm_js_path, bio_js_path, phys_js_path, anat_js_path, beh_js_path, micro_js_path]
    print("Successfully generated question bank database files:")
    for fp in all_files:
        mb = os.path.getsize(fp) / 1024 / 1024
        print(f" - {os.path.basename(fp):<32}: {mb:6.2f} MB")

if __name__ == '__main__':
    build_database()
