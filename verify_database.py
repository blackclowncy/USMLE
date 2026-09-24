# -*- coding: utf-8 -*-
"""
Verification script for questions_data.js.
Ensures 100% data integrity and zero omissions across USMLE Step 1 question banks:
1. Pathology: 14 chapters, 2,100 questions.
2. Pharmacology: 9 chapters, 1,350 questions.
3. Total: 3,450 questions, all fully formed with valid options, answers, and explanations.
"""

import os
import sys
import json
import re

def verify_database():
    current_dir = os.path.dirname(os.path.abspath(__file__))
    js_path = os.path.join(current_dir, 'questions_data.js')

    if not os.path.exists(js_path):
        print(f"ERROR: {js_path} does not exist!")
        sys.exit(1)

    print("Reading questions_data.js...")
    with open(js_path, 'r', encoding='utf-8') as f:
        content = f.read()

    # Extract JSON objects
    m_disc = re.search(r'window\.USMLE_DISCIPLINES\s*=\s*(\[[\s\S]*?\]);', content)
    m_path_ch = re.search(r'window\.USMLE_PATHOLOGY_CHAPTERS\s*=\s*(\[[\s\S]*?\]);', content)
    m_pharm_ch = re.search(r'window\.USMLE_PHARMACOLOGY_CHAPTERS\s*=\s*(\[[\s\S]*?\]);', content)
    m_bio_ch = re.search(r'window\.USMLE_BIOCHEMISTRY_CHAPTERS\s*=\s*(\[[\s\S]*?\]);', content)
    m_q = re.search(r'window\.USMLE_QUESTIONS\s*=\s*(\[[\s\S]*?\]);', content)

    assert m_disc, "Failed to extract USMLE_DISCIPLINES"
    assert m_path_ch, "Failed to extract USMLE_PATHOLOGY_CHAPTERS"
    assert m_pharm_ch, "Failed to extract USMLE_PHARMACOLOGY_CHAPTERS"
    assert m_bio_ch, "Failed to extract USMLE_BIOCHEMISTRY_CHAPTERS"
    assert m_q, "Failed to extract USMLE_QUESTIONS"

    disciplines = json.loads(m_disc.group(1))
    pathology_chapters = json.loads(m_path_ch.group(1))
    pharmacology_chapters = json.loads(m_pharm_ch.group(1))
    biochemistry_chapters = json.loads(m_bio_ch.group(1))
    questions = json.loads(m_q.group(1))

    print(f"\n[1/5] Disciplines Verified: {len(disciplines)} disciplines registered.")
    for d in disciplines:
        print(f"  - {d['name']}: {d['count']} questions ({d['status']})")

    assert len(pathology_chapters) == 14, f"Expected 14 Pathology chapters, got {len(pathology_chapters)}"
    assert len(pharmacology_chapters) == 9, f"Expected 9 Pharmacology chapters, got {len(pharmacology_chapters)}"
    assert len(biochemistry_chapters) == 23, f"Expected 23 Biochemistry chapters, got {len(biochemistry_chapters)}"

    print(f"\n[2/5] Chapter Definitions Verified:")
    print(f"  - Pathology: {len(pathology_chapters)} chapters (150 Qs each = 2,100 Qs)")
    print(f"  - Pharmacology: {len(pharmacology_chapters)} chapters (150 Qs each = 1,350 Qs)")
    print(f"  - Biochemistry: {len(biochemistry_chapters)} chapters (150 Qs each = 3,450 Qs)")

    for ch in pathology_chapters:
        assert ch['totalQuestions'] == 150, f"Pathology chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"
    for ch in pharmacology_chapters:
        assert ch['totalQuestions'] == 150, f"Pharmacology chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"
    for ch in biochemistry_chapters:
        assert ch['totalQuestions'] == 150, f"Biochemistry chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"

    print(f"\n[3/5] Total Questions Count: {len(questions)} (Expected: 6,900)")
    assert len(questions) == 6900, f"Expected 6,900 questions, found {len(questions)}"

    print("\n[4/5] Question Level Data Integrity Audit...")
    errors = 0
    seen_ids = set()
    counts_by_discipline = {"Pathology": 0, "Pharmacology": 0, "Biochemistry": 0}
    counts_by_chapter = {}

    for idx, q in enumerate(questions):
        qid = q.get('id')
        if qid in seen_ids or qid != idx + 1:
            print(f"Error: Invalid or non-sequential ID {qid} at index {idx}")
            errors += 1
        seen_ids.add(qid)

        disc = q.get('discipline')
        if disc not in counts_by_discipline:
            print(f"Error: Unknown discipline '{disc}' in question #{qid}")
            errors += 1
        else:
            counts_by_discipline[disc] += 1

        chap = q.get('chapter')
        counts_by_chapter[chap] = counts_by_chapter.get(chap, 0) + 1

        # Check fields
        if not q.get('stem') or len(q['stem'].strip()) < 10:
            print(f"Error: Empty or too short stem in question #{qid}")
            errors += 1
        if not q.get('leadQuestion'):
            print(f"Error: Missing lead question in question #{qid}")
            errors += 1
        opts = q.get('options', [])
        if len(opts) != 5 or any(not o.strip() for o in opts):
            print(f"Error: Invalid options in question #{qid}: {opts}")
            errors += 1
        if q.get('correct') not in ['A', 'B', 'C', 'D', 'E']:
            print(f"Error: Invalid correct answer '{q.get('correct')}' in question #{qid}")
            errors += 1
        if not q.get('explanation') or len(q['explanation'].strip()) < 20:
            print(f"Error: Missing or too short explanation in question #{qid}")
            errors += 1

    print(f"\n[5/5] Distribution by Discipline:")
    print(f"  - Pathology: {counts_by_discipline['Pathology']} questions (Expected: 2,100)")
    print(f"  - Pharmacology: {counts_by_discipline['Pharmacology']} questions (Expected: 1,350)")
    print(f"  - Biochemistry: {counts_by_discipline['Biochemistry']} questions (Expected: 3,450)")
    assert counts_by_discipline['Pathology'] == 2100
    assert counts_by_discipline['Pharmacology'] == 1350
    assert counts_by_discipline['Biochemistry'] == 3450

    print(f"\nDistribution across all 46 Chapters (14 Path + 9 Pharm + 23 Bio):")
    for chap, count in counts_by_chapter.items():
        assert count == 150, f"Chapter {chap} has {count} questions (expected 150)"
        print(f"  - {chap}: {count} Qs [OK]")

    if errors == 0:
        print("\n========================================================")
        print("  SUCCESS: 100% Data Integrity Check PASSED! 0 Errors.")
        print("  All 6,900 questions across 46 chapters are verified!")
        print("========================================================")
    else:
        print(f"\nFAILURE: Encountered {errors} data integrity errors.")
        sys.exit(1)

if __name__ == '__main__':
    verify_database()
