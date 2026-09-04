/**
 * TrustLayer-AI: Master Report Website Ultra-Premium Interactive Controller
 * High-Performance, Zero-Jank Architecture (60/120fps optimized)
 * Author: K.C (IIIT-Delhi)
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initUnifiedScroll();
  initReadingTime();
  initScrollSpy();
  initLightbox();
  initCommandPalette();
  initCopyButtons();
  initStageFilter();
  initSearch();
  initMobileDrawer();
  renderMathFormulas();
});

/* --------------------------------------------------------------------------
   1. Theme Management (Dark / Light Mode - Default: Light Mode)
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const savedTheme = localStorage.getItem('trustlayer-theme');
  const isDark = savedTheme === 'dark'; // Default to light mode unless explicitly saved as 'dark'

  if (isDark) {
    document.documentElement.classList.add('dark');
    updateThemeIcon(true);
  } else {
    document.documentElement.classList.remove('dark');
    updateThemeIcon(false);
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      document.documentElement.classList.add('theme-switching');
      const isDarkNow = document.documentElement.classList.toggle('dark');
      localStorage.setItem('trustlayer-theme', isDarkNow ? 'dark' : 'light');
      updateThemeIcon(isDarkNow);
      
      // Remove theme-switching in next animation frame to re-enable hover micro-interactions
      window.requestAnimationFrame(() => {
        window.requestAnimationFrame(() => {
          document.documentElement.classList.remove('theme-switching');
        });
      });
    });
  }
}

function updateThemeIcon(isDark) {
  const moonIcon = document.getElementById('theme-icon-moon');
  const sunIcon = document.getElementById('theme-icon-sun');
  if (moonIcon && sunIcon) {
    if (isDark) {
      moonIcon.classList.add('hidden');
      sunIcon.classList.remove('hidden');
    } else {
      moonIcon.classList.remove('hidden');
      sunIcon.classList.add('hidden');
    }
  }
}

/* --------------------------------------------------------------------------
   2. Unified High-Performance Scroll Handler (Progress Bar & Back-to-Top)
   -------------------------------------------------------------------------- */
function initUnifiedScroll() {
  const progressBar = document.getElementById('reading-progress');
  const backToTopBtn = document.getElementById('back-to-top');
  
  let ticking = false;

  function onScroll() {
    if (!ticking) {
      window.requestAnimationFrame(() => {
        const scrollY = window.scrollY || window.pageYOffset;
        
        // 1. Reading Progress
        if (progressBar) {
          const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
          if (totalHeight > 0) {
            const progress = (scrollY / totalHeight) * 100;
            progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
          }
        }

        // 2. Back to Top Visibility
        if (backToTopBtn) {
          if (scrollY > 450) {
            backToTopBtn.classList.remove('opacity-0', 'pointer-events-none');
            backToTopBtn.classList.add('opacity-100', 'pointer-events-auto');
          } else {
            backToTopBtn.classList.add('opacity-0', 'pointer-events-none');
            backToTopBtn.classList.remove('opacity-100', 'pointer-events-auto');
          }
        }

        ticking = false;
      });
      ticking = true;
    }
  }

  window.addEventListener('scroll', onScroll, { passive: true });

  if (backToTopBtn) {
    backToTopBtn.addEventListener('click', () => {
      window.scrollTo({ top: 0, behavior: 'smooth' });
    });
  }
}

/* --------------------------------------------------------------------------
   3. Non-Blocking Reading Time Calculation (Zero Reflow via textContent)
   -------------------------------------------------------------------------- */
function initReadingTime() {
  const mainContent = document.getElementById('main-content');
  const timeBadge = document.getElementById('reading-time-badge');
  if (!mainContent || !timeBadge) return;

  // Use textContent instead of innerText to prevent expensive synchronous layout reflow
  const text = mainContent.textContent || '';
  const wordCount = text.trim().split(/\s+/).length;
  const readTimeMinutes = Math.max(1, Math.ceil(wordCount / 220)); // ~220 WPM
  timeBadge.innerText = `~${readTimeMinutes} min read (${wordCount.toLocaleString()} words)`;
}

