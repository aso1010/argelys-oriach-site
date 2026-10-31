(() => {
  const menu = document.getElementById('ao-menu');
  if (!menu) return;
  const opener = document.querySelector('[data-ao-open]');
  let back = null;
  const previousInert = new Map();
  function set(open) {
    menu.classList.toggle('is-open', open);
    document.documentElement.classList.toggle('ao-menu-open', open);
    opener.setAttribute('aria-expanded', String(open));
    if (open) {
      back = document.activeElement;
      for (const el of document.body.children) {
        if (el === menu || el.tagName === 'SCRIPT') continue;
        previousInert.set(el, el.inert);
        el.inert = true;
      }
      menu.querySelector('[data-ao-close]').focus();
    } else {
      for (const [el, inert] of previousInert) el.inert = inert;
      previousInert.clear();
      if (location.hash === '#ao-menu') history.replaceState(null, '', location.pathname + location.search);
      back?.focus();
      back = null;
    }
  }
  opener.addEventListener('click', e => { e.preventDefault(); set(true); });
  menu.addEventListener('click', e => {
    const a = e.target.closest('a');
    if (!a) return;
    if (a.hasAttribute('data-ao-close')) { e.preventDefault(); set(false); }
    else set(false);
  });
  document.addEventListener('keydown', e => {
    if (!menu.classList.contains('is-open')) return;
    if (e.key === 'Escape') { e.preventDefault(); set(false); }
    if (e.key !== 'Tab') return;
    const links = [...menu.querySelectorAll('a[href]')];
    const first = links[0], last = links.at(-1);
    if (e.shiftKey && document.activeElement === first) { e.preventDefault(); last.focus(); }
    else if (!e.shiftKey && document.activeElement === last) { e.preventDefault(); first.focus(); }
  });
  if (location.hash === '#ao-menu') set(true);
})();
