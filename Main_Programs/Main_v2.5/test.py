import time
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager

def click_on_sunny():
    # Set up the Chrome driver
    service = Service(ChromeDriverManager().install())
    driver = webdriver.Chrome(service=service)

    try:
        # Open a web page (replace the URL with your target web page)
        driver.get("https://example.com")  # Replace with your target URL

        # Give the page some time to load
        time.sleep(2)

        # Find the element with the text "Sunny" and click on it
        sunny_element = driver.find_element(By.XPATH, "//*[text()='Sunny']")
        sunny_element.click()

        # Optionally, wait a bit after clicking
        time.sleep(2)

    except Exception as e:
        print(f"An error occurred: {e}")

    finally:
        # Close the browser
        driver.quit()

if __name__ == "__main__":
    click_on_sunny()