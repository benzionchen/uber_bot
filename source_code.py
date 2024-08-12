from playwright.async_api import async_playwright
import os
import random
import asyncio

# Path to store the browser context (cookies, local storage, etc.)
context_storage_path = "context_storage.json"


async def save_progress(checkpoint):
    with open("progress_checkpoint.txt", "w") as f:
        f.write(checkpoint)
    print(f"Progress saved at: {checkpoint}")


async def load_progress():
    if os.path.exists("progress_checkpoint.txt"):
        with open("progress_checkpoint.txt", "r") as f:
            return f.read().strip()
    return None


async def reset_progress():
    if os.path.exists("progress_checkpoint.txt"):
        os.remove("progress_checkpoint.txt")
    print("Progress has been reset.")


async def type_with_delay(page, selector, text):
    # Focus on the input field
    await page.click(selector)
    # Type each character with a small random delay
    for char in text:
        await page.keyboard.press(char)
        # Random delay between 50ms to 200ms
        await asyncio.sleep(random.uniform(0.05, 0.2))


async def reenter_password(page):
    # Re-enter the password with randomized typing speed
    password_input_selector = "input[type='password']"
    await page.wait_for_selector(password_input_selector, state="visible")
    await type_with_delay(page, password_input_selector, "efdagflk138257448")
    print("Password entered again.")

    # Click the "Next" button
    next_buttons = page.locator("div.VfPpkd-RLmnJb")
    count = await next_buttons.count()
    if count >= 3:
        try:
            await next_buttons.nth(2).click()
            print("Clicked 'Next' button after re-entering the password")
        except Exception as e:
            print(
                f"Failed to click 'Next' button after re-entering the password: {e}")


async def click_all_try_again_buttons(page):
    # Locate all the "Try Again" buttons and click them one by one
    try_again_buttons = page.locator("a[aria-label='Try again']")
    count = await try_again_buttons.count()
    if count == 0:
        print("No 'Try Again' buttons found.")
    else:
        for i in range(count):
            try:
                # Ensure the button is visible and enabled
                if await try_again_buttons.nth(i).is_visible() and await try_again_buttons.nth(i).is_enabled():
                    await try_again_buttons.nth(i).click()
                    print(f"Clicked 'Try Again' button {i + 1}")
                else:
                    print(
                        f"'Try Again' button {i + 1} is not visible or enabled.")
            except Exception as e:
                print(f"Failed to click 'Try Again' button {i + 1}: {e}")


async def click_next_button(page):
    next_button_selector = "div.VfPpkd-RLmnJb"
    next_buttons = page.locator(next_button_selector)
    count = await next_buttons.count()
    if count > 0:
        try:
            # Click the first "Next" button found
            await next_buttons.nth(0).click()
            print("Clicked 'Next' button on the account recovery page")
        except Exception as e:
            print(
                f"Failed to click 'Next' button on the account recovery page: {e}")
    else:
        print("No 'Next' button found on the account recovery page")


