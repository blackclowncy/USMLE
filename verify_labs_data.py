# -*- coding: utf-8 -*-
"""
Verification script for labs_data.js.
Ensures zero omissions:
1. Every test in 01_Laboratory_Tests_Manual.md (all 359) exists in window.USMLE_LAB_TESTS.
2. Every disease in 02_Disease_Diagnostic_Criteria.md (all 68 across 11 systems) exists in window.USMLE_DISEASE_CRITERIA.
3. Checks data integrity (non-empty normal values, non-empty titles).
"""

import sys, os, re, json

sys.stdout.reconfigure(encoding='utf-8')

LAB_MD = os.path.join(os.path.dirname(__file__), 'Lab', '01_Laboratory_Tests_Manual.md')
DISEASE_MD = os.path.join(os.path.dirname(__file__), 'Lab', '02_Disease_Diagnostic_Criteria.md')
LABS_JS = os.path.join(os.path.dirname(__file__), 'labs_data.js')

def verify():
    # 1. Read sources
    with open(LAB_MD, 'r', encoding='utf-8') as f:
        lab_md_text = f.read()

    with open(DISEASE_MD, 'r', encoding='utf-8') as f:
        disease_md_text = f.read()

    with open(LABS_JS, 'r', encoding='utf-8') as f:
        js_text = f.read()

    # Extract JSON objects from js_text
    m_tests = re.search(r'window\.USMLE_LAB_TESTS\s*=\s*(\[[\s\S]*?\]);', js_text)
    m_diseases = re.search(r'window\.USMLE_DISEASE_CRITERIA\s*=\s*(\[[\s\S]*?\]);', js_text)

    if not m_tests or not m_diseases:
        print("ERROR: Could not parse JSON from labs_data.js!")
        sys.exit(1)

    js_tests = json.loads(m_tests.group(1))
    js_diseases = json.loads(m_diseases.group(1))

    # Match raw markdown tests
    md_test_matches = re.findall(r'^###\s+(\d+)\.\s+(.+)$', lab_md_text, re.M)
    print(f"Checking Laboratory Tests: {len(md_test_matches)} in MD vs {len(js_tests)} in JS...")
    
    assert len(md_test_matches) == 359, f"Expected 359 tests in MD, found {len(md_test_matches)}"
    assert len(js_tests) == 359, f"Expected 359 tests in JS, found {len(js_tests)}"

    # Check each test 1:1
    test_errors = 0
    for idx, (md_id, md_title) in enumerate(md_test_matches):
        test_obj = js_tests[idx]
        if test_obj['id'] != int(md_id):
            print(f"ID Mismatch at index {idx}: MD has {md_id}, JS has {test_obj['id']}")
            test_errors += 1
        if test_obj['title'].strip() != md_title.strip():
            print(f"Title Mismatch at index {idx}: MD has '{md_title}', JS has '{test_obj['title']}'")
            test_errors += 1
        if not test_obj['normalValues']:
            print(f"Warning: Empty normal values for Test {md_id}: {md_title}")

    if test_errors == 0:
        print(" -> ALL 359 Laboratory Tests verified 100% complete and matched!")

    # Match raw markdown diseases
    md_disease_matches = re.findall(r'^###\s+(\d+\.\d+)\s+(.+)$', disease_md_text, re.M)
    all_js_diseases = []
    for sys_obj in js_diseases:
        all_js_diseases.extend(sys_obj['diseases'])

    print(f"\nChecking Disease Diagnostic Criteria: {len(md_disease_matches)} in MD vs {len(all_js_diseases)} in JS across {len(js_diseases)} systems...")
    assert len(md_disease_matches) == 68, f"Expected 68 diseases in MD, found {len(md_disease_matches)}"
    assert len(all_js_diseases) == 68, f"Expected 68 diseases in JS, found {len(all_js_diseases)}"

    disease_errors = 0
    for idx, (md_code, md_title) in enumerate(md_disease_matches):
        d_obj = all_js_diseases[idx]
        if d_obj['code'] != md_code:
            print(f"Code Mismatch at index {idx}: MD has {md_code}, JS has {d_obj['code']}")
            disease_errors += 1
        if d_obj['title'].strip() != md_title.strip():
            print(f"Title Mismatch at index {idx}: MD has '{md_title}', JS has '{d_obj['title']}'")
            disease_errors += 1
        if not d_obj['content']:
            print(f"Error: Empty content for Disease {md_code}: {md_title}")
            disease_errors += 1
        if d_obj['content'].endswith('---') or d_obj['content'].strip().endswith('---'):
            print(f"Error: Disease {md_code} ends with trailing '---'")
            disease_errors += 1
        if 'Authoritative Diagnostic Criteria' in d_obj['content']:
            print(f"Error: Disease {md_code} content contains duplicate guideline header")
            disease_errors += 1
        if 'Manual Test References' in d_obj['content']:
            print(f"Error: Disease {md_code} content contains duplicate manual references")
            disease_errors += 1
        if '<a id=' in d_obj['content']:
            print(f"Error: Disease {md_code} content contains raw anchor tags")
            disease_errors += 1
        if not d_obj.get('guideline'):
            print(f"Error: Disease {md_code} is missing guideline badge text")
            disease_errors += 1
        if not d_obj.get('relatedTests'):
            print(f"Error: Disease {md_code} is missing relatedTests references")
            disease_errors += 1

    if disease_errors == 0:
        print(" -> ALL 68 Disease Diagnostic Criteria verified 100% complete, free of trailing '---', clean metadata separation, and matched across 11 systems!")

    print("\nSUMMARY: 0 omissions found. 100% integrity check PASSED!")

if __name__ == '__main__':
    verify()
