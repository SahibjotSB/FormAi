from playwright.sync_api import sync_playwright

def run():
    with sync_playwright() as p:
        browser = p.chromium.launch(headless=False)  # Launch browser visibly
        page = browser.new_page()
        page.goto('http://example.com')
        print(page.title())  # Should print 'Example Domain'
        browser.close()

run()
