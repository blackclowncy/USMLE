# -*- coding: utf-8 -*-
"""
Builder script to convert Wilson's Manual of Laboratory and Diagnostic Tests
from markdown files in D:/Github/USMLE/Lab into a structured labs_data.js.

Sources:
1. Lab/01_Laboratory_Tests_Manual.md (359 Tests)
2. Lab/02_Disease_Diagnostic_Criteria.md (11 Systems, 68 Diseases)
Output:
- labs_data.js (Exposes window.USMLE_LAB_TESTS and window.USMLE_DISEASE_CRITERIA)
"""

import sys, os, io, re, json

sys.stdout.reconfigure(encoding='utf-8')

LAB_TESTS_FILE = os.path.join(os.path.dirname(__file__), 'Lab', '01_Laboratory_Tests_Manual.md')
DISEASE_FILE = os.path.join(os.path.dirname(__file__), 'Lab', '02_Disease_Diagnostic_Criteria.md')
OUTPUT_JS_FILE = os.path.join(os.path.dirname(__file__), 'labs_data.js')

def assign_category(title, aliases, desc, normal_vals):
    full_text = (title + " " + aliases + " " + desc).lower()
    
    # Imaging / Procedures
    if any(k in full_text for k in ['sonogram', 'ultrasound', 'x-ray', 'radiography', 'scan', 'biopsy', 
                                    'scintigraphy', 'catheterization', 'angiography', 'endoscopy', 
                                    'colonoscopy', 'bronchoscopy', 'arthroscopy', 'echocardiography', 
                                    'magnetic resonance', 'computed tomography', 'electrocardiography', 
                                    'densitometry', 'mammography', 'swallow', 'enema', 'pyelography']):
        return "Imaging & Procedures"
    
    # Body Fluids / CSF / Synovial
    if any(k in full_text for k in ['cerebrospinal', 'csf', 'synovial', 'arthrocentesis', 'amniocentesis', 
                                    'thoracentesis', 'paracentesis', 'pleural fluid', 'peritoneal', 'semen']):
        return "Body Fluids & CSF"
    
    # Urinalysis
    if any(k in full_text for k in ['urine', 'urinalysis', 'creatinine clearance', 'microalbuminuria', 'proteinuria', 'bence jones']):
        return "Urinalysis & Renal Clearance"

    # Hematology & Coagulation
    if any(k in full_text for k in ['blood smear', 'complete blood count', 'cbc', 'red blood cell', 'rbc', 
                                    'hemoglobin', 'hematocrit', 'platelet', 'prothrombin', 'pt/inr', 'ptt', 
                                    'partial thromboplastin', 'fibrinogen', 'd-dimer', 'bleeding time', 
                                    'erythrocyte sedimentation', 'esr', 'reticulocyte', 'antithrombin', 
                                    'coagulation', 'bone marrow', 'white blood cell count', 'differential count']):
        return "Hematology & Coagulation"

    # Endocrine & Hormones
    if any(k in full_text for k in ['hormone', 'thyroid', 'tsh', 'thyroxine', 'triiodothyronine', 
                                    'cortisol', 'acth', 'aldosterone', 'renin', 'insulin', 'c-peptide', 
                                    'glucagon', 'prolactin', 'growth hormone', 'catecholamines', 
                                    'metanephrines', 'vanillylmandelic', 'parathyroid', 'pth', 
                                    'estrogen', 'progesterone', 'testosterone', 'lh', 'fsh', 'gastrin', 'hCG']):
        return "Endocrine & Hormones"

    # Immunology, Serology & Autoantibodies
    if any(k in full_text for k in ['antibody', 'antibodies', 'antinuclear', 'ana', 'anca', 'rheumatoid factor', 
                                    'complement', 'immunoglobulin', 'iga', 'igg', 'igm', 'ige', 'hla', 
                                    'antigen', 'titer', 'monospot', 'serology', 'hepatitis b surface', 
                                    'western blot', 'elisa', 'treponema', 'vdrl', 'rpr']):
        return "Immunology & Serology"

    # Microbiology & Infectious
    if any(k in full_text for k in ['culture', 'sensitivity', 'gram stain', 'bacilli', 'afb', 'fungal', 
                                    'tuberculosis', 'chlamydia', 'gonorrhea', 'streptococcal', 'candida']):
        return "Microbiology & Cultures"

    # Default to Blood Chemistry
    return "Blood Chemistry & Metabolism"

