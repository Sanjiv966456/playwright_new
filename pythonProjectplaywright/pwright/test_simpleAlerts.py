import subprocess
import os
from playwright.sync_api import sync_playwright

# Create trace output directory
trace_dir = "traces"
os.makedirs(trace_dir, exist_ok=True)
trace_file = os.path.join(trace_dir, "trace.zip")

with sync_playwright() as p:
    browser = p.chromium.launch(headless=False)
    context = browser.new_context()
    context.tracing.start(screenshots=True, snapshots=True, sources=True)

    page = context.new_page()
    page.goto("https://demoqa.com")
    page.click("text=Elements")
    page.wait_for_timeout(2000)
    context.tracing.stop(path=trace_file)
    page.close()
    context.close()
    browser.close()

# Open trace viewer
print(f"✓ Trace saved to: {trace_file}")
print("Opening trace viewer...")
try:
    subprocess.Popen(["playwright", "show-trace", trace_file])
except FileNotFoundError:
    print("Playwright CLI not found. View trace manually with:")
    print(f"  playwright show-trace {trace_file}")

