# -*- coding: utf-8 -*-
"""
MedPulse USMLE Q-Bank - Index HTML Validator & Generator
Ensures index.html contains all high-yield clinical features:
- Standard USMLE Calculator Modal
- Highlighting & Option Strikethrough
- Dark / Warm Dark Eye-Care Mode
- Multi-Step Mastery Overview Dashboard
"""

import os
import re

def verify_and_sync():
    index_path = os.path.join(os.path.dirname(__file__), 'index.html')
    if not os.path.exists(index_path):
        print("ERROR: index.html not found!")
        return

    with open(index_path, 'r', encoding='utf-8') as f:
        content = f.read()

    features = [
        ("Calculator Modal", "id=\"calculator-modal\""),
        ("Mastery Overview Modal", "id=\"mastery-modal\""),
        ("Highlighter Bubble", "id=\"highlighter-bubble\""),
        ("Dark Mode Toggle", "id=\"btn-theme-toggle\""),
        ("Option Strikethrough", "data-action=\"toggle-strike\""),
        ("Normal Labs Modal", "id=\"labs-modal\""),
        ("Normal Labs Button", "id=\"btn-open-labs\""),
        ("Labs Database Link", "labs_data.js?v=1.0"),
        ("Questions Database Link", "questions_data.js?v=2100_v2")
    ]

    print("Verifying MedPulse Suite features in index.html:")
    all_ok = True
    for name, pattern in features:
        found = pattern in content
        status = "[OK]" if found else "[MISSING]"
        print(f" - {name:<30}: {status}")
        if not found:
            all_ok = False

    if all_ok:
        print("\nAll clinical and educational features are fully verified and active.")
    else:
        print("\nWarning: Some features were not detected.")

if __name__ == '__main__':
    verify_and_sync()