/* --------------------------------------------------------------------------
   4. Efficient ScrollSpy & Active Navigation
   -------------------------------------------------------------------------- */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id], div[id^="stage-"], div[id^="sec-"]');
  const navLinks = Array.from(document.querySelectorAll('#sidebar-nav a[href^="#"]'));

  if (sections.length === 0 || navLinks.length === 0) return;

  const linkMap = new Map();
  navLinks.forEach((link) => {
    const href = link.getAttribute('href');
    if (href) linkMap.set(href.substring(1), link);
  });

  const observerOptions = {
    root: null,
    rootMargin: '-10% 0px -65% 0px',
    threshold: 0
  };

  let currentActiveId = null;

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        if (id && id !== currentActiveId) {
          currentActiveId = id;
          
          navLinks.forEach((link) => {
            link.classList.remove('text-blue-600', 'dark:text-blue-400', 'font-semibold', 'bg-blue-50/90', 'dark:bg-blue-900/40', 'rounded-lg');
            link.classList.add('text-slate-600', 'dark:text-slate-400');
          });

          const activeLink = linkMap.get(id);
          if (activeLink) {
            activeLink.classList.add('text-blue-600', 'dark:text-blue-400', 'font-semibold', 'bg-blue-50/90', 'dark:bg-blue-900/40', 'rounded-lg');
            activeLink.classList.remove('text-slate-600', 'dark:text-slate-400');
          }
        }
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));
}

/* --------------------------------------------------------------------------
   5. Interactive Image Lightbox with Zoom & Keyboard Controls
   -------------------------------------------------------------------------- */
function initLightbox() {
  const modal = document.getElementById('lightbox-modal');
  const modalImg = document.getElementById('lightbox-img');
  const modalCaption = document.getElementById('lightbox-caption');
  const closeBtn = document.getElementById('lightbox-close');
  const figureContainers = document.querySelectorAll('.figure-container, .figure-hero');

  if (!modal || !modalImg || !modalCaption) return;

  figureContainers.forEach((container) => {
    container.addEventListener('click', () => {
      const img = container.querySelector('img');
      const caption = container.querySelector('.figure-caption');
      if (img) {
        modalImg.src = img.src;
        modalImg.alt = img.alt || 'Figure Image';
        modalCaption.innerHTML = caption ? caption.innerHTML : '';
        modal.classList.add('active');
        document.body.style.overflow = 'hidden';
      }
    });
  });

  const closeModal = () => {
    modal.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (closeBtn) closeBtn.addEventListener('click', closeModal);
  modal.addEventListener('click', (e) => {
    if (e.target === modal || e.target.classList.contains('lightbox-backdrop')) {
      closeModal();
    }
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && modal.classList.contains('active')) {
      closeModal();
    }
  });
}

/* --------------------------------------------------------------------------
   6. Command Palette (Ctrl+K / ⌘K) with Keyboard Navigation
   -------------------------------------------------------------------------- */
