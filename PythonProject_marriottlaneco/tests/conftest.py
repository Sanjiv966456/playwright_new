import os
from pathlib import Path
import shutil
import glob
import pytest
from playwright.sync_api import sync_playwright

BASE_URL = os.getenv("BASE_URL", "https://marriottlaneco.wpenginepowered.com/")
ARTIFACTS_DIR = Path(os.getenv("ARTIFACTS_DIR", "artifacts"))


def _ensure_dirs():
    (ARTIFACTS_DIR / "screenshots").mkdir(parents=True, exist_ok=True)
    (ARTIFACTS_DIR / "videos").mkdir(parents=True, exist_ok=True)


@pytest.fixture(scope="session", autouse=True)
def session_setup():
    _ensure_dirs()
    yield


@pytest.fixture(scope="function")
def page(request):
    """Yields a Playwright page. After the test finishes a full-page screenshot is saved and the recorded video is moved/renamed.

    Videos are recorded via context.record_video_dir and are finalized when the context is closed.
    """
    test_name = request.node.name
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        video_temp_dir = ARTIFACTS_DIR / "videos" / "_tmp"
        video_temp_dir.mkdir(parents=True, exist_ok=True)
        context = browser.new_context(record_video_dir=str(video_temp_dir))
        page = context.new_page()
        try:
            yield page
        finally:
            # take final screenshot
            screenshots_dir = ARTIFACTS_DIR / "screenshots"
            screenshots_dir.mkdir(parents=True, exist_ok=True)
            screenshot_path = screenshots_dir / f"{test_name}.png"
            try:
                page.screenshot(path=str(screenshot_path), full_page=True)
            except Exception:
                # ignore screenshot errors
                pass
            # close context to finalize video files
            try:
                context.close()
            except Exception:
                pass
            try:
                browser.close()
            except Exception:
                pass

            # move the latest video file(s) to artifacts/videos and rename with test name
            try:
                vids = sorted(glob.glob(str(video_temp_dir / "**" / "*.webm"), recursive=True), key=os.path.getmtime)
                if vids:
                    latest = vids[-1]
                    dest = ARTIFACTS_DIR / "videos" / f"{test_name}.webm"
                    shutil.move(latest, dest)
                # cleanup tmp subfolders
                for folder in video_temp_dir.iterdir():
                    if folder.is_dir():
                        try:
                            shutil.rmtree(folder)
                        except Exception:
                            pass
            except Exception:
                pass


@pytest.fixture(scope="session")
def base_url():
    return BASE_URL

