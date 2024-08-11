from playwright.sync_api import sync_playwright


def visit_uber(num_visits):
    with sync_playwright() as p:
        # Define the path to the Google Chrome executable
        chrome_path = "C:/Program Files/Google/Chrome/Application/chrome.exe"

        # Launch Google Chrome in incognito mode
        browser = p.chromium.launch(
            executable_path=chrome_path,
            headless=False,
            args=['--incognito']
        )

        # Create a single context that will be reused
        context = browser.new_context(viewport={"width": 1280, "height": 800})

        for i in range(num_visits):
            print(f"Visit {i+1}")

            page = context.new_page()
            try:
                page.goto("https://www.uber.com")

                # Wait for the page to load completely
                page.wait_for_timeout(8000)

                # Use the aria-label attribute to find the pickup location input field
                pickup_input_selector = "input[aria-label='Pickup location']"
                page.click(pickup_input_selector)
                page.fill(pickup_input_selector, "333 Market Street")
                # Wait for dropdown suggestions to load
                page.wait_for_timeout(3000)

                # Simulate selecting the first suggestion from the dropdown
                page.keyboard.press("ArrowDown")
                page.keyboard.press("Enter")
                # Wait for the selection to be processed
                page.wait_for_timeout(5000)

                # Use the same method for the drop-off location
                # Assuming similar structure for drop-off
                dropoff_input_selector = "input[aria-label='Dropoff location']"
                page.click(dropoff_input_selector)
                page.fill(dropoff_input_selector, "425 Mission St")
                # Wait for dropdown suggestions to load
                page.wait_for_timeout(3000)

                # Simulate selecting the first suggestion from the dropdown
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
                    page.click(google_login_button_selector)
                    print("Clicked 'Continue with Google'")

                    # Wait for the Google login page to load
                    page.wait_for_selector(
                        "input#identifierId", state="visible")
                    page.wait_for_timeout(2000)

                    # Use JavaScript to input the email directly
                    page.evaluate("""
                    const emailField = document.getElementById('identifierId');
                    emailField.value = 'rraiubusiness@gmail.com';
                    emailField.dispatchEvent(new Event('input', { bubbles: true }));
                    """)
                    page.wait_for_timeout(2000)

                    # Click the "Next" button (using the correct selector)
                    next_button_selector = "div.VfPpkd-RLmnJb"
                    page.click(next_button_selector)
                    print("Entered Google email and clicked 'Next'")

            except Exception as e:
                print(f"Error during visit {i+1}: {e}")
                # Capture a screenshot on error
                page.screenshot(path="error_screenshot.png")
            finally:
                # Leave the browser open for manual inspection
                print(
                    "The browser will remain open. You can check the prices manually. Press Ctrl+C to exit the script.")

        # Keep the browser open without closing it
        if context.pages:
            # Wait for 10 minutes or until you manually close it
            context.pages[0].wait_for_timeout(600000)
        else:
            print("No pages are open in the context to wait on.")


# Set the number of visits
number_of_visits = 1

visit_uber(number_of_visits)
