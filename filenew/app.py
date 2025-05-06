# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests
from bs4 import BeautifulSoup
import os 
import shutil
import time 

app = Flask(__name__)

os.makedirs('templates', exist_ok=True)

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

# Mock function for demonstration; replace with your actual scraping logic
# Each restaurant is a dict with at least 'name' and 'type_of_food' keys
MOCK_RESTAURANTS = {
    city: [
        {"name": f"{city.split(',')[0]} Restaurant {i+1}", "type_of_food": "Italian" if i % 2 == 0 else "Chinese"}
        for i in range(10)
    ] for city in CITIES
}

def get_restaurants(city):
    return MOCK_RESTAURANTS.get(city, [])

@app.route("/", methods=["GET"])
def index():
    selected_city = request.args.get("city", CITIES[0])
    type_of_food = request.args.get("type_of_food", "")
    selected_restaurant_name = request.args.get("restaurant", "")

    # Get all restaurants for the selected city
    restaurants = get_restaurants(selected_city)

    # Filter by type_of_food if provided
    if type_of_food:
        restaurants = [r for r in restaurants if type_of_food.lower() in r.get("type_of_food", "").lower()]

    # Find the selected restaurant if any
    selected_restaurant = None
    if selected_restaurant_name:
        for r in restaurants:
            if r["name"] == selected_restaurant_name:
                selected_restaurant = r
                break

    return render_template(
        "webscraping.html",
        cities=CITIES,
        selected_city=selected_city,
        type_of_food=type_of_food,
        restaurants=restaurants,
        selected_restaurant=selected_restaurant
    )

@app.route("/")
@app.route("/home")

def home():
    try:
        url = 'https://www.yelp.com/search?find_desc=+Restaurants&find_loc=San+Jose%2C+CA'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers, timeout=15)

        # return render_template('webscraping.html')
    
        if 'You have been blocked' in response.text:
            print('You have been blocked, resorting to mock data instead')
            resturants = get_resturant_data()
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            resturant = []
            # this is looking for resturant listings
            resturant_elements = soup.select('div[data-testid="serp-ia-card"]')
            
            if resturant_elements:
                for element in resturant_elements[:10]:
                    try:
                        name_element = element.select_one('a[data-testid="header-link"]') or element.select_one('h3')
                        if not name_element:
                            continue
                        name = name_element.get_text().strip()

                        rating_element = element.selected_one('div[aria-label*="star rating"]')
                        rating = 4.0
                        if rating_element:
                            aria_label = rating_element.get('aria-label', '')
                            if 'star rating' in aria_label.lower():
                                parts = aria_label.split()
                                for part in parts:
                                    try:
                                        rating - float(part.replace(',','.'))
                                        break
                                    except ValueError:
                                        continue

                        # extract price and category 
                        price = '$'
                        category = 'Resturant'
                        price_category_element = element.select_one('p')
                        if price_category_element:
                            text = price_category_element.get_text().strip()
                            if '$' in text:
                                price_part = ""
                                for char in text:
                                    if char == '$':
                                        price_part += '$'
                                    elif price_part:
                                        break
                                if price_part:
                                    price = price_part
                            if "." in text:
                                parts = text.split(".")
                                if len(parts) > 1:
                                    category = parts[1].strip()
                        address = 'San Jose, CA'
                        address_element = element.select_one('address')
                        if address_element:
                            address = address_element.get_text().strip()

                        image_url = f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"
                        img_element = element.select_one('img')
                        if img_element and img_element.get('src'):
                            image_url = img_element.get('src')

                        resturant.append ({
                            'name': name,
                            'rating': rating,
                            'price': price,
                            'category': category,
                            'address': address,
                            "phone": f"(408) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                            "image_url": image_url
                            #'reviews': ['Great! amazing!'] 
                        })

                    except Exception as e:
                        print("Error with extracting data: "+e)
    except Exception as e:
        print(f'Error scraping Yelp: {e}')
        resturants = get_resturant_data()

        
                                

                                    
                                    
        # this is going to look for the 10 resturants
        if not resturant_elements:
            text_lines = response.text.split('\n')
            for i in range(1,11):
                prefix = f"{i}. "
                for prefix in text_lines:
                    # this is going to extract the names
                    start_idx = line.find(prefix)+len(prefix)
                    end_idx = line.find("(", start_idx) if line.find("(", start_idx) > -1 else len(line)
                    name = line[start_idx:end_idx].strip()

                    if name and len(name) > 0:
                        rating = round(random.uniform(3.5, 5.0), 1)

                        price = random.choice(["$", "$$", "$$$", "$$$$"])

                        categories = ['French', 'Vietnamese', 'Mexican', 'Chinese', 'Thai', 'Italian', 'Seafood', 'Asian Fusion', 'Cocktail Bars']
                        category = random.choice(categories)

                        resturant.append({
                            'name': name,
                            'rating': rating,
                            'price': price,
                            'category': category,
                            'address': f'{random.randint(100, 999)} Main St, San Jose, CA',
                            "phone": f"(408) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                            "image_url": f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"
                            # 'reviews': ['']
                        })
        if not resturant:
            print('no resturant was successfullt extracted')
        resturant = get_resturant_data()
    except Exception as e:
        print(f'Error scraping Yelp: {e}')
        resturant = get_resturant_data()
    return render_template('webscraping.html')
# returant data will run if the scraping fails
def get_resturant_data():
    return [
        {
            'name': 'Casa Juana',
            'rating': 2.8,
            'price': '$$',
            'category': 'Colobian',
            'address': '581 W Alma Ave San Jose, CA 95125',
            'phone': 'None',
            'image_url': 'https://s3-media0.fl.yelpcdn.com/bphoto/HYAEl-VoHjFLb6aXs-9HbA/348s.jpg',
            'reviews': ['Could be better']
        }
    ]


if __name__ == "__main__":
    app.run(debug=True)
