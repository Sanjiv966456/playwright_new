#!/usr/bin/env python3
"""
Simple automation to find broken images on a page.
Usage:
  python test_broken_image.py https://alexandriaadev.wpenginepowered.com/ --timeout 15

Requires: playwright, requests
  pip install playwright requests
  python -m playwright install

Checks <img> tags (src / srcset / data-src). Reports images with 4xx/5xx status, empty content, or non-image content-type.
"""
import argparse
import sys
import requests
from urllib.parse import urljoin
from playwright.sync_api import sync_playwright


def collect_image_urls(page, base_url):
    urls = []
    imgs = page.query_selector_all("img")
    for img in imgs:
        # prefer src, fallback data-src, then srcset
        src = img.get_attribute("src") or img.get_attribute("data-src") or img.get_attribute("srcset")
        if not src:
            continue
        # handle srcset: take all candidates
        if "," in src and "srcset" in (img.get_attribute("srcset") or ""):
            for part in src.split(','):
                url_part = part.strip().split(' ')[0]
                if url_part:
                    urls.append(urljoin(base_url, url_part))
        else:
            urls.append(urljoin(base_url, src))
    # deduplicate while preserving order
    seen = set()
    dedup = []
    for u in urls:
        if u not in seen:
            seen.add(u)
            dedup.append(u)
    return dedup


def check_image(url, timeout, session):
    result = {"url": url, "ok": True, "status": None, "reason": None}
    if url.startswith('data:'):
        result['ok'] = True
        result['status'] = 'data'
        return result
    try:
        # prefer HEAD to be faster, fall back to GET if HEAD not allowed
        resp = session.head(url, allow_redirects=True, timeout=timeout)
        result['status'] = resp.status_code
        if resp.status_code >= 400:
            # try GET to confirm
            resp = session.get(url, stream=True, timeout=timeout)
            result['status'] = resp.status_code
            if resp.status_code >= 400:
                result['ok'] = False
                result['reason'] = f"HTTP {resp.status_code}"
                return result
        # check content-type
        ctype = resp.headers.get('Content-Type', '')
        if not ctype.startswith('image'):
            # sometimes HEAD doesn't provide content-type; try GET
            resp_get = session.get(url, stream=True, timeout=timeout)
            result['status'] = resp_get.status_code
            ctype = resp_get.headers.get('Content-Type', '')
            if not ctype.startswith('image') or resp_get.status_code >= 400:
                result['ok'] = False
                result['reason'] = f"Non-image content-type: {ctype} (status {resp_get.status_code})"
                return result
            # also check content length
            length = resp_get.headers.get('Content-Length')
            if length is not None and int(length) == 0:
                result['ok'] = False
                result['reason'] = 'Content-Length 0'
                return result
        else:
            # content-type says image; check length if available
            length = resp.headers.get('Content-Length')
            if length is not None and int(length) == 0:
                result['ok'] = False
                result['reason'] = 'Content-Length 0'
                return result
    except requests.RequestException as exc:
        result['ok'] = False
        result['reason'] = str(exc)
    return result


def find_broken_images(url, timeout=15, verify_ssl=True, headless=True):
    """Return a list of broken image result dicts for the given page URL.
    Each result dict matches what check_image(...) returns.
    """
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=headless)
        page = browser.new_page()
        try:
            page.goto(url, wait_until='load', timeout=60000)
        except Exception as e:
            browser.close()
            raise RuntimeError(f"Failed to load page {url}: {e}") from e
        image_urls = collect_image_urls(page, url)
        browser.close()

    if not image_urls:
        return []

    session = requests.Session()
    session.headers.update({'User-Agent': 'img-checker/1.0'})
    session.verify = verify_ssl

    broken = []
    for img_url in image_urls:
        res = check_image(img_url, timeout=timeout, session=session)
        if not res['ok']:
            broken.append(res)

    return broken


def main():
    parser = argparse.ArgumentParser(description='Find broken images on a page')
    parser.add_argument('url', help='Page URL to scan')
    parser.add_argument('--timeout', type=int, default=15, help='HTTP request timeout (seconds)')
    parser.add_argument('--verify-ssl', action='store_true', help='Verify SSL certificates for HTTP requests')
    args = parser.parse_args()

    try:
        broken = find_broken_images(args.url, timeout=args.timeout, verify_ssl=args.verify_ssl, headless=True)
    except RuntimeError as e:
        print(str(e))
        sys.exit(2)

    if not broken:
        print('No broken images found.')
        sys.exit(0)

    print('\nSummary:')
    print(f'  Broken images: {len(broken)}')
    print('\nBroken image list:')
    for b in broken:
        print('-', b['url'], '=>', b.get('reason'))

    sys.exit(1)

if __name__ == '__main__':
    main()
