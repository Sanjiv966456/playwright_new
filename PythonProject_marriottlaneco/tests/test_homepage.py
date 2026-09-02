from pages.home_page import HomePage


def test_homepage_basic(page, base_url):
    home = HomePage(page, base_url=base_url)
    resp = home.goto_home()
    # ensure page loaded (response should be present and not an error)
    assert resp is not None, "No response when navigating to homepage"
    try:
        status = resp.status
    except Exception:
        status = None
    if status is not None:
        assert status < 400, f"Homepage returned HTTP {status}"
    # page URL should start with base_url
    assert page.url.startswith(base_url.rstrip('/'))
    # title may be empty in some WP themes that render dynamically; don't fail on empty title
    title = home.title()
    # check header/nav/footer exist
    assert home.has_nav(), "Main navigation not found"
    assert home.has_footer(), "Footer not found"


def test_homepage_has_hero(page, base_url):
    home = HomePage(page, base_url=base_url)
    home.goto_home()
    assert home.has_hero(), "Hero/header section not detected on homepage"

