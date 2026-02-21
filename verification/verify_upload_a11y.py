import os
from playwright.sync_api import sync_playwright

def verify_upload_card():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=True)
        page = browser.new_page()
        try:
            print("Navigating to app...")
            page.goto("http://localhost:4173/")

            print("Waiting for Upload Dataset card...")
            # Look for the card header
            page.get_by_text("1. Upload Dataset").wait_for()

            # Find the drop zone by the aria-label I added
            drop_zone = page.get_by_label("Upload dataset file. Drag and drop or press Enter to select.")

            if drop_zone.count() > 0:
                print("✅ Found drop zone with correct aria-label.")
            else:
                print("❌ Drop zone not found by aria-label!")
                # Fallback to verify if it exists at all
                if page.get_by_text("Drag & drop file here").count() > 0:
                     print("ℹ️ Drop zone text found, but aria-label might be missing.")

            # Verify role
            role = drop_zone.get_attribute("role")
            if role == "button":
                print("✅ Drop zone has role='button'.")
            else:
                print(f"❌ Drop zone has role='{role}' (expected 'button').")

            # Verify tabIndex
            tabindex = drop_zone.get_attribute("tabindex")
            if tabindex == "0":
                 print("✅ Drop zone has tabindex='0'.")
            else:
                 print(f"❌ Drop zone has tabindex='{tabindex}' (expected '0').")

            # Verify focusability
            print("Attempting to focus...")
            drop_zone.focus()

            # Take screenshot of focused state
            os.makedirs("verification", exist_ok=True)
            screenshot_path = "verification/upload_card_focused.png"
            page.screenshot(path=screenshot_path)
            print(f"📸 Screenshot saved to {screenshot_path}")

            # Verify input is hidden
            input_el = page.locator("input[type='file']")
            if input_el.is_hidden():
                print("✅ File input is hidden.")
            else:
                print("❌ File input is visible.")

        except Exception as e:
            print(f"❌ Error: {e}")
        finally:
            browser.close()

if __name__ == "__main__":
    verify_upload_card()
