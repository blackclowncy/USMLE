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

    manifest_path = os.path.join(current_dir, 'questions_data.js')
    path_path = os.path.join(current_dir, 'questions_data_pathology.js')
    pharm_path = os.path.join(current_dir, 'questions_data_pharmacology.js')
    bio_path = os.path.join(current_dir, 'questions_data_biochemistry.js')
    phys_path = os.path.join(current_dir, 'questions_data_physiology.js')
    anat_path = os.path.join(current_dir, 'questions_data_anatomy.js')

    for p in [manifest_path, path_path, pharm_path, bio_path, phys_path, anat_path]:
        if not os.path.exists(p):
            print(f"ERROR: {p} does not exist!")
            sys.exit(1)

    print("Reading questions database files...")
    with open(manifest_path, 'r', encoding='utf-8') as f:
        c_manifest = f.read()
    with open(path_path, 'r', encoding='utf-8') as f:
        c_path = f.read()
    with open(pharm_path, 'r', encoding='utf-8') as f:
        c_pharm = f.read()
    with open(bio_path, 'r', encoding='utf-8') as f:
        c_bio = f.read()
    with open(phys_path, 'r', encoding='utf-8') as f:
        c_phys = f.read()
    with open(anat_path, 'r', encoding='utf-8') as f:
        c_anat = f.read()

    def extract_json_after_prefix(text, prefix, suffix=";"):
        idx = text.find(prefix)
        assert idx != -1, f"Prefix '{prefix}' not found in file"
        rest = text[idx + len(prefix):].strip()
        if rest.endswith(suffix):
            rest = rest[:-len(suffix)].strip()
        return json.loads(rest)

    def extract_chapters(text, var_name):
        prefix = f"{var_name} = "
        idx = text.find(prefix)
        assert idx != -1, f"Var '{var_name}' not found"
        rest = text[idx + len(prefix):]
        # chapters array is followed by ;\n\nwindow.USMLE_QUESTIONS
        end_idx = rest.find(";\n")
        return json.loads(rest[:end_idx])

    disciplines = extract_json_after_prefix(c_manifest, "window.USMLE_DISCIPLINES = ", ";")
    pathology_chapters = extract_chapters(c_path, "window.USMLE_PATHOLOGY_CHAPTERS")
    pharmacology_chapters = extract_chapters(c_pharm, "window.USMLE_PHARMACOLOGY_CHAPTERS")
    biochemistry_chapters = extract_chapters(c_bio, "window.USMLE_BIOCHEMISTRY_CHAPTERS")
    physiology_chapters = extract_chapters(c_phys, "window.USMLE_PHYSIOLOGY_CHAPTERS")
    anatomy_chapters = extract_chapters(c_anat, "window.USMLE_ANATOMY_CHAPTERS")

    concat_prefix = "window.USMLE_QUESTIONS = (window.USMLE_QUESTIONS || []).concat("
    questions = (
        extract_json_after_prefix(c_path, concat_prefix, ");") +
        extract_json_after_prefix(c_pharm, concat_prefix, ");") +
        extract_json_after_prefix(c_bio, concat_prefix, ");") +
        extract_json_after_prefix(c_phys, concat_prefix, ");") +
        extract_json_after_prefix(c_anat, concat_prefix, ");")
    )

    print(f"\n[1/5] Disciplines Verified: {len(disciplines)} disciplines registered.")
    for d in disciplines:
        print(f"  - {d['name']}: {d['count']} questions ({d['status']})")

    assert len(pathology_chapters) == 14, f"Expected 14 Pathology chapters, got {len(pathology_chapters)}"
    assert len(pharmacology_chapters) == 9, f"Expected 9 Pharmacology chapters, got {len(pharmacology_chapters)}"
    assert len(biochemistry_chapters) == 23, f"Expected 23 Biochemistry chapters, got {len(biochemistry_chapters)}"
    assert len(physiology_chapters) == 34, f"Expected 34 Physiology chapters, got {len(physiology_chapters)}"
    assert len(anatomy_chapters) == 20, f"Expected 20 Anatomy chapters, got {len(anatomy_chapters)}"

    print(f"\n[2/5] Chapter Definitions Verified:")
    print(f"  - Pathology: {len(pathology_chapters)} chapters (150 Qs each = 2,100 Qs)")
    print(f"  - Pharmacology: {len(pharmacology_chapters)} chapters (150 Qs each = 1,350 Qs)")
    print(f"  - Biochemistry: {len(biochemistry_chapters)} chapters (150 Qs each = 3,450 Qs)")
    print(f"  - Physiology: {len(physiology_chapters)} chapters (150 Qs each = 5,100 Qs)")
    print(f"  - Anatomy: {len(anatomy_chapters)} chapters (150 Qs each = 3,000 Qs)")

    for ch in pathology_chapters:
        assert ch['totalQuestions'] == 150, f"Pathology chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"
    for ch in pharmacology_chapters:
        assert ch['totalQuestions'] == 150, f"Pharmacology chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"
    for ch in biochemistry_chapters:
        assert ch['totalQuestions'] == 150, f"Biochemistry chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"
    for ch in physiology_chapters:
        assert ch['totalQuestions'] == 150, f"Physiology chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"
    for ch in anatomy_chapters:
        assert ch['totalQuestions'] == 150, f"Anatomy chapter {ch['id']} has {ch['totalQuestions']} Qs (expected 150)"

    print(f"\n[3/5] Total Questions Count: {len(questions)} (Expected: 15,000)")
    assert len(questions) == 15000, f"Expected 15,000 questions, found {len(questions)}"

    print("\n[4/5] Question Level Data Integrity Audit...")
    errors = 0
    seen_ids = set()
    counts_by_discipline = {"Pathology": 0, "Pharmacology": 0, "Biochemistry": 0, "Physiology": 0, "Anatomy": 0}
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
    print(f"  - Physiology: {counts_by_discipline['Physiology']} questions (Expected: 5,100)")
    print(f"  - Anatomy: {counts_by_discipline['Anatomy']} questions (Expected: 3,000)")
    assert counts_by_discipline['Pathology'] == 2100
    assert counts_by_discipline['Pharmacology'] == 1350
    assert counts_by_discipline['Biochemistry'] == 3450
    assert counts_by_discipline['Physiology'] == 5100
    assert counts_by_discipline['Anatomy'] == 3000

    print(f"\nDistribution across all 100 Chapters (14 Path + 9 Pharm + 23 Bio + 34 Physio + 20 Anat):")
    for chap, count in counts_by_chapter.items():
        assert count == 150, f"Chapter {chap} has {count} questions (expected 150)"
        print(f"  - {chap}: {count} Qs [OK]")

    if errors == 0:
        print("\n========================================================")
        print("  SUCCESS: 100% Data Integrity Check PASSED! 0 Errors.")
        print("  All 15,000 questions across 100 chapters are verified!")
        print("========================================================")
    else:
        print(f"\nFAILURE: Encountered {errors} data integrity errors.")
        sys.exit(1)

if __name__ == '__main__':
    verify_database()
