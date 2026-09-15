(() => {
  'use strict';
  const root = document.documentElement;
  const theme = document.getElementById('theme-toggle');
  function themeLabel() {
    const label = root.dataset.theme === 'dark' ? 'Switch to light mode' : 'Switch to dark mode';
    theme.setAttribute('aria-label', label);
    theme.title = label;
  }
  theme.hidden = false;
  themeLabel();
  theme.addEventListener('click', () => {
    root.dataset.theme = root.dataset.theme === 'dark' ? 'light' : 'dark';
    try { localStorage.setItem('theme', root.dataset.theme); } catch (_) { /* Optional. */ }
    themeLabel();
  });
  const menu = document.getElementById('docs-menu');
  const compact = matchMedia('(max-width: 900px)');
  const syncMenu = () => { menu.open = !compact.matches; };
  syncMenu();
  compact.addEventListener('change', syncMenu);

  // Mark the section at the reading edge, including direct fragment navigation.
  const sections = [...document.querySelectorAll('.on-this-page a[href^="#"]')]
    .map(link => ({link, heading: document.getElementById(decodeURIComponent(link.hash.slice(1)))}))
    .filter(section => section.heading);
  let sectionFrame = 0;
  let activeSection;
  function updateSection() {
    sectionFrame = 0;
    if (!sections.length) return;
    const readingEdge = document.querySelector('.topbar').getBoundingClientRect().bottom + 24;
    let current = sections[0];
    for (const section of sections) {
      if (section.heading.getBoundingClientRect().top <= readingEdge) current = section;
      else break;
    }
    if (window.scrollY > 0 && window.scrollY + window.innerHeight >= root.scrollHeight - 2) {
      current = sections[sections.length - 1];
    }
    if (current === activeSection) return;
    if (activeSection) activeSection.link.removeAttribute('aria-current');
    current.link.setAttribute('aria-current', 'location');
    activeSection = current;
  }
  function scheduleSection() {
    if (!sectionFrame) sectionFrame = requestAnimationFrame(updateSection);
  }
  window.addEventListener('scroll', scheduleSection, {passive: true});
  window.addEventListener('resize', scheduleSection);
  window.addEventListener('hashchange', scheduleSection);
  window.addEventListener('load', scheduleSection);
  if ('ResizeObserver' in window) {
    new ResizeObserver(scheduleSection).observe(document.querySelector('.reading-column'));
  }
  updateSection();

  document.querySelectorAll('article table').forEach(table => {
    const wrapper = document.createElement('div');
    wrapper.className = 'table-scroll';
    wrapper.tabIndex = 0;
    wrapper.setAttribute('role', 'region');
    wrapper.setAttribute('aria-label', 'Scrollable reference table');
    table.before(wrapper);
    wrapper.append(table);
  });
  document.querySelectorAll('pre > code:not(.language-text)').forEach(code => {
    const button = document.createElement('button');
    button.className = 'copy-code';
    button.type = 'button';
    button.textContent = 'Copy';
    button.setAttribute('aria-label', 'Copy code example');
    button.setAttribute('aria-live', 'polite');
    code.parentElement.append(button);
    button.addEventListener('click', async () => {
      try {
        await navigator.clipboard.writeText(code.textContent);
        button.textContent = 'Copied!';
      } catch (_) {
        const range = document.createRange();
        range.selectNodeContents(code);
        const selection = window.getSelection();
        selection.removeAllRanges();
        selection.addRange(range);
        button.textContent = 'Selected — copy manually';
      }
      setTimeout(() => { button.textContent = 'Copy'; }, 2500);
    });
  });

  const search = document.querySelector('.search');
  const input = document.getElementById('docs-search');
  const panel = document.getElementById('search-panel');
  const results = document.getElementById('search-results');
  const status = document.getElementById('search-status');
  if (!Array.isArray(window.DOCS_INDEX)) return;
  search.hidden = false;
  const entries = window.DOCS_INDEX.map(entry => ({...entry,
    haystack: `${entry.title} ${entry.heading} ${entry.text}`.toLocaleLowerCase()
  }));
  function render() {
    const query = input.value.trim().toLocaleLowerCase();
    results.replaceChildren();
    panel.hidden = !query;
    if (!query) return;
    const words = query.split(/\s+/);
    const matches = entries.filter(entry => words.every(word => entry.haystack.includes(word)))
      .map(entry => ({...entry, score: entry.title.toLocaleLowerCase().includes(query) ? 2 :
        entry.heading.toLocaleLowerCase().includes(query) ? 1 : 0}))
      .sort((a, b) => b.score - a.score);
    status.textContent = matches.length ? `${matches.length} results. Showing up to 20.` :
      'No results. Try a keyword such as “functions”, “ganit” or “install”.';
    matches.slice(0, 20).forEach(entry => {
      const item = document.createElement('li');
      const link = document.createElement('a');
      link.href = entry.url;
      const heading = document.createElement('strong');
      heading.textContent = `${entry.title} › ${entry.heading}`;
      const snippet = document.createElement('span');
      const start = Math.max(0, entry.text.toLocaleLowerCase().indexOf(words[0]) - 40);
      snippet.textContent = (start ? '…' : '') + entry.text.slice(start, start + 160) + '…';
      link.append(heading, snippet);
      item.append(link);
      results.append(item);
    });
  }
  input.addEventListener('input', render);
  input.addEventListener('keydown', event => {
    if (event.key === 'ArrowDown' || event.key === 'Enter') {
      const first = results.querySelector('a');
      if (first) { event.preventDefault(); first.focus(); }
    }
  });
  results.addEventListener('keydown', event => {
    if (!['ArrowDown', 'ArrowUp'].includes(event.key)) return;
    const links = [...results.querySelectorAll('a')];
    const index = links.indexOf(document.activeElement);
    if (index < 0) return;
    event.preventDefault();
    const next = index + (event.key === 'ArrowDown' ? 1 : -1);
    if (next < 0) input.focus();
    else links[Math.min(next, links.length - 1)].focus();
  });
  document.addEventListener('keydown', event => {
    if ((event.ctrlKey || event.metaKey) && event.key.toLowerCase() === 'k') {
      event.preventDefault();
      input.focus();
      input.select();
    }
    if (event.key === 'Escape' && search.contains(document.activeElement)) {
      input.value = '';
      render();
      input.focus();
    }
  });
})();
