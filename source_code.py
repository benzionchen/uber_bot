import pyautogui
import time
from playwright.async_api import async_playwright
import os
import random
import asyncio

# Path to store the browser context (cookies, local storage, etc.)
context_storage_path = "context_storage.json"


async def type_with_delay(page, selector, text):
    await page.click(selector)
    for char in text:
        await page.keyboard.press(char)
        # Random delay between 50ms to 200ms
        await asyncio.sleep(random.uniform(0.05, 0.2))


async def automate_uber_with_google_login():
    async with async_playwright() as p:
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"
        browser = await p.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )

        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            storage_state=context_storage_path if os.path.exists(
                context_storage_path) else None
        )

        page = await context.new_page()

        try:
            await page.goto("https://www.uber.com")
            await page.wait_for_timeout(8000)

            pickup_input_selector = "input[aria-label='Pickup location']"
            await page.click(pickup_input_selector)
            await page.fill(pickup_input_selector, "333 Market Street")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)

            dropoff_input_selector = "input[aria-label='Dropoff location']"
            await page.click(dropoff_input_selector)
            await page.fill(dropoff_input_selector, "425 Mission St")
            await page.wait_for_timeout(3000)
            await page.keyboard.press("ArrowDown")
            await page.keyboard.press("Enter")
            await page.wait_for_timeout(5000)

            see_prices_button_selector = "a[data-baseweb='button'][text='See prices']"
            await page.wait_for_selector(see_prices_button_selector, state="visible")
            await page.wait_for_timeout(3000)
            await page.click(see_prices_button_selector)
            await page.wait_for_timeout(5000)

            print("Prices should now be visible in the browser.")

            google_login_button_selector = "button#google-login-btn"
            if await page.is_visible(google_login_button_selector):
                async with page.expect_popup() as popup_info:
                    await page.click(google_login_button_selector)
                    print("Clicked 'Continue with Google'")
                google_popup = await popup_info.value

                await google_popup.wait_for_load_state('networkidle')

                # Click the account "rraiutest1@gmail.com"
                account_selector = "div[data-identifier='rraiutest1@gmail.com']"
                await google_popup.click(account_selector)
                print("Selected the 'rraiutest1@gmail.com' account")

                # Re-focus the popup window to ensure it's active
                await google_popup.bring_to_front()

                # Click the SECOND "Continue" button (skip the first, which might be "Cancel")
                continue_button_selector = "div.VfPpkd-RLmnJb"
                all_buttons = google_popup.locator(continue_button_selector)
                count = await all_buttons.count()

                if count >= 2:
                    await all_buttons.nth(1).click()
                    print("Clicked the 'Continue' button")
                else:
                    print(
                        "Could not find the 'Continue' button, clicking the only visible one.")
                    await all_buttons.first().click()

                await google_popup.wait_for_timeout(5000)

                print("Process completed successfully.")

        except Exception as e:
            print(f"Error during the process: {e}")
            await page.screenshot(path="error_screenshot.png")
        finally:
            await context.storage_state(path=context_storage_path)
            print("Browser context saved. The browser will remain open for inspection. Press Ctrl+C to exit the script.")
            if context.pages:
                await context.pages[0].wait_for_timeout(600000)
            else:
                print("No pages are open in the context to wait on.")

# Run the function to automate the process
asyncio.run(automate_uber_with_google_login())
