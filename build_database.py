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
    }
]

def parse_discipline(discipline_name, base_dir, chapters_metadata, start_id):
    questions = []
    current_global_id = start_id

    for chap in chapters_metadata:
        ch_dir = os.path.join(base_dir, chap["dirName"])
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
    output_js_path = os.path.join(current_dir, 'questions_data.js')

    print("=== Building USMLE Step 1 Comprehensive Question Database ===")
    print("Parsing Step 1 Pathology...")
    pathology_questions, next_id = parse_discipline("Pathology", pathology_dir, PATHOLOGY_CHAPTERS, 1)
    print(f" -> Pathology Complete: {len(pathology_questions)} questions loaded.\n")

    print("Parsing Step 1 Pharmacology...")
    pharmacology_questions, next_id2 = parse_discipline("Pharmacology", pharmacology_dir, PHARMACOLOGY_CHAPTERS, next_id)
    print(f" -> Pharmacology Complete: {len(pharmacology_questions)} questions loaded.\n")

    print("Parsing Step 1 Biochemistry & Genetics...")
    biochemistry_questions, final_id = parse_discipline("Biochemistry", biochemistry_dir, BIOCHEMISTRY_CHAPTERS, next_id2)
    print(f" -> Biochemistry Complete: {len(biochemistry_questions)} questions loaded.\n")

    all_questions = pathology_questions + pharmacology_questions + biochemistry_questions
    print(f"Total Questions Compiled: {len(all_questions)}")

    disciplines_metadata = [
        {
            "id": "Pathology",
            "name": "Pathology",
            "step": 1,
            "count": len(pathology_questions),
            "status": "active",
            "description": "General and systemic pathology (14 chapters)"
        },
        {
            "id": "Pharmacology",
            "name": "Pharmacology",
            "step": 1,
            "count": len(pharmacology_questions),
            "status": "active",
            "description": "Comprehensive preclinical pharmacology (9 chapters)"
        },
        {
            "id": "Biochemistry",
            "name": "Biochemistry & Genetics",
            "step": 1,
            "count": len(biochemistry_questions),
            "status": "active",
            "description": "Comprehensive biochemistry, metabolism, molecular biology, and medical genetics (23 chapters)"
        }
    ]

    # Write questions_data.js
    with open(output_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 Comprehensive Question Bank Database\n")
        out_f.write("// Contains Step 1 Pathology (2,100 Qs), Pharmacology (1,350 Qs), and Biochemistry & Genetics (3,450 Qs)\n\n")
        out_f.write("window.USMLE_DISCIPLINES = ")
        json.dump(disciplines_metadata, out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_PATHOLOGY_CHAPTERS = ")
        json.dump(PATHOLOGY_CHAPTERS, out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_PHARMACOLOGY_CHAPTERS = ")
        json.dump(PHARMACOLOGY_CHAPTERS, out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_BIOCHEMISTRY_CHAPTERS = ")
        json.dump(BIOCHEMISTRY_CHAPTERS, out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = ")
        json.dump(all_questions, out_f, ensure_ascii=False, separators=(',', ':'))
        out_f.write(";\n")

    file_size_mb = os.path.getsize(output_js_path) / 1024 / 1024
    print(f"Successfully generated {output_js_path} ({file_size_mb:.2f} MB)")

if __name__ == '__main__':
    build_database()