function initCommandPalette() {
  const palette = document.getElementById('command-palette');
  const searchInput = document.getElementById('palette-search');
  const triggerBtn = document.getElementById('palette-trigger');
  const closeBtn = document.getElementById('palette-close');
  const resultsContainer = document.getElementById('palette-results');

  if (!palette || !searchInput || !resultsContainer) return;

  const quickLinks = [
    { title: 'Chapter 1: Executive Summary & Abstract', href: '#ch-executive-summary', category: 'Chapter' },
    { title: 'Chapter 2: Problem Statement & RQs', href: '#ch-problem-statement', category: 'Chapter' },
    { title: 'Chapter 3: Theoretical Foundations & Math', href: '#ch-theory', category: 'Chapter' },
    { title: 'Chapter 4: Master Development Journey (Stages 01–18)', href: '#ch-dev-journey', category: 'Chapter' },
    { title: 'Chapter 5: System Architecture & Pivots', href: '#ch-architecture', category: 'Chapter' },
    { title: 'Chapter 6: Data Lineage & Database Schema', href: '#ch-data-lineage', category: 'Chapter' },
    { title: 'Chapter 7: Experimental Evaluations & Evidence', href: '#ch-experiments', category: 'Chapter' },
    { title: 'Chapter 8: Engineering Contributions & Status', href: '#ch-contributions', category: 'Chapter' },
    { title: 'Chapter 9: Complete Master File Inventory', href: '#ch-file-inventory', category: 'Chapter' },
    { title: 'Chapter 10: References', href: '#ch-references', category: 'Chapter' },
    { title: 'Chapter 11: Complete System Architecture & Blueprint', href: '#ch-complete-arch', category: 'Chapter' },
    { title: 'Figure 11.1: Complete System Architecture (Complete_Arch.png)', href: '#ch-complete-arch', category: 'Architecture' },
    { title: 'Stage 01: Raw Ingestion (Google Places)', href: '#stage01', category: 'Stage' },
    { title: 'Stage 03: DistilBERT NLP & 5D ABSA', href: '#stage03', category: 'Stage' },
    { title: 'Stage 07: Diagnostic Recommender NO-GO', href: '#stage07', category: 'Stage' },
    { title: 'Stage 08: Reciprocal Rank Fusion (RRF k=60) GO', href: '#stage08', category: 'Stage' },
    { title: 'Stage 09: Analytical Explainer (<5ms Latency)', href: '#stage09', category: 'Stage' },
    { title: 'Stage 10: RAG Hybrid Retrieval (7,910 Chunks)', href: '#stage10', category: 'Stage' },
    { title: 'Stage 11: Grounding & Hallucination Interception', href: '#stage11', category: 'Stage' },
    { title: 'Stage 14: PostgreSQL 17 + pgvector (1.0000 Parity)', href: '#stage14', category: 'Stage' },
    { title: 'Stage 17: Master CLI Orchestrator Engine', href: '#stage17', category: 'Stage' },
    { title: 'Stage 18: Live Terminal Progress & 109/109 Tests', href: '#stage18', category: 'Stage' },
    { title: 'Formula: Reciprocal Rank Fusion (RRF)', href: '#sec-rrf', category: 'Formula' },
    { title: 'Formula: Composite Gaussian Trust Score', href: '#sec-trust-score', category: 'Formula' },
    { title: 'Schema: PostgreSQL 17.6 Relational & pgvector DDL', href: '#sec-pg-schema', category: 'Schema' },
    { title: 'Section 7.8: Live Production Query & Response Explorer (91 Benchmarks)', href: '#sec-query-explorer', category: 'Benchmark' },
    { title: 'Table: Master 109/109 Automated Tests Breakdown', href: '#sec-test-suite', category: 'Benchmark' },
    { title: 'Table: 10 Empirical Experiments & Interventions', href: '#sec-ten-experiments', category: 'Benchmark' }
  ];

  let selectedIndex = -1;

  const renderResults = (query = '') => {
    resultsContainer.innerHTML = '';
    const cleanQuery = query.toLowerCase().trim();
    const filtered = quickLinks.filter(item => 
      item.title.toLowerCase().includes(cleanQuery) || 
      item.category.toLowerCase().includes(cleanQuery)
    );

    selectedIndex = -1;

    if (filtered.length === 0) {
      resultsContainer.innerHTML = '<div class="p-4 text-center text-xs text-slate-400">No matching sections found.</div>';
      return;
    }

    filtered.forEach((item, idx) => {
      const a = document.createElement('a');
      a.href = item.href;
      a.className = 'palette-item flex items-center justify-between p-3 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/30 text-slate-700 dark:text-slate-200 transition-colors text-xs';
      a.setAttribute('data-index', idx);
      a.innerHTML = `
        <div class="flex items-center gap-2">
          <span class="w-1.5 h-1.5 rounded-full bg-blue-600"></span>
          <span class="font-medium">${item.title}</span>
        </div>
        <span class="px-2 py-0.5 rounded text-[10px] font-mono uppercase bg-slate-100 dark:bg-slate-800 text-slate-500">${item.category}</span>
      `;
      a.addEventListener('click', () => {
        closePalette();
      });
      resultsContainer.appendChild(a);
    });
  };

  const openPalette = () => {
    palette.classList.add('active');
    searchInput.value = '';
    renderResults();
    setTimeout(() => searchInput.focus(), 50);
  };

  const closePalette = () => {
    palette.classList.remove('active');
  };

  if (triggerBtn) triggerBtn.addEventListener('click', openPalette);
  if (closeBtn) closeBtn.addEventListener('click', closePalette);

  palette.addEventListener('click', (e) => {
    if (e.target === palette) closePalette();
  });

  searchInput.addEventListener('input', (e) => {
    renderResults(e.target.value);
  });

  document.addEventListener('keydown', (e) => {
    if ((e.ctrlKey || e.metaKey) && e.key.toLowerCase() === 'k') {
      e.preventDefault();
      if (palette.classList.contains('active')) {
        closePalette();
      } else {
        openPalette();
      }
    }
    if (e.key === 'Escape' && palette.classList.contains('active')) {
      closePalette();
    }
  });
}

/* --------------------------------------------------------------------------
   7. Copy Code, Terminal & LaTeX Blocks (Event Delegation & Feedback)
   -------------------------------------------------------------------------- */
function initCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre, .terminal-block');

  codeBlocks.forEach((block) => {
    if (block.querySelector('.copy-btn')) return;

    block.style.position = 'relative';
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.setAttribute('aria-label', 'Copy code to clipboard');
    btn.innerHTML = `
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
      </svg>
      <span>Copy</span>
    `;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const textToCopy = block.textContent.replace(/Copy/g, '').replace(/Copied!/g, '').trim();
      navigator.clipboard.writeText(textToCopy).then(() => {
        btn.innerHTML = `
          <svg class="w-3.5 h-3.5 text-emerald-400" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"></path>
          </svg>
          <span class="text-emerald-400">Copied!</span>
        `;
        setTimeout(() => {
          btn.innerHTML = `
            <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
              <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
            </svg>
            <span>Copy</span>
          `;
        }, 2000);
      });
    });

    block.appendChild(btn);
  });
}