COMPOUND_PAIRS = {
    ('rh', 'negative'): 'Rh-negative',
    ('rh', 'positive'): 'Rh-positive',
    ('stuart', 'prower'): 'Stuart-Prower',
    ('zollinger', 'ellison'): 'Zollinger-Ellison',
    ('corticotropin', 'releasing'): 'corticotropin-releasing',
    ('thyrotropin', 'releasing'): 'thyrotropin-releasing',
    ('gonadotropin', 'releasing'): 'gonadotropin-releasing',
    ('water', 'based'): 'water-based',
    ('enzyme', 'linked'): 'enzyme-linked',
    ('false', 'positive'): 'false-positive',
    ('false', 'negative'): 'false-negative',
    ('acid', 'base'): 'acid-base',
    ('acid', 'fast'): 'acid-fast',
    ('follow', 'up'): 'follow-up',
    ('first', 'line'): 'first-line',
    ('second', 'line'): 'second-line',
    ('short', 'term'): 'short-term',
    ('long', 'term'): 'long-term',
    ('dose', 'dependent'): 'dose-dependent',
    ('cell', 'mediated'): 'cell-mediated',
    ('antigen', 'antibody'): 'antigen-antibody',
    ('carrier', 'mediated'): 'carrier-mediated',
    ('weight', 'bearing'): 'weight-bearing',
    ('life', 'threatening'): 'life-threatening',
    ('dye', 'induced'): 'dye-induced',
    ('contrast', 'induced'): 'contrast-induced',
}

def repl_hyphen(m):
    w1, w2 = m.group(1), m.group(2)
    key_lower = (w1.lower(), w2.lower())
    if key_lower in COMPOUND_PAIRS:
        return COMPOUND_PAIRS[key_lower]
    if w1[0].isupper() and w2[0].isupper():
        return f'{w1}-{w2}'
    return f'{w1}{w2}'

def clean_prose(raw_text):
    if not raw_text:
        return ''
    text = raw_text.strip()
    text = re.sub(r'<a id=[^>]+></a>', '', text)
    text = re.sub(r'(?:^|\n)>\s*\[!(?:WARNING|NOTE|CAUTION|IMPORTANT|TIP)\]\s*', '\n', text)
    text = re.sub(r'\[!(?:WARNING|NOTE|CAUTION|IMPORTANT|TIP)\]\s*', '', text)
    text = re.sub(r'(^|\n)>\s*', r'\1', text)
    text = re.sub(r'\n---\s*$', '', text.strip())
    text = re.sub(r'<a id=[^>]+></a>', '', text)
    text = re.sub(r'([a-zA-Z]{2,})-\n\s*([a-zA-Z]{2,})', repl_hyphen, text)
    
    paragraphs = re.split(r'\n\s*\n', text)
    clean_paragraphs = []
    for p in paragraphs:
        p = p.strip()
        if not p or p == '---':
            continue
        lines = p.split('\n')
        clean_lines = []
        cur_item = ''
        for line in lines:
            line_str = line.strip()
            if not line_str or line_str == '---' or '<a id=' in line_str:
                continue
            is_bullet = bool(re.match(r'^(?:[•\-\*]|\d+[\.\)])\s+', line_str))
            if is_bullet:
                content_after_bullet = re.sub(r'^(?:[•\-\*]|\d+[\.\)])\s+', '', line_str).strip()
                if cur_item and content_after_bullet and content_after_bullet[0].islower() and not content_after_bullet.startswith(('ph', 'egfr', 'ctn', 'pco2', 'po2', 's/p', 'beta', 't(')):
                    if cur_item.endswith('/') or cur_item.endswith('-'):
                        cur_item += content_after_bullet
                    else:
                        cur_item += ' ' + content_after_bullet
                else:
                    if cur_item:
                        clean_lines.append(cur_item)
                    cur_item = line_str
            else:
                if cur_item:
                    if cur_item.endswith('/') or cur_item.endswith('-'):
                        cur_item += line_str
                    else:
                        cur_item += ' ' + line_str
                else:
                    cur_item = line_str
        if cur_item:
            clean_lines.append(cur_item)
        clean_paragraphs.append('\n'.join(clean_lines))
        
    res = '\n\n'.join(clean_paragraphs).strip()
    res = re.sub(r'<a id=[^>]+></a>', '', res)
    res = re.sub(r'\n---\s*$', '', res.strip())
    return res.strip()

