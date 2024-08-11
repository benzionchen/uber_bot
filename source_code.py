from playwright.sync_api import sync_playwright


def visit_uber(num_visits):
    with sync_playwright() as p:
        # Launch browser in incognito mode without proxy
        browser = p.chromium.launch(headless=False, args=['--incognito'])

        # Create a single context that will be reused
        context = browser.new_context(viewport={"width": 1280, "height": 800})

        for i in range(num_visits):
            print(f"Visit {i+1}")

            page = context.new_page()
            try:
                page.goto("https://www.uber.com")
                # Wait for the page to load (adjust as needed)
                page.wait_for_timeout(5000)
            except Exception as e:
                print(f"Error during visit {i+1}: {e}")
            finally:
                page.close()

        # Keep the browser open for manual login or further interaction
        print("The browser will remain open for manual login. Press Ctrl+C to exit the script.")
        # Wait for a long time to keep the window open
        context.pages[0].wait_for_timeout(600000)

        browser.close()


# Set the number of visits
number_of_visits = 100

visit_uber(number_of_visits)

# in icognito mode, ran 100 times safely without triggering bot detection or 2FA