/* --------------------------------------------------------------------------
   8. Stage Timeline Filtering
   -------------------------------------------------------------------------- */
function initStageFilter() {
  const filterBtns = document.querySelectorAll('.stage-filter-btn');
  const stageCards = document.querySelectorAll('.stage-card');

  if (filterBtns.length === 0 || stageCards.length === 0) return;

  filterBtns.forEach((btn) => {
    btn.addEventListener('click', () => {
      const filter = btn.getAttribute('data-filter');

      filterBtns.forEach((b) => {
        b.classList.remove('bg-blue-600', 'text-white', 'shadow-md');
        b.classList.add('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300');
      });

      btn.classList.add('bg-blue-600', 'text-white', 'shadow-md');
      btn.classList.remove('bg-slate-100', 'dark:bg-slate-800', 'text-slate-700', 'dark:text-slate-300');

      stageCards.forEach((card) => {
        const category = card.getAttribute('data-category') || '';
        if (filter === 'all' || category.includes(filter)) {
          card.style.display = 'block';
        } else {
          card.style.display = 'none';
        }
      });
    });
  });
}

/* --------------------------------------------------------------------------
   9. In-Page High-Speed Filter / Search (Debounced + Zero Reflow)
   -------------------------------------------------------------------------- */
function initSearch() {
  const searchInput = document.getElementById('report-search');
  if (!searchInput) return;

  let debounceTimer;

  searchInput.addEventListener('input', (e) => {
    clearTimeout(debounceTimer);
    debounceTimer = setTimeout(() => {
      const query = e.target.value.toLowerCase().trim();
      const searchableElements = document.querySelectorAll('#main-content section, #main-content .stage-card');

      if (query.length === 0) {
        searchableElements.forEach((el) => (el.style.opacity = '1'));
        return;
      }

      searchableElements.forEach((el) => {
        const text = (el.textContent || '').toLowerCase();
        if (text.includes(query)) {
          el.style.opacity = '1';
        } else {
          el.style.opacity = '0.35';
        }
      });
    }, 120);
  });
}

/* --------------------------------------------------------------------------
   10. KaTeX Mathematical Typesetting
   -------------------------------------------------------------------------- */
function renderMathFormulas() {
  const tryRender = () => {
    if (typeof renderMathInElement === 'function') {
      try {
        renderMathInElement(document.body, {
          delimiters: [
            { left: '$$', right: '$$', display: true },
            { left: '\\[', right: '\\]', display: true },
            { left: '$', right: '$', display: false },
            { left: '\\(', right: '\\)', display: false }
          ],
          throwOnError: false,
          ignoredTags: ['script', 'noscript', 'style', 'textarea', 'pre', 'code', 'option', 'svg']
        });
        return true;
      } catch (err) {
        console.warn('KaTeX render warning:', err);
      }
    }
    return false;
  };

  if (!tryRender()) {
    let attempts = 0;
    const interval = setInterval(() => {
      attempts++;
      if (tryRender() || attempts > 30) {
        clearInterval(interval);
      }
    }, 100);
  }
}
window.renderMathFormulas = renderMathFormulas;
window.addEventListener('load', renderMathFormulas);

/* --------------------------------------------------------------------------
   11. Mobile Table of Contents Drawer
   -------------------------------------------------------------------------- */
function initMobileDrawer() {
  const drawer = document.getElementById('mobile-toc-drawer');
  const openBtn = document.getElementById('mobile-menu-btn');
  const toggleBtn = document.getElementById('mobile-toc-toggle');
  const closeBtn = document.getElementById('mobile-toc-close');
  const navLinks = document.querySelectorAll('.mobile-nav-link');

  if (!drawer) return;

  const openDrawer = () => {
    drawer.classList.add('active');
    document.body.style.overflow = 'hidden';
  };

  const closeDrawer = () => {
    drawer.classList.remove('active');
    document.body.style.overflow = '';
  };

  if (openBtn) openBtn.addEventListener('click', openDrawer);
  if (toggleBtn) toggleBtn.addEventListener('click', openDrawer);
  if (closeBtn) closeBtn.addEventListener('click', closeDrawer);

  drawer.addEventListener('click', (e) => {
    if (e.target === drawer) {
      closeDrawer();
    }
  });

  navLinks.forEach((link) => {
    link.addEventListener('click', () => {
      closeDrawer();
    });
  });

  document.addEventListener('keydown', (e) => {
    if (e.key === 'Escape' && drawer.classList.contains('active')) {
      closeDrawer();
    }
  });
}