def parse_bullet_list(raw_text):
    if not raw_text:
        return []
    text = raw_text.strip()
    text = re.sub(r'<a id=[^>]+></a>', '', text)
    text = re.sub(r'\n---\s*$', '', text.strip())
    text = re.sub(r'(^|\n)>\s*', r'\1', text)
    text = re.sub(r'([a-zA-Z]{2,})-\n\s*([a-zA-Z]{2,})', repl_hyphen, text)
    
    items = []
    cur_item = ''
    for line in text.split('\n'):
        l = line.strip()
        if not l or l == '---' or '<a id=' in l:
            continue
        m_bullet = re.match(r'^(?:[•\-\*]|\d+[\.\)])\s+(.*)$', l)
        if m_bullet:
            content = m_bullet.group(1).strip()
            if cur_item and content and content[0].islower() and not content.startswith(('ph', 'egfr', 'ctn', 'pco2', 'po2', 's/p', 'beta', 't(')):
                if cur_item.endswith('/') or cur_item.endswith('-'):
                    cur_item += content
                else:
                    cur_item += ' ' + content
            else:
                if cur_item:
                    items.append(cur_item)
                cur_item = content
        else:
            if cur_item:
                if cur_item.endswith('/') or cur_item.endswith('-'):
                    cur_item += l
                else:
                    cur_item += ' ' + l
            else:
                cur_item = l
    if cur_item:
        items.append(cur_item)
    return [it.strip() for it in items if it.strip() and it.strip() != '---']

