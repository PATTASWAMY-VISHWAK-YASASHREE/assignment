import time
from playwright.sync_api import sync_playwright

def verify_playground_format():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Navigate to the app (vite preview usually runs on 4173)
        page.goto("http://localhost:4173")

        # Wait for the page to load
        page.wait_for_load_state("networkidle")

        # Locate the Playground Card (it has the title "Playground")
        # We might need to scroll or ensure it's visible.
        # Assuming the standard layout, it should be on the dashboard.

        # Find the text area with "JSON input" label
        # Note: MUI TextField with label "JSON input" usually has an input or textarea with that label
        input_area = page.get_by_label("JSON input")

        # Fill with messy JSON
        messy_json = '{"key":1,"value":   2}'
        input_area.fill(messy_json)

        # Find the Format button and click it
        format_button = page.get_by_role("button", name="Format")
        format_button.click()

        # Wait a brief moment for state update
        time.sleep(0.5)

        # Get the value and verify it is formatted
        formatted_value = input_area.input_value()
        print(f"Formatted Value:\n{formatted_value}")

        # Take a screenshot of the Playground Card area
        # We'll try to screenshot the whole page for context
        page.screenshot(path="verification_playground.png")

        browser.close()

if __name__ == "__main__":
    verify_playground_format()
