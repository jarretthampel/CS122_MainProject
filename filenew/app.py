# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests
from bs4 import BeautifulSoup
import os 
import shutil
import time 
from datetime import datetime
import math

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
def scrape_yelp_restaurants(location="San Jose, CA",search_term="", limit=30):
    restaurants = []
    try:
        url = f'https://www.yelp.com/search?find_desc={search_term.replace(" ", "+")}+Restaurants&find_loc={location.replace(" ", "+")}'

        time.sleep(random.uniform(1,3))

        response = request.get(url,header=headers, timeout=20)

        if 'You have been blocked' in response.text:
            print('Yelp has blocked the request. Using mock data.')
            return get_mock_restaurant_data(location,limit)

        soup = BeautifulSoup(response.content, 'html.parser')

        restaurant_elements = soup.select('div[data-testid="serp-ia-card"]')

        if not restaurant_elements:
            restaurant_elements = soup.select('li.border-color--default__09f24__NPAKY')

        if not restaurant_elements:
            restaurant_elements = soup.select('div.container__09f24__mpR8_')

        if restaurant_elements:
            for element in restaurant_elements[:limit]:
                try:
                    name_element = element.slect_one('a[data-testid="header-link"]') or element.select_one('h3') or element.select_one('a.css-19v1rkv')
                    if not name_element:
                        continue
                    name = name_elementget_text().strip()

                    rating_element = element.select_one('div[aria-label*="star rating"]') or element.select_one('span.css-1e4fdj9')
                    rating = 4.0
                    if rating_element:
                        aria_label = rating_element.get('aria-label', '')
                        if 'star rating' in aria_label.lower():
                            for part in aria_label.split():
                                try:
                                    rating = float(part.replace(',','.'))
                                    break
                                except ValueError:
                                    continue
                    review_count_element = element.select_one('span.css-chan6m') or element.select_one('span[aria-label*="review"]')
                    review_count = random.radiant(10,500)
                    if review_count_element:
                        text = review_count_element.get_text().strip()
                        try:
                            review_count = int(''.join(filter(str.isdigit.text)))
                        except ValueError:
                            pass
                    # extract price and category
                    price = random.choice(['$','$$','$$$','$$$$'])
                    category = 'Restaurant'
                    price_category_element = element.select_one('p.css-16lklrv') or element.select_one('p')
                    if price_category_element:
                        text = price_category_element.get_text().strip()
                        if '$' in text:
                            price_part = ''
                            for char in text:
                                if char == '$':
                                    price_part += '$'
                                elif price_part:
                                    break
                            if price_part:
                                price = price_part

                        if '.' in text:
                            parts = text.split('.')
                            if len(parts) > 1:
                                category = parts[1].strip()
                    address = f'{random.radint(100,999)} Main St, {location}'
                    address_element = element.select_one('address') or element.selected_one('span.css-4g6ai3')
                    if address_element:
                        address = address_element.get_text().strip() or address
                    
                    image_url = f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"
                    img_element = element.select_one('img')
                    if img_element and img_element.get('src'):

                        image_url = img_element.get('src')

                    base_lat = 37.335480
                    base_lon = -121.893028

                    if "san Francisco" in location:
                        base_lat = 37.7749
                        base_lon = -122.4194
                    elif "Oakland" in location:
                        base_lat = 37.8044
                        base_lon = -122.2711
                    elif "Berkeley" in location:
                        base_lat = 37.8715
                        base_lon = -122.2730
                    elif "Palo Alto" in location:
                        base_lat = 37.4419
                        base_lon = -122.1430
                    
                    lat = base_lat + random.uniform(-0.0, 0.03)
                    lon = base_lon + random.unfiform(-0.03, 0.03)

                    popularity = review_count*(rating/5)

                    review = ['this is great']

                    resturant.append ({
                            'name': name,
                            'rating': rating,
                            'review_count': review_count,
                            'price': price,
                            'category': category,
                            'address': address,
                            "phone": f"(408) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                            "image_url": image_url,
                            'lon': lon,
                            'lat': lat,
                            'popularity': popularity,
                            'reviews': review
                            })
                except Exception as e:
                    print('Error from extracting restaurant: ' +e)
        if not restaurants:
            print("No restaurants were successfully extracted. Using mock data.")
            return get_mock_restaurant_data(location, limit)
            
    except Exception as e:
        print(f"Error scraping Yelp: {e}")
        return get_mock_restaurant_data(location, limit)
    
    restaurants.sort(key=lambda x: x['popularity'], reverse=True)
    return restaurants

