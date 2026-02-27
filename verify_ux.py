from playwright.sync_api import sync_playwright

def verify_format_button():
    with sync_playwright() as p:
        browser = p.chromium.launch()
        page = browser.new_page()

        # Go to the app
        page.goto("http://localhost:4173/")

        # Scroll to Playground section
        playground = page.locator("text=Playground").first
        playground.scroll_into_view_if_needed()

        # Locate the input field
        input_field = page.locator('textarea[aria-invalid="false"]').first

        # Set some messy JSON
        messy_json = '{"a":1,"b":   2}'
        input_field.fill(messy_json)

        # Click format button
        page.get_by_role("button", name="Format").click()

        # Verify content is formatted
        # formatted content should span multiple lines
        content = input_field.input_value()
        print(f"Content after formatting:\n{content}")

        if '\n' in content and '"a": 1' in content:
            print("✅ JSON formatted successfully")
        else:
            print("❌ JSON formatting failed")

        # Take screenshot
        page.screenshot(path="verification_playground.png")
        browser.close()

if __name__ == "__main__":
    verify_format_button()
