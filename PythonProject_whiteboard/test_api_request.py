"""
API / status-code checks for https://energusdev.wpenginepowered.com/

Run:
    pip install pytest-playwright requests
    pytest test_api_status.py -v
    pytest test_api_status.py -v -n 4 --alluredir=allure-results
"""

import re
import pytest
from playwright.sync_api import Playwright, APIRequestContext

BASE_URL = "https://energusdev.wpenginepowered.com"

# Add/remove paths as needed
PATHS = [
    "/",
    "/about-us/",
    "/contact-us/",
    "/services/",
    "/blog/",
]


# ---------------------------------------------------------------- fixtures
@pytest.fixture(scope="session")
def api(playwright: Playwright) -> APIRequestContext:
    """Session-scoped APIRequestContext — reused across all tests."""
    ctx = playwright.request.new_context(
        base_url=BASE_URL,
        ignore_https_errors=True,
        timeout=30_000,
        extra_http_headers={
            "User-Agent": "QA-Playwright-Bot/1.0",
            "Accept": "text/html,application/json",
            # WPEngine staging basic auth, if enabled:
            # "Authorization": "Basic <base64-user:pass>",
        },
    )
    yield ctx
    ctx.dispose()


# ---------------------------------------------------------------- tests
def test_homepage_returns_200(api: APIRequestContext):
    res = api.get("/")
    assert res.status == 200, f"Expected 200, got {res.status} for {res.url}"
    assert res.ok


@pytest.mark.parametrize("path", PATHS)
def test_pages_return_200(api: APIRequestContext, path):
    res = api.get(path)
    assert res.status == 200, f"{path} -> {res.status}"


def test_no_redirect_on_homepage(api: APIRequestContext):
    """Catches staging-URL contamination / unexpected 301s."""
    res = api.get("/", max_redirects=0)
    assert res.status == 200, f"Homepage redirected: {res.status} -> {res.headers.get('location')}"


def test_404_page_returns_404(api: APIRequestContext):
    res = api.get("/this-page-does-not-exist-qa/")
    assert res.status == 404, f"Expected 404, got {res.status}"


def test_response_headers(api: APIRequestContext):
    res = api.get("/")
    headers = res.headers
    assert "text/html" in headers.get("content-type", "")
    print("\nServer:", headers.get("server"))
    print("Cache:", headers.get("x-cache"))


def test_robots_and_sitemap_exist(api: APIRequestContext):
    assert api.get("/robots.txt").status == 200
    assert api.get("/sitemap_index.xml").status == 200


# ---------------------------------------------------------------- WP REST API
def test_wp_rest_api_posts(api: APIRequestContext):
    res = api.get("/wp-json/wp/v2/posts", params={"per_page": 5})
    assert res.status == 200, f"WP REST API -> {res.status}"
    data = res.json()
    assert isinstance(data, list)
    for post in data:
        assert "id" in post and "link" in post
        assert BASE_URL in post["link"], f"Staging leak: {post['link']}"


def test_wp_rest_api_pages(api: APIRequestContext):
    res = api.get("/wp-json/wp/v2/pages", params={"per_page": 10})
    assert res.status == 200
    for page in res.json():
        assert page["status"] == "publish"


# ---------------------------------------------------------------- bulk sitemap crawl
def _sitemap_urls(api: APIRequestContext, limit=50):
    """Pull URLs from the sitemap index -> child sitemaps."""
    urls = []
    index = api.get("/sitemap_index.xml")
    if index.status != 200:
        return urls
    children = re.findall(r"<loc>(.*?)</loc>", index.text())
    for child in children:
        if not child.endswith(".xml"):
            urls.append(child)
            continue
        sub = api.get(child)
        if sub.status == 200:
            urls += re.findall(r"<loc>(.*?)</loc>", sub.text())
        if len(urls) >= limit:
            break
    return urls[:limit]


def test_all_sitemap_urls_return_200(api: APIRequestContext):
    urls = _sitemap_urls(api)
    assert urls, "No URLs found in sitemap"

    broken = []
    for url in urls:
        try:
            res = api.get(url)
            if res.status != 200:
                broken.append((url, res.status))
        except Exception as e:
            broken.append((url, str(e)))

    print(f"\nChecked {len(urls)} URLs, {len(broken)} broken")
    for url, status in broken:
        print(f"  {status}  {url}")
    assert not broken, f"{len(broken)} URLs did not return 200"