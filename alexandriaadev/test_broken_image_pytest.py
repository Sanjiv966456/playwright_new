import pytest
from test_broken_image import find_broken_images


def test_no_broken_images_on_homepage():
    # Run quickly; disable SSL verification if site uses non-standard certs
    broken = find_broken_images("https://alexandriaadev.wpenginepowered.com/", timeout=15, verify_ssl=False, headless=True)
    assert broken == [], f"Found broken images: {broken}"
