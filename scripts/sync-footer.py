"""Render the shared brutalist site footer, preserving editorial footers and credits."""
from pathlib import Path
import re
root=Path(__file__).resolve().parents[1]/'argelysoriach-site'
template=(root/'assets/footer.html').read_text().strip()
credits={
 'portfolio/index.html':'Set in Archivo · Direction, writing and design: Argelys Samuel Oriach · Built with Claude',
 'banana-republic/index.html':'Set in Archivo · Direction, writing and design: Argelys Samuel Oriach · Built with Claude',
 'catalogue-001/index.html':'Catalogue 001 · October 2026 · Set in Archivo and JetBrains Mono · Built with Claude · With <a href="https://wild-lake.org/">Wild-Lake</a>, the artists agency',
 'catalogue-002/index.html':'<a href="/catalogue-001/">Catalogue 001</a> · Catalogue 002 · October 2026 · Set in Archivo and JetBrains Mono · Built with Claude',
 'this-is-not-a-love-story-yankees/index.html':'Universe API · Seven Eighty Three · <a href="#top">Return to threshold</a>',
}
for p in root.rglob('*.html'):
 rel=p.relative_to(root).as_posix()
 if p.parent.name=='assets' or rel in ['banana-republic/homepage/index.html','community-presentation/index.html']:continue
 s=p.read_text()
 footer=template.replace('  <!-- Page credits -->','<p class="ao-footer-notes">'+credits[rel]+'</p>' if rel in credits else '')
 current='/'+rel.removesuffix('index.html')
 footer=footer.replace(f'href="{current}"',f'href="{current}" aria-current="page"')
 if '<!-- Shared footer -->' in s:
  s=re.sub(r'<!-- Shared footer -->.*?<!-- /Shared footer -->',lambda _:footer,s,flags=re.S)
 else:
  def replace(m):
   # Article colophons and reading controls remain part of the document itself.
   if re.search(r'class="(?:colophon|reading-end)"',m[0]):return m[0]
   return footer
  s,count=re.subn(r'<footer\b.*?</footer>',replace,s,flags=re.S)
  if '<!-- Shared footer -->' not in s:s=s.replace('</main>','</main>\n'+footer,1)
 p.write_text(s)
