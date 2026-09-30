"""
Playwright + Python script
Crawls all internal pages of https://mckinnonheadev.wpenginepowered.com/
and reports every page where the text "4.7" is found.

Install dependencies first:
    pip install playwright
    playwright install chromium

Run:
    python find_4_7_site_crawl.py
"""

import re
from collections import deque
from urllib.parse import urljoin, urlparse

from playwright.sync_api import sync_playwright, TimeoutError as PWTimeoutError

BASE_URL = "https://mckinnonheadev.wpenginepowered.com/"
SEARCH_TEXT = "4.7"
MAX_PAGES = 300  # safety cap so the crawl can't run forever
NAV_TIMEOUT_MS = 20000

# File/link patterns we don't want to try to crawl as HTML pages
SKIP_EXTENSIONS = (
    ".pdf", ".jpg", ".jpeg", ".png", ".gif", ".svg", ".webp", ".ico",
    ".zip", ".rar", ".doc", ".docx", ".xls", ".xlsx", ".mp4", ".mp3",
    ".css", ".js", ".woff", ".woff2", ".ttf", ".eot", ".xml",
)


def is_same_domain(url: str, base_domain: str) -> bool:
    return urlparse(url).netloc == base_domain


def normalize_url(url: str) -> str:
    # Strip fragments (#section) and trailing slashes for de-duplication
    parsed = urlparse(url)
    cleaned = parsed._replace(fragment="")
    normalized = cleaned.geturl()
    if normalized.endswith("/") and normalized != BASE_URL:
        normalized = normalized[:-1]
    return normalized


def should_skip(url: str) -> bool:
    lowered = url.lower()
    return any(lowered.endswith(ext) for ext in SKIP_EXTENSIONS) or "wp-admin" in lowered


def crawl_site():
    base_domain = urlparse(BASE_URL).netloc

    visited = set()
    to_visit = deque([normalize_url(BASE_URL)])

    pages_with_match = []
    pages_checked = []

    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        context = browser.new_context()
        page = context.new_page()
        page.set_default_navigation_timeout(NAV_TIMEOUT_MS)

        while to_visit and len(visited) < MAX_PAGES:
            url = to_visit.popleft()
            if url in visited or should_skip(url):
                continue
            visited.add(url)

            print(f"Visiting ({len(visited)}/{MAX_PAGES}): {url}")

            try:
                page.goto(url, wait_until="networkidle")
            except PWTimeoutError:
                try:
                    page.goto(url, wait_until="domcontentloaded")
                except Exception as e:
                    print(f"  ! Failed to load {url}: {e}")
                    continue
            except Exception as e:
                print(f"  ! Failed to load {url}: {e}")
                continue

            pages_checked.append(url)

            # --- Search visible page text for "4.7" ---
            try:
                body_text = page.inner_text("body")
            except Exception:
                body_text = ""

            occurrences = len(re.findall(re.escape(SEARCH_TEXT), body_text))
            if occurrences > 0:
                print(f"  -> FOUND '{SEARCH_TEXT}' {occurrences} time(s) on {url}")
                pages_with_match.append((url, occurrences))

            # --- Collect internal links to keep crawling ---
            try:
                hrefs = page.eval_on_selector_all(
                    "a[href]", "elements => elements.map(el => el.href)"
                )
            except Exception:
                hrefs = []

            for href in hrefs:
                if not href:
                    continue
                full_url = urljoin(url, href)
                full_url = normalize_url(full_url)

                if not is_same_domain(full_url, base_domain):
                    continue
                if should_skip(full_url):
                    continue
                if full_url not in visited and full_url not in to_visit:
                    to_visit.append(full_url)

        browser.close()

    # --- Report ---
    print("\n" + "=" * 60)
    print(f"Crawl complete. Checked {len(pages_checked)} page(s).")
    print(f"Pages containing '{SEARCH_TEXT}': {len(pages_with_match)}")
    print("=" * 60)

    if pages_with_match:
        for url, count in pages_with_match:
            print(f" - {url}  ({count} occurrence{'s' if count != 1 else ''})")
    else:
        print(f"No pages contained the text '{SEARCH_TEXT}'.")

    # Optional: write results to a text file
    with open("pages_with_4_7.txt", "w", encoding="utf-8") as f:
        f.write(f"Search term: {SEARCH_TEXT}\n")
        f.write(f"Base URL: {BASE_URL}\n")
        f.write(f"Pages checked: {len(pages_checked)}\n\n")
        if pages_with_match:
            for url, count in pages_with_match:
                f.write(f"{url}\t{count} occurrence(s)\n")
        else:
            f.write("No matches found.\n")

    return pages_with_match


if __name__ == "__main__":
    crawl_site()