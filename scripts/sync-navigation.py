"""Render the shared site navigation into static pages (no runtime fetch required)."""
from pathlib import Path
import re
root = Path(__file__).resolve().parents[1] / 'argelysoriach-site'
template = (root / 'assets/navigation.html').read_text().strip()
for p in root.rglob('*.html'):
    if p.parent.name == 'assets' or p.relative_to(root).as_posix() == 'banana-republic/homepage/index.html':
        continue  # The embedded retail prototype keeps its own product navigation.
    s = p.read_text()
    if p.relative_to(root).as_posix() == 'index.html' and '<!-- Structural homepage -->' in s: continue
    if '<!-- Shared navigation -->' in s:
        s = re.sub(r'\n?<!-- Shared navigation -->.*?<!-- /Shared navigation -->\n*', '', s, flags=re.S)
    else:
        s = re.sub(r'<nav class="site-menu".*?</nav>', '', s, flags=re.S)
        s = re.sub(r'<header class="(?:top mono|label)">.*?</header>', lambda m: m[0] if 'id="ground"' in m[0] else '', s, flags=re.S)
        s = re.sub(r'<script>\s*/\* Site menu\..*?</script>', '', s, flags=re.S)
        if p.parent.name == 'nothing-artist':
            s = re.sub(r'<button class="menu" id="menu-btn".*?</nav>', '', s, flags=re.S)
            s = re.sub(r'<script>\s*\(function \(\) \{\s*var btn = document.getElementById\(\'menu-btn\'\);.*?</script>', '', s, flags=re.S)
        if p.parent.name == 'community-presentation':
            s = re.sub(r'<header class="bar bar--top mono">.*?</header>', '', s, flags=re.S)
    rel = p.relative_to(root).as_posix()
    current = '/' if rel == 'index.html' else '/' + rel.removesuffix('index.html')
    nav = template.replace(f'href="{current}"', f'href="{current}" aria-current="page"')
    if rel == 'index.html':
        nav = nav.replace('href="https://wild-lake.org/"', 'href="https://wildlakestudio.com/"')
        nav = re.sub(r'<div class="ao-shell ao-bar" role="banner">.*?</div>', '<a class="ao-shell ao-icon" href="#ao-menu" aria-label="Open menu" aria-controls="ao-menu" aria-expanded="false" data-ao-open><svg viewBox="0 0 24 24" width="24" height="24" aria-hidden="true"><path d="M2 6h20M2 12h20M2 18h20"/></svg></a>', nav, count=1, flags=re.S)
    s = re.sub(r'(<body\b[^>]*>)', lambda m: m[0]+'\n'+nav+'\n', s, count=1)
    if '/assets/navigation.css' not in s:
        s = s.replace('</head>', '<link rel="stylesheet" href="/assets/navigation.css?v=6">\n<script src="/assets/navigation.js?v=2" defer></script>\n</head>')
    s = re.sub(r'/assets/navigation.css\?v=\d+', '/assets/navigation.css?v=6', s)
    s = re.sub(r'/assets/navigation.js\?v=\d+', '/assets/navigation.js?v=2', s)
    p.write_text(s)
