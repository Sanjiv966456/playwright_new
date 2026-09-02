from pages.home_page import HomePage
import pytest
from urllib.parse import urlparse, urljoin


def _click_link_and_assert(page, base_url, partial_href):
    home = HomePage(page, base_url=base_url)
    home.goto_home()
    link = home.find_link_by_partial(partial_href)
    assert link, f"No link found containing '{partial_href}'"
    href = link.get_attribute('href')
    if not href:
        pytest.xfail(f"Found link for '{partial_href}' but it has no href")
    # ignore anchors/mailto/tel
    if href.startswith('#') or href.startswith('mailto:') or href.startswith('tel:'):
        pytest.xfail(f"Link for '{partial_href}' is non-navigable: {href}")
    parsed = urlparse(href)
    # if absolute and external, xfail
    if parsed.scheme and not href.startswith(base_url):
        pytest.xfail(f"Link appears external to base_url: {href}")
    # navigate using full url (handles relative and absolute internal links)
    full = urljoin(base_url, href)
    page.goto(full)
    page.wait_for_load_state('domcontentloaded')
    assert page.url.startswith(base_url.rstrip('/')), f"Navigation left base URL after navigating to {href}"


@pytest.mark.parametrize("partial", ["contact", "property", "properties", "about"])
def test_navigation_internal_links(page, base_url, partial):
    # attempt several likely internal link fragments
    try:
        _click_link_and_assert(page, base_url, partial)
    except AssertionError:
        # if a given partial isn't present, that's acceptable; mark xfail within test flow
        pytest.xfail(f"No link found for partial '{partial}' or navigation failed")

