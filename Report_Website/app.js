/**
 * TrustLayer-AI: Master Report Website Ultra-Premium Interactive Controller
 * Author: K.C (IIIT-Delhi)
 */

document.addEventListener('DOMContentLoaded', () => {
  initTheme();
  initReadingProgress();
  initReadingTime();
  initScrollSpy();
  initLightbox();
  initCommandPalette();
  initCopyButtons();
  initStageFilter();
  initSearch();
  initBackToTop();
  initMobileDrawer();
  initPinchZoomPrevention();
  renderMathFormulas();
});

/* --------------------------------------------------------------------------
   1. Theme Management (Dark / Light Mode)
   -------------------------------------------------------------------------- */
function initTheme() {
  const themeToggleBtn = document.getElementById('theme-toggle');
  const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
  const savedTheme = localStorage.getItem('trustlayer-theme');

  if (savedTheme === 'dark' || (!savedTheme && prefersDark)) {
    document.documentElement.classList.add('dark');
    updateThemeIcon(true);
  } else {
    document.documentElement.classList.remove('dark');
    updateThemeIcon(false);
  }

  if (themeToggleBtn) {
    themeToggleBtn.addEventListener('click', () => {
      const isDark = document.documentElement.classList.toggle('dark');
      localStorage.setItem('trustlayer-theme', isDark ? 'dark' : 'light');
      updateThemeIcon(isDark);
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
   2. Reading Progress Bar & Reading Time Estimation
   -------------------------------------------------------------------------- */
function initReadingProgress() {
  const progressBar = document.getElementById('reading-progress');
  if (!progressBar) return;

  window.addEventListener('scroll', () => {
    const totalHeight = document.documentElement.scrollHeight - window.innerHeight;
    if (totalHeight > 0) {
      const progress = (window.scrollY / totalHeight) * 100;
      progressBar.style.width = `${Math.min(100, Math.max(0, progress))}%`;
    }
  }, { passive: true });
}

function initReadingTime() {
  const mainContent = document.getElementById('main-content');
  const timeBadge = document.getElementById('reading-time-badge');
  if (!mainContent || !timeBadge) return;

  const text = mainContent.innerText || '';
  const wordCount = text.split(/\s+/).length;
  const readTimeMinutes = Math.ceil(wordCount / 220); // standard reading speed
  timeBadge.innerText = `~${readTimeMinutes} min read (${wordCount.toLocaleString()} words)`;
}

/* --------------------------------------------------------------------------
   3. ScrollSpy & Active Navigation
   -------------------------------------------------------------------------- */
function initScrollSpy() {
  const sections = document.querySelectorAll('section[id], div[id^="stage-"], div[id^="sec-"]');
  const navLinks = document.querySelectorAll('#sidebar-nav a[href^="#"], #right-telemetry a[href^="#"]');

  if (sections.length === 0 || navLinks.length === 0) return;

  const observerOptions = {
    root: null,
    rootMargin: '-15% 0px -70% 0px',
    threshold: 0
  };

  const observer = new IntersectionObserver((entries) => {
    entries.forEach((entry) => {
      if (entry.isIntersecting) {
        const id = entry.target.getAttribute('id');
        navLinks.forEach((link) => {
          if (link.getAttribute('href') === `#${id}`) {
            link.classList.add('text-blue-600', 'dark:text-blue-400', 'font-semibold', 'bg-blue-50/90', 'dark:bg-blue-900/40', 'rounded-lg');
            link.classList.remove('text-slate-600', 'dark:text-slate-400');
          } else {
            link.classList.remove('text-blue-600', 'dark:text-blue-400', 'font-semibold', 'bg-blue-50/90', 'dark:bg-blue-900/40', 'rounded-lg');
            link.classList.add('text-slate-600', 'dark:text-slate-400');
          }
        });
      }
    });
  }, observerOptions);

  sections.forEach((section) => observer.observe(section));
}

/* --------------------------------------------------------------------------
   4. Interactive Image Lightbox with Zoom & Keyboard Controls
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
   5. Command Palette (Ctrl+K / ⌘K)
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
    { title: 'Table: Master 109/109 Automated Tests Breakdown', href: '#sec-test-suite', category: 'Benchmark' },
    { title: 'Table: 10 Empirical Experiments & Interventions', href: '#sec-ten-experiments', category: 'Benchmark' }
  ];

  const renderResults = (query = '') => {
    resultsContainer.innerHTML = '';
    const filtered = quickLinks.filter(item => 
      item.title.toLowerCase().includes(query.toLowerCase()) || 
      item.category.toLowerCase().includes(query.toLowerCase())
    );

    if (filtered.length === 0) {
      resultsContainer.innerHTML = '<div class="p-4 text-center text-xs text-slate-400">No matching sections found.</div>';
      return;
    }

    filtered.forEach(item => {
      const a = document.createElement('a');
      a.href = item.href;
      a.className = 'flex items-center justify-between p-3 rounded-lg hover:bg-blue-50 dark:hover:bg-blue-900/30 text-slate-700 dark:text-slate-200 transition-colors text-xs';
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
    if ((e.ctrlKey || e.metaKey) && e.key === 'k') {
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
   6. Copy Code, Terminal & LaTeX Blocks
   -------------------------------------------------------------------------- */
function initCopyButtons() {
  const codeBlocks = document.querySelectorAll('pre, .terminal-block');

  codeBlocks.forEach((block) => {
    if (block.querySelector('.copy-btn')) return;

    block.style.position = 'relative';
    const btn = document.createElement('button');
    btn.className = 'copy-btn';
    btn.innerHTML = `
      <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8 16H6a2 2 0 01-2-2V6a2 2 0 012-2h8a2 2 0 012 2v2m-6 12h8a2 2 0 002-2v-8a2 2 0 00-2-2h-8a2 2 0 00-2 2v8a2 2 0 002 2z"></path>
      </svg>
      <span>Copy</span>
    `;

    btn.addEventListener('click', (e) => {
      e.stopPropagation();
      const textToCopy = block.innerText.replace(/Copy/g, '').trim();
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
   7. Stage Timeline Filtering
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
   8. In-Page Fast Filter / Search
   -------------------------------------------------------------------------- */
function initSearch() {
  const searchInput = document.getElementById('report-search');
  if (!searchInput) return;

  searchInput.addEventListener('input', (e) => {
    const query = e.target.value.toLowerCase().trim();
    const searchableElements = document.querySelectorAll('#main-content section, #main-content .stage-card');

    if (query.length === 0) {
      searchableElements.forEach((el) => (el.style.opacity = '1'));
      return;
    }

    searchableElements.forEach((el) => {
      const text = el.innerText.toLowerCase();
      if (text.includes(query)) {
        el.style.opacity = '1';
      } else {
        el.style.opacity = '0.35';
      }
    });
  });
}

/* --------------------------------------------------------------------------
   9. Back to Top Button
   -------------------------------------------------------------------------- */
function initBackToTop() {
  const backToTopBtn = document.getElementById('back-to-top');
  if (!backToTopBtn) return;

  window.addEventListener('scroll', () => {
    if (window.scrollY > 450) {
      backToTopBtn.classList.remove('opacity-0', 'pointer-events-none');
      backToTopBtn.classList.add('opacity-100', 'pointer-events-auto');
    } else {
      backToTopBtn.classList.add('opacity-0', 'pointer-events-none');
      backToTopBtn.classList.remove('opacity-100', 'pointer-events-auto');
    }
  }, { passive: true });

  backToTopBtn.addEventListener('click', () => {
    window.scrollTo({ top: 0, behavior: 'smooth' });
  });
}

/* --------------------------------------------------------------------------
   10. KaTeX Automatic Formula Rendering
   -------------------------------------------------------------------------- */
function renderMathFormulas() {
  if (typeof renderMathInElement === 'function') {
    renderMathInElement(document.body, {
      delimiters: [
        { left: '$$', right: '$$', display: true },
        { left: '\\[', right: '\\]', display: true },
        { left: '$', right: '$', display: false },
        { left: '\\(', right: '\\)', display: false }
      ],
      throwOnError: false
    });
  }
}

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

/* --------------------------------------------------------------------------
   12. Pinch-Zoom & Mobile Multi-Touch Lock
   -------------------------------------------------------------------------- */
function initPinchZoomPrevention() {
  // Prevent gesture zoom on iOS Safari
  document.addEventListener('gesturestart', (e) => e.preventDefault());
  document.addEventListener('gesturechange', (e) => e.preventDefault());
  document.addEventListener('gestureend', (e) => e.preventDefault());

  // Prevent multi-touch pinch zooming
  document.addEventListener('touchmove', (e) => {
    if (e.touches.length > 1) {
      e.preventDefault();
    }
  }, { passive: false });
}


