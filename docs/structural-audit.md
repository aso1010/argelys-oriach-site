# Structural audit and implementation

## Current hierarchy

1. Systems architecture — Seven Eighty Three and Universe API.
2. Talent infrastructure — Wild-Lake / Wild Lake Studio.
3. Art and writing — Portfolio and This Is Not a Love Story (Yankees).
4. Background — Biography and CV.
5. Contact — Email and the existing detailed intake form.
6. Historical material — One collapsed archive index.

## Controlled demolition

- Replaced the homepage's duplicate venture lists, long positioning copy, animation runtime, image-letter assembly, and homepage-only email form with the approved static page. The detailed `/intake/` form remains.
- Replaced standalone ethos navigation with an archive entry. Earlier practice definitions and roles remain historical records rather than current positioning.
- Removed archival pages from the current sitemap and current work graph. Added visible archive status and `noindex, follow` metadata/headers.
- Removed the old first-person biography from `llms.txt` and the replicated schema hub. Canonical JSON records describe the current person, services, works, and website.
- Reused Person and organization IDs. Seven Eighty Three remains the story publisher. The story domain identifies the work.
- Updated current CV service descriptions, role line, Wild-Lake URL, and coaching terminology.
- Replaced Universe API's philosophical positioning and indexing-control language with a framework description and operational mechanics.
- Removed group entrance animations, menu entrance animations, control motion and image-flight effects. Portfolio image inspection uses native dialog behavior.
- Replaced navigation-group headings with non-heading labels so a hidden menu does not precede the page H1 with H2 elements.
- Preserved creative works, artistic media, legal disclaimers, education, employment dates and publisher attribution.

Removed the 20 unreferenced raster assets used by the replaced homepage letter assembly. Historical art/media and social cards remain.

## Slug ledger

| Existing route | Treatment |
| --- | --- |
| `/` | Rebuilt current-practice homepage |
| `/portfolio/` | Current art and project evidence |
| `/universe-api/` | Current systems framework; copy reduced |
| `/cv/` | Current background; service copy updated |
| `/intake/` | Existing detailed form retained |
| `/beauty-salon/` | Literary work retained |
| `/banana-republic/` | Art/design case study retained |
| `/banana-republic/homepage/` | Embedded retail prototype retained |
| `/ethos/` | Historical archive; noindex, follow |
| `/nothing-artist/` | Historical archive; noindex, follow |
| `/matter-and-body-architecture/` | Historical archive; noindex, follow |
| `/mad-matter/` | Historical artist statement; noindex, follow |
| `/sovereignty/` | Historical statement; noindex, follow |
| `/catalogue-001/` | Historical catalogue; noindex, follow |
| `/catalogue-002/` | Historical specification; noindex, follow |
| `/community-presentation/` | Historical proposal; noindex, follow |
| `/this-is-not-a-love-story-yankees/` | Retained reading mirror; canonical publication is `https://thisisnotalovestory.net/`; noindex, follow |
| `/schema/` | Current record index |
| `/privacy/`, `/terms/` | Legal pages retained |

Preserved homepage anchor destinations: `#headline`, `#main`, `#bio`, `#intake`, `#writing`, `#wild-lake`, `#deployments`, `#availability`.

Run `python scripts/sync-navigation.py` and `python scripts/sync-footer.py` for secondary-page chrome. Both preserve the standalone structural homepage.
