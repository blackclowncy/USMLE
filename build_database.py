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
        edu_html = f'''
        <div class="p-4.5 rounded-2xl neu-groove bg-[#e4efe8]/70 border border-emerald-500/30 flex flex-col gap-2 mt-4">
            <div class="flex items-center gap-2 text-accentSuccess font-display font-bold text-[14px]">
                <span class="material-symbols-outlined text-[20px]">school</span>
                <span>Educational Objective / USMLE High-Yield Takeaway</span>
            </div>
            <p class="text-[13.5px] leading-relaxed text-[#1c382b] font-medium pl-1">
                {clean_edu}
            </p>
        </div>
        '''

    # Format Distractor Analysis header
    body_text = re.sub(
        r'#{4,5}\s*(?:\d+\.\s*)?(?:Comprehensive\s+)?Distractor Analysis[^:]*:', 
        r'<div class="font-display font-bold text-[14.5px] text-primaryDark mt-4 mb-2 pb-1 border-b border-[#ded7ca] flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">rule</span><span>Distractor Analysis / 干扰项深度剖析</span></div>', 
        body_text, 
        flags=re.IGNORECASE
    )
    
    # Format Explanation header
    body_text = re.sub(
        r'#{4,5}\s*(?:High-Yield Pathophysiological Explanation|Detailed Explanations?|Explanation):',
        r'<div class="font-display font-bold text-[14.5px] text-primaryDark mt-2 mb-2 pb-1 border-b border-[#ded7ca] flex items-center gap-2"><span class="material-symbols-outlined text-[18px]">auto_stories</span><span>Pathophysiological Explanation / 机制详析</span></div>',
        body_text,
        flags=re.IGNORECASE
    )

    # Format Section headers
    body_text = re.sub(
        r'#####\s*(\d+\.\s*[^\n\r]+)',
        r'<div class="font-semibold text-[13.5px] text-[#2c3138] mt-3 mb-1.5 flex items-center gap-2 pl-1"><span class="w-2 h-2 rounded-full bg-primary shrink-0"></span><span>\1</span></div>',
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
                formatted_lines.append(f'''
                <div class="flex items-start gap-2.5 my-2 pl-2 bg-[#e6e1d7]/40 p-2.5 rounded-xl border border-white/50">
                    <span class="w-6 h-6 rounded-lg neu-extruded-xs bg-[#ded7ca] text-[#2c3138] flex items-center justify-center font-mono text-[11px] font-bold shrink-0 mt-0.5">{letter}</span>
                    <div class="text-[13px] leading-relaxed text-[#2c3138] flex-1">{rest}</div>
                </div>
                ''')
            else:
                formatted_lines.append(f'''
                <div class="flex items-start gap-2.5 my-1.5 pl-2">
                    <span class="text-primary font-bold text-[14px] shrink-0 mt-0.5">•</span>
                    <div class="text-[13px] leading-relaxed text-[#2c3138] flex-1">{item_text}</div>
                </div>
                ''')
        elif s.startswith('<div') or s.startswith('</div') or s.startswith('<h') or s.startswith('</h'):
            formatted_lines.append(s)
        else:
            formatted_lines.append(f'<p class="text-[13px] leading-relaxed text-[#2c3138] my-1.5 pl-1">{s}</p>')

    return '\n'.join(formatted_lines) + '\n' + edu_html

def build_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    base_dir = os.path.join(current_dir, 'step 1-Pathology')
    output_js_path = os.path.join(current_dir, 'questions_data.js')
    
    # 14 Chapter definitions
    chapters_metadata = [
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
            "id": "11_Cancer_Genetics_Oncogenes_and_TSGs_QA",
            "name": "11 Cancer Genetics Oncogenes and TSGs QA",
            "fileName": "11_Cancer_Genetics_Oncogenes_and_TSGs_QA.md",
            "totalQuestions": 0,
            "status": "placeholder",
            "description": "Proto-oncogenes, tumor suppressor genes (p53, Rb), DNA repair defects, and epigenetic changes (待更新 - 占位章节)."
        },
        {
            "id": "12_Clinical_Oncology_Staging_and_Tumor_Markers_QA",
            "name": "12 Clinical Oncology Staging and Tumor Markers QA",
            "fileName": "12_Clinical_Oncology_Staging_and_Tumor_Markers_QA.md",
            "totalQuestions": 0,
            "status": "placeholder",
            "description": "TNM staging, histological grading, serum tumor markers, and diagnostic laboratory methods (待更新 - 占位章节)."
        },
        {
            "id": "13_Paraneoplastic_Syndromes_QA",
            "name": "13 Paraneoplastic Syndromes QA",
            "fileName": "13_Paraneoplastic_Syndromes_QA.md",
            "totalQuestions": 0,
            "status": "placeholder",
            "description": "Endocrinopathies, neuromyopathies, dermatologic, and hematologic paraneoplastic syndromes (待更新 - 占位章节)."
        },
        {
            "id": "14_Cellular_Aging_and_Systemic_Changes_QA",
            "name": "14 Cellular Aging and Systemic Changes QA",
            "fileName": "14_Cellular_Aging_and_Systemic_Changes_QA.md",
            "totalQuestions": 0,
            "status": "placeholder",
            "description": "Telomere shortening, cellular senescence, DNA damage accumulation, and metabolic decline (待更新 - 占位章节)."
        }
    ]

    all_questions = []
    global_id = 1

    # Parse active chapters
    active_chapters = [c for c in chapters_metadata if c["status"] == "active"]
    
    for chap in active_chapters:
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
                ans_m = re.search(r'####\s*Correct Answer:\s*(?:\n\s*)?(?:\*\*)?\(?([A-E])\)?', qb, re.IGNORECASE)
                diff_m = re.search(r'-\s*\*\*Difficulty\*\*:\s*(.*)', qb)
                core_m = re.search(r'-\s*\*\*Core Concept[^:]*\*\*:\s*(.*)', qb)
                
                # Clinical Vignette
                vig_m = re.search(r'####\s*Clinical Vignette:\s*(.*?)(?=\n\s*\([A-E]\)|\Z)', qb, re.DOTALL)
                vig_text = vig_m.group(1).strip() if vig_m else ''
                
                # Options
                opt_pat = re.compile(r'^\s*\(([A-E])\)\s+(.*?)(?=\n\s*\([A-E]\)|\n\s*####|\Z)', re.DOTALL | re.MULTILINE)
                opts = opt_pat.findall(qb)
                options = [o[1].strip().replace('\n', ' ') for o in opts]
                
                # Fallback if fewer than 4 options captured
                if len(options) < 4:
                    opts_alt = re.findall(r'^\s*\(([A-E])\)\s+([^\n\r]+)', qb, re.MULTILINE)
                    options = [o[1].strip() for o in opts_alt]

                # Explanation text
                exp_m = re.search(r'####\s*(?:High-Yield Pathophysiological Explanation|Detailed Explanations?|Explanation):\s*(.*)', qb, re.DOTALL)
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

                all_questions.append({
                    'id': global_id,
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
                
                global_id += 1
                chap_q_count += 1
        
        chap["totalQuestions"] = chap_q_count
        print(f"Loaded {chap['id']}: {chap_q_count} questions")

    print(f"\nTotal Questions loaded across all chapters: {len(all_questions)}")

    # Write questions_data.js
    with open(output_js_path, 'w', encoding='utf-8') as out_f:
        out_f.write("// Autogenerated USMLE Step 1 Pathology Question Bank Database\n")
        out_f.write("window.USMLE_PATHOLOGY_CHAPTERS = ")
        json.dump(chapters_metadata, out_f, ensure_ascii=False, indent=2)
        out_f.write(";\n\n")
        out_f.write("window.USMLE_QUESTIONS = ")
        json.dump(all_questions, out_f, ensure_ascii=False)
        out_f.write(";\n")

    print(f"Successfully generated {output_js_path} ({os.path.getsize(output_js_path)/1024/1024:.2f} MB)")

if __name__ == '__main__':
    build_database()
