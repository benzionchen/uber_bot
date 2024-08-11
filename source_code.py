from playwright.sync_api import sync_playwright

# Global variable to track progress
progress_checkpoint = None


def save_progress(checkpoint):
    global progress_checkpoint
    progress_checkpoint = checkpoint
    print(f"Progress saved at: {checkpoint}")


def load_progress():
    global progress_checkpoint
    return progress_checkpoint


def automate_uber_with_google_login():
    global progress_checkpoint

    with sync_playwright() as p:
        # Define the path to the Google Chrome executable
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        # Launch Google Chrome in incognito mode
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
            # Load progress and decide where to start
            progress = load_progress()

            if progress == "password_screen":
                print("Resuming from the password screen...")

                # Input the password
                password_input_selector = "input[type='password']"
                page.wait_for_selector(
                    password_input_selector, state="visible")
                page.fill(password_input_selector, "38257448")
                print("Password entered.")

                # Click the correct "Next" button (Button 3) on the password screen
                next_buttons = page.locator("div.VfPpkd-RLmnJb")
                count = next_buttons.count()
                if count >= 3:
                    try:
                        # Click "Next button 3"
                        next_buttons.nth(2).click()
                        print("Clicked 'Next button 3' on the password screen")
                    except Exception as e:
                        print(
                            f"Failed to click 'Next button 3' on the password screen: {e}")

                # Continue the rest of the login process if any
                page.wait_for_load_state('networkidle')

            else:
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
                page.wait_for_selector(
                    see_prices_button_selector, state="visible")
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

                    # Click the correct "Next" button (Button 2) on the email screen
                    next_buttons = google_popup.locator("div.VfPpkd-RLmnJb")
                    count = next_buttons.count()
                    if count >= 2:
                        try:
                            # Click "Next button 2"
                            next_buttons.nth(1).click()
                            print("Clicked 'Next button 2' on the email screen")
                        except Exception as e:
                            print(
                                f"Failed to click 'Next button 2' on the email screen: {e}")

                    # Save progress after reaching the password screen
                    save_progress("password_screen")

                    # Proceed to the password screen after clicking "Next button 2"
                    # Wait for the password input to be visible
                    google_popup.wait_for_selector(
                        "input[type='password']", state="visible")
                    save_progress("password_screen")
                    print("Ready for password input.")

                    # Input the password
                    password_input_selector = "input[type='password']"
                    google_popup.click(password_input_selector)
                    google_popup.fill(password_input_selector, "38257448")
                    print("Password entered.")

                    # Click "Next button 3"
                    next_buttons = google_popup.locator("div.VfPpkd-RLmnJb")
                    if next_buttons.count() >= 3:
                        try:
                            next_buttons.nth(2).click()
                            print("Clicked 'Next button 3' on the password screen")
                        except Exception as e:
                            print(
                                f"Failed to click 'Next button 3' on the password screen: {e}")

                    # Continue the rest of the login process if any
                    google_popup.wait_for_load_state('networkidle')

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
