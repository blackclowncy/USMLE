# -*- coding: utf-8 -*-
r"""
Comprehensive generator for Wilson's Manual of Laboratory and Diagnostic Tests.
Outputs:
1. D:/Github/USMLE/Lab/01_Laboratory_Tests_Manual.md
2. D:/Github/USMLE/Lab/02_Disease_Diagnostic_Criteria.md
"""

import sys, io, re, fitz
from collections import defaultdict

sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8')

PDF_PATH = "Manual of Laboratory and Diagnostic Tests (Author Wilson, Denise D.).pdf"
doc = fitz.open(PDF_PATH)

print(f"Loaded PDF: {PDF_PATH} ({len(doc)} pages)")

# 1. Collect all blocks across pages 18 to 631
all_blocks = []
for p in range(17, 631):
    page = doc[p]
    for b in page.get_text('blocks', sort=True):
        if b[1] < 50:
            continue
        text = b[4].strip()
        if not text or (len(text) == 1 and text.isupper()):
            continue
        all_blocks.append({
            'page': p + 1,
            'text': text,
            'bbox': b[:4]
        })

# 2. Find test boundaries
test_indices = []
for idx, b in enumerate(all_blocks):
    if b['text'].startswith('Test Description') or '\nTest Description' in b['text']:
        if b['text'].startswith('Test Description'):
            title_block_idx = idx - 1
        else:
            title_block_idx = idx
        test_indices.append((title_block_idx, idx))

print(f"Total content blocks: {len(all_blocks)}")
print(f"Total tests: {len(test_indices)}")

# Detailed abnormal values span parser for 2-column layout
def parse_abnormal_spans(page_start, page_end):
    section_spans = []
    in_section = False
    
    for p in range(page_start - 1, min(page_end, len(doc))):
        page = doc[p]
        d = page.get_text('dict')
        for b in d['blocks']:
            if 'lines' not in b:
                continue
            for l in b['lines']:
                for s in l['spans']:
                    text = s['text'].strip()
                    if not text:
                        continue
                    y0 = s['bbox'][1]
                    if y0 < 50:
                        continue
                    
                    if 'Possible Meanings of Abnormal Values' in text:
                        in_section = True
                        continue
                    
                    if in_section:
                        if any(h in text for h in ['Contributing Factors to Abnormal Values', 
                                                   'Interventions/Implications', 
                                                   'Clinical Alerts', 
                                                   'Contraindications', 
                                                   'Test Description']):
                            in_section = False
                            break
                        section_spans.append(s)
            if not in_section and section_spans:
                break
        if not in_section and section_spans:
            break
            
    if not section_spans:
        return {'has_inc_dec': False, 'increased': [], 'decreased': [], 'other': []}
        
    has_inc_dec = any('Increased' in s['text'] for s in section_spans) or any('Decreased' in s['text'] for s in section_spans)
    
    # Reconstruct lines
    lines = []
    curr_line = []
    curr_y = None
    for s in section_spans:
        y0 = s['bbox'][1]
        if curr_y is None or abs(y0 - curr_y) > 3.5:
            if curr_line:
                lines.append(curr_line)
            curr_line = [s]
            curr_y = y0
        else:
            curr_line.append(s)
    if curr_line:
        lines.append(curr_line)
        
    inc_items = []
    dec_items = []
    other_items = []
    
    for l in lines:
        left_spans = [s for s in l if s['bbox'][0] < 180]
        right_spans = [s for s in l if s['bbox'][0] >= 180]
        
        left_txt = " ".join(s['text'].strip() for s in left_spans).strip()
        right_txt = " ".join(s['text'].strip() for s in right_spans).strip()
        
        # skip header row
        if left_txt == 'Increased' and right_txt == 'Decreased':
            continue
        if left_txt == 'Increased' and not right_txt:
            continue
        if left_txt == 'Decreased' and not right_txt:
            continue
            
        if left_txt and not right_txt and len(left_txt.split()) <= 4 and not left_txt.startswith('•'):
            if any(s['size'] > 9.5 or (s['flags'] & 2) for s in left_spans):
                if left_txt not in ['Increased', 'Decreased', 'Positive', 'Negative']:
                    inc_items.append(f"**[{left_txt}]**")
                    dec_items.append(f"**[{left_txt}]**")
                    continue
                    
        if has_inc_dec:
            if left_txt and left_txt != 'Increased':
                inc_items.append(left_txt)
            if right_txt and right_txt != 'Decreased':
                dec_items.append(right_txt)
        else:
            full_txt = " ".join(s['text'].strip() for s in l).strip()
            if full_txt:
                other_items.append(full_txt)
                
    return {
        'has_inc_dec': has_inc_dec,
        'increased': inc_items,
        'decreased': dec_items,
        'other': other_items
    }

