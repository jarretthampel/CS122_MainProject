from os import access
import jwt.utils
import math
import requests
from flask import Flask, render_template, request
import time
import pandas as pd
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

app = Flask(__name__)

# List of Bay Area cities for the dropdown
CITIES = [
    "San Francisco, CA",
    "Oakland, CA",
    "San Jose, CA",
    "Berkeley, CA",
    "Palo Alto, CA",
    "Mountain View, CA",
    "Fremont, CA",
    "Sunnyvale, CA",
    "Santa Clara, CA",
    "Redwood City, CA",
    "Richmond, CA",
    "Pleasanton, CA",
    "San Ramon, CA",
    "Dublin, CA"
]

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
                
                # Try to extract type of food and price range
                try:
                    # This is often in a span with class "fontBodyMedium" near the top, or in a div with aria-label
                    details = driver.find_elements(By.CLASS_NAME, "fontBodyMedium")
                    type_of_food = None
                    price_range = None
                    for d in details:
                        text = d.text
                        # Price range is usually like "$", "$$", etc.
                        if "$" in text and len(text) <= 4:
                            price_range = text.strip()
                        # Type of food is usually a word or phrase, not containing $ or numbers
                        elif text and not any(char.isdigit() for char in text) and "$" not in text and len(text) < 30:
                            type_of_food = text.strip()
                    # Sometimes both are in the same element, e.g. "Italian · $$"
                    if not type_of_food or not price_range:
                        for d in details:
                            text = d.text
                            if "·" in text:
                                parts = [p.strip() for p in text.split("·")]
                                for p in parts:
                                    if "$" in p and len(p) <= 4:
                                        price_range = p
                                    elif p and not any(char.isdigit() for char in p) and "$" not in p and len(p) < 30:
                                        type_of_food = p
                except:
                    type_of_food = None
                    price_range = None
                
                restaurants.append({
                    'name': name,
                    'rating': rating,
                    'reviews': reviews,
                    'type_of_food': type_of_food,
                    'price_range': price_range
                })
                
            except Exception as e:
                print(f"Error processing restaurant: {e}")
                continue
                
    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        driver.quit()
        
    return restaurants

@app.route('/', methods=['GET', 'POST'])
def index():
    selected_city = CITIES[0]
    type_of_food = ''
    price_range = ''
    restaurants = []
    if request.method == 'POST':
        selected_city = request.form.get('location', CITIES[0])
        type_of_food = request.form.get('type_of_food', '').strip()
        price_range = request.form.get('price_range', '').strip()
        all_restaurants = scrape_restaurant_data(selected_city)
        # Filter by type_of_food and price_range if provided
        restaurants = []
        for r in all_restaurants:
            matches_type = True
            matches_price = True
            if type_of_food:
                matches_type = r.get('type_of_food') and type_of_food.lower() in r['type_of_food'].lower()
            if price_range:
                matches_price = r.get('price_range') == price_range
            if matches_type and matches_price:
                restaurants.append(r)
    return render_template('index.html', cities=CITIES, selected_city=selected_city, type_of_food=type_of_food, price_range=price_range, restaurants=restaurants)

if __name__ == "__main__":
    app.run(debug=True)