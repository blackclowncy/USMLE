import re

def generate_html():
    with open('index.html.original', 'r', encoding='utf-8') as f:
        orig = f.read()

    # 1. Add questions_data.js to head
    head_insertion = '<script src="questions_data.js"></script>\n<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>'
    orig = orig.replace('<script src="https://cdn.tailwindcss.com?plugins=forms,container-queries"></script>', head_insertion, 1)

    # 2. Add id to search input
    orig = orig.replace('placeholder="Search stems..." type="text"', 'placeholder="Search stems & concepts..." type="text" id="stem-search-input"')

    # 3. Add id to breadcrumb
    orig = orig.replace('<span class="text-[#544f45] font-semibold">All Chapters</span>', '<span id="active-chapter-breadcrumb" class="text-[#544f45] font-semibold">Ch01_Cellular_Adaptations_and_Reversible_Injury</span>')

    # 4. Extract parts before questions-container and after questions-container
    # In original:
    # starts before: <div class="col-span-12 lg:col-span-8 space-y-9" id="questions-container">
    # ends after: </footer>\n</div>\n<!-- Clinical Questions Database & Neumorphic Interactions -->\n<script>
    
    split_start_token = '<div class="col-span-12 lg:col-span-8 space-y-9" id="questions-container">'
    split_end_token = '<!-- Clinical Questions Database & Neumorphic Interactions -->\n<script>'

    idx_start = orig.find(split_start_token)
    idx_end = orig.find(split_end_token)

    if idx_start == -1 or idx_end == -1:
        print("ERROR: Split tokens not found!")
        return

    part1 = orig[:idx_start]
    part2 = orig[idx_end + len(split_end_token):]

    # New Right Column HTML with Banner, Block filter tabs, and Questions container
    right_column_html = '''<div class="col-span-12 lg:col-span-8 space-y-6">
  <!-- Dynamic Chapter Banner & Block Filter Header -->
  <div id="chapter-header-banner" class="p-6 rounded-3xl neu-extruded border border-white/70 flex flex-col gap-4 transition-all">
    <div class="flex flex-wrap items-center justify-between gap-4 border-b border-[#dfd9cc] pb-4">
      <div class="flex items-center gap-3.5">
        <div class="w-12 h-12 rounded-2xl neu-extruded-xs flex items-center justify-center text-primary shrink-0 border border-white/60">
          <span class="material-symbols-outlined text-[24px]">menu_book</span>
        </div>
        <div>
          <div class="flex items-center gap-2.5 flex-wrap">
            <h2 class="font-display font-extrabold text-[17.5px] text-[#181d24] tracking-tight" id="banner-chapter-title">Ch01_Cellular_Adaptations_and_Reversible_Injury</h2>
            <span id="banner-chapter-badge" class="px-3 py-0.5 rounded-full neu-groove-sm text-[11px] font-mono font-bold text-accentSuccess bg-[#dfeae3]">Active (150 Qs)</span>
          </div>
          <p class="text-[12px] text-[#6b665c] mt-0.5" id="banner-chapter-desc">USMLE Step 1 Pathology Review & Question Bank (MedGemma 27B)</p>
        </div>
      </div>
      <!-- Block Filter Pills (All, Block 1, Block 2, Block 3) -->
      <div class="p-1 rounded-2xl neu-groove-sm flex items-center gap-1 border border-white/50" id="block-tabs-container">
        <!-- Injected by JS -->
      </div>
    </div>
    
    <!-- Chapter Mini Stats Bar -->
    <div class="flex flex-wrap items-center justify-between gap-3 text-[11.5px] text-[#6b665c]">
      <div class="flex items-center gap-4">
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-accentSuccess"></span>Correct: <strong class="text-accentSuccess font-mono" id="banner-stat-correct">0</strong></span>
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-accentDanger"></span>Incorrect: <strong class="text-accentDanger font-mono" id="banner-stat-incorrect">0</strong></span>
        <span class="flex items-center gap-1.5"><span class="w-2 h-2 rounded-full bg-[#9e988c]"></span>Unanswered: <strong class="text-[#181d24] font-mono" id="banner-stat-unanswered">0</strong></span>
        <span class="flex items-center gap-1.5 text-amber-800"><span class="material-symbols-outlined text-[14px] fill-current">bookmark</span>Marked: <strong class="font-mono font-bold" id="banner-stat-flagged">0</strong></span>
      </div>
      <div class="flex items-center gap-2">
        <button id="reset-chapter-answers-btn" class="text-[11px] font-semibold text-[#736e62] hover:text-accentDanger transition-colors px-2 py-1 rounded-lg hover:underline flex items-center gap-1" title="Clear answers for current chapter">
          <span class="material-symbols-outlined text-[14px]">restart_alt</span>
          <span>Reset Current Chapter</span>
        </button>
      </div>
    </div>
  </div>

  <!-- Questions Container (Populated dynamically) -->
  <div class="space-y-8" id="questions-container">
    <!-- Question Cards injected by JS -->
  </div>
</div>
</div>
</main>
<!-- Footer in Warm Neumorphic Style -->
<footer class="mt-16 py-8 border-t border-[#dfd9cc] bg-[#eae6de] text-center text-[12.5px] text-[#787266]">
<p class="font-medium">MedPulse Clinical Diagnostic Suite • High-Yield USMLE Step 1 Simulation • Tactile Warm-Bone Clay Neumorphic Architecture</p>
</footer>
</div>
<!-- Clinical Questions Database & Neumorphic Interactions -->
<script>
'''

    # New Comprehensive JavaScript Application
    new_script_js = '''
    (function() {
      // 1. Data Initialization from questions_data.js
      const chaptersData = window.USMLE_PATHOLOGY_CHAPTERS || [
        { id: "Ch01_Cellular_Adaptations_and_Reversible_Injury", name: "Ch01_Cellular_Adaptations_and_Reversible_Injury", totalQuestions: 150, status: "active" },
        { id: "Ch02_Cell_Death_Necrosis_and_Apoptosis", name: "Ch02_Cell_Death_Necrosis_and_Apoptosis", totalQuestions: 150, status: "active" },
        { id: "Ch03_Cellular_Accumulations_and_Amyloidosis", name: "Ch03_Cellular_Accumulations_and_Amyloidosis", totalQuestions: 150, status: "active" },
        { id: "Ch04_Acute_Inflammation_and_Leukocyte_Dynamics", name: "Ch04_Acute_Inflammation_and_Leukocyte_Dynamics", totalQuestions: 150, status: "active" },
        { id: "Ch05_Inflammatory_Mediators_and_Microbial_Killing", name: "Ch05_Inflammatory_Mediators_and_Microbial_Killing", totalQuestions: 150, status: "active" },
        { id: "Ch06_Chronic_and_Granulomatous_Inflammation", name: "Ch06_Chronic_and_Granulomatous_Inflammation", totalQuestions: 150, status: "active" },
        { id: "Ch07_Tissue_Repair_and_Wound_Healing", name: "Ch07_Tissue_Repair_and_Wound_Healing", totalQuestions: 150, status: "active" },
        { id: "08_Hemodynamic_Disorders_Thrombosis_and_Embolism_QA", name: "08_Hemodynamic_Disorders_Thrombosis_and_Embolism_QA", totalQuestions: 0, status: "placeholder" },
        { id: "09_Infarction_and_Shock_QA", name: "09_Infarction_and_Shock_QA", totalQuestions: 0, status: "placeholder" },
        { id: "10_Principles_of_Neoplasia_and_Carcinogenesis_QA", name: "10_Principles_of_Neoplasia_and_Carcinogenesis_QA", totalQuestions: 0, status: "placeholder" },
        { id: "11_Cancer_Genetics_Oncogenes_and_TSGs_QA", name: "11_Cancer_Genetics_Oncogenes_and_TSGs_QA", totalQuestions: 0, status: "placeholder" },
        { id: "12_Clinical_Oncology_Staging_and_Tumor_Markers_QA", name: "12_Clinical_Oncology_Staging_and_Tumor_Markers_QA", totalQuestions: 0, status: "placeholder" },
        { id: "13_Paraneoplastic_Syndromes_QA", name: "13_Paraneoplastic_Syndromes_QA", totalQuestions: 0, status: "placeholder" },
        { id: "14_Cellular_Aging_and_Systemic_Changes_QA", name: "14_Cellular_Aging_and_Systemic_Changes_QA", totalQuestions: 0, status: "placeholder" }
      ];

      const allQuestions = window.USMLE_QUESTIONS || [];

      // 2. Persistent State Management via localStorage
      const STORAGE_KEY_ANSWERS = "usmle_qa_answers_v1";
      const STORAGE_KEY_FLAGS = "usmle_qa_flags_v1";

      let savedAnswers = {};
      let savedFlags = {};
      try {
        savedAnswers = JSON.parse(localStorage.getItem(STORAGE_KEY_ANSWERS)) || {};
        savedFlags = JSON.parse(localStorage.getItem(STORAGE_KEY_FLAGS)) || {};
      } catch(e) {
        console.warn("Storage access restricted, using memory state", e);
      }

      // Attach saved progress to questions
      allQuestions.forEach(q => {
        if (savedAnswers[q.id]) {
          q.answered = true;
          q.userChoice = savedAnswers[q.id];
        }
        if (savedFlags[q.id]) {
          q.flagged = true;
        }
      });

      // 3. App State Tracking
      let activeChapter = "Ch01_Cellular_Adaptations_and_Reversible_Injury";
      let activeBlock = "all"; // "all", "Block 1", "Block 2", "Block 3"
      let flaggedOnlyMode = false;
      let searchQuery = "";

      // DOM Elements
      const navGrid = document.getElementById('nav-buttons-grid');
      const questionsWrapper = document.getElementById('questions-container');
      const chapterPillGroup = document.getElementById('chapter-flag-pill-group');
      const chapterSelectDropdown = document.getElementById('chapter-select-dropdown');
      const breadcrumbEl = document.getElementById('active-chapter-breadcrumb');
      const blockTabsContainer = document.getElementById('block-tabs-container');
      const searchInput = document.getElementById('stem-search-input');

      // 4. Initialize Dropdowns
      function initChapterDropdown() {
        if (!chapterSelectDropdown) return;
        chapterSelectDropdown.innerHTML = '';

        // All active chapters option
        const optAll = document.createElement('option');
        optAll.value = "all";
        optAll.textContent = `All Active Chapters (${allQuestions.length} Qs)`;
        chapterSelectDropdown.appendChild(optAll);

        // 14 Chapters
        chaptersData.forEach((ch, idx) => {
          const opt = document.createElement('option');
          opt.value = ch.id;
          if (ch.status === 'active') {
            opt.textContent = `${ch.id} (${ch.totalQuestions} Qs)`;
          } else {
            opt.textContent = `${ch.id} [待更新 / 占位]`;
          }
          if (ch.id === activeChapter) {
            opt.selected = true;
          }
          chapterSelectDropdown.appendChild(opt);
        });

        chapterSelectDropdown.addEventListener('change', (e) => {
          selectChapter(e.target.value);
        });
      }

      // 5. Select Chapter Handler
      window.selectChapter = function(chapId) {
        activeChapter = chapId;
        activeBlock = "all";
        flaggedOnlyMode = false;
        searchQuery = "";
        if (searchInput) searchInput.value = "";

        if (chapterSelectDropdown) {
          chapterSelectDropdown.value = chapId;
        }

        if (breadcrumbEl) {
          breadcrumbEl.textContent = chapId === 'all' ? 'All Active Chapters' : chapId;
        }

        updateUI();
      };

      // 6. Filter Questions Helper
      function getFilteredQuestions() {
        return allQuestions.filter(q => {
          // Chapter filter
          if (activeChapter !== 'all' && q.chapter !== activeChapter) {
            return false;
          }
          // Block filter
          if (activeBlock !== 'all' && q.block !== activeBlock) {
            return false;
          }
          // Flagged only filter
          if (flaggedOnlyMode && !q.flagged) {
            return false;
          }
          // Search query filter
          if (searchQuery) {
            const qStr = (q.stem + ' ' + q.leadQuestion + ' ' + q.title + ' ' + (q.subtag || '')).toLowerCase();
            if (!qStr.includes(searchQuery.toLowerCase())) {
              return false;
            }
          }
          return true;
        });
      }

      // 7. Render Block Selector Tabs
      function renderBlockTabs() {
        if (!blockTabsContainer) return;
        blockTabsContainer.innerHTML = '';

        const currentChapterObj = chaptersData.find(c => c.id === activeChapter);
        if (!currentChapterObj || currentChapterObj.status !== 'active') {
          blockTabsContainer.style.display = 'none';
          return;
        }
        blockTabsContainer.style.display = 'flex';

        // Count blocks in current chapter
        const chapterQs = allQuestions.filter(q => q.chapter === activeChapter);
        const blocks = ['all', 'Block 1', 'Block 2', 'Block 3'];

        blocks.forEach(blk => {
          const btn = document.createElement('button');
          btn.type = 'button';
          const isBlkActive = activeBlock === blk;
          
          let count = chapterQs.length;
          let label = "All (1-150)";
          if (blk === 'Block 1') { count = chapterQs.filter(q => q.block === 'Block 1').length; label = "Block 1 (1-50)"; }
          if (blk === 'Block 2') { count = chapterQs.filter(q => q.block === 'Block 2').length; label = "Block 2 (51-100)"; }
          if (blk === 'Block 3') { count = chapterQs.filter(q => q.block === 'Block 3').length; label = "Block 3 (101-150)"; }

          btn.className = `px-3 py-1.5 rounded-xl text-[11px] font-bold transition-all ${
            isBlkActive ? 'neu-extruded-xs text-primary neu-pill-active' : 'text-[#656054] hover:text-[#181d24]'
          }`;
          btn.textContent = label;

          btn.addEventListener('click', () => {
            activeBlock = blk;
            updateUI();
          });

          blockTabsContainer.appendChild(btn);
        });
      }

      // 8. Render Navigator Buttons
      function renderNavigator(filteredQs) {
        navGrid.innerHTML = '';

        const navTotalLabel = document.querySelector('aside h3 + span') || document.getElementById('nav-total-count');
        if (navTotalLabel) {
          navTotalLabel.textContent = `${filteredQs.length} Questions`;
        }

        filteredQs.forEach((q, idx) => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.setAttribute('data-q', q.id);
          btn.title = `#${q.qNum || idx+1}: ${q.title}`;
          
          let stateStyle = "neu-groove text-[#3e3931] border border-white/50";
          if (q.answered) {
            if (q.userChoice === q.correct) {
              stateStyle = "bg-[#2d7a5b] text-white neu-extruded-xs border border-white/40 font-bold shadow-sm";
            } else {
              stateStyle = "bg-[#c24141] text-white neu-extruded-xs border border-white/40 font-bold shadow-sm";
            }
          }

          const displayNum = q.qNum ? (q.qNum < 10 ? '0' + q.qNum : q.qNum) : (idx + 1 < 10 ? '0' + (idx + 1) : idx + 1);

          btn.className = `relative h-11 rounded-2xl ${stateStyle} text-[12px] font-mono font-bold flex items-center justify-center transition-all hover:scale-[1.04] active:scale-95 shadow-sm`;
          btn.innerHTML = `
            ${displayNum}
            ${q.flagged ? '<span class="absolute -top-1.5 -right-1.5 w-4 h-4 rounded-full bg-amber-400 border-2 border-white shadow-sm flex items-center justify-center text-[9px] text-amber-950 font-extrabold">★</span>' : ''}
          `;

          btn.addEventListener('click', () => {
            const el = document.getElementById(`question-card-${q.id}`);
            if (el) {
              el.scrollIntoView({ behavior: 'smooth', block: 'center' });
              el.classList.add('ring-2', 'ring-primary');
              setTimeout(() => el.classList.remove('ring-2', 'ring-primary'), 1400);
            }
          });

          navGrid.appendChild(btn);
        });
      }

      // 9. Render Question Cards in Main Container
      function renderQuestions(filteredQs) {
        questionsWrapper.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D', 'E'];

        const currentChapterObj = chaptersData.find(c => c.id === activeChapter);

        // If Placeholder Chapter Selected
        if (currentChapterObj && currentChapterObj.status === 'placeholder') {
          questionsWrapper.innerHTML = `
            <div class="p-10 rounded-3xl neu-extruded border border-white/80 flex flex-col items-center justify-center text-center gap-5 my-6">
              <div class="w-16 h-16 rounded-2xl neu-groove flex items-center justify-center text-amber-700">
                <span class="material-symbols-outlined text-[36px]">hourglass_top</span>
              </div>
              <div class="max-w-xl space-y-2">
                <span class="px-3.5 py-1 rounded-full neu-groove-sm text-[11.5px] font-mono font-bold text-amber-800 bg-[#f3ecd8]">
                  Chapter Status: 待更新 / In Preparation (占位章节)
                </span>
                <h2 class="font-display font-extrabold text-[20px] text-[#181d24] mt-2">${currentChapterObj.id}</h2>
                <p class="text-[13.5px] text-[#6b665c] leading-relaxed mt-1">
                  该章节题目仍在整理校对中，先不载入试题，当前作为标准大纲占位。请在上方或左侧切换至已开放的 <strong>Ch01 至 Ch07 章节</strong> 开展全仿真 USMLE 刷题（共 1,050 道高难度病例试题）。
                </p>
              </div>
              <button class="px-6 py-3 rounded-2xl bg-gradient-to-b from-[#22719f] to-[#175275] text-white font-display text-[13px] font-bold neu-btn border border-white/40 flex items-center gap-2 shadow-md hover:scale-[1.02] active:scale-95 transition-all mt-2" onclick="selectChapter('Ch01_Cellular_Adaptations_and_Reversible_Injury')">
                <span class="material-symbols-outlined text-[19px]">play_circle</span>
                <span>立即进入 Ch01: Cellular Adaptations & Reversible Injury (150题)</span>
              </button>
            </div>
          `;
          return;
        }

        if (filteredQs.length === 0) {
          questionsWrapper.innerHTML = `
            <div class="p-10 rounded-3xl neu-extruded text-center text-[#6b665c] flex flex-col items-center gap-3">
              <span class="material-symbols-outlined text-[36px] text-[#9c9689]">find_in_page</span>
              <p class="font-medium text-[14px]">No questions match current filter criteria.</p>
              <button onclick="selectChapter('Ch01_Cellular_Adaptations_and_Reversible_Injury')" class="text-primary font-bold hover:underline text-[12.5px]">Clear filters</button>
            </div>
          `;
          return;
        }

        filteredQs.forEach((q, idx) => {
          const card = document.createElement('section');
          card.id = `question-card-${q.id}`;
          card.className = "question-card p-8 rounded-3xl neu-extruded border border-white/70 flex flex-col gap-6 scroll-mt-36 transition-all duration-300 mb-8";

          // Options markup as sunken grooves
          let optionsHtml = '';
          q.options.forEach((optText, optIdx) => {
            const letter = letters[optIdx] || String.fromCharCode(65 + optIdx);
            let optStyle = "neu-groove-sm hover:border-white/80 cursor-pointer";
            let letterStyle = "neu-extruded-xs text-[#3a352d] border border-white/60";
            let statusIcon = "";

            if (q.answered) {
              if (letter === q.correct) {
                optStyle = "neu-groove bg-[#dfeae3] border border-emerald-500/50 text-[#1f5c42] font-semibold";
                letterStyle = "bg-[#2d7a5b] text-white shadow-sm";
                statusIcon = `<span class="material-symbols-outlined text-[#2d7a5b] text-[22px]">check_circle</span>`;
              } else if (letter === q.userChoice && q.userChoice !== q.correct) {
                optStyle = "neu-groove bg-[#f4e2e2] border border-rose-400/50 text-[#9b2a2a] line-through";
                letterStyle = "bg-[#c24141] text-white shadow-sm";
                statusIcon = `<span class="material-symbols-outlined text-[#c24141] text-[22px]">cancel</span>`;
              } else {
                optStyle = "neu-groove opacity-50 border border-white/20 cursor-not-allowed";
              }
            } else if (q.tempChoice === letter) {
              optStyle = "neu-groove border border-primary/50 bg-[#e1e9ef]";
              letterStyle = "bg-primary text-white shadow-sm";
            }

            optionsHtml += `
              <div class="option-item p-4 rounded-2xl ${optStyle} flex items-center justify-between transition-all" data-q="${q.id}" data-opt="${letter}">
                <div class="flex items-center gap-3.5 flex-1 pr-2">
                  <span class="w-8 h-8 rounded-full ${letterStyle} flex items-center justify-center font-mono text-[12.5px] font-bold shrink-0">${letter}</span>
                  <span class="text-[14px] text-[#242930] font-medium leading-relaxed">${optText}</span>
                </div>
                ${statusIcon}
              </div>
            `;
          });

          // Flag button visual state with soft tactile pill
          const flagBtnMarkup = q.flagged ? `
            <button class="flag-toggle-btn px-3.5 py-1.5 rounded-full neu-extruded-xs border border-amber-300 bg-[#f3ecd8] text-amber-800 flex items-center gap-1.5 transition-all shadow-sm active:neu-groove" data-q="${q.id}">
              <span class="material-symbols-outlined text-[17px] text-amber-600 fill-current">bookmark</span>
              <span class="font-mono text-[11px] font-bold">Flagged</span>
            </button>
          ` : `
            <button class="flag-toggle-btn px-3.5 py-1.5 rounded-full neu-btn border border-white/80 text-[#6d685c] hover:text-amber-700 flex items-center gap-1.5 transition-all active:neu-groove" data-q="${q.id}">
              <span class="material-symbols-outlined text-[17px]">bookmark_border</span>
              <span class="font-mono text-[11px] font-semibold">Flag</span>
            </button>
          `;

          const qIndexLabel = q.qNum ? `Question ${q.qNum < 10 ? '0' + q.qNum : q.qNum}` : `Question ${idx + 1}`;

          // Card Content
          card.innerHTML = `
            <!-- Question Top Meta Header -->
            <div class="flex items-center justify-between pb-4 border-b border-[#dfd9cc] flex-wrap gap-2">
              <div class="flex flex-wrap items-center gap-2.5">
                <span class="px-3 py-1 rounded-full neu-groove text-primary font-mono text-[11.5px] font-bold border border-white/60">
                  ${qIndexLabel} ${q.block ? `(${q.block})` : ''}
                </span>
                <span class="px-3 py-1 rounded-full neu-extruded-xs text-[11px] font-semibold text-[#3e3931] border border-white/80">
                  ${q.chapter}
                </span>
                <span class="px-2.5 py-0.5 rounded-full neu-groove-sm text-[10.5px] font-bold font-mono text-amber-900 bg-[#ede4d5]">
                  ${q.difficulty || 'USMLE Step 1'}
                </span>
              </div>

              <!-- Flag / Bookmark Pill -->
              ${flagBtnMarkup}
            </div>

            <!-- Clinical Vignette Stem -->
            <p class="text-[14.5px] text-[#242930] leading-relaxed font-normal">
              ${q.stem}
            </p>

            <!-- Tactile Inset Lead Question Prompt -->
            <div class="p-4.5 rounded-2xl neu-groove flex items-center gap-3.5 border border-white/50 bg-[#e7e2d9]">
              <div class="w-9 h-9 rounded-xl neu-extruded-xs flex items-center justify-center text-primary shrink-0">
                <span class="material-symbols-outlined text-[20px]">troubleshoot</span>
              </div>
              <span class="font-display font-bold text-[14.5px] text-[#181d24] leading-snug">
                ${q.leadQuestion}
              </span>
            </div>

            <!-- Answer Options (Tactile Sunken Grooves) -->
            <div class="options-container flex flex-col gap-3.5" data-q="${q.id}">
              ${optionsHtml}
            </div>

            <!-- Action Ribbon -->
            <div class="flex items-center justify-between pt-2">
              <button class="submit-btn px-6 py-2.5 rounded-2xl bg-gradient-to-b from-[#22719f] to-[#175275] text-white font-display text-[13px] font-bold neu-btn border border-white/40 active:neu-groove transition-all ${q.answered ? 'opacity-45 pointer-events-none' : ''}" data-q="${q.id}">
                ${q.answered ? 'Answer Submitted' : 'Submit Answer'}
              </button>
              ${!q.answered ? `<button class="clear-btn text-[11.5px] text-[#736e62] hover:text-primary transition-colors font-semibold" data-q="${q.id}">Clear Selection</button>` : ''}
            </div>

            <!-- Detailed Explanation Box -->
            <div class="explanation-box ${q.answered ? 'flex' : 'hidden'} p-6 rounded-2xl neu-groove flex-col gap-4 border border-white/50 bg-[#e8e3da]">
              <div class="flex items-center gap-2 font-display text-[15px] font-bold ${q.userChoice === q.correct ? 'text-accentSuccess' : 'text-accentDanger'}">
                <span class="material-symbols-outlined text-[24px]">
                  ${q.userChoice === q.correct ? 'check_circle' : 'cancel'}
                </span>
                <span>
                  ${q.userChoice === q.correct ? 'Correct! High-Yield Concept Mastered' : `Incorrect (Your Selection: Option ${q.userChoice || 'None'} | Key: Option ${q.correct})`}
                </span>
              </div>
              
              <!-- Pre-rendered Rich Explanation HTML -->
              <div class="explanation-content text-[13.5px] text-[#242930] leading-relaxed space-y-2">
                ${q.explanation || `<p>${q.rawObjective || ''}</p>`}
              </div>
            </div>
          `;

          questionsWrapper.appendChild(card);
        });
      }

      // 10. Update Metrics and Chapter Pills
      function updateMetricsAndChapterPills() {
        let totalAnswered = 0;
        let totalCorrect = 0;
        let totalIncorrect = 0;
        let totalFlagged = 0;

        const chapterFlagCounts = {};
        const chapterAnsCounts = {};

        allQuestions.forEach(q => {
          if (q.answered) {
            totalAnswered++;
            chapterAnsCounts[q.chapter] = (chapterAnsCounts[q.chapter] || 0) + 1;
            if (q.userChoice === q.correct) totalCorrect++;
            else totalIncorrect++;
          }
          if (q.flagged) {
            totalFlagged++;
            chapterFlagCounts[q.chapter] = (chapterFlagCounts[q.chapter] || 0) + 1;
          }
        });

        // Current Chapter Stats
        const currentFiltered = getFilteredQuestions();
        let curCorrect = 0, curIncorrect = 0, curAnswered = 0, curFlagged = 0;
        currentFiltered.forEach(q => {
          if (q.answered) {
            curAnswered++;
            if (q.userChoice === q.correct) curCorrect++;
            else curIncorrect++;
          }
          if (q.flagged) curFlagged++;
        });

        // Update Inset Panel Stats
        const statCorrectEl = document.getElementById('stat-correct');
        const statIncorrectEl = document.getElementById('stat-incorrect');
        const statUnansweredEl = document.getElementById('stat-unanswered');
        const statFlaggedEl = document.getElementById('stat-flagged');
        const topFlagCountEl = document.getElementById('top-flag-count');
        const topAnsweredCountEl = document.getElementById('top-answered-count');
        const badgeTotalFlaggedEl = document.getElementById('badge-total-flagged');

        if (statCorrectEl) statCorrectEl.innerText = curCorrect;
        if (statIncorrectEl) statIncorrectEl.innerText = curIncorrect;
        if (statUnansweredEl) statUnansweredEl.innerText = (currentFiltered.length - curAnswered);
        if (statFlaggedEl) statFlaggedEl.innerText = curFlagged;
        if (topFlagCountEl) topFlagCountEl.innerText = totalFlagged;
        if (badgeTotalFlaggedEl) badgeTotalFlaggedEl.innerText = `${totalFlagged} Marked`;
        if (topAnsweredCountEl) topAnsweredCountEl.innerText = `${totalAnswered}/${allQuestions.length}`;

        // Banner Stats
        const bCorrect = document.getElementById('banner-stat-correct');
        const bIncorrect = document.getElementById('banner-stat-incorrect');
        const bUnanswered = document.getElementById('banner-stat-unanswered');
        const bFlagged = document.getElementById('banner-stat-flagged');
        if (bCorrect) bCorrect.innerText = curCorrect;
        if (bIncorrect) bIncorrect.innerText = curIncorrect;
        if (bUnanswered) bUnanswered.innerText = (currentFiltered.length - curAnswered);
        if (bFlagged) bFlagged.innerText = curFlagged;

        // Banner Header text
        const bTitle = document.getElementById('banner-chapter-title');
        const bBadge = document.getElementById('banner-chapter-badge');
        const bDesc = document.getElementById('banner-chapter-desc');
        const curChapObj = chaptersData.find(c => c.id === activeChapter);

        if (bTitle) {
          bTitle.textContent = activeChapter === 'all' ? 'All Active Pathology Chapters' : (curChapObj ? curChapObj.id : activeChapter);
        }
        if (bBadge) {
          if (activeChapter === 'all') {
            bBadge.className = "px-3 py-0.5 rounded-full neu-groove-sm text-[11px] font-mono font-bold text-accentSuccess bg-[#dfeae3]";
            bBadge.textContent = `Active (${allQuestions.length} Qs)`;
          } else if (curChapObj && curChapObj.status === 'active') {
            bBadge.className = "px-3 py-0.5 rounded-full neu-groove-sm text-[11px] font-mono font-bold text-accentSuccess bg-[#dfeae3]";
            bBadge.textContent = `Active (${curChapObj.totalQuestions} Qs)`;
          } else {
            bBadge.className = "px-3 py-0.5 rounded-full neu-groove-sm text-[11px] font-mono font-bold text-amber-800 bg-[#f3ecd8]";
            bBadge.textContent = "待更新 / 占位章节 (0 Qs)";
          }
        }
        if (bDesc) {
          bDesc.textContent = curChapObj ? curChapObj.description : "USMLE Step 1 Pathology Review & Question Bank (MedGemma 27B)";
        }

        // Render Left Sidebar Chapter Pills (All 14 Chapters!)
        if (chapterPillGroup) {
          chapterPillGroup.innerHTML = '';

          // 1. "All Active Chapters" Master Pill
          const allBtn = document.createElement('button');
          allBtn.type = 'button';
          const isAllActive = activeChapter === 'all';
          allBtn.className = `w-full flex items-center justify-between px-3.5 py-2 rounded-2xl text-[11.5px] transition-all ${
            isAllActive 
              ? 'neu-groove text-primary bg-[#e1dbd0] border border-primary/40 font-bold' 
              : 'neu-btn text-[#3e3931] border-white/60 hover:text-primary'
          }`;
          allBtn.innerHTML = `
            <span class="flex items-center gap-1.5 truncate">
              <span class="w-2 h-2 rounded-full bg-primary shrink-0"></span>
              <span class="truncate">All Pathology (${allQuestions.length} Qs)</span>
            </span>
            <span class="font-mono text-[10.5px] px-2 py-0.5 rounded-full neu-groove-sm text-primary shrink-0 font-bold">${totalFlagged} ★</span>
          `;
          allBtn.addEventListener('click', () => selectChapter('all'));
          chapterPillGroup.appendChild(allBtn);

          // 2. 14 Chapters
          chaptersData.forEach(chap => {
            const btn = document.createElement('button');
            btn.type = 'button';
            const isChapActive = activeChapter === chap.id;
            const flagCount = chapterFlagCounts[chap.id] || 0;

            let statusBadge = "";
            if (chap.status === 'active') {
              statusBadge = flagCount > 0 ? `<span class="font-mono text-[10.5px] font-bold text-amber-800">${flagCount} ★</span>` : `<span class="font-mono text-[10.5px] text-[#8c867a]">150</span>`;
            } else {
              statusBadge = `<span class="text-[9.5px] px-1.5 py-0.5 rounded-md neu-groove-sm text-amber-800 bg-[#ede5d8] font-mono">待更新</span>`;
            }

            btn.className = `w-full flex items-center justify-between px-3 py-2 rounded-2xl text-[11px] transition-all text-left ${
              isChapActive 
                ? 'neu-groove text-primary bg-[#dfd9ce] border border-primary/40 font-bold' 
                : 'neu-groove-sm text-[#4c473d] border-white/40 hover:text-[#181d24]'
            }`;
            btn.innerHTML = `
              <span class="truncate pr-2 font-mono text-[11px]">${chap.id}</span>
              ${statusBadge}
            `;
            btn.addEventListener('click', () => selectChapter(chap.id));
            chapterPillGroup.appendChild(btn);
          });
        }
      }

      // 11. Full UI Refresh Orchestrator
      function updateUI() {
        const filtered = getFilteredQuestions();
        renderBlockTabs();
        renderNavigator(filtered);
        renderQuestions(filtered);
        updateMetricsAndChapterPills();
      }

      // 12. Global Click & Delegation Listener
      document.addEventListener('click', (e) => {
        // A. Toggle Flag / Bookmark
        const flagBtn = e.target.closest('.flag-toggle-btn');
        if (flagBtn) {
          const qId = parseInt(flagBtn.getAttribute('data-q'), 10);
          const q = allQuestions.find(item => item.id === qId);
          if (q) {
            q.flagged = !q.flagged;
            if (q.flagged) savedFlags[q.id] = true;
            else delete savedFlags[q.id];
            try { localStorage.setItem(STORAGE_KEY_FLAGS, JSON.stringify(savedFlags)); } catch(err){}
            updateUI();
          }
          return;
        }

        // B. Select Option
        const optItem = e.target.closest('.option-item');
        if (optItem) {
          const qId = parseInt(optItem.getAttribute('data-q'), 10);
          const chosenOpt = optItem.getAttribute('data-opt');
          const q = allQuestions.find(item => item.id === qId);
          if (q && !q.answered) {
            q.tempChoice = chosenOpt;
            const container = optItem.closest('.options-container');
            container.querySelectorAll('.option-item').forEach(el => {
              el.className = "option-item p-4 rounded-2xl neu-groove-sm hover:border-white/80 cursor-pointer flex items-center justify-between transition-all";
              const lSpan = el.querySelector('span:first-child');
              lSpan.className = "w-8 h-8 rounded-full neu-extruded-xs text-[#3a352d] border border-white/60 flex items-center justify-center font-mono text-[12.5px] font-bold shrink-0";
            });
            // highlight chosen
            optItem.className = "option-item p-4 rounded-2xl neu-groove border border-primary/50 bg-[#e1e9ef] flex items-center justify-between cursor-pointer transition-all";
            const lSpan = optItem.querySelector('span:first-child');
            lSpan.className = "w-8 h-8 rounded-full bg-primary text-white flex items-center justify-center font-mono text-[12.5px] font-bold shadow-sm shrink-0";
          }
          return;
        }

        // C. Clear Option Selection
        const clearBtn = e.target.closest('.clear-btn');
        if (clearBtn) {
          const qId = parseInt(clearBtn.getAttribute('data-q'), 10);
          const q = allQuestions.find(item => item.id === qId);
          if (q && !q.answered) {
            delete q.tempChoice;
            const card = document.getElementById(`question-card-${qId}`);
            if (card) {
              card.querySelectorAll('.option-item').forEach(el => {
                el.className = "option-item p-4 rounded-2xl neu-groove-sm hover:border-white/80 cursor-pointer flex items-center justify-between transition-all";
                const lSpan = el.querySelector('span:first-child');
                lSpan.className = "w-8 h-8 rounded-full neu-extruded-xs text-[#3a352d] border border-white/60 flex items-center justify-center font-mono text-[12.5px] font-bold shrink-0";
              });
            }
          }
          return;
        }

        // D. Submit Answer
        const submitBtn = e.target.closest('.submit-btn');
        if (submitBtn) {
          const qId = parseInt(submitBtn.getAttribute('data-q'), 10);
          const q = allQuestions.find(item => item.id === qId);
          if (q && !q.answered) {
            if (!q.tempChoice) {
              alert("Please pick an answer option (A - E) prior to submitting.");
              return;
            }
            q.userChoice = q.tempChoice;
            q.answered = true;
            savedAnswers[q.id] = q.userChoice;
            try { localStorage.setItem(STORAGE_KEY_ANSWERS, JSON.stringify(savedAnswers)); } catch(err){}
            updateUI();
          }
          return;
        }
      });

      // 13. Top Toolbar Controls
      const toggleFlaggedTopBtn = document.getElementById('toggle-flagged-only-btn');
      if (toggleFlaggedTopBtn) {
        toggleFlaggedTopBtn.addEventListener('click', () => {
          flaggedOnlyMode = !flaggedOnlyMode;
          if (flaggedOnlyMode) {
            toggleFlaggedTopBtn.className = "flex items-center gap-2 px-4 py-1.5 rounded-full neu-groove text-[11.5px] font-bold text-amber-800 bg-[#e4ded4] border border-amber-300 transition-all";
          } else {
            toggleFlaggedTopBtn.className = "flex items-center gap-2 px-4 py-1.5 rounded-full neu-btn text-[11.5px] font-bold text-amber-700 hover:text-amber-800 transition-all border border-white/60";
          }
          updateUI();
        });
      }

      const resetFlagBtn = document.getElementById('reset-flag-filter-btn');
      if (resetFlagBtn) {
        resetFlagBtn.addEventListener('click', () => {
          flaggedOnlyMode = false;
          selectChapter('all');
        });
      }

      // Reset Chapter Answers
      const resetChapterBtn = document.getElementById('reset-chapter-answers-btn');
      if (resetChapterBtn) {
        resetChapterBtn.addEventListener('click', () => {
          if (!confirm(`Are you sure you want to clear your submitted answers for this chapter?`)) return;
          const currentFiltered = getFilteredQuestions();
          currentFiltered.forEach(q => {
            q.answered = false;
            delete q.userChoice;
            delete q.tempChoice;
            delete savedAnswers[q.id];
          });
          try { localStorage.setItem(STORAGE_KEY_ANSWERS, JSON.stringify(savedAnswers)); } catch(err){}
          updateUI();
        });
      }

      // Search Filter
      if (searchInput) {
        searchInput.addEventListener('input', (e) => {
          searchQuery = e.target.value.trim();
          updateUI();
        });
      }

      // 14. Interactive Examination Timer Implementation
      let timerSeconds = 45 * 60;
      let timerRunning = false;
      let isStopwatch = false;
      let timerInterval = null;

      const timerEl = document.getElementById('exam-timer');
      const timerPlayIcon = document.getElementById('timer-play-icon');
      const timerLabel = document.getElementById('timer-mode-label');
      const timerToggleBtn = document.getElementById('timer-start-pause-btn');
      const timerResetBtn = document.getElementById('timer-reset-btn');
      const timerSettingsBtn = document.getElementById('timer-settings-toggle-btn');
      const timerDropdown = document.getElementById('timer-dropdown');
      const timerModeToggle = document.getElementById('timer-mode-toggle');

      function formatTime(sec) {
        const m = Math.floor(sec / 60);
        const s = sec % 60;
        return `${m < 10 ? '0' + m : m}:${s < 10 ? '0' + s : s}`;
      }

      function updateTimerDisplay() {
        if (timerEl) timerEl.textContent = formatTime(timerSeconds);
      }

      if (timerToggleBtn) {
        timerToggleBtn.addEventListener('click', () => {
          timerRunning = !timerRunning;
          if (timerRunning) {
            timerPlayIcon.textContent = 'pause';
            timerInterval = setInterval(() => {
              if (isStopwatch) {
                timerSeconds++;
              } else {
                if (timerSeconds > 0) timerSeconds--;
                else {
                  timerRunning = false;
                  clearInterval(timerInterval);
                  timerPlayIcon.textContent = 'play_arrow';
                  alert("Time expired for this USMLE examination block!");
                }
              }
              updateTimerDisplay();
            }, 1000);
          } else {
            timerPlayIcon.textContent = 'play_arrow';
            clearInterval(timerInterval);
          }
        });
      }

      if (timerResetBtn) {
        timerResetBtn.addEventListener('click', () => {
          timerRunning = false;
          clearInterval(timerInterval);
          if (timerPlayIcon) timerPlayIcon.textContent = 'play_arrow';
          timerSeconds = isStopwatch ? 0 : 45 * 60;
          updateTimerDisplay();
        });
      }

      if (timerSettingsBtn && timerDropdown) {
        timerSettingsBtn.addEventListener('click', () => {
          timerDropdown.classList.toggle('hidden');
        });
      }

      if (timerModeToggle) {
        timerModeToggle.addEventListener('click', () => {
          isStopwatch = !isStopwatch;
          timerModeToggle.textContent = isStopwatch ? 'Switch to Countdown' : 'Switch to Stopwatch';
          if (timerLabel) timerLabel.textContent = isStopwatch ? 'Stopw' : 'Count';
          timerSeconds = isStopwatch ? 0 : 45 * 60;
          timerRunning = false;
          clearInterval(timerInterval);
          if (timerPlayIcon) timerPlayIcon.textContent = 'play_arrow';
          updateTimerDisplay();
          if (timerDropdown) timerDropdown.classList.add('hidden');
        });
      }

      document.querySelectorAll('.timer-preset-btn').forEach(btn => {
        btn.addEventListener('click', () => {
          const mins = parseInt(btn.getAttribute('data-mins'), 10);
          isStopwatch = false;
          if (timerLabel) timerLabel.textContent = 'Count';
          timerSeconds = mins * 60;
          timerRunning = false;
          clearInterval(timerInterval);
          if (timerPlayIcon) timerPlayIcon.textContent = 'play_arrow';
          updateTimerDisplay();
          document.querySelectorAll('.timer-preset-btn').forEach(b => b.classList.remove('neu-pill-active', 'text-primary'));
          btn.classList.add('neu-pill-active', 'text-primary');
          if (timerDropdown) timerDropdown.classList.add('hidden');
        });
      });

      const setCustomBtn = document.getElementById('timer-set-custom-btn');
      const customInput = document.getElementById('timer-custom-input');
      if (setCustomBtn && customInput) {
        setCustomBtn.addEventListener('click', () => {
          const val = parseInt(customInput.value, 10);
          if (val > 0) {
            isStopwatch = false;
            if (timerLabel) timerLabel.textContent = 'Count';
            timerSeconds = val * 60;
            timerRunning = false;
            clearInterval(timerInterval);
            if (timerPlayIcon) timerPlayIcon.textContent = 'play_arrow';
            updateTimerDisplay();
            if (timerDropdown) timerDropdown.classList.add('hidden');
          }
        });
      }

      // 15. Initial Boot
      initChapterDropdown();
      updateUI();
    })();
'''

    final_html = part1 + right_column_html + new_script_js + '\n  </script>\n</body></html>'

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Successfully generated index.html ({len(final_html)} chars)")

if __name__ == '__main__':
    generate_html()
