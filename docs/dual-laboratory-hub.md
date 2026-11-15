# Dual-laboratory hub

`argelysoriach-site/index.html` is a self-contained white landing page with embedded Archivo, inline CSS, JSON-LD, and a structural figure-eight SVG. It has no executable JavaScript or runtime asset dependencies. The social-preview image remains a metadata reference.

The previous homepage is preserved at `/biography/`, including its monolith, animation scripts, Writing features, and intake form. Relative font and media URLs were made absolute for the new route. The canonical and Open Graph page URLs now identify `/biography/`.

Internal biography anchor links and llms.txt point to `/biography/`. Old externally bookmarked root fragments still open the root hub; fragment redirects would require client-side code, which is intentionally absent from this hub. Biography links are present in the header and footer.

`scripts/sync-profile.py` reads the biography from the new route. Shared navigation and footer generators continue to skip the standalone root page.

The two organization IDs and Person ID are retained. Wild Lake Studio retains Seven Eighty Three as its parentOrganization. The homepage Profile reference remains `/about/`, the extended first-party biography.