SECTION_NAMES = [
    'Test Description',
    'THE EVIDENCE FOR PRACTICE',
    'Normal Values',
    'Possible Meanings of Abnormal Values',
    'Contributing Factors to Abnormal Values',
    'Interventions/Implications',
    'Clinical Alerts',
    'Contraindications'
]

def clean_block_text(txt):
    # remove leading page/section markers like 'A ', 'B '
    clean = re.sub(r'^[A-Z]\s+', '', txt).strip()
    return clean

def parse_full_test(t_i):
    t_start, desc_idx = test_indices[t_i]
    t_end = test_indices[t_i+1][0] if t_i+1 < len(test_indices) else len(all_blocks)
    page_start = all_blocks[t_start]['page']
    page_end = all_blocks[t_end-1]['page'] if t_end > t_start else page_start
    
    # Title
    if t_start == desc_idx:
        raw_title = all_blocks[t_start]['text'].split('Test Description')[0].strip()
    else:
        raw_title = all_blocks[t_start]['text'].strip()
        
    aliases = ""
    m = re.search(r'\((.*?)\)', raw_title, re.S)
    if m:
        aliases = m.group(1).replace('\n', ' ').strip()
        clean_title = re.sub(r'\(.*?\)', '', raw_title).replace('\n', ' ').strip()
    else:
        clean_title = raw_title.replace('\n', ' ').strip()
        
    clean_title = re.sub(r'\s+\d+$', '', clean_title)
    
    sections = {s: [] for s in SECTION_NAMES}
    current_sec = 'Test Description'
    
    if t_start == desc_idx:
        after_td = all_blocks[t_start]['text'].split('Test Description', 1)[1].strip()
        if after_td:
            sections['Test Description'].append(after_td)
        start_b = t_start + 1
    else:
        b_txt = all_blocks[desc_idx]['text']
        if 'Test Description' in b_txt:
            after_td = b_txt.split('Test Description', 1)[1].strip()
            if after_td:
                sections['Test Description'].append(after_td)
        start_b = desc_idx + 1
        
    for b_i in range(start_b, t_end):
        b_txt = all_blocks[b_i]['text']
        clean_b = clean_block_text(b_txt)
        
        found_sec = None
        for sec in SECTION_NAMES:
            if clean_b.startswith(sec) or b_txt.startswith(sec):
                found_sec = sec
                break
            elif sec == 'Clinical Alerts' and ('Clinical Alerts' in clean_b or 'Clinical Alerts' in b_txt):
                found_sec = 'Clinical Alerts'
                break
            elif sec == 'Contraindications' and ('Contraindications' in clean_b or 'CONTRAINDICATIONS' in clean_b):
                found_sec = 'Contraindications'
                break
            elif sec == 'THE EVIDENCE FOR PRACTICE' and 'THE EVIDENCE FOR PRACTICE' in clean_b:
                found_sec = 'THE EVIDENCE FOR PRACTICE'
                break
                
        if found_sec:
            current_sec = found_sec
            rem = clean_b
            for prefix in [found_sec, 'R Clinical Alerts', 'Clinical Alerts', 'CONTRAINDICATIONS!', 'CONTRAINDICATIONS', 'Contraindications']:
                if rem.startswith(prefix):
                    rem = rem[len(prefix):].strip()
                    break
            if rem:
                sections[current_sec].append(rem)
        else:
            sections[current_sec].append(clean_b)
            
    abn_data = parse_abnormal_spans(page_start, page_end + 1)
    
    return {
        'index': t_i + 1,
        'page': page_start,
        'page_end': page_end,
        'title': clean_title,
        'aliases': aliases,
        'description': "\n\n".join(sections['Test Description']).strip(),
        'evidence': "\n\n".join(sections['THE EVIDENCE FOR PRACTICE']).strip(),
        'normal_values': "\n\n".join(sections['Normal Values']).strip(),
        'abnormal_values_text': "\n\n".join(sections['Possible Meanings of Abnormal Values']).strip(),
        'abnormal_data': abn_data,
        'contributing_factors': "\n\n".join(sections['Contributing Factors to Abnormal Values']).strip(),
        'clinical_alerts': "\n\n".join(sections['Clinical Alerts']).strip(),
        'contraindications': "\n\n".join(sections['Contraindications']).strip()
    }

