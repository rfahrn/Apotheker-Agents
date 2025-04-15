from playwright.sync_api import sync_playwright

with sync_playwright() as p:
    browser = p.chromium.launch()
    page = browser.new_page()
    page.goto("https://compendium.ch/product/1450988-dafalgan-extra-filmtabl-500-65-mg")
    print(page.title())
    browser.close()
