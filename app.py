from os import access
import jwt.utils
import time
import math
import requests
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import pandas as pd

def setup_driver():
    # Setup Chrome options
    options = webdriver.ChromeOptions()
    options.add_argument('--headless')  # Run in headless mode (no GUI)
    options.add_argument('--disable-gpu')
    return webdriver.Chrome(options=options)

def scrape_restaurant_data(location):
    driver = setup_driver()
    restaurants = []
    
    try:
        # Navigate to Google Maps
        driver.get('https://www.google.com/maps')
        
        # Wait for search box and enter query
        search_box = WebDriverWait(driver, 10).until(
            EC.presence_of_element_located((By.ID, "searchboxinput"))
        )
        search_box.send_keys(f"restaurants in {location}")
        search_box.send_keys(Keys.ENTER)
        
        # Wait for results to load
        time.sleep(5)
        
        # Find restaurant elements
        restaurant_elements = driver.find_elements(By.CLASS_NAME, "hfpxzc")
        
        # Iterate through first 10 restaurants
        for element in restaurant_elements[:10]:
            try:
                element.click()
                time.sleep(2)  # Wait for details to load
                
                # Extract restaurant information
                name = driver.find_element(By.CLASS_NAME, "fontHeadlineLarge").text
                try:
                    rating = driver.find_element(By.CLASS_NAME, "fontDisplayLarge").text
                except:
                    rating = "No rating"
                    
                try:
                    reviews = driver.find_element(By.CLASS_NAME, "fontBodyMedium").text
                except:
                    reviews = "No reviews"
                
                restaurants.append({
                    'name': name,
                    'rating': rating,
                    'reviews': reviews
                })
                
            except Exception as e:
                print(f"Error processing restaurant: {e}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()
        
    return restaurants

def main():
    # Specify the location you want to search
    location = "San Francisco, CA"
    
    # Scrape restaurant data
    results = scrape_restaurant_data(location)
    
    # Convert to DataFrame and save to CSV
    df = pd.DataFrame(results)
    df.to_csv('restaurants.csv', index=False)
    print("Results saved to restaurants.csv")
    
    # Print results
    for restaurant in results:
        print(f"Name: {restaurant['name']}")
        print(f"Rating: {restaurant['rating']}")
        print(f"Reviews: {restaurant['reviews']}")
        print("-" * 50)

if __name__ == "__main__":
    main()