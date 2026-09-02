#!/usr/bin/env python3
"""
Simple crawler to find occurrences of a phone number on pages of heatingandcoolingfixer.com.au
Usage: python find_phone.py
Outputs matches to console and writes results to results.txt
"""
import sys
import time
import re
from collections import deque
from urllib.parse import urljoin, urlparse
from urllib.request import Request, urlopen
import ssl

START_URL = "https://heatingandcoolingfixer.com.au/"
ALLOWED_DOMAIN = "heatingandcoolingfixer.com.au"
NUMBER_RAW = "1800 548 492"
# normalized digits-only form
NUMBER_DIGITS = re.sub(r"\D", "", NUMBER_RAW)

HEADERS = {"User-Agent": "Mozilla/5.0 (compatible; PhoneFinder/1.0)"}

FETCH_TIMEOUT = 15
MAX_PAGES = 500
DELAY_BETWEEN = 0.5

visited = set()
found_pages = []

link_re = re.compile(r'href=["\']([^"\'#>]+)')


def fetch(url):
    try:
        req = Request(url, headers=HEADERS)
        # use an unverified SSL context because the target site has an expired cert
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        with urlopen(req, timeout=FETCH_TIMEOUT, context=ctx) as resp:
            ctype = resp.headers.get('Content-Type', '')
            if 'text' not in ctype and 'html' not in ctype:
                return None
            raw = resp.read()
            try:
                # try utf-8 then fallback
                text = raw.decode('utf-8')
            except Exception:
                try:
                    text = raw.decode('latin-1')
                except Exception:
                    text = raw.decode('utf-8', errors='ignore')
            return text
    except Exception as e:
        print(f"[fetch error] {url} -> {e}")
        return None


def extract_links(base_url, html):
    links = []
    for m in link_re.finditer(html):
        href = m.group(1).strip()
        if href.startswith('mailto:') or href.startswith('tel:') or href.startswith('javascript:'):
            continue
        # join relative
        try:
            full = urljoin(base_url, href)
        except Exception:
            continue
        parsed = urlparse(full)
        if parsed.scheme not in ('http', 'https'):
            continue
        # remove fragment
        full = full.split('#', 1)[0]
        links.append(full)
    return links


def normalize_digits(s):
    return re.sub(r"\D", "", s or "")


def is_allowed(url):
    try:
        p = urlparse(url)
        host = p.netloc.lower()
        return host.endswith(ALLOWED_DOMAIN)
    except Exception:
        return False


def main():
    q = deque([START_URL])
    visited.add(START_URL)
    pages_crawled = 0

    while q and pages_crawled < MAX_PAGES:
        url = q.popleft()
        print(f"Crawling ({pages_crawled+1}) {url}")
        html = fetch(url)
        pages_crawled += 1
        if html is None:
            time.sleep(DELAY_BETWEEN)
            continue

        # search for number
        normalized_page_digits = normalize_digits(html)
        if NUMBER_DIGITS in normalized_page_digits:
            print(f"FOUND {NUMBER_RAW} (digits match) on: {url}")
            found_pages.append((url, 'digits'))
        # also search for exact spaced occurrence as given
        if NUMBER_RAW in html:
            print(f"FOUND exact string '{NUMBER_RAW}' on: {url}")
            found_pages.append((url, 'exact'))

        # extract and enqueue links
        links = extract_links(url, html)
        for link in links:
            if not is_allowed(link):
                continue
            if link in visited:
                continue
            visited.add(link)
            q.append(link)

        time.sleep(DELAY_BETWEEN)

    # dedupe found_pages by url
    found_unique = {}
    for url, kind in found_pages:
        found_unique.setdefault(url, set()).add(kind)

    if found_unique:
        print('\nMatches found:')
        with open('results.txt', 'w', encoding='utf-8') as f:
            for url, kinds in found_unique.items():
                line = f"{url} -> {', '.join(sorted(kinds))}"
                print(line)
                f.write(line + '\n')
        print('\nWrote results to results.txt')
    else:
        print('\nNo matches found for', NUMBER_RAW)


if __name__ == '__main__':
    try:
        main()
    except KeyboardInterrupt:
        print('\nInterrupted by user')
        sys.exit(1)
