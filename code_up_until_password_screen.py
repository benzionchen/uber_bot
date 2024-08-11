from playwright.sync_api import sync_playwright


def automate_uber_with_google_login():
    with sync_playwright() as p:
        # Define the path to the Google Chrome executable
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        # Launch Google Chrome in incognito mode by specifying the executable path
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            # Use incognito mode and disable automation control
            args=['--incognito', '--disable-blink-features=AutomationControlled']
        )

        # Create a single context that will be reused to preserve session data
        context = browser.new_context(viewport={"width": 1280, "height": 800})

        page = context.new_page()

        try:
            # Navigate to Uber's website
            page.goto("https://www.uber.com")

            # Wait for the page to load completely
            page.wait_for_timeout(8000)

            # Select the pickup location
            pickup_input_selector = "input[aria-label='Pickup location']"
            page.click(pickup_input_selector)
            page.fill(pickup_input_selector, "333 Market Street")
            # Wait for dropdown suggestions to load
            page.wait_for_timeout(3000)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            # Wait for the selection to be processed
            page.wait_for_timeout(5000)

            # Select the drop-off location
            dropoff_input_selector = "input[aria-label='Dropoff location']"
            page.click(dropoff_input_selector)
            page.fill(dropoff_input_selector, "425 Mission St")
            # Wait for dropdown suggestions to load
            page.wait_for_timeout(3000)
            page.keyboard.press("ArrowDown")
            page.keyboard.press("Enter")
            # Wait for the selection to be processed
            page.wait_for_timeout(5000)

            # Click on "See prices"
            see_prices_button_selector = "a[data-baseweb='button'][text='See prices']"
            page.wait_for_selector(see_prices_button_selector, state="visible")
            # Extra delay to ensure everything is loaded
            page.wait_for_timeout(3000)
            page.click(see_prices_button_selector)
            page.wait_for_timeout(5000)  # Wait for the prices to load

            print("Prices should now be visible in the browser.")

            # Check if redirected to the login page and click "Continue with Google"
            google_login_button_selector = "button#google-login-btn"
            if page.is_visible(google_login_button_selector):
                with page.expect_popup() as popup_info:
                    page.click(google_login_button_selector)
                    print("Clicked 'Continue with Google'")
                google_popup = popup_info.value  # Get the new popup window

                # Wait for the Google login page to load in the new window
                google_popup.wait_for_load_state('networkidle')
                google_popup.wait_for_selector(
                    "input#identifierId", state="visible")

                # Input the Google account username (email)
                email_input_selector = "input#identifierId"
                google_popup.click(email_input_selector)
                google_popup.fill(email_input_selector,
                                  "rraiubusiness@gmail.com")

                # Click all the "Next" buttons on the page
                next_buttons = google_popup.locator("div.VfPpkd-RLmnJb")
                count = next_buttons.count()
                for i in range(count):
                    try:
                        next_buttons.nth(i).click()
                        print(f"Clicked 'Next' button {i + 1}")
                    except Exception as e:
                        print(f"Failed to click 'Next' button {i + 1}: {e}")

                # Continue with the rest of the login process as needed
                google_popup.wait_for_load_state('networkidle')

                # Switch back to the original window (if needed)
                page.bring_to_front()

        except Exception as e:
            print(f"Error during the process: {e}")
            # Capture a screenshot on error
            page.screenshot(path="error_screenshot.png")
        finally:
            # Leave the browser open for manual inspection if necessary
            print(
                "The browser will remain open for inspection. Press Ctrl+C to exit the script.")

        # Keep the browser open without closing it
        if context.pages:
            # Wait for 10 minutes or until you manually close it
            context.pages[0].wait_for_timeout(600000)
        else:
            print("No pages are open in the context to wait on.")


# Run the function to automate the process
automate_uber_with_google_login()
