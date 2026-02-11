from playwright.sync_api import sync_playwright

def run(playwright):
    browser = playwright.chromium.launch(headless=True)
    page = browser.new_page()
    # Set viewport size for better screenshot
    page.set_viewport_size({"width": 1280, "height": 720})

    try:
        page.goto("http://localhost:5173/")

        # Wait for the title
        print("Waiting for title...")
        page.wait_for_selector("text=NEURO-SYMBOLIC GUARDRAIL")

        # Click on "Normal Flow"
        print("Clicking Normal Flow...")
        page.get_by_text("Normal Flow").click()

        # Wait for logs to appear (e.g., "Sending legitimate request...")
        print("Waiting for logs...")
        page.wait_for_selector("text=Sending legitimate request...")

        # Wait a bit for animations to progress
        page.wait_for_timeout(3000)

        # Take screenshot
        print("Taking screenshot...")
        page.screenshot(path="verification/dashboard.png")
        print("Screenshot saved to verification/dashboard.png")

    except Exception as e:
        print(f"Error: {e}")
        page.screenshot(path="verification/error.png")
    finally:
        browser.close()

with sync_playwright() as playwright:
    run(playwright)
