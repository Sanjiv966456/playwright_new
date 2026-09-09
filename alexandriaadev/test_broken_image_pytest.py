import pytest
from test_broken_image import find_broken_images

# Silence unverified HTTPS warnings when tests intentionally disable SSL verification
import warnings
from urllib3.exceptions import InsecureRequestWarning
warnings.filterwarnings('ignore', category=InsecureRequestWarning)


def test_no_broken_images_on_homepage():
    # Run quickly; disable SSL verification if site uses non-standard certs
    broken = find_broken_images("https://alexandriaadev.wpenginepowered.com/", timeout=15, verify_ssl=False, headless=True)
    # Ignore favicon.ico which may be served with zero-length body on this host
    filtered = [b for b in broken if not b['url'].endswith('/favicon.ico')]
    assert filtered == [], f"Found broken images: {filtered}"
