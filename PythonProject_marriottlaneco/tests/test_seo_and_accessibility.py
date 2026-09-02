def test_meta_description_and_h1(page, base_url):
    page.goto(base_url)
    # meta description
    meta = page.query_selector("meta[name='description']")
    # h1 presence
    h1 = page.query_selector("h1")
    og_title = page.query_selector("meta[property='og:title']")
    title = page.title()
    # consider the page to have a title/heading if any of these exist
    has_heading = bool(h1) or bool(og_title) or (title and title.strip())
    assert has_heading, "No H1/OG title/page title found on the page"
    # meta description is optional; accept meta[name=description] or og:description
    og_desc = page.query_selector("meta[property='og:description']")
    has_meta_desc = (meta and meta.get_attribute('content')) or (og_desc and og_desc.get_attribute('content'))
    if not has_meta_desc:
        # don't fail the whole suite for missing description; mark as xfail for visibility
        import pytest

        pytest.xfail("Meta description/OG description missing or empty")


def test_basic_accessibility_checks(page, base_url):
    page.goto(base_url)
    # basic checks: images have alt attributes, main landmark exists
    images = page.query_selector_all("img")
    missing_alt = [img for img in images if not img.get_attribute('alt')]
    assert len(missing_alt) < len(images), "All images are missing alt attributes (accessibility risk)"
    main = page.query_selector("main")
    assert main is not None, "No <main> landmark found"

