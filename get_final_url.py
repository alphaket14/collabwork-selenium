from selenium import webdriver
from selenium.webdriver.chrome.options import Options as ChromeOptions
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time # For optional explicit sleeps or debugging

# --- Configuration ---
# The appcast URL you want to resolve
APPCAST_URL = "https://click.appcast.io/t/T3ypiAgKZH2x6-XIGcE-sQ4sjEcRjXc9qOJhuzwmAlpC3J59Ct9xzE_ic1JapkvqkPAkooMhmzPOYpQ-FA5FYA=="
# The expected domain of the final URL (helps in waiting condition)
# Based on your example, the final URL is on 'execthread.com'
EXPECTED_FINAL_DOMAIN = "execthread.com"
# Maximum time to wait for redirection in seconds
WAIT_TIMEOUT = 30

def get_final_redirected_url(url_to_visit, expected_domain_in_final_url, timeout):
    """
    Navigates to a URL using headless Chrome and returns the final URL after redirects.
    """
    print("Setting up Chrome options for headless mode...")
    chrome_options = ChromeOptions()
    chrome_options.add_argument("--headless")  # Enable headless mode
    chrome_options.add_argument("--no-sandbox") # Essential for running in containers like Codespaces
    chrome_options.add_argument("--disable-dev-shm-usage") # Overcome limited resource problems in containers
    chrome_options.add_argument("--disable-gpu") # Generally good practice for headless
    chrome_options.add_argument("window-size=1920x1080") # Set a reasonable window size
    # You can set a common user-agent if needed, though default Selenium one often works
    # chrome_options.add_argument("user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/98.0.4758.102 Safari/537.36")

    driver = None  # Initialize driver to None for robust error handling in finally block

    try:
        print(f"Initializing Chrome WebDriver (Selenium Manager should handle ChromeDriver)...")
        # Selenium Manager (Selenium 4.6.0+) will attempt to download
        # the correct ChromeDriver if Google Chrome is installed and no driver is found on PATH.
        driver = webdriver.Chrome(options=chrome_options)
        print("Chrome WebDriver initialized successfully in headless mode.")

        print(f"Navigating to initial URL: {url_to_visit}")
        driver.get(url_to_visit)
        initial_url_loaded = driver.current_url
        print(f"Loaded initial URL: {initial_url_loaded}. Waiting for redirection...")

        # Wait until the URL changes from the initial appcast domain
        # and contains the expected final domain.
        WebDriverWait(driver, timeout).until(
            EC.url_contains(expected_domain_in_final_url)
            # You could add more conditions, e.g.,
            # lambda d: expected_domain_in_final_url in d.current_url and "appcast.io" not in d.current_url
        )
        
        final_url = driver.current_url
        print(f"Redirection complete. Final URL: {final_url}")
        return final_url

    except Exception as e:
        print(f"An error occurred during the process: {e}")
        if driver:
            current_url_on_error = driver.current_url
            print(f"Current URL at time of error: {current_url_on_error}")
            # For debugging in Codespaces, you might save a screenshot if an error occurs
            # driver.save_screenshot("error_screenshot.png")
            # print("Error screenshot saved as error_screenshot.png (if path is writable)")
        return None
    finally:
        if driver:
            print("Closing the browser...")
            driver.quit()
            print("Browser closed.")

if __name__ == "__main__":
    print("Starting the URL resolution process...")
    final_destination_url = get_final_redirected_url(APPCAST_URL, EXPECTED_FINAL_DOMAIN, WAIT_TIMEOUT)

    if final_destination_url:
        print(f"\nSuccessfully retrieved final URL: {final_destination_url}")
    else:
        print("\nFailed to retrieve the final URL.")