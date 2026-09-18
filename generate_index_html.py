import re

def generate_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        content = f.read()

    nav_replacement = '''<!-- 1. Question Navigator Grid Card -->
<div class="p-7 rounded-3xl neu-extruded flex flex-col gap-4">
<div class="flex items-center justify-between pb-3 border-b border-[#ded7ca]">
<div class="flex items-center gap-2.5">
<div class="w-8 h-8 rounded-xl neu-extruded-xs flex items-center justify-center text-primary">
<span class="material-symbols-outlined text-[20px]">grid_view</span>
</div>
<h3 class="font-display font-bold text-[15.5px] text-[#181d24]">Question Navigator</h3>
</div>
<span class="font-mono text-[11px] px-2.5 py-0.5 rounded-full neu-groove-sm text-primary font-bold" id="nav-total-count">20 Questions</span>
</div>

<!-- 20-Question Module Selector & Pagination Toolbar -->
<div class="flex items-center justify-between gap-2 p-1.5 rounded-2xl neu-groove-sm border border-white/40">
  <div class="flex items-center gap-1.5 pl-2 flex-1 min-w-0">
    <span class="text-[#756f64] font-bold text-[10.5px] uppercase font-mono tracking-wider shrink-0">Range:</span>
    <div class="relative flex items-center flex-1 min-w-0">
      <select id="module-select-dropdown" class="appearance-none bg-[#eae6de] neu-extruded-xs border border-white/80 rounded-xl px-2.5 py-1.5 pr-6 text-[11.5px] font-bold text-[#181d24] cursor-pointer outline-none transition-all shadow-sm w-full truncate">
        <!-- Dynamically injected: e.g. Q01 - Q20, Q21 - Q40... -->
      </select>
      <span class="material-symbols-outlined text-[15px] text-[#6d675b] absolute right-1.5 pointer-events-none">expand_more</span>
    </div>
  </div>
  <div class="flex items-center gap-1 shrink-0">
    <button id="nav-prev-set-btn" class="w-7 h-7 rounded-xl neu-btn flex items-center justify-center text-[#555047] hover:text-primary transition-all disabled:opacity-30 disabled:pointer-events-none" title="Previous 20 Questions">
      <span class="material-symbols-outlined text-[16px]">chevron_left</span>
    </button>
    <button id="nav-next-set-btn" class="w-7 h-7 rounded-xl neu-btn flex items-center justify-center text-[#555047] hover:text-primary transition-all disabled:opacity-30 disabled:pointer-events-none" title="Next 20 Questions">
      <span class="material-symbols-outlined text-[16px]">chevron_right</span>
    </button>
  </div>
</div>

<!-- 20 Interactive Grid Badges (Locked at max 20 buttons) -->
<div class="grid grid-cols-5 gap-2.5" id="nav-buttons-grid"></div>'''

    c_start = content.find('<!-- 1. Question Navigator Grid Card -->')
    c_end = content.find('<!-- Neumorphic Metric Inset Panel -->')
    if c_start != -1 and c_end != -1:
        content = content[:c_start] + nav_replacement + '\n' + content[c_end:]

    # Now update the script section with the new 20-question module pagination logic
    script_start_idx = content.rfind('<script>')
    script_end_idx = content.rfind('</script>')

    if script_start_idx == -1 or script_end_idx == -1:
        print("ERROR: Script tags not found!")
        return

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
      
      // ★ Pagination / 20-Question Module Tracking
      const PAGE_SIZE = 20;
      let currentModuleIndex = 0; // 0-indexed: 0 = Q1-20, 1 = Q21-40, etc.

      // DOM Elements
      const navGrid = document.getElementById('nav-buttons-grid');
      const questionsWrapper = document.getElementById('questions-container');
      const chapterPillGroup = document.getElementById('chapter-flag-pill-group');
      const chapterSelectDropdown = document.getElementById('chapter-select-dropdown');
      const breadcrumbEl = document.getElementById('active-chapter-breadcrumb');
      const blockTabsContainer = document.getElementById('block-tabs-container');
      const searchInput = document.getElementById('stem-search-input');
      const moduleSelectDropdown = document.getElementById('module-select-dropdown');
      const navPrevSetBtn = document.getElementById('nav-prev-set-btn');
      const navNextSetBtn = document.getElementById('nav-next-set-btn');
      const navTotalLabel = document.getElementById('nav-total-count');

      // 4. Initialize Dropdowns
      function initChapterDropdown() {
        if (!chapterSelectDropdown) return;
        chapterSelectDropdown.innerHTML = '';

        const optAll = document.createElement('option');
        optAll.value = "all";
        optAll.textContent = `All Active Chapters (${allQuestions.length} Qs)`;
        chapterSelectDropdown.appendChild(optAll);

        chaptersData.forEach((ch) => {
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
        currentModuleIndex = 0; // Reset to first 20 questions
        if (searchInput) searchInput.value = "";

        if (chapterSelectDropdown) {
          chapterSelectDropdown.value = chapId;
        }

        if (breadcrumbEl) {
          breadcrumbEl.textContent = chapId === 'all' ? 'All Active Chapters' : chapId;
        }

        updateUI();
        scrollQuestionsToTop();
      };

      // 6. Filter Questions Helper
      function getFilteredQuestions() {
        return allQuestions.filter(q => {
          if (activeChapter !== 'all' && q.chapter !== activeChapter) {
            return false;
          }
          if (activeBlock !== 'all' && q.block !== activeBlock) {
            return false;
          }
          if (flaggedOnlyMode && !q.flagged) {
            return false;
          }
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
            currentModuleIndex = 0; // Reset to first 20 of this block
            updateUI();
            scrollQuestionsToTop();
          });

          blockTabsContainer.appendChild(btn);
        });
      }

      // 8. Render Module Dropdown & Pagination Controls
      function updateModuleControls(totalQuestions) {
        const totalModules = Math.ceil(totalQuestions / PAGE_SIZE) || 1;
        if (currentModuleIndex >= totalModules) {
          currentModuleIndex = Math.max(0, totalModules - 1);
        }

        if (moduleSelectDropdown) {
          moduleSelectDropdown.innerHTML = '';
          for (let i = 0; i < totalModules; i++) {
            const startQ = i * PAGE_SIZE + 1;
            const endQ = Math.min((i + 1) * PAGE_SIZE, totalQuestions);
            
            const opt = document.createElement('option');
            opt.value = i;
            const startStr = startQ < 10 ? '0' + startQ : startQ;
            const endStr = endQ < 10 ? '0' + endQ : endQ;
            opt.textContent = `Q${startStr} - Q${endStr}`;
            if (i === currentModuleIndex) {
              opt.selected = true;
            }
            moduleSelectDropdown.appendChild(opt);
          }
        }

        if (navPrevSetBtn) {
          navPrevSetBtn.disabled = (currentModuleIndex === 0);
        }
        if (navNextSetBtn) {
          navNextSetBtn.disabled = (currentModuleIndex >= totalModules - 1);
        }

        if (navTotalLabel) {
          if (totalQuestions === 0) {
            navTotalLabel.textContent = "0 Questions";
          } else {
            const startQ = currentModuleIndex * PAGE_SIZE + 1;
            const endQ = Math.min((currentModuleIndex + 1) * PAGE_SIZE, totalQuestions);
            navTotalLabel.textContent = `${startQ}-${endQ} of ${totalQuestions}`;
          }
        }
      }

      // Helper: Isolated Smooth Scrolling for Right Questions Panel
      function scrollQuestionsToTop() {
        const rc = document.getElementById('right-scroll-container');
        if (rc && window.innerWidth >= 1024) {
          rc.scrollTo({ top: 0, behavior: 'smooth' });
        } else {
          window.scrollTo({ top: 120, behavior: 'smooth' });
        }
      }

      function scrollToQuestion(qId) {
        const el = document.getElementById(`question-card-${qId}`);
        const rc = document.getElementById('right-scroll-container');
        if (!el) return;
        if (rc && window.innerWidth >= 1024) {
          const rcRect = rc.getBoundingClientRect();
          const elRect = el.getBoundingClientRect();
          const targetTop = rc.scrollTop + (elRect.top - rcRect.top) - 16;
          rc.scrollTo({ top: Math.max(0, targetTop), behavior: 'smooth' });
        } else {
          el.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }
        el.classList.add('ring-2', 'ring-primary');
        setTimeout(() => el.classList.remove('ring-2', 'ring-primary'), 1400);
      }

      // 9. Render Navigator Buttons (Strictly 20 Questions)
      function renderNavigator(current20Qs) {
        if (!navGrid) return;
        navGrid.innerHTML = '';

        current20Qs.forEach((q, idx) => {
          const btn = document.createElement('button');
          btn.type = 'button';
          btn.setAttribute('data-q', q.id);
          btn.title = `#${q.qNum || idx + 1}: ${q.title}`;
          
          let stateStyle = "neu-groove text-[#3e3931] border border-white/50";
          if (q.answered) {
            if (q.userChoice === q.correct) {
              stateStyle = "bg-[#2d7a5b] text-white neu-extruded-xs border border-white/40 font-bold shadow-sm";
            } else {
              stateStyle = "bg-[#c24141] text-white neu-extruded-xs border border-white/40 font-bold shadow-sm";
            }
          }

          const displayNum = q.qNum ? (q.qNum < 10 ? '0' + q.qNum : q.qNum) : (idx + 1 < 10 ? '0' + (idx + 1) : idx + 1);

          btn.className = `relative h-11 rounded-2xl ${stateStyle} text-[12px] font-mono font-bold flex items-center justify-center transition-all hover:scale-[1.05] active:scale-95 shadow-sm`;
          btn.innerHTML = `
            ${displayNum}
            ${q.flagged ? '<span class="absolute -top-1.5 -right-1.5 w-4 h-4 rounded-full bg-amber-400 border-2 border-white shadow-sm flex items-center justify-center text-[9px] text-amber-950 font-extrabold">★</span>' : ''}
          `;

          btn.addEventListener('click', () => {
            scrollToQuestion(q.id);
          });

          navGrid.appendChild(btn);
        });
      }

      // 10. Render Question Cards in Main Container (Current 20 Questions)
      function renderQuestions(current20Qs, totalQuestions, totalModules) {
        if (!questionsWrapper) return;
        questionsWrapper.innerHTML = '';
        const letters = ['A', 'B', 'C', 'D', 'E'];

        const currentChapterObj = chaptersData.find(c => c.id === activeChapter);

        // Placeholder Chapter View
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
                <span>立即进入 Ch01: Cellular Adaptations & Reversible Injury (150 Qs)</span>
              </button>
            </div>
          `;
          return;
        }

        if (totalQuestions === 0) {
          questionsWrapper.innerHTML = `
            <div class="p-10 rounded-3xl neu-extruded text-center text-[#6b665c] flex flex-col items-center gap-3">
              <span class="material-symbols-outlined text-[36px] text-[#9c9689]">find_in_page</span>
              <p class="font-medium text-[14px]">No questions match current filter criteria.</p>
              <button onclick="selectChapter('Ch01_Cellular_Adaptations_and_Reversible_Injury')" class="text-primary font-bold hover:underline text-[12.5px]">Clear filters</button>
            </div>
          `;
          return;
        }

        // Render current 20 question cards
        current20Qs.forEach((q, idx) => {
          const card = document.createElement('section');
          card.id = `question-card-${q.id}`;
          card.className = "question-card p-8 rounded-3xl neu-extruded border border-white/70 flex flex-col gap-6 scroll-mt-36 transition-all duration-300 mb-8";

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

          card.innerHTML = `
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
              ${flagBtnMarkup}
            </div>

            <p class="text-[14.5px] text-[#242930] leading-relaxed font-normal">
              ${q.stem}
            </p>

            <div class="p-4.5 rounded-2xl neu-groove flex items-center gap-3.5 border border-white/50 bg-[#e7e2d9]">
              <div class="w-9 h-9 rounded-xl neu-extruded-xs flex items-center justify-center text-primary shrink-0">
                <span class="material-symbols-outlined text-[20px]">troubleshoot</span>
              </div>
              <span class="font-display font-bold text-[14.5px] text-[#181d24] leading-snug">
                ${q.leadQuestion}
              </span>
            </div>

            <div class="options-container flex flex-col gap-3.5" data-q="${q.id}">
              ${optionsHtml}
            </div>

            <div class="flex items-center justify-between pt-2">
              <button class="submit-btn px-6 py-2.5 rounded-2xl bg-gradient-to-b from-[#22719f] to-[#175275] text-white font-display text-[13px] font-bold neu-btn border border-white/40 active:neu-groove transition-all ${q.answered ? 'opacity-45 pointer-events-none' : ''}" data-q="${q.id}">
                ${q.answered ? 'Answer Submitted' : 'Submit Answer'}
              </button>
              ${!q.answered ? `<button class="clear-btn text-[11.5px] text-[#736e62] hover:text-primary transition-colors font-semibold" data-q="${q.id}">Clear Selection</button>` : ''}
            </div>

            <div class="explanation-box ${q.answered ? 'flex' : 'hidden'} p-6 rounded-2xl neu-groove flex-col gap-4 border border-white/50 bg-[#e8e3da]">
              <div class="flex items-center gap-2 font-display text-[15px] font-bold ${q.userChoice === q.correct ? 'text-accentSuccess' : 'text-accentDanger'}">
                <span class="material-symbols-outlined text-[24px]">
                  ${q.userChoice === q.correct ? 'check_circle' : 'cancel'}
                </span>
                <span>
                  ${q.userChoice === q.correct ? 'Correct! High-Yield Concept Mastered' : `Incorrect (Your Selection: Option ${q.userChoice || 'None'} | Key: Option ${q.correct})`}
                </span>
              </div>
              
              <div class="explanation-content text-[13.5px] text-[#242930] leading-relaxed space-y-2">
                ${q.explanation || `<p>${q.rawObjective || ''}</p>`}
              </div>
            </div>
          `;

          questionsWrapper.appendChild(card);
        });

        // Add Next / Prev 20-Question Module Navigation Bar at Bottom
        if (totalModules > 1) {
          const paginationFooter = document.createElement('div');
          paginationFooter.className = "p-6 rounded-3xl neu-extruded border border-white/80 flex flex-wrap items-center justify-between gap-4 mt-6 shadow-sm";
          
          const startQ = currentModuleIndex * PAGE_SIZE + 1;
          const endQ = Math.min((currentModuleIndex + 1) * PAGE_SIZE, totalQuestions);

          paginationFooter.innerHTML = `
            <button id="bottom-prev-btn" class="px-5 py-2.5 rounded-2xl neu-btn text-[12px] font-bold text-[#3e3931] hover:text-primary transition-all flex items-center gap-2 disabled:opacity-30 disabled:pointer-events-none" ${currentModuleIndex === 0 ? 'disabled' : ''}>
              <span class="material-symbols-outlined text-[18px]">arrow_back</span>
              <span>Previous 20 Questions</span>
            </button>
            <div class="font-mono text-[12px] text-[#6b665c] font-semibold text-center">
              Questions <strong class="text-primary">${startQ} - ${endQ}</strong> of <strong>${totalQuestions}</strong>
            </div>
            <button id="bottom-next-btn" class="px-5 py-2.5 rounded-2xl bg-gradient-to-b from-[#22719f] to-[#175275] text-white neu-btn text-[12px] font-bold transition-all flex items-center gap-2 disabled:opacity-30 disabled:pointer-events-none shadow-md" ${currentModuleIndex >= totalModules - 1 ? 'disabled' : ''}>
              <span>Next 20 Questions</span>
              <span class="material-symbols-outlined text-[18px]">arrow_forward</span>
            </button>
          `;

          const bPrev = paginationFooter.querySelector('#bottom-prev-btn');
          const bNext = paginationFooter.querySelector('#bottom-next-btn');

          if (bPrev) {
            bPrev.addEventListener('click', () => {
              if (currentModuleIndex > 0) {
                currentModuleIndex--;
                updateUI();
                scrollQuestionsToTop();
              }
            });
          }
          if (bNext) {
            bNext.addEventListener('click', () => {
              if (currentModuleIndex < totalModules - 1) {
                currentModuleIndex++;
                updateUI();
                scrollQuestionsToTop();
              }
            });
          }

          questionsWrapper.appendChild(paginationFooter);
        }
      }

      // 11. Update Metrics and Chapter Pills
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

        const bCorrect = document.getElementById('banner-stat-correct');
        const bIncorrect = document.getElementById('banner-stat-incorrect');
        const bUnanswered = document.getElementById('banner-stat-unanswered');
        const bFlagged = document.getElementById('banner-stat-flagged');
        if (bCorrect) bCorrect.innerText = curCorrect;
        if (bIncorrect) bIncorrect.innerText = curIncorrect;
        if (bUnanswered) bUnanswered.innerText = (currentFiltered.length - curAnswered);
        if (bFlagged) bFlagged.innerText = curFlagged;

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

        // Render Left Sidebar Chapter Pills
        if (chapterPillGroup) {
          chapterPillGroup.innerHTML = '';

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

      // 12. Full UI Refresh Orchestrator (With 20-Question Module Pagination)
      function updateUI() {
        const filtered = getFilteredQuestions();
        const totalQuestions = filtered.length;
        const totalModules = Math.ceil(totalQuestions / PAGE_SIZE) || 1;

        if (currentModuleIndex >= totalModules) {
          currentModuleIndex = Math.max(0, totalModules - 1);
        }

        // Slice exactly 20 questions for the current module
        const startIdx = currentModuleIndex * PAGE_SIZE;
        const endIdx = Math.min(startIdx + PAGE_SIZE, totalQuestions);
        const current20 = filtered.slice(startIdx, endIdx);

        renderBlockTabs();
        updateModuleControls(totalQuestions);
        renderNavigator(current20);
        renderQuestions(current20, totalQuestions, totalModules);
        updateMetricsAndChapterPills();
      }

      // 13. Module Dropdown & Chevron Listeners
      if (moduleSelectDropdown) {
        moduleSelectDropdown.addEventListener('change', (e) => {
          currentModuleIndex = parseInt(e.target.value, 10);
          updateUI();
          scrollQuestionsToTop();
        });
      }

      if (navPrevSetBtn) {
        navPrevSetBtn.addEventListener('click', () => {
          if (currentModuleIndex > 0) {
            currentModuleIndex--;
            updateUI();
            scrollQuestionsToTop();
          }
        });
      }

      if (navNextSetBtn) {
        navNextSetBtn.addEventListener('click', () => {
          const filtered = getFilteredQuestions();
          const totalModules = Math.ceil(filtered.length / PAGE_SIZE) || 1;
          if (currentModuleIndex < totalModules - 1) {
            currentModuleIndex++;
            updateUI();
            scrollQuestionsToTop();
          }
        });
      }

      // 14. Global Click & Delegation Listener
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

      // 15. Top Toolbar Controls
      const toggleFlaggedTopBtn = document.getElementById('toggle-flagged-only-btn');
      if (toggleFlaggedTopBtn) {
        toggleFlaggedTopBtn.addEventListener('click', () => {
          flaggedOnlyMode = !flaggedOnlyMode;
          currentModuleIndex = 0;
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

      if (searchInput) {
        searchInput.addEventListener('input', (e) => {
          searchQuery = e.target.value.trim();
          currentModuleIndex = 0;
          updateUI();
        });
      }

      // 16. Examination Timer
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
                  alert("Time expired for this examination module!");
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

      // 17. Initial Boot
      initChapterDropdown();
      updateUI();
    })();
'''

    final_html = content[:script_start_idx + 8] + new_script_js + '\n  ' + content[script_end_idx:]

    with open('index.html', 'w', encoding='utf-8') as f:
        f.write(final_html)

    print(f"Successfully generated index.html ({len(final_html)} chars)")

if __name__ == '__main__':
    generate_html()
