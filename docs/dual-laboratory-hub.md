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
