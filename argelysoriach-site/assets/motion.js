/* Small, finite enhancements. All source content is visible before this script runs. */
(() => {
  'use strict';
  const preference = matchMedia('(prefers-reduced-motion: reduce)');
  const ease = 'cubic-bezier(.22,1,.36,1)';
  const running = new Set();
  const protectedMark = '.mark,.wordmark,.monolith,.cap,.mark-b,.mark-a,svg';
  function animate(element, frames, duration = 350) {
    if (preference.matches || !element.animate) return;
    const animation = element.animate(frames, {duration, easing:ease});
    running.add(animation);
    animation.finished.catch(() => {}).finally(() => running.delete(animation));
    return animation;
  }
  // Live preference changes finish only our animations, never the site's existing monoliths.
  preference.addEventListener('change', () => {
    if (preference.matches) for (const animation of running) animation.finish();
  });
  document.querySelectorAll('a,button,input,textarea,select').forEach(element => {
    if (!element.closest(protectedMark) && !element.closest('.fold')) element.classList.add('motion-feedback');
  });
  // No pre-hiding, timers, sequential staggers or scroll handlers. Each group animates once.
  const candidates = document.querySelectorAll('.bio,.deploy,.avail,.gate,main>section,main>article>section,.say,.g,.lead');
  const groups = [];
  for (const element of candidates) {
    if (element.closest('.fold,.deck,.dispatch,.view') || element.matches('.fold') || element.querySelector(protectedMark) || element.querySelector('video') || element.closest('.ao-shell')) continue;
    if (groups.some(parent => parent.contains(element))) continue;
    groups.push(element);
  }
  if ('IntersectionObserver' in window) {
    const observer = new IntersectionObserver(entries => {
      for (const entry of entries) {
        if (!entry.isIntersecting) continue;
        observer.unobserve(entry.target);
        if (preference.matches || entry.target.contains(document.activeElement) || (location.hash && entry.target.querySelector(':target')) || entry.target.matches(':target')) continue;
        animate(entry.target,[{opacity:.78,transform:'translateY(8px)'},{opacity:1,transform:'translateY(0)'}]);
      }
    }, {threshold:0,rootMargin:'0px 0px -24px 0px'});
    for (const group of groups) {
      // The opening viewport and deep-linked content are available immediately at rest.
      if (group.getBoundingClientRect().top >= innerHeight) observer.observe(group);
    }
    // Finish any entrance as soon as someone interacts with its content.
    for (const type of ['focusin','pointerdown']) document.addEventListener(type, event => {
      for (const animation of running) if (animation.effect.target.contains(event.target)) animation.finish();
    });
  }
  const links = [...document.querySelectorAll('a.motion-image')];
  if (!links.length || !window.HTMLDialogElement || !HTMLDialogElement.prototype.showModal) return;
  const dialog = document.createElement('dialog');
  dialog.className = 'motion-viewer';
  dialog.setAttribute('aria-label','Larger portfolio image');
  dialog.setAttribute('aria-describedby','motion-viewer-caption');
  // Fixed markup only; all source captions and alt text are assigned via textContent.
  dialog.innerHTML = '<div class="motion-viewer-bar"><button class="motion-viewer-close" type="button" autofocus>Close image</button></div><figure class="motion-viewer-figure"><img class="motion-viewer-img" alt=""><figcaption class="motion-viewer-caption" id="motion-viewer-caption"></figcaption></figure>';
  document.body.append(dialog);
  const picture = dialog.querySelector('img');
  const caption = dialog.querySelector('figcaption');
  const close = dialog.querySelector('button');
  let origin = null;
  let imageFlight = null;
  let generation = 0;
  function dismiss() { if (dialog.open) dialog.close(); }
  close.addEventListener('click',dismiss);
  dialog.addEventListener('click',event => { if (event.target === dialog) dismiss(); });
  // Native dialog supplies background inertness and Escape dismissal; explicit Tab cycling
  // also contains focus on engines with older dialog keyboard behavior.
  dialog.addEventListener('keydown',event => {
    if (event.key === 'Tab') { event.preventDefault(); close.focus(); }
  });
  dialog.addEventListener('close',() => {
    generation++;
    imageFlight?.cancel();
    document.documentElement.classList.remove('motion-viewer-open');
    origin?.focus({preventScroll:true});
    origin = null;
  });
  for (const link of links) link.addEventListener('click',event => {
    // Preserve normal link behavior for new-tab / download / modified activation.
    if (event.button !== 0 || event.metaKey || event.ctrlKey || event.shiftKey || event.altKey) return;
    const source = link.querySelector('img');
    if (!source?.complete || !source.naturalWidth) return;
    event.preventDefault();
    origin = link;
    const from = source.getBoundingClientRect();
    picture.alt = source.alt;
    picture.src = link.href;
    caption.textContent = link.closest('figure').querySelector('figcaption')?.textContent || source.alt;
    dialog.showModal();
    document.documentElement.classList.add('motion-viewer-open');
    close.focus({preventScroll:true});
    const current = ++generation;
    const fly = () => {
      if (!dialog.open || current !== generation) return;
      const to = picture.getBoundingClientRect();
      if (!to.width || !to.height) return;
      // Adapt image-open-tilt to one flat transform flight: no bend, 3D or corner morph.
      imageFlight = animate(picture,[{transform:`translate(${from.left-to.left}px,${from.top-to.top}px) scale(${from.width/to.width},${from.height/to.height})`},{transform:'none'}],340);
    };
    if (picture.complete) fly(); else picture.addEventListener('load',fly,{once:true});
  });
})();
