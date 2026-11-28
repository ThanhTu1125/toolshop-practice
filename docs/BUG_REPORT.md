# BUG_REPORT - Toolshop BUGGY

A defect counts when: green on PROD, red on BUGGY, evidence attached (trace or screenshot),
and you can say what was expected and what happened. Several red tests from one defect = one bug.

Run: `pytest tests/buoi4/test_b4_loose.py -v`, 28/11/2026

| Code | Feature | Title | Severity | Detected by |
|---|---|---|---|---|
| BUG-001 | Shopping Cart | Error toast "Oeps, something went wrong." displayed on adding product | High | `tests/buoi4/test_b4_loose.py::test_b4_a_add_to_cart_shows_a_toast` |
| BUG-002 | Navigation Header | Menu displays misspelled "Contakt" instead of "Contact" | Medium | `tests/buoi4/test_b4_loose.py::test_b4_e_header_has_contact_and_search` |
| BUG-003 | Search API | Search API returns unrelated tools for query "wrench" | Medium | `tests/buoi4/test_b4_loose.py::test_b4_g_search_api_finds_wrench` |

## BUG-001 - Error toast "Oeps, something went wrong." displayed on adding product to cart

- **Feature:** Shopping Cart / Add to Cart
- **Environment:** https://with-bugs.practicesoftwaretesting.com (green on PROD)
- **Steps to reproduce:**
  1. Open the home page: `https://with-bugs.practicesoftwaretesting.com/#/`
  2. Click on product "Combination Pliers" to navigate to its details page (`/#/product/1`)
  3. Click the "Add to cart" button (`data-test="add-to-cart"`)
- **Expected:** Success toast message appears with text: `"Product added to shopping cart."`
- **Actual:** Danger toast message appears with text: `"Oeps, something went wrong."`
- **Detected by:** `tests/buoi4/test_b4_loose.py::test_b4_a_add_to_cart_shows_a_toast`
- **Evidence:** `docs/screenshots/BUG-001.png`, trace in artifact `report-buggy`
- **Notes:** Blocks users from adding products to the shopping cart.

## BUG-002 - Navigation menu displays misspelled "Contakt" instead of "Contact"

- **Feature:** Navigation Header
- **Environment:** https://with-bugs.practicesoftwaretesting.com (green on PROD)
- **Severity:** Medium
- **Steps to reproduce:**
  1. Open the home page: `https://with-bugs.practicesoftwaretesting.com/#/`
  2. Observe the main navigation menu bar at the top of the page.
- **Expected:** The contact page navigation link has text `"Contact"`.
- **Actual:** The contact page navigation link displays `"Contakt"` (spelled with a 'k').
- **Detected by:** `tests/buoi4/test_b4_loose.py::test_b4_e_header_has_contact_and_search`
- **Evidence:** `docs/screenshots/BUG-002.png`, trace in artifact `report-buggy`
- **Notes:** Typo in user interface navigation bar.

## BUG-003 - Search API returns unrelated tools for query "wrench"

- **Feature:** Search API
- **Environment:** https://api-with-bugs.practicesoftwaretesting.com (green on PROD)
- **Severity:** Medium
- **Steps to reproduce:**
  1. Send a GET request to `/products/search?q=wrench`
  2. Inspect the `data` array in the JSON response.
- **Expected:** Only products containing "wrench" in their name are returned (e.g. `["Adjustable Wrench"]`).
- **Actual:** The API returns unrelated tools: `['Adjustable Wrench', 'Angled Spanner', 'Phillips Screwdriver', 'Circular Saw']`.
- **Detected by:** `tests/buoi4/test_b4_loose.py::test_b4_g_search_api_finds_wrench`
- **Evidence:** API JSON response, trace in artifact `report-buggy`
- **Notes:** Backend search filter does not match keyword accurately.