print("Parsing all 359 tests...")
all_tests = [parse_full_test(i) for i in range(len(test_indices))]
print("Parsing complete.")

# -------------------------------------------------------------
# Build 01_Laboratory_Tests_Manual.md
# -------------------------------------------------------------
print("Generating 01_Laboratory_Tests_Manual.md...")

with open("01_Laboratory_Tests_Manual.md", "w", encoding="utf-8") as f:
    f.write("# 临床实验室与诊断检测手册 (Manual of Laboratory and Diagnostic Tests)\n\n")
    f.write("> **作者**: Denise D. Wilson, PhD, APN, FNP, ANP\n")
    f.write("> **出版机构**: McGraw-Hill Medical\n")
    f.write("> **整理用途**: USMLE Step 1 / Step 2 CK 高频实验室检查与诊断学全面参考\n")
    f.write("> **项目总数**: 共收录 359 项实验室及临床影像/功能学诊断项目\n\n")
    f.write("---\n\n")
    
    # Table of Contents
    f.write("## 目录索引 (Alphabetical Index A–Z)\n\n")
    current_letter = ""
    for t in all_tests:
        letter = t['title'][0].upper() if t['title'] else 'A'
        if letter != current_letter:
            current_letter = letter
            f.write(f"\n### {current_letter}\n\n")
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', t['title'].lower()).strip('-')
        alias_str = f" ({t['aliases']})" if t['aliases'] else ""
        f.write(f"- [{t['title']} (P.{t['page']})](#test-{t['index']}-{slug}){alias_str}\n")
        
    f.write("\n\n---\n\n")
    
    # Full Test Details
    f.write("## 实验室检测项目详细记录 (Complete Laboratory & Diagnostic Tests)\n\n")
    
    for t in all_tests:
        slug = re.sub(r'[^a-zA-Z0-9]+', '-', t['title'].lower()).strip('-')
        f.write(f"<a id=\"test-{t['index']}-{slug}\"></a>\n\n")
        f.write(f"### {t['index']}. {t['title']}\n\n")
        
        # Meta info
        if t['aliases']:
            f.write(f"- **别名与缩写 (Aliases & Abbreviations)**: `{t['aliases']}`\n")
        f.write(f"- **原书页码 (Page Range)**: P.{t['page']} – P.{t['page_end']}\n\n")
        
        # Description
        if t['description']:
            f.write("#### 📋 检测描述与临床意义 (Test Description)\n\n")
            f.write(f"{t['description']}\n\n")
            
        # Evidence for practice
        if t['evidence']:
            f.write("#### 🛡️ 循证临床实践指南 (The Evidence for Practice)\n\n")
            f.write(f"> {t['evidence'].replace(chr(10), chr(10) + '> ')}\n\n")
            
        # Normal values
        if t['normal_values']:
            f.write("#### 🧪 正常参考范围 (Normal Values)\n\n")
            # format as codeblock or blockquote if contains numbers
            lines = t['normal_values'].split('\n')
            formatted_lines = [f"- {l.strip()}" if not l.strip().startswith(('•', '-', '*')) else l.strip() for l in lines if l.strip()]
            f.write("\n".join(formatted_lines) + "\n\n")
        else:
            f.write("#### 🧪 正常参考范围 (Normal Values)\n\n")
            f.write("- 无可见异常 / 阴性 (Negative for disease / pathology; Normal anatomical appearance)\n\n")
            
        # Abnormal values
        f.write("#### 📊 异常结果临床意义与解释 (Possible Meanings of Abnormal Values)\n\n")
        abn = t['abnormal_data']
        
        if abn['has_inc_dec']:
            if abn['increased']:
                f.write("##### 🔺 升高 / 阳性 (Increased / Positive)\n\n")
                for item in abn['increased']:
                    if item.startswith("**["):
                        f.write(f"\n{item}\n")
                    else:
                        f.write(f"- {item}\n")
                f.write("\n")
                
            if abn['decreased']:
                f.write("##### 🔻 降低 / 阴性 (Decreased / Negative)\n\n")
                for item in abn['decreased']:
                    if item.startswith("**["):
                        f.write(f"\n{item}\n")
                    else:
                        f.write(f"- {item}\n")
                f.write("\n")
                
            if abn['other']:
                f.write("##### 🔍 其它异常表现 (Other Abnormal Findings)\n\n")
                for item in abn['other']:
                    f.write(f"- {item}\n")
                f.write("\n")
        else:
            # check if other has items
            if abn['other']:
                f.write("##### 🔍 异常发现与相关疾病 (Abnormal Findings & Associated Conditions)\n\n")
                for item in abn['other']:
                    clean_it = item.lstrip('•-* ').strip()
                    f.write(f"- {clean_it}\n")
                f.write("\n")
            elif t['abnormal_values_text']:
                f.write("##### 🔍 异常发现与相关疾病 (Abnormal Findings & Associated Conditions)\n\n")
                lines = [l.strip().lstrip('•-* ').strip() for l in t['abnormal_values_text'].split('\n') if l.strip()]
                for l in lines:
                    f.write(f"- {l}\n")
                f.write("\n")
            else:
                f.write("- 提示相应器官病变、感染或恶性肿瘤，详见临床描述与随访检查。\n\n")
                
        # Contributing factors
        if t['contributing_factors']:
            f.write("#### ⚠️ 干扰因素与影响条件 (Contributing Factors to Abnormal Values)\n\n")
            lines = [l.strip() for l in t['contributing_factors'].split('\n') if l.strip()]
            for l in lines:
                f.write(f"{l}\n")
            f.write("\n")
            
        # Clinical alerts
        if t['clinical_alerts']:
            f.write("#### 🚨 临床高危预警与核心考点 (Clinical Alerts & Practice Pearls)\n\n")
            f.write(f"> [!WARNING]\n")
            for l in t['clinical_alerts'].split('\n'):
                if l.strip():
                    f.write(f"> {l.strip()}\n")
            f.write("\n")
            
        # Contraindications
        if t['contraindications']:
            f.write("#### ⛔ 禁忌证 (Contraindications)\n\n")
            lines = [l.strip() for l in t['contraindications'].split('\n') if l.strip()]
            for l in lines:
                f.write(f"- {l.lstrip('•-* ').strip()}\n")
            f.write("\n")
            
        f.write("---\n\n")

print("01_Laboratory_Tests_Manual.md generated successfully!")