def get_mock_restaurant_data(location="San Jose, CA"):
    # center coordinates for different cities
    city_coord = {
        'San Jose, CA': (37.335480,-121.893028),
        'San Francisco, CA': (37.784279,-122.407234),
        'Oakland, CA': (37.804363,-122.271111),
        'Berkley, CA': (37.871666,-122.272781),
        'Palo Alto, CA': (37.468319,-122.143936),
        "Mountain View, CA": (37.386051,-122.083855),
        "Fremont, CA": (37.548271,-121.988571),
        "Sunnyvale, CA": (37.368832,-122.036346),
        "Santa Clara, CA": (37.354107,-121.955238),
        "Redwood City, CA": (37.487846,-122.236115),
        "Richmond, CA": (37.935757,-122.347748),
        "Pleasanton, CA": (37.658435,-121.876997),
        "San Ramon, CA": (37.7747,-121.9735),
        "Dublin, CA": (37.702152,-121.935791)
    }

    # get base coords for the selected location

    base_lat, base_lon = city_coord.get(location, (37.335480, -121.893028))

    restaruant_names = ['Athena Grill Catering',
                        'Casa Juana',
                        'Fleming\'s Prime Steakhouse & Wine Bar',
                        'Élyse Restaurant',
                        'Blue Monkey Cafe & Restaurant',
                        'Joey Valley Fair',
                        'Water Tower Kitchen',
                        'The Grand View Restaurant',
                        'Goodtime Bar',
                        'Must be Thai',
                        'Eos & Nyx',
                        'Jackie\'s Place',
                        'Fox Tale Fermentation Project',
                        'Benihana'
    ]
    categories = [
        'Falafel, Caterers, Greek',
        'Colobian',
        'Wine Bars, Steakhouses,Seafood',
        'French, Vietnamese, Cocktail Bars',
        'Vietnamese',
        'Sushi Bars, Steakhouses, Wine Bars',
        'New American, Sports Bars, Cocktail Bar',
        'Venues & Event Spaces, Steakhouses, New American',
        'Wine Bars, Tapas/Small Plates, Seafood',
        'Thai, Seafood, Noodles',
        'Cocktail Bars, Breakfast & Brunch, New American',
        'Soul Food, Barbeque',
        'Specialty Food, Vegetarian Brewpubs'
        'Japanese, Sushi Bars, Teppanyaki'
    ]

    prices = ['$', '$$', '$$$', '$$$$']

    images = [
        'https://s3-media0.fl.yelpcdn.com/bphoto/Ls0vBoGGa_vL3QlYq1x8xQ/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/Sz_8YKQLGzMfmLeeoq43zA/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/offerphoto/wrvbIfmyDAxF6M-AAOgHSQ/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/-ryDQxwnP0xogwMN1C89Hg/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/NSm93YsKOb2C53Qt6IJiMw/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/aJ8iQ1YtqUCiwsdndb5hyA/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/mNKjS4IIPBX-WT2fsxfQFA/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/gsy_3gmpd7f_Y-Rey8RAbw/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/lEEjBtL6qaBCYS_BC2CrnA/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/3cW19YDRs1O-sF2Unu8anw/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/cI-3vLaqaGZ3GAA8HjIHEQ/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/HAGJsU8qOir5qvMjr8vO3Q/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/qM81A51AeEgkHEAeJm8SJg/348s.jpg',
        'https://s3-media0.fl.yelpcdn.com/bphoto/oHFtt-32ptbcqJpbK_uzyw/348s.jpg',
    ]

    
    


                                                                                                                



# Mock function for demonstration; replace with your actual scraping logic
# Each restaurant is a dict with all keys expected by the template
MOCK_RESTAURANTS = {
    city: [
        {
            "name": f"{city.split(',')[0]} Restaurant {i+1}",
            "type_of_food": "Italian" if i % 2 == 0 else "Chinese",
            "rating": round(4.0 + (i % 5) * 0.2, 1),
            "price": ["$", "$$", "$$$", "$$$$"][i % 4],
            "category": "Italian, Pizza" if i % 2 == 0 else "Chinese, Noodles",
            "image_url": "https://via.placeholder.com/400x200.png?text=Restaurant+Image",
            "address": f"{100+i} Main St, {city.split(',')[0]}",
            "phone": f"(555) 123-45{str(i).zfill(2)}"
        }
        for i in range(10)
    ] for city in CITIES
}

def get_restaurants(city):
    return MOCK_RESTAURANTS.get(city, [])

# Example template for real scraping (replace with your actual logic):
# def scrape_restaurant_data(city, type_of_food=None):
#     ...
#     for each_restaurant in scraped_results:
#         restaurant = {
#             "name": ...,
#             "type_of_food": ...,
#             "rating": ...,
#             "price": ...,
#             "category": ...,
#             "image_url": ...,
#             "address": ...,
#             "phone": ...
#         }
#         ...
#     return restaurant_list

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


@app.route('/map')
def map_page():
    return render_template('map.html')

if __name__ == "__main__":
    app.run(debug=True)
