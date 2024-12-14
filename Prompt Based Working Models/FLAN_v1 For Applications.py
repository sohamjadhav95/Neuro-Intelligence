from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from webdriver_manager.chrome import ChromeDriverManager
import time


def interact_with_twitter():
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))
    driver.get("https://twitter.com/login")
    time.sleep(2)

    # Login process
    username_field = driver.find_element(By.NAME, "text")
    username_field.send_keys("Soham_Jadhav_95")  # Replace with your username
    username_field.send_keys(Keys.RETURN)
    time.sleep(2)

    password_field = driver.find_element(By.NAME, "password")
    password_field.send_keys("Soham@987*#")  # Replace with your password
    password_field.send_keys(Keys.RETURN)
    time.sleep(5)

    # Search for "machine learning"
    search_box = driver.find_element(By.XPATH, "//input[@aria-label='Search query']")
    search_box.send_keys("machine learning")
    search_box.send_keys(Keys.RETURN)
    time.sleep(3)

    # Like and comment on first 5 posts
    tweets = driver.find_elements(By.XPATH, "//article")[:5]
    for tweet in tweets:
        try:
            like_button = tweet.find_element(By.XPATH, ".//div[@data-testid='like']")
            like_button.click()
            print("Liked a tweet.")
        except Exception as e:
            print(f"Error interacting with tweet: {e}")




if __name__ == "__main__":
    
    print("\nInteracting with Twitter...")
    interact_with_twitter()

