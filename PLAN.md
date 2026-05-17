# Review Affiliate WP Jtec – Discovery Plan (Step 0)

## Step 1 – Confirm MVP Scope
Before scaffolding code, define the **first shippable version (MVP)** to avoid overengineering.

### Proposed MVP modules
- Core bootstrap (main plugin file, activation/deactivation hooks, loader).
- Data model (CPT + Meta for products, comparisons, stores/offers).
- Admin UI (Product fields + basic settings page).
- Frontend SSR shortcodes:
  - `[review_card id="123"]`
  - `[compare ids="12,15,18"]`
  - `[top_products category="slug"]`
- Basic schema output (Product, Review/AggregateRating, Offer, FAQPage).
- Affiliate link cloaker + click tracking table.
- Conditional assets loading.

## Step 2 – Data Strategy (recommended)
- Use **CPT + post meta** for editorial content and compatibility.
- Use **one custom DB table** only for click analytics/metrics.
- Use options (Settings API) for plugin-level configuration.

## Step 3 – Questions to lock requirements
1. Which feature set is your strict MVP for v1 (must-have vs later)?
2. Do you want CPT slugs in Portuguese (e.g., `produto`, `comparativo`) or English (`product`, `comparison`)?
3. Should affiliate cloaked links use path style like `/go/{slug}`?
4. For click tracking, do you need per-user/IP details or only aggregate counters?
5. Do you need Gutenberg blocks in v1, or shortcodes-first with blocks in v1.1?
6. Which schema types are mandatory in v1 (Product/Review/Offer/FAQ, ItemList, ComparisonPage)?
7. Should pricing be manual-only in v1 or include 1 API importer (which provider first)?
8. Do you want a top-level admin menu or submenu under Settings?
9. Do you need multisite awareness in v1?
10. Should we include dark mode controls in v1 or postpone?

## Step 4 – Implementation sequence after answers
1. Scaffold plugin structure and bootstrap classes.
2. Register CPTs + meta fields + capabilities.
3. Build settings page (Settings API + sanitization).
4. Build shortcodes SSR + template renderer.
5. Add affiliate cloaker + analytics table + nonce/cap checks.
6. Add schema generator + transient cache.
7. Add conditional asset loader and baseline CSS.
8. Hardening pass (escaping/sanitization/nonces/prepared statements).

## Windows command note
When we start scaffolding files manually on Windows PowerShell, commands will be provided in Windows-compatible form.
