// Apply the homepage's saved theme before the first paint; storage is optional.
(() => {
  let theme;
  try { theme = localStorage.getItem('theme'); } catch (_) { /* Storage may be blocked. */ }
  if (theme !== 'dark' && theme !== 'light') {
    theme = matchMedia('(prefers-color-scheme: dark)').matches ? 'dark' : 'light';
  }
  document.documentElement.dataset.theme = theme;
})();