def parse_lab_tests(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    chunks = re.split(r'\n###\s+(\d+)\.\s+', content)
    tests = []
    num_tests = (len(chunks) - 1) // 2

    section_headers = [
        ("aliases", r'-\s+\*\*别名与缩写\s*\(Aliases & Abbreviations\)\*\*:\s*(.+)'),
        ("pages", r'-\s+\*\*原书页码\s*\(Page Range\)\*\*:\s*(.+)'),
        ("desc", r'####\s+📋\s+检测描述与临床意义\s*\(Test Description\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
        ("evidence", r'####\s+🛡️\s+循证临床实践指南\s*\(The Evidence for Practice\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
        ("normal", r'####\s+🧪\s+正常参考范围\s*\(Normal Values\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
        ("abnormal", r'####\s+📊\s+异常结果临床意义与解释\s*\(Possible Meanings of Abnormal Values\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
        ("factors", r'####\s+⚠️\s+干扰因素与影响条件\s*\(Contributing Factors to Abnormal Values\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
        ("alerts", r'####\s+🚨\s+临床高危预警与核心考点\s*\(Clinical Alerts & Practice Pearls\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
        ("contra", r'####\s+⛔\s+禁忌证\s*\(Contraindications\)\s*\n([\s\S]*?)(?=\n####|\Z)'),
    ]

    for i in range(1, num_tests + 1):
        test_id = int(chunks[2*i - 1])
        body = chunks[2*i]
        # Clean anchors and trailing dividers from body chunk immediately
        body = re.sub(r'<a id=[^>]+></a>', '', body)
        body = re.sub(r'\n---\s*$', '', body.strip())

        lines = body.split('\n')
        title = lines[0].strip()

        # Parse sections
        aliases = ""
        m_al = re.search(section_headers[0][1], body)
        if m_al:
            aliases = m_al.group(1).strip().strip('`')

        pages = ""
        m_pg = re.search(section_headers[1][1], body)
        if m_pg:
            pages = m_pg.group(1).strip()

        def get_sec(regex):
            m = re.search(regex, body)
            return m.group(1).strip() if m else ""

        desc = clean_prose(get_sec(section_headers[2][1]))
        evidence = clean_prose(get_sec(section_headers[3][1]))
        normal = clean_prose(get_sec(section_headers[4][1]))
        abnormal_raw = get_sec(section_headers[5][1])
        factors = clean_prose(get_sec(section_headers[6][1]))
        alerts = clean_prose(get_sec(section_headers[7][1]))
        contra = clean_prose(get_sec(section_headers[8][1]))

        # Parse increased / decreased / abnormal findings inside abnormal_raw
        increased = []
        decreased = []
        abnormal_findings = []

        m_inc = re.search(r'#####\s+🔺\s+升高\s*/\s*阳性\s*\(Increased / Positive\)\s*\n([\s\S]*?)(?=\n#####|\Z)', abnormal_raw)
        if m_inc:
            increased = parse_bullet_list(m_inc.group(1))

        m_dec = re.search(r'#####\s+🔻\s+降低\s*/\s*阴性\s*\(Decreased / Negative\)\s*\n([\s\S]*?)(?=\n#####|\Z)', abnormal_raw)
        if m_dec:
            decreased = parse_bullet_list(m_dec.group(1))

        m_ab = re.search(r'#####\s+🔍\s+异常发现与相关疾病\s*\(Abnormal Findings & Associated Conditions\)\s*\n([\s\S]*?)(?=\n#####|\Z)', abnormal_raw)
        if m_ab:
            abnormal_findings = parse_bullet_list(m_ab.group(1))

        cat = assign_category(title, aliases, desc, normal)

        tests.append({
            "id": test_id,
            "title": title,
            "aliases": aliases,
            "pages": pages,
            "category": cat,
            "description": desc,
            "evidence": evidence,
            "normalValues": normal,
            "increased": increased,
            "decreased": decreased,
            "abnormalFindings": abnormal_findings,
            "contributingFactors": factors,
            "clinicalAlerts": alerts,
            "contraindications": contra
        })

    return tests

def parse_disease_criteria(filepath):
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()

    system_blocks = re.split(r'\n##\s+(\d+\.\s*.+)\n', content)
    num_systems = (len(system_blocks) - 1) // 2

    systems_data = []

    for i in range(1, num_systems + 1):
        raw_sys_title = system_blocks[2*i - 1].strip()
        sys_body = system_blocks[2*i]

        # Clean system title e.g. "1. Cardiovascular Disorders"
        sys_en = re.sub(r'^\d+\.\s*', '', raw_sys_title).strip()

        # Split diseases in this system: e.g. '### 1.1 Acute Coronary Syndrome & Acute Myocardial Infarction'
        d_chunks = re.split(r'\n###\s+(\d+\.\d+)\s+', '\n' + sys_body)
        num_diseases = (len(d_chunks) - 1) // 2
        diseases = []

        for d_idx in range(1, num_diseases + 1):
            d_code = d_chunks[2*d_idx - 1].strip()
            d_body = d_chunks[2*d_idx]
            lines = d_body.split('\n')
            d_full_title = lines[0].strip()

            # Extract fields
            guideline = ""
            m_guide = re.search(r'-\s+\*\*Authoritative Diagnostic Criteria & Guideline Source\*\*:\s*(.+)', d_body)
            if m_guide:
                guideline = m_guide.group(1).strip()

            related_tests = ""
            m_rel = re.search(r'-\s+\*\*Manual Test References\*\*:\s*(.+)', d_body)
            if m_rel:
                related_tests = m_rel.group(1).strip()

            # Clean up the body lines
            body_content = "\n".join(lines[1:]).strip()

            diseases.append({
                "code": d_code,
                "title": d_full_title,
                "titleEn": d_full_title,
                "guideline": guideline,
                "relatedTests": related_tests,
                "content": body_content
            })

        systems_data.append({
            "systemId": i,
            "systemTitle": sys_en,
            "systemEn": sys_en,
            "diseases": diseases
        })

    return systems_data

def build():
    print("Parsing 01_Laboratory_Tests_Manual.md...")
    tests = parse_lab_tests(LAB_TESTS_FILE)
    print(f" -> Successfully parsed {len(tests)} tests!")

    print("Parsing 02_Disease_Diagnostic_Criteria.md...")
    systems = parse_disease_criteria(DISEASE_FILE)
    total_diseases = sum(len(s['diseases']) for s in systems)
    print(f" -> Successfully parsed {len(systems)} systems and {total_diseases} diseases!")

    js_content = f"""/* Auto-generated Clinical Laboratory and Disease Diagnostic Criteria Database */
/* Generated from Wilson's Manual of Laboratory and Diagnostic Tests */
window.USMLE_LAB_TESTS = {json.dumps(tests, ensure_ascii=False, indent=2)};

window.USMLE_DISEASE_CRITERIA = {json.dumps(systems, ensure_ascii=False, indent=2)};
"""

    with open(OUTPUT_JS_FILE, 'w', encoding='utf-8') as f:
        f.write(js_content)

    print(f"Done! Written to {OUTPUT_JS_FILE} ({len(js_content)} chars)")

if __name__ == '__main__':
    build()
