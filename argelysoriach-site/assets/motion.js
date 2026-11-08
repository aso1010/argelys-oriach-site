/* Native image inspection; source links remain usable without JavaScript. */
(() => {
  const links = [...document.querySelectorAll('a.motion-image')];
  if (!links.length || !window.HTMLDialogElement || !HTMLDialogElement.prototype.showModal) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'motion-viewer';
  dialog.setAttribute('aria-label','Portfolio image');
  dialog.innerHTML = '<div class="motion-viewer-bar"><button class="motion-viewer-close" type="button" autofocus>Close image</button></div><figure class="motion-viewer-figure"><img class="motion-viewer-img" alt=""><figcaption class="motion-viewer-caption"></figcaption></figure>';
  document.body.append(dialog);
  const close = dialog.querySelector('button');
  let origin;
  close.addEventListener('click', () => dialog.close());
  dialog.addEventListener('click', event => { if (event.target === dialog) dialog.close(); });
  dialog.addEventListener('keydown', event => { if (event.key === 'Tab') { event.preventDefault(); close.focus(); } });
  dialog.addEventListener('close', () => { document.documentElement.classList.remove('motion-viewer-open'); origin?.focus({preventScroll:true}); });
  for (const link of links) link.addEventListener('click', event => {
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    event.preventDefault();
    origin = link;
    dialog.querySelector('img').src = link.href;
    dialog.querySelector('img').alt = link.querySelector('img')?.alt || '';
    dialog.querySelector('figcaption').textContent = link.closest('figure')?.querySelector('figcaption')?.textContent || '';
    dialog.showModal();
    document.documentElement.classList.add('motion-viewer-open');
    close.focus({preventScroll:true});
  });
})();