async def automate_uber_with_google_login():
    progress_checkpoint = await load_progress()

    async with async_playwright() as p:
        # Define the path to the Google Chrome executable
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        # Launch Google Chrome
        browser = await p.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            args=['--disable-blink-features=AutomationControlled']
        )

        # Load the saved browser context if it exists
        context = await browser.new_context(
            viewport={"width": 1280, "height": 800},
            storage_state=context_storage_path if os.path.exists(
                context_storage_path) else None
        )

        # Open a single page
        page = await context.new_page()

        try:
            # Check if resuming from the password screen
            if progress_checkpoint == "password_screen":
                print("Resuming from the password screen...")

                # Check if the password screen is still present
                if await page.locator("input[type='password']").is_visible():
                    await reenter_password(page)
                    await page.wait_for_load_state('networkidle')
                else:
                    print(
                        "Password screen not found, resetting progress and starting over.")
                    await reset_progress()
                    await automate_uber_with_google_login()  # Restart the script
                    return  # Exit the current function to avoid continuing with invalid state

            else:
                # No valid progress checkpoint or starting fresh
                await reset_progress()

                # Navigate to Uber's website
                await page.goto("https://www.uber.com")
                await page.wait_for_timeout(8000)

                # Select the pickup location
                pickup_input_selector = "input[aria-label='Pickup location']"
                await page.click(pickup_input_selector)
                await page.fill(pickup_input_selector, "333 Market Street")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("ArrowDown")
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(5000)

                # Select the drop-off location
                dropoff_input_selector = "input[aria-label='Dropoff location']"
                await page.click(dropoff_input_selector)
                await page.fill(dropoff_input_selector, "425 Mission St")
                await page.wait_for_timeout(3000)
                await page.keyboard.press("ArrowDown")
                await page.keyboard.press("Enter")
                await page.wait_for_timeout(5000)

                # Click on "See prices"
                see_prices_button_selector = "a[data-baseweb='button'][text='See prices']"
                await page.wait_for_selector(see_prices_button_selector, state="visible")
                await page.wait_for_timeout(3000)
                await page.click(see_prices_button_selector)
                await page.wait_for_timeout(5000)

                print("Prices should now be visible in the browser.")

                # Check if redirected to the login page and click "Continue with Google"
                google_login_button_selector = "button#google-login-btn"
                if await page.is_visible(google_login_button_selector):
                    async with page.expect_popup() as popup_info:
                        await page.click(google_login_button_selector)
                        print("Clicked 'Continue with Google'")
                    google_popup = await popup_info.value

                    # Wait for the Google login page to load in the new window
                    await google_popup.wait_for_load_state('networkidle')
                    await google_popup.wait_for_selector("input#identifierId", state="visible")

                    # Input the Google account username (email) with randomized typing speed
                    email_input_selector = "input#identifierId"
                    await type_with_delay(google_popup, email_input_selector, "rraiutest1@gmail.com")

                    # Click the correct "Next" button (Button 2) on the email screen
                    next_buttons = google_popup.locator("div.VfPpkd-RLmnJb")
                    count = await next_buttons.count()
                    if count >= 2:
                        try:
                            await next_buttons.nth(1).click()
                            print("Clicked 'Next button 2' on the email screen")
                        except Exception as e:
                            print(
                                f"Failed to click 'Next button 2' on the email screen: {e}")

                    # Save progress after reaching the password screen
                    await save_progress("password_screen")

                    # Wait for the password input to be visible
                    await google_popup.wait_for_selector("input[type='password']", state="visible")
                    print("Ready for password input.")

                    # Input the password with randomized typing speed
                    await type_with_delay(google_popup, "input[type='password']", "efdagflk138257448")
                    print("Password entered.")

                    # Click "Next button 3"
                    if await next_buttons.count() >= 3:
                        try:
                            await next_buttons.nth(2).click()
                            print("Clicked 'Next button 3' on the password screen")
                        except Exception as e:
                            print(
                                f"Failed to click 'Next button 3' on the password screen: {e}")

                    await google_popup.wait_for_load_state('networkidle')

                    # Introduce a delay to allow the page to fully load
                    await google_popup.wait_for_timeout(5000)

                    # Check for the "Try Again" button and click all visible ones
                    print("Checking for 'Try Again' buttons...")
                    if await google_popup.is_visible("a[aria-label='Try again']"):
                        print(
                            "Detected 'Try Again' button, bringing popup to the front...")
                        await google_popup.bring_to_front()  # Refocus the Google popup
                        await click_all_try_again_buttons(google_popup)
                        await reenter_password(google_popup)
                    else:
                        print("No 'Try Again' button detected after password entry.")

                    # Wait for the account recovery page to load
                    await google_popup.wait_for_timeout(3000)

                    # Refocus on the account recovery page and check for "Next" button
                    print(
                        "Refocusing on the account recovery page and looking for 'Next' button...")
                    # Ensure the account recovery page is in focus
                    await google_popup.bring_to_front()
                    await click_next_button(google_popup)

        except Exception as e:
            print(f"Error during the process: {e}")
            await page.screenshot(path="error_screenshot.png")
        finally:
            # Save the browser context (cookies, local storage, etc.)
            await context.storage_state(path=context_storage_path)
            print("Browser context saved. The browser will remain open for inspection. Press Ctrl+C to exit the script.")
            if context.pages:
                await context.pages[0].wait_for_timeout(600000)
            else:
                print("No pages are open in the context to wait on.")

# Run the function to automate the process
asyncio.run(automate_uber_with_google_login())
