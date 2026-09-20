# -*- coding: utf-8 -*-
"""
Integrate Normal Labs Modal, Dual-Tab Engine, Search and Filter into index.html:
1. Links labs_data.js?v=1.0 in <head>
2. Sets id="btn-open-labs" on header button
3. Adds #labs-modal markup
4. Injects JavaScript interactive controller in the bottom script
"""

import re, os

def integrate():
    index_path = 'index.html'
    with open(index_path, 'r', encoding='utf-8') as f:
        html = f.read()

    # 1. Add labs_data.js script to <head>
    if 'labs_data.js' not in html:
        target = '<script src="questions_data.js?v=2100_v2"></script>'
        replacement = '<script src="questions_data.js?v=2100_v2"></script>\n<script src="labs_data.js?v=1.0"></script>'
        if target in html:
            html = html.replace(target, replacement, 1)
            print("1. Added labs_data.js to head.")
        else:
            print("Warning: questions_data.js script tag not found!")

    # 2. Wire id="btn-open-labs" on Normal Labs button in header
    old_btn = '<button class="flex items-center gap-1.5 px-3 py-2 rounded-2xl neu-btn text-[12px] font-bold text-[#444038] hover:text-primary transition-all" title="Clinical Reference Values">'
    new_btn = '<button id="btn-open-labs" class="flex items-center gap-1.5 px-3 py-2 rounded-2xl neu-btn text-[12px] font-bold text-[#444038] hover:text-primary transition-all" title="Clinical Reference Values & Diagnostic Criteria">'
    if old_btn in html:
        html = html.replace(old_btn, new_btn, 1)
        print("2. Added id='btn-open-labs' to header button.")
    else:
        print("Note: Header button already updated or different.")

    # 3. Add #labs-modal HTML markup
    labs_modal_markup = '''
<!-- Clinical Reference Values & Disease Criteria Modal (Normal Labs) -->
<div id="labs-modal" class="hidden fixed inset-0 z-50 bg-black/60 backdrop-blur-md flex items-center justify-center p-2 sm:p-4 lg:p-6 overflow-hidden">
  <div class="relative w-full max-w-6xl h-[94vh] rounded-3xl neu-extruded border border-white/80 shadow-2xl flex flex-col overflow-hidden bg-[#eae6de]">
    <!-- Modal Header -->
    <div class="px-5 py-3.5 border-b border-[#ded7ca] flex items-center justify-between bg-[#e4ded4]/90 shrink-0 gap-3">
      <div class="flex items-center gap-3">
        <div class="w-10 h-10 rounded-2xl neu-extruded-xs flex items-center justify-center text-primary border border-white/80 shrink-0">
          <span class="material-symbols-outlined text-[22px]">science</span>
        </div>
        <div>
          <h2 class="font-display font-extrabold text-[17px] text-[#181d24] leading-tight">Normal Labs &amp; Diagnostic Reference Manual</h2>
          <p class="text-[11px] text-[#6b665c]">Wilson's Clinical Tests &amp; Evidence-Based Disease Criteria • 359 Tests &amp; 68 Diseases</p>
        </div>
      </div>
      <div class="flex items-center gap-2">
        <span class="hidden sm:inline-block font-mono text-[10px] px-2 py-0.5 rounded-md neu-groove-sm text-[#756f64]">ESC to close</span>
        <button type="button" id="btn-close-labs" class="w-9 h-9 rounded-2xl neu-btn flex items-center justify-center text-[#555047] hover:text-accentDanger transition-all" title="Close Modal (Esc)">
          <span class="material-symbols-outlined text-[18px]">close</span>
        </button>
      </div>
    </div>

    <!-- Top Navigation Toolbar: Primary Mode Tabs & Integrated Search Bar -->
    <div class="px-5 py-3 bg-[#e8e3da]/80 border-b border-[#dfd9cc] flex flex-wrap items-center justify-between gap-3 shrink-0">
      <!-- Dual Main Tabs -->
      <div class="p-1 rounded-2xl neu-groove-sm flex items-center gap-1 border border-white/40">
        <button type="button" id="tab-btn-lab-tests" class="px-4 py-1.5 rounded-xl neu-extruded-xs text-[11.5px] font-bold text-primary neu-pill-active flex items-center gap-1.5 transition-all">
          <span class="material-symbols-outlined text-[16px]">biotechnology</span>
          <span>Laboratory Tests (359)</span>
        </button>
        <button type="button" id="tab-btn-disease-criteria" class="px-4 py-1.5 rounded-xl text-[11.5px] font-semibold text-[#656054] hover:text-[#181d24] flex items-center gap-1.5 transition-all">
          <span class="material-symbols-outlined text-[16px]">local_hospital</span>
          <span>Disease Criteria (68)</span>
        </button>
      </div>

      <!-- Prominent Search Bar with Clear Button & Result Count -->
      <div class="flex items-center gap-2.5 flex-1 max-w-xl min-w-[280px]">
        <div class="flex items-center gap-2 px-3.5 py-1.5 rounded-2xl neu-groove-sm w-full border border-white/40 relative">
          <span class="material-symbols-outlined text-[#7f7a70] text-[18px]">search</span>
          <input id="labs-search-input" type="text" class="bg-transparent border-0 p-0 text-[12.5px] text-[#242930] placeholder-[#8e887c] focus:ring-0 w-full font-medium outline-none" placeholder="Search tests, reference ranges, increased/decreased causes..." autocomplete="off">
          <button type="button" id="labs-search-clear" class="hidden text-[#8e887c] hover:text-[#181d24] text-[14px]">
            <span class="material-symbols-outlined text-[16px]">close</span>
          </button>
        </div>
        <span id="labs-count-badge" class="font-mono text-[11px] px-2.5 py-1 rounded-xl neu-groove-sm text-primary font-bold shrink-0">359 Tests</span>
      </div>
    </div>

    <!-- Secondary Filters Ribbon (Category pills or System pills) -->
    <div id="labs-filters-bar" class="px-5 py-2 bg-[#eae6de] border-b border-[#ded7ca] flex items-center gap-2 overflow-x-auto shrink-0 scrollbar-none text-[11px]">
      <!-- Populated dynamically by JS -->
    </div>

    <!-- Alphabetical A-Z Quick Jump Ribbon (Only in Lab Tests mode) -->
    <div id="labs-az-ribbon" class="px-5 py-1.5 bg-[#e4ded4]/60 border-b border-white/60 flex items-center gap-1 overflow-x-auto shrink-0 text-[10px] font-mono font-bold text-[#6b665c]">
      <!-- Injected by JS -->
    </div>

    <!-- Main Scrollable Content Area -->
    <div id="labs-content-scroll" class="flex-1 p-5 overflow-y-auto space-y-4 overscroll-contain">
      <!-- Cards rendered by JS -->
    </div>
  </div>
</div>
'''

    if 'id="labs-modal"' not in html:
        # Insert before closing </main> or before <script>
        insert_marker = '<!-- Multi-Step Mastery Overview Modal -->'
        if insert_marker in html:
            html = html.replace(insert_marker, labs_modal_markup + '\n' + insert_marker, 1)
            print("3. Inserted #labs-modal markup.")
        else:
            print("Warning: Could not find insert marker for labs modal!")

    # 4. Add Dark mode styling rules for labs modal
    dark_css_addition = '''
    /* Dark Mode Overrides for Normal Labs Modal */
    html.dark #labs-modal .bg-\\[\\#eae6de\\], 
    html.dark #labs-modal .bg-\\[\\#e4ded4\\]\\/90, 
    html.dark #labs-modal .bg-\\[\\#e8e3da\\]\\/80, 
    html.dark #labs-modal .bg-\\[\\#e4ded4\\]\\/60 {
      background-color: #1a1e24 !important;
    }
    html.dark #labs-modal .border-\\[\\#ded7ca\\], 
    html.dark #labs-modal .border-\\[\\#dfd9cc\\] {
      border-color: rgba(255, 255, 255, 0.08) !important;
    }
    html.dark .lab-card-detail {
      background-color: #16191f !important;
      border-color: rgba(255, 255, 255, 0.06) !important;
    }
    html.dark .lab-normal-box {
      background-color: #14171d !important;
      border-color: rgba(255, 255, 255, 0.08) !important;
      color: #93c5fd !important;
    }
    html.dark .lab-inc-box {
      background-color: #172c23 !important;
      border-color: rgba(72, 187, 120, 0.2) !important;
    }
    html.dark .lab-dec-box {
      background-color: #3b1c1c !important;
      border-color: rgba(245, 101, 101, 0.2) !important;
    }
  </style>'''

    if '/* Dark Mode Overrides for Normal Labs Modal */' not in html:
        html = html.replace('</style>', dark_css_addition, 1)
        print("4. Added dark mode styles for labs modal.")

    # 5. Inject JavaScript controller into main script
    js_controller = r'''
      // 25. Normal Labs & Clinical Diagnostic Manual Engine
      const labsModal = document.getElementById('labs-modal');
      const btnOpenLabs = document.getElementById('btn-open-labs');
      const btnCloseLabs = document.getElementById('btn-close-labs');
      const tabBtnLabTests = document.getElementById('tab-btn-lab-tests');
      const tabBtnDiseaseCriteria = document.getElementById('tab-btn-disease-criteria');
      const labsSearchInput = document.getElementById('labs-search-input');
      const labsSearchClear = document.getElementById('labs-search-clear');
      const labsCountBadge = document.getElementById('labs-count-badge');
      const labsFiltersBar = document.getElementById('labs-filters-bar');
      const labsAzRibbon = document.getElementById('labs-az-ribbon');
      const labsContentScroll = document.getElementById('labs-content-scroll');

      let currentLabsTab = 'tests'; // 'tests' or 'diseases'
      let labsSearchQuery = '';
      let activeLabCategory = 'all';
      let activeDiseaseSystem = 0; // 0 for all, 1-11 for specific system
      let expandedTestCards = {}; // testId -> boolean

      const allLabTests = window.USMLE_LAB_TESTS || [];
      const allDiseaseSystems = window.USMLE_DISEASE_CRITERIA || [];

      // Category list for tests
      const LAB_CATEGORIES = [
        { id: 'all', label: 'All Tests' },
        { id: 'Blood Chemistry & Metabolism', label: 'Blood Chemistry' },
        { id: 'Hematology & Coagulation', label: 'Hematology & Coagulation' },
        { id: 'Endocrine & Hormones', label: 'Endocrine & Hormones' },
        { id: 'Immunology & Serology', label: 'Immunology & Serology' },
        { id: 'Urinalysis & Renal Clearance', label: 'Urinalysis' },
        { id: 'Body Fluids & CSF', label: 'Body Fluids & CSF' },
        { id: 'Microbiology & Cultures', label: 'Microbiology' },
        { id: 'Imaging & Procedures', label: 'Imaging & Procedures' }
      ];

      function toggleLabsModal(show) {
        if (!labsModal) return;
        const isHidden = labsModal.classList.contains('hidden');
        const shouldShow = show !== undefined ? show : isHidden;
        labsModal.classList.toggle('hidden', !shouldShow);
        if (shouldShow) {
          renderLabsModal();
          setTimeout(() => { if (labsSearchInput) labsSearchInput.focus(); }, 100);
        }
      }

      if (btnOpenLabs) btnOpenLabs.addEventListener('click', () => toggleLabsModal(true));
      if (btnCloseLabs) btnCloseLabs.addEventListener('click', () => toggleLabsModal(false));

      // Close modal on Escape
      window.addEventListener('keydown', (e) => {
        if (e.key === 'Escape' && labsModal && !labsModal.classList.contains('hidden')) {
          toggleLabsModal(false);
        }
      });

      // Tab switching
      if (tabBtnLabTests) {
        tabBtnLabTests.addEventListener('click', () => {
          if (currentLabsTab !== 'tests') {
            currentLabsTab = 'tests';
            tabBtnLabTests.className = "px-4 py-1.5 rounded-xl neu-extruded-xs text-[11.5px] font-bold text-primary neu-pill-active flex items-center gap-1.5 transition-all";
            tabBtnDiseaseCriteria.className = "px-4 py-1.5 rounded-xl text-[11.5px] font-semibold text-[#656054] hover:text-[#181d24] flex items-center gap-1.5 transition-all";
            if (labsSearchInput) {
              labsSearchInput.placeholder = "Search 359 tests by name, alias (e.g. ALT, Troponin, KUB), reference range...";
            }
            renderLabsModal();
          }
        });
      }

      if (tabBtnDiseaseCriteria) {
        tabBtnDiseaseCriteria.addEventListener('click', () => {
          if (currentLabsTab !== 'diseases') {
            currentLabsTab = 'diseases';
            tabBtnDiseaseCriteria.className = "px-4 py-1.5 rounded-xl neu-extruded-xs text-[11.5px] font-bold text-primary neu-pill-active flex items-center gap-1.5 transition-all";
            tabBtnLabTests.className = "px-4 py-1.5 rounded-xl text-[11.5px] font-semibold text-[#656054] hover:text-[#181d24] flex items-center gap-1.5 transition-all";
            if (labsSearchInput) {
              labsSearchInput.placeholder = "Search 68 diseases, diagnostic guidelines (e.g. AMI, DVT, Wells, ADA, ISTH, CKD)...";
            }
            renderLabsModal();
          }
        });
      }

      // Search input listener
      if (labsSearchInput) {
        labsSearchInput.addEventListener('input', (e) => {
          labsSearchQuery = e.target.value.trim().toLowerCase();
          if (labsSearchClear) {
            labsSearchClear.classList.toggle('hidden', labsSearchQuery.length === 0);
          }
          renderLabsContent();
        });
      }

      if (labsSearchClear) {
        labsSearchClear.addEventListener('click', () => {
          labsSearchQuery = '';
          if (labsSearchInput) {
            labsSearchInput.value = '';
            labsSearchInput.focus();
          }
          labsSearchClear.classList.add('hidden');
          renderLabsContent();
        });
      }

      function escapeHtml(text) {
        if (!text) return '';
        return text.replace(/&/g, "&amp;").replace(/</g, "&lt;").replace(/>/g, "&gt;");
      }

      function renderLabsModal() {
        renderLabsFilters();
        renderLabsAzRibbon();
        renderLabsContent();
      }

      function renderLabsFilters() {
        if (!labsFiltersBar) return;
        labsFiltersBar.innerHTML = '';

        if (currentLabsTab === 'tests') {
          LAB_CATEGORIES.forEach(cat => {
            const isCatActive = activeLabCategory === cat.id;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `px-3 py-1 rounded-xl whitespace-nowrap font-semibold transition-all ${
              isCatActive 
                ? 'neu-pill-active text-primary font-bold' 
                : 'neu-btn text-[#555047] hover:text-primary'
            }`;
            btn.textContent = cat.label;
            btn.addEventListener('click', () => {
              activeLabCategory = cat.id;
              renderLabsFilters();
              renderLabsContent();
            });
            labsFiltersBar.appendChild(btn);
          });
        } else {
          // Systems filters for diseases
          const allBtn = document.createElement('button');
          allBtn.type = 'button';
          allBtn.className = `px-3 py-1 rounded-xl whitespace-nowrap font-semibold transition-all ${
            activeDiseaseSystem === 0 
              ? 'neu-pill-active text-primary font-bold' 
              : 'neu-btn text-[#555047] hover:text-primary'
          }`;
          allBtn.textContent = 'All Systems (68)';
          allBtn.addEventListener('click', () => {
            activeDiseaseSystem = 0;
            renderLabsFilters();
            renderLabsContent();
          });
          labsFiltersBar.appendChild(allBtn);

          allDiseaseSystems.forEach(sys => {
            const isSysActive = activeDiseaseSystem === sys.systemId;
            const btn = document.createElement('button');
            btn.type = 'button';
            btn.className = `px-3 py-1 rounded-xl whitespace-nowrap font-semibold transition-all ${
              isSysActive 
                ? 'neu-pill-active text-primary font-bold' 
                : 'neu-btn text-[#555047] hover:text-primary'
            }`;
            btn.textContent = `${sys.systemId}. ${sys.systemEn} (${sys.diseases.length})`;
            btn.addEventListener('click', () => {
              activeDiseaseSystem = sys.systemId;
              renderLabsFilters();
              renderLabsContent();
            });
            labsFiltersBar.appendChild(btn);
          });
        }
      }

      function renderLabsAzRibbon() {
        if (!labsAzRibbon) return;
        if (currentLabsTab !== 'tests') {
          labsAzRibbon.classList.add('hidden');
          return;
        }
        labsAzRibbon.classList.remove('hidden');
        labsAzRibbon.innerHTML = '<span class="text-[#8e887c] uppercase tracking-wider text-[9px] mr-1 shrink-0">Jump A-Z:</span>';

        const letters = "ABCDEFGHIJKLMNOPQRSTUVWXYZ".split('');
        letters.forEach(letter => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.className = "w-6 h-6 rounded-lg neu-btn flex items-center justify-center hover:text-primary hover:font-extrabold transition-all shrink-0";
          btn.textContent = letter;
          btn.addEventListener('click', () => {
            activeLabCategory = 'all';
            labsSearchQuery = '';
            if (labsSearchInput) labsSearchInput.value = '';
            if (labsSearchClear) labsSearchClear.classList.add('hidden');
            renderLabsFilters();
            renderLabsContent();

            // Scroll to the first test starting with this letter
            setTimeout(() => {
              const target = document.querySelector(`.lab-test-card[data-letter="${letter}"]`);
              if (target) {
                target.scrollIntoView({ behavior: 'smooth', block: 'start' });
              }
            }, 50);
          });
          labsAzRibbon.appendChild(btn);
        });
      }

      function renderLabsContent() {
        if (!labsContentScroll) return;
        labsContentScroll.innerHTML = '';

        if (currentLabsTab === 'tests') {
          renderTestList();
        } else {
          renderDiseaseList();
        }
      }

      function renderTestList() {
        // Filter tests
        const filtered = allLabTests.filter(t => {
          const matchCat = (activeLabCategory === 'all' || t.category === activeLabCategory);
          if (!matchCat) return false;
          if (!labsSearchQuery) return true;

          const inTitle = t.title.toLowerCase().includes(labsSearchQuery);
          const inAliases = t.aliases && t.aliases.toLowerCase().includes(labsSearchQuery);
          const inNormal = t.normalValues && t.normalValues.toLowerCase().includes(labsSearchQuery);
          const inDesc = t.description && t.description.toLowerCase().includes(labsSearchQuery);
          const inInc = t.increased && t.increased.some(x => x.toLowerCase().includes(labsSearchQuery));
          const inDec = t.decreased && t.decreased.some(x => x.toLowerCase().includes(labsSearchQuery));
          const inAb = t.abnormalFindings && t.abnormalFindings.some(x => x.toLowerCase().includes(labsSearchQuery));

          return inTitle || inAliases || inNormal || inDesc || inInc || inDec || inAb;
        });

        if (labsCountBadge) {
          labsCountBadge.textContent = `${filtered.length} of ${allLabTests.length} Tests`;
        }

        if (filtered.length === 0) {
          labsContentScroll.innerHTML = `
            <div class="p-10 rounded-3xl neu-groove text-center flex flex-col items-center gap-3">
              <span class="material-symbols-outlined text-[36px] text-[#9c9689]">science</span>
              <p class="font-medium text-[13.5px] text-[#6b665c]">No laboratory tests match "${escapeHtml(labsSearchQuery)}".</p>
              <button type="button" id="btn-labs-reset-search" class="text-primary font-bold hover:underline text-[12px]">Reset Search &amp; Show All</button>
            </div>
          `;
          const rBtn = document.getElementById('btn-labs-reset-search');
          if (rBtn) {
            rBtn.addEventListener('click', () => {
              labsSearchQuery = '';
              activeLabCategory = 'all';
              if (labsSearchInput) labsSearchInput.value = '';
              if (labsSearchClear) labsSearchClear.classList.add('hidden');
              renderLabsModal();
            });
          }
          return;
        }

        filtered.forEach(t => {
          const isExpanded = !!expandedTestCards[t.id];
          const firstLetter = t.title.trim()[0].toUpperCase();
          const card = document.createElement('div');
          card.id = `lab-test-${t.id}`;
          card.setAttribute('data-letter', firstLetter);
          card.className = "lab-test-card p-4 sm:p-5 rounded-3xl neu-extruded border border-white/80 shadow-sm flex flex-col gap-3.5 transition-all";

          // Formatted Normal Range
          const normalFormatted = escapeHtml(t.normalValues).replace(/\n/g, '<br>');

          // Increased / Decreased lists
          let incHtml = '';
          if (t.increased && t.increased.length > 0) {
            incHtml = `
              <div class="lab-inc-box p-3 rounded-2xl neu-groove-sm bg-[#dfeae3]/60 border border-emerald-500/20 flex flex-col gap-1.5 flex-1">
                <div class="flex items-center gap-1.5 text-accentSuccess font-bold text-[11.5px]">
                  <span class="material-symbols-outlined text-[16px]">arrow_upward</span>
                  <span>Increased / Positive (升高意义)</span>
                </div>
                <ul class="text-[11.5px] text-[#242930] space-y-0.5 list-disc list-inside leading-relaxed">
                  ${t.increased.map(x => `<li>${escapeHtml(x)}</li>`).join('')}
                </ul>
              </div>
            `;
          }

          let decHtml = '';
          if (t.decreased && t.decreased.length > 0) {
            decHtml = `
              <div class="lab-dec-box p-3 rounded-2xl neu-groove-sm bg-[#f4e2e2]/60 border border-rose-400/20 flex flex-col gap-1.5 flex-1">
                <div class="flex items-center gap-1.5 text-accentDanger font-bold text-[11.5px]">
                  <span class="material-symbols-outlined text-[16px]">arrow_downward</span>
                  <span>Decreased / Negative (降低意义)</span>
                </div>
                <ul class="text-[11.5px] text-[#242930] space-y-0.5 list-disc list-inside leading-relaxed">
                  ${t.decreased.map(x => `<li>${escapeHtml(x)}</li>`).join('')}
                </ul>
              </div>
            `;
          }

          let abFindingsHtml = '';
          if (t.abnormalFindings && t.abnormalFindings.length > 0) {
            abFindingsHtml = `
              <div class="p-3 rounded-2xl neu-groove-sm bg-[#ede4d5]/50 border border-amber-500/20 flex flex-col gap-1.5 flex-1">
                <div class="flex items-center gap-1.5 text-amber-800 font-bold text-[11.5px]">
                  <span class="material-symbols-outlined text-[16px]">troubleshoot</span>
                  <span>Abnormal Findings &amp; Conditions</span>
                </div>
                <ul class="text-[11.5px] text-[#242930] space-y-0.5 list-disc list-inside leading-relaxed">
                  ${t.abnormalFindings.map(x => `<li>${escapeHtml(x)}</li>`).join('')}
                </ul>
              </div>
            `;
          }

          // Clinical alerts & pearls
          let alertsHtml = '';
          if (t.clinicalAlerts) {
            alertsHtml = `
              <div class="p-3 rounded-2xl bg-amber-500/10 border border-amber-500/30 text-[11.5px] text-amber-900 leading-relaxed flex items-start gap-2">
                <span class="material-symbols-outlined text-amber-700 text-[18px] shrink-0 mt-0.5">warning</span>
                <div>
                  <strong class="font-bold">Clinical Alerts &amp; Practice Pearls:</strong>
                  <div class="whitespace-pre-line mt-0.5">${escapeHtml(t.clinicalAlerts)}</div>
                </div>
              </div>
            `;
          }

          // Contributing factors
          let factorsHtml = '';
          if (t.contributingFactors) {
            factorsHtml = `
              <div class="text-[11.5px] text-[#4a453d] leading-relaxed">
                <strong class="text-[#181d24] font-bold">Contributing Factors &amp; Interferences:</strong>
                <div class="whitespace-pre-line mt-0.5">${escapeHtml(t.contributingFactors)}</div>
              </div>
            `;
          }

          // Evidence for Practice
          let evidenceHtml = '';
          if (t.evidence) {
            evidenceHtml = `
              <div class="p-3 rounded-2xl neu-groove-sm bg-[#e8e3da] text-[11px] text-[#555047] leading-relaxed">
                <strong class="text-primary font-bold flex items-center gap-1 mb-1">
                  <span class="material-symbols-outlined text-[15px]">verified</span>
                  <span>The Evidence for Practice:</span>
                </strong>
                <div class="whitespace-pre-line">${escapeHtml(t.evidence)}</div>
              </div>
            `;
          }

          card.innerHTML = `
            <!-- Card Header -->
            <div class="flex items-start justify-between gap-3 flex-wrap">
              <div class="flex items-start gap-2.5">
                <span class="px-2 py-0.5 rounded-lg neu-groove-sm font-mono font-bold text-[11px] text-primary shrink-0 mt-0.5">#${t.id < 10 ? '00' + t.id : (t.id < 100 ? '0' + t.id : t.id)}</span>
                <div>
                  <h3 class="font-display font-bold text-[15px] text-[#181d24] leading-snug">${escapeHtml(t.title)}</h3>
                  ${t.aliases ? `<span class="text-[11px] text-[#6d675b] font-medium block mt-0.5">Aliases: <code class="font-mono text-[10.5px] text-[#242930]">${escapeHtml(t.aliases)}</code></span>` : ''}
                </div>
              </div>
              <div class="flex items-center gap-2 shrink-0">
                <span class="px-2.5 py-0.5 rounded-full neu-extruded-xs font-mono text-[10px] text-[#656054]">${escapeHtml(t.category)}</span>
                <span class="px-2 py-0.5 rounded-full neu-groove-sm font-mono text-[9.5px] text-[#787266]">${escapeHtml(t.pages)}</span>
              </div>
            </div>

            <!-- Normal Reference Values Box (Prominent Inset) -->
            <div class="lab-normal-box p-3 rounded-2xl neu-groove-sm bg-[#e8e3da] border border-white/60 flex flex-col gap-1">
              <span class="text-[10px] font-mono font-bold uppercase tracking-wider text-primary flex items-center gap-1">
                <span class="material-symbols-outlined text-[14px]">fact_check</span>
                <span>Normal Reference Range (正常参考范围)</span>
              </span>
              <div class="font-mono text-[12px] font-semibold text-[#181d24] leading-relaxed">
                ${normalFormatted || '<span class="text-[#787266] italic">See clinical diagnostic evaluation</span>'}
              </div>
            </div>

            <!-- Increased / Decreased Significance Grid -->
            ${(incHtml || decHtml || abFindingsHtml) ? `
              <div class="grid grid-cols-1 md:grid-cols-2 gap-3 pt-1">
                ${incHtml}
                ${decHtml}
                ${abFindingsHtml}
              </div>
            ` : ''}

            <!-- Expandable Accordion Toggle -->
            <div class="pt-1 flex items-center justify-between border-t border-white/50">
              <button type="button" class="btn-toggle-test-detail text-[11px] font-bold text-primary hover:text-primaryDark flex items-center gap-1 transition-all" data-id="${t.id}">
                <span class="material-symbols-outlined text-[16px]">${isExpanded ? 'expand_less' : 'expand_more'}</span>
                <span>${isExpanded ? 'Hide Clinical Details &amp; Alerts' : 'View Test Description &amp; Clinical Pearls'}</span>
              </button>
            </div>

            <!-- Expandable Content -->
            <div class="lab-card-detail ${isExpanded ? 'flex' : 'hidden'} flex-col gap-3 p-3.5 rounded-2xl neu-groove-sm bg-[#e8e3da]/70 border border-white/40 mt-1">
              ${t.description ? `
                <div class="text-[12px] text-[#242930] leading-relaxed">
                  <strong class="text-[#181d24] font-bold">Test Description &amp; Clinical Background:</strong>
                  <p class="mt-0.5">${escapeHtml(t.description)}</p>
                </div>
              ` : ''}
              ${factorsHtml}
              ${alertsHtml}
              ${evidenceHtml}
            </div>
          `;

          // Bind Accordion Click
          const toggleBtn = card.querySelector('.btn-toggle-test-detail');
          if (toggleBtn) {
            toggleBtn.addEventListener('click', () => {
              expandedTestCards[t.id] = !expandedTestCards[t.id];
              renderTestList();
            });
          }

          labsContentScroll.appendChild(card);
        });
      }

      function renderDiseaseList() {
        let matchedDiseases = [];

        allDiseaseSystems.forEach(sys => {
          if (activeDiseaseSystem === 0 || activeDiseaseSystem === sys.systemId) {
            sys.diseases.forEach(d => {
              if (!labsSearchQuery) {
                matchedDiseases.append ? matchedDiseases.append({ sys, d }) : matchedDiseases.push({ sys, d });
                return;
              }
              const inTitle = d.title.toLowerCase().includes(labsSearchQuery);
              const inGuide = d.guideline && d.guideline.toLowerCase().includes(labsSearchQuery);
              const inContent = d.content && d.content.toLowerCase().includes(labsSearchQuery);
              const inRel = d.relatedTests && d.relatedTests.toLowerCase().includes(labsSearchQuery);
              if (inTitle || inGuide || inContent || inRel) {
                matchedDiseases.push({ sys, d });
              }
            });
          }
        });

        if (labsCountBadge) {
          labsCountBadge.textContent = `${matchedDiseases.length} of 68 Diseases`;
        }

        if (matchedDiseases.length === 0) {
          labsContentScroll.innerHTML = `
            <div class="p-10 rounded-3xl neu-groove text-center flex flex-col items-center gap-3">
              <span class="material-symbols-outlined text-[36px] text-[#9c9689]">local_hospital</span>
              <p class="font-medium text-[13.5px] text-[#6b665c]">No disease diagnostic criteria match "${escapeHtml(labsSearchQuery)}".</p>
              <button type="button" id="btn-disease-reset-search" class="text-primary font-bold hover:underline text-[12px]">Reset Search &amp; Show All</button>
            </div>
          `;
          const rBtn = document.getElementById('btn-disease-reset-search');
          if (rBtn) {
            rBtn.addEventListener('click', () => {
              labsSearchQuery = '';
              activeDiseaseSystem = 0;
              if (labsSearchInput) labsSearchInput.value = '';
              if (labsSearchClear) labsSearchClear.classList.add('hidden');
              renderLabsModal();
            });
          }
          return;
        }

        let currentSystemId = null;

        matchedDiseases.forEach(({ sys, d }) => {
          // Add system banner if system changed
          if (sys.systemId !== currentSystemId) {
            currentSystemId = sys.systemId;
            const sysBanner = document.createElement('div');
            sysBanner.className = "px-4 py-2.5 rounded-2xl neu-groove-sm bg-[#e2ddd4] flex items-center justify-between mt-3 first:mt-0";
            sysBanner.innerHTML = `
              <div class="flex items-center gap-2 font-display font-bold text-[13px] text-[#181d24]">
                <span class="w-6 h-6 rounded-lg neu-extruded-xs flex items-center justify-center font-mono text-[11px] text-primary font-bold">${sys.systemId}</span>
                <span>${escapeHtml(sys.systemEn)}</span>
                <span class="text-[11.5px] text-[#6b665c] font-normal">(${escapeHtml(sys.systemZh)})</span>
              </div>
              <span class="font-mono text-[10px] px-2 py-0.5 rounded-full neu-extruded-xs text-primary font-bold">${sys.diseases.length} Criteria</span>
            `;
            labsContentScroll.appendChild(sysBanner);
          }

          const card = document.createElement('div');
          card.className = "p-5 rounded-3xl neu-extruded border border-white/80 shadow-sm flex flex-col gap-3 transition-all";

          // Format content markdown into html
          let contentHtml = escapeHtml(d.content)
            .replace(/\*\*(.*?)\*\*/g, '<strong>$1</strong>')
            .replace(/`([^`]+)`/g, '<code class="px-1.5 py-0.2 rounded bg-white/60 font-mono text-[11px] text-primary font-bold">$1</code>')
            .replace(/\n- /g, '<br>• ')
            .replace(/\n  - /g, '<br>&nbsp;&nbsp;▪ ')
            .replace(/\n    \d+\. /g, '<br>&nbsp;&nbsp;&nbsp;&nbsp; ')
            .replace(/\n/g, '<br>');

          // Related tests tags
          let relatedTagsHtml = '';
          if (d.relatedTests) {
            const items = d.relatedTests.split(',').map(s => s.trim()).filter(Boolean);
            relatedTagsHtml = `
              <div class="flex items-center gap-1.5 flex-wrap pt-2 border-t border-white/50 text-[11px]">
                <span class="text-[#756f64] font-semibold text-[10.5px]">Related Lab Tests:</span>
                ${items.map(it => `
                  <button type="button" class="btn-jump-lab-test px-2 py-0.5 rounded-lg neu-btn text-[10.5px] font-bold text-primary hover:text-primaryDark transition-all" data-keyword="${escapeHtml(it)}">
                    ${escapeHtml(it)}
                  </button>
                `).join('')}
              </div>
            `;
          }

          card.innerHTML = `
            <div class="flex items-start justify-between gap-3 flex-wrap">
              <div class="flex items-start gap-2.5">
                <span class="px-2 py-0.5 rounded-lg neu-groove-sm font-mono font-bold text-[11px] text-primary shrink-0 mt-0.5">${d.code}</span>
                <div>
                  <h3 class="font-display font-bold text-[15px] text-[#181d24] leading-snug">${escapeHtml(d.title)}</h3>
                  ${d.guideline ? `<span class="inline-block text-[10.5px] font-mono font-semibold px-2 py-0.5 rounded-md bg-emerald-100 text-emerald-800 mt-1">Guideline: ${escapeHtml(d.guideline)}</span>` : ''}
                </div>
              </div>
            </div>

            <div class="p-3.5 rounded-2xl neu-groove-sm bg-[#e8e3da] text-[12px] text-[#242930] leading-relaxed">
              ${contentHtml}
            </div>

            ${relatedTagsHtml}
          `;

          // Handle related test jump button
          card.querySelectorAll('.btn-jump-lab-test').forEach(btn => {
            btn.addEventListener('click', () => {
              const kw = btn.getAttribute('data-keyword').replace(/\(P\.\d+\)/g, '').replace(/`/g, '').trim();
              currentLabsTab = 'tests';
              tabBtnLabTests.className = "px-4 py-1.5 rounded-xl neu-extruded-xs text-[11.5px] font-bold text-primary neu-pill-active flex items-center gap-1.5 transition-all";
              tabBtnDiseaseCriteria.className = "px-4 py-1.5 rounded-xl text-[11.5px] font-semibold text-[#656054] hover:text-[#181d24] flex items-center gap-1.5 transition-all";
              activeLabCategory = 'all';
              labsSearchQuery = kw.toLowerCase();
              if (labsSearchInput) {
                labsSearchInput.value = kw;
                labsSearchInput.placeholder = "Search 359 tests by name, alias, reference range...";
              }
              if (labsSearchClear) labsSearchClear.classList.remove('hidden');
              renderLabsModal();
            });
          });

          labsContentScroll.appendChild(card);
        });
      }
'''

    # Inject into the main script
    if '// 25. Normal Labs & Clinical Diagnostic Manual Engine' not in html:
        # Find where the script ends (before updateUI(); or before })();)
        boot_marker = 'initChapterDropdown();'
        if boot_marker in html:
            html = html.replace(boot_marker, js_controller + '\n      ' + boot_marker, 1)
            print("5. Injected JavaScript controller for Normal Labs.")
        else:
            print("Warning: Could not find boot marker in script!")

    with open(index_path, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f"Integration successfully completed! index.html is now {len(html)} chars.")

if __name__ == '__main__':
    integrate()
