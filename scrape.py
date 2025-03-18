from selenium.webdriver import Remote, ChromeOptions
from selenium.webdriver.chromium.remote_connection import ChromiumRemoteConnection
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from bs4 import BeautifulSoup
import time

AUTH = 'brd-customer-hl_feaaa768-zone-scraping_browser1:gteqgj15x295'
SBR_WEBDRIVER = f'https://{AUTH}@brd.superproxy.io:9515'

def check_for_captcha(driver):
    """Check for captcha iframe on the page."""
    try:
        WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.CSS_SELECTOR, 'iframe[src*="recaptcha"]'))
        )
        print("Captcha detected!")
        return True
    except:
        return False

def scrape_website(website):
    """Scrape website content."""
    print("Launching Chrome browser...")
    try:
        print('Connecting to Scraping Browser...')
        sbr_connection = ChromiumRemoteConnection(SBR_WEBDRIVER, 'goog', 'chrome')
        options = ChromeOptions()
        options.add_argument('--headless')  # Run in headless mode to avoid UI issues
        options.add_argument('--disable-blink-features=AutomationControlled')  # Avoid bot detection

        # Connect to the Remote WebDriver
        with Remote(sbr_connection, options=options) as driver:
            driver.get(website)

            # Check if captcha is present
            if check_for_captcha(driver):
                print("Captcha detected. Please solve it manually or use a captcha-solving service.")
                time.sleep(60)  # Wait for manual solving
            else:
                print("No captcha detected. Proceeding with scraping...")

            # Scrape the page content
            html = driver.page_source
            return html

    except Exception as e:
        print(f"Error occurred: {e}")
        return None

def extract_body_content(html_content):
    """Extract the main body content from HTML."""
    soup = BeautifulSoup(html_content, "html.parser")
    return str(soup.body) if soup.body else ""

def clean_body_content(body_content):
    """Clean the scraped body content by removing scripts, styles, and HTML tags."""
    soup = BeautifulSoup(body_content, "html.parser")

    # Remove script and style elements
    for script_or_style in soup(["script", "style"]):
        script_or_style.extract()

    # Extract only visible text
    cleaned_content = soup.get_text(separator="\n")
    cleaned_content = "\n".join(
        line.strip() for line in cleaned_content.splitlines() if line.strip()
    )

    return cleaned_content

def split_dom_content(dom_content, max_length=6000):
    """Split the cleaned content into chunks if needed."""
    return [dom_content[i:i + max_length] for i in range(0, len(dom_content), max_length)]
