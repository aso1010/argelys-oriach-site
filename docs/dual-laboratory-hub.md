# Dual-laboratory hub

`argelysoriach-site/index.html` is a self-contained white landing page with embedded Archivo, inline CSS, JSON-LD, and a structural figure-eight SVG. The white hub has no external JavaScript dependencies. A small native inline controller loads the preserved biography in a same-origin frame as its reveal enters the viewport, and expands that frame to its document height to keep scrolling in the main page. The social-preview image remains a metadata reference.

The previous homepage is preserved at `/biography/`, including its monolith, animation scripts, Writing features, and intake form. Relative font and media URLs were made absolute for the new route. The canonical and Open Graph page URLs now identify `/biography/`.

Internal biography anchor links and llms.txt point to `/biography/`. Old externally bookmarked root fragments still open the root hub; fragment redirects would require client-side code, which is intentionally absent from this hub. Biography links are present in the header and footer.

`scripts/sync-profile.py` reads the biography from the new route. Shared navigation and footer generators continue to skip the standalone root page.

The two organization IDs and Person ID are retained. Wild Lake Studio retains Seven Eighty Three as its parentOrganization. The homepage Profile reference remains `/about/`, the extended first-party biography.

## Scroll descent

The white hub uses a regular Archivo name heading. After the hub, a full visible viewport of black space precedes the preserved biography. IntersectionObserver starts loading `/biography/?embedded=1` only as the frame enters view. The existing monolith animation then runs on document load, once. Direct `/biography/` visits retain their original behavior.

Embedded mode uses the parent viewport height for the opening composition and void spacing. This prevents feedback between iframe document height and viewport units. ResizeObserver reports body height through messages validated against origin and source; no inner scrollbar or scroll hijacking is added. Links leave the frame normally, while local anchor messages update the parent hash and scroll to the corresponding position.

Reduced motion shows the settled monolith. Live reduced-motion changes suppress letter transforms. If JavaScript is disabled, a visible link opens the complete biography directly.

The combined page uses one white footer after the black biography. The embedded biography hides its local menu and footer; direct `/biography/` visits retain both. The final footer includes a direct Biography link for no-JavaScript access.

## Letters carry the descent

The original 19-letter drop trajectories now run in the parent page over the white/black boundary. The monolith uses difference blending so white letters display as black against the white hub and white against the black descent. Its once-only observer starts as the first sliver of the black section enters view. The biography frame preloads at the boundary; its own opening monolith is hidden in embedded mode to avoid a duplicate. Direct biography visits retain the original opening and animation. The black section keeps the original monospaced caption. Reduced motion shows the settled name and live preference changes suppress transformations.

## Current sequence

The opening screen is the falling white name monolith on black. Desktop rows fill the viewport; phone rows retain natural proportions at nearly full width. The white Two of Pentacles hub follows, without repeating the name as a visual heading. The black biography follows the white hub, then the Wild-Lake featured venture, intake, and one white footer. The original scroll-boundary fall was replaced by the same once-only drop starting immediately on initial load. The shared menu remains available throughout. The embedded biography's own monolith, menu, and footer remain hidden; the direct biography route remains usable.

## Visual restoration with nonvisual cleanup

The full-screen falling monolith, white Two of Pentacles hub, black biography, featured venture, white intake, single menu, and white footer are restored to the pre-demolition design. The letter assets and animation scripts remain required by that design.

Canonical Wild Lake Studio entity IDs and current organization descriptions are retained in JSON-LD and schema JSON. Third-party analytics and captured challenge scripts are removed without changing visible markup or styles. The sync helper preserves the original visible biography while updating machine-readable data.
