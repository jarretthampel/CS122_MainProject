# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for, jsonify
import json
import os
import requests
from bs4 import BeautifulSoup
import random
import time
import pandas as pd
from datetime import datetime
import math
import random

app = Flask(__name__)

os.makedirs('templates', exist_ok=True)

def get_mock_restaurant_locations():
    restaurant_data = [
        {
            "name": "Athena Grill Catering",
            "location": "Downtown"
        },
        {
            "name": "Casa Juana",
            "location": "Willow Glen"
        },
        {
            "name": "Fleming's Prime Steakhouse & Wine Bar",
            "location": "Santa Clara"
        },
        {
            "name": "Élyse Restaurant",
            "location": "Downtown"
        },
        {
            "name": "Blue Monkey Cafe & Restaurant",
            "location": "East San Jose"
        },
        {
            "name": "JOEY Valley Fair",
            "location": "West San Jose"
        },
        {
            "name": "Water Tower Kitchen",
            "location": "Campbell"
        },
        {
            "name": "The Grandview Restaurant",
            "location": "Los Gatos"
        },
        {
            "name": "Goodtime Bar",
            "location": "Downtown"
        },
        {
            "name": "Must be Thai",
            "location": "West San Jose"
        },
        {
            "name": "Eos & Nyx",
            "location": "Downtown"
        },
        {
            "name": "Jackie's Place",
            "location": "Downtown"
        },
        {
            "name": "Fox Tale Fermentation Project",
            "location": "Downtown"
        },
        {
            "name": "Benihana",
            "location": "Cupertino"
        }
    ]
    locations = sorted(set(r["location"] for r in restaurant_data))
    return locations

CITIES = get_mock_restaurant_locations()

# Function to scrape Yelp for restaurant data - now using mock data with real restaurant info
def scrape_yelp_restaurants(location="San Jose, CA", search_term="", limit=30):
    # Since Yelp blocks scraping (as seen in the screenshot), we'll use mock data with real restaurant info
    print('Using realistic mock data based on San Jose restaurants')
    return get_mock_restaurant_data(location, limit)

def get_mock_restaurant_data(location="San Jose, CA", limit=20):
    # Base coordinates for different cities
    city_coords = {
        "San Jose, CA": (37.3382, -121.8863),
        "San Francisco, CA": (37.7749, -122.4194),
        "Oakland, CA": (37.8044, -122.2711),
        "Berkeley, CA": (37.8715, -122.2730),
        "Palo Alto, CA": (37.4419, -122.1430),
        "Mountain View, CA": (37.3861, -122.0839),
        "Fremont, CA": (37.5485, -121.9886),
        "Sunnyvale, CA": (37.3688, -122.0363),
        "Santa Clara, CA": (37.3541, -121.9552),
        "Redwood City, CA": (37.4852, -122.2364),
        "Richmond, CA": (37.9357, -122.3477),
        "Pleasanton, CA": (37.6624, -121.8747),
        "San Ramon, CA": (37.7799, -121.9780),
        "Dublin, CA": (37.7021, -121.9357)
    }
    
    # Get base coordinates for the selected location
    base_lat, base_lng = city_coords.get(location, (37.3382, -121.8863))
    
    # Real San Jose restaurant data from the screenshots
    restaurant_data = [
        {
            "name": "Athena Grill Catering",
            "rating": 4.6,
            "review_count": 46,
            "price": "$$",
            "category": "Greek, Falafel, Caterers",
            "location": "Downtown",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/Ls0vBoGGa_vL3QlYq1x8xQ/348s.jpg",
            "lat_offset": 0.015,
            "lng_offset": 0.008
        },
        {
            "name": "Casa Juana",
            "rating": 3.0,
            "review_count": 16,
            "price": "$$",
            "category": "Colombian",
            "location": "Willow Glen",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/Sz_8YKQLGzMfmLeeoq43zA/348s.jpg",
            "lat_offset": -0.02,
            "lng_offset": 0.01
        },
        {
            "name": "Fleming's Prime Steakhouse & Wine Bar",
            "rating": 4.3,
            "review_count": 1200,
            "price": "$$$$",
            "category": "Steakhouses, Wine Bars, Seafood",
            "location": "Santa Clara",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/wrvbIfmyDAxF6M-AAOgHSQ/348s.jpg",
            "lat_offset": 0.01,
            "lng_offset": 0.02
        },
        {
            "name": "Élyse Restaurant",
            "rating": 4.4,
            "review_count": 506,
            "price": "$$",
            "category": "French, Vietnamese, Cocktail Bars",
            "location": "Downtown",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/-ryDQxwnP0xogwMN1C89Hg/348s.jpg",
            "lat_offset": -0.005,
            "lng_offset": -0.01
        },
        {
            "name": "Blue Monkey Cafe & Restaurant",
            "rating": 4.0,
            "review_count": 359,
            "price": "$$",
            "category": "Vietnamese",
            "location": "East San Jose",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/NSm93YsKOb2C53Qt6IJiMw/348s.jpg",
            "lat_offset": 0.025,
            "lng_offset": 0.015
        },
        {
            "name": "JOEY Valley Fair",
            "rating": 4.2,
            "review_count": 876,
            "price": "$$$",
            "category": "Sushi Bars, Steakhouses, Wine Bars",
            "location": "West San Jose",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/aJ8iQ1YtqUCiwsdndb5hyA/348s.jpg",
            "lat_offset": -0.015,
            "lng_offset": -0.02
        },
        {
            "name": "Water Tower Kitchen",
            "rating": 4.1,
            "review_count": 543,
            "price": "$$",
            "category": "New American, Sports Bars, Cocktail Bars",
            "location": "Campbell",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/mNKjS4IIPBX-WT2fsxfQFA/348s.jpg",
            "lat_offset": -0.025,
            "lng_offset": -0.01
        },
        {
            "name": "The Grandview Restaurant",
            "rating": 3.9,
            "review_count": 2200,
            "price": "$$$$",
            "category": "Venues & Event Spaces, Steakhouses, New American",
            "location": "Los Gatos",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/gsy_3gmpd7f_Y-Rey8RAbw/348s.jpg",
            "lat_offset": -0.03,
            "lng_offset": -0.025
        },
        {
            "name": "Goodtime Bar",
            "rating": 4.8,
            "review_count": 150,
            "price": "$$",
            "category": "Wine Bars, Tapas/Small Plates, Seafood",
            "location": "Downtown",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/lEEjBtL6qaBCYS_BC2CrnA/348s.jpg",
            "lat_offset": 0.005,
            "lng_offset": 0.005
        },
        {
            "name": "Must be Thai",
            "rating": 4.0,
            "review_count": 2300,
            "price": "$$",
            "category": "Thai, Seafood, Noodles",
            "location": "West San Jose",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/3cW19YDRs1O-sF2Unu8anw/348s.jpg",
            "lat_offset": 0.01,
            "lng_offset": -0.015
        },
        {
            "name": "Eos & Nyx",
            "rating": 4.2,
            "review_count": 289,
            "price": "$$$",
            "category": "Cocktail Bars, Breakfast & Brunch, New American",
            "location": "Downtown",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/cI-3vLaqaGZ3GAA8HjIHEQ/348s.jpg",
            "lat_offset": 0.002,
            "lng_offset": 0.008
        },
        {
            "name": "Jackie's Place",
            "rating": 4.4,
            "review_count": 1700,
            "price": "$$",
            "category": "Soul Food, Barbeque",
            "location": "Downtown",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/HAGJsU8qOir5qvMjr8vO3Q/348s.jpg",
            "lat_offset": -0.008,
            "lng_offset": 0.012
        },
        {
            "name": "Fox Tale Fermentation Project",
            "rating": 4.8,
            "review_count": 134,
            "price": "$$",
            "category": "Specialty Food, Vegetarian, Brewpubs",
            "location": "Downtown",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/qM81A51AeEgkHEAeJm8SJg/348s.jpg",
            "lat_offset": 0.007,
            "lng_offset": -0.007
        },
        {
            "name": "Benihana",
            "rating": 3.4,
            "review_count": 2700,
            "price": "$$$",
            "category": "Japanese, Sushi Bars, Teppanyaki",
            "location": "Cupertino",
            "image_url": "https://s3-media0.fl.yelpcdn.com/bphoto/oHFtt-32ptbcqJpbK_uzyw/348s.jpg",
            "lat_offset": -0.02,
            "lng_offset": 0.02
        }
    ]
    
    # Filter by location if specified
    if location:
        restaurant_data = [r for r in restaurant_data if r["location"] == location]

    restaurants = []
    
    for i, data in enumerate(restaurant_data[:limit]):
        # Generate coordinates based on the base location and offsets
        lat = base_lat + data["lat_offset"]
        lng = base_lng + data["lng_offset"]
        
        # Calculate popularity score
        popularity = data["review_count"] * (data["rating"] / 5)
        
        # Generate mock reviews
        reviews = [
            f"Great {data['category'].split(',')[0].lower()} restaurant!",
            f"I love their food and atmosphere. The service was excellent."
        ]
        
        restaurants.append({
            "name": data["name"],
            "rating": data["rating"],
            "review_count": data["review_count"],
            "price": data.get("price", ""),
            "category": data["category"],
            "address": f"{random.randint(100, 999)} {data['location']} St, {location}",
            "phone": f"({random.randint(200, 999)}) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
            "image_url": data["image_url"],
            "lat": lat,
            "lng": lng,
            "popularity": popularity,
            "reviews": reviews
        })
    
    # Sort by popularity
    restaurants.sort(key=lambda x: x['popularity'], reverse=True)
    return restaurants

def get_restaurant_categories(restaurants):
    """Extract unique categories from restaurant data"""
    all_categories = []
    for restaurant in restaurants:
        categories = restaurant.get('category', '').split(',')
        for category in categories:
            category = category.strip()
            if category and category not in all_categories:
                all_categories.append(category)
    return sorted(all_categories)

def analyze_restaurant_data(restaurants):
    """Generate analytics from restaurant data"""
    if not restaurants:
        return {
            'category_ratings': [],
            'price_distribution': {},
            'rating_distribution': {},
            'top_by_reviews': [],
            'top_by_rating': []
        }
    # Convert to DataFrame for easier analysis
    df = pd.DataFrame(restaurants)
    
    # Calculate average rating by category
    category_ratings = {}
    for restaurant in restaurants:
        categories = restaurant['category'].split(',')
        for category in categories:
            category = category.strip()
            if category not in category_ratings:
                category_ratings[category] = {'total': 0, 'count': 0}
            category_ratings[category]['total'] += restaurant['rating']
            category_ratings[category]['count'] += 1
    
    for category in category_ratings:
        category_ratings[category]['average'] = category_ratings[category]['total'] / category_ratings[category]['count']
    
    # Sort categories by average rating
    sorted_categories = sorted(category_ratings.items(), key=lambda x: x[1]['average'], reverse=True)
    
    # Calculate price distribution
    price_distribution = df['price'].value_counts().to_dict()
    
    # Calculate rating distribution
    rating_distribution = {}
    for rating in range(1, 6):
        rating_distribution[rating] = len(df[(df['rating'] >= rating - 0.5) & (df['rating'] < rating + 0.5)])
    
    # Get top 10 restaurants by review count
    top_by_reviews = df.sort_values('review_count', ascending=False).head(10).to_dict('records')
    
    # Get top 10 restaurants by rating (with at least 10 reviews)
    top_by_rating = df[df['review_count'] >= 10].sort_values('rating', ascending=False).head(10).to_dict('records')
    
    return {
        'category_ratings': sorted_categories,
        'price_distribution': price_distribution,
        'rating_distribution': rating_distribution,
        'top_by_reviews': top_by_reviews,
        'top_by_rating': top_by_rating
    }

@app.route("/")
@app.route("/home")
def home():
    # Get query parameters
    selected_city = request.args.get("city", CITIES[2])  # Default to San Jose
    search_term = request.args.get("search", "")
    category_filter = request.args.get("category", "")
    price_filter = request.args.get("price", "")
    selected_restaurant_name = request.args.get("restaurant", "")
    
    # Get restaurant data
    restaurants = scrape_yelp_restaurants(selected_city, search_term)
    
    # Apply filters if needed
    if category_filter:
        restaurants = [r for r in restaurants if category_filter.lower() in r.get('category', '').lower()]
    
    if price_filter:
        restaurants = [r for r in restaurants if r.get('price') == price_filter]
    
    # Get all unique categories
    categories = get_restaurant_categories(restaurants)
    
    # Find the selected restaurant if any
    selected_restaurant = None
    if selected_restaurant_name:
        for r in restaurants:
            if r["name"] == selected_restaurant_name:
                selected_restaurant = r
                break
    
    # Generate analytics data
    analytics = analyze_restaurant_data(restaurants)
    
    return render_template(
        "webscraping.html",
        cities=CITIES,
        selected_city=selected_city,
        search_term=search_term,
        categories=categories,
        category_filter=category_filter,
        price_filter=price_filter,
        restaurants=restaurants,
        selected_restaurant=selected_restaurant,
        analytics=analytics
    )

@app.route('/api/restaurants')
def get_restaurants_api():
    """API endpoint to get restaurant data as JSON"""
    city = request.args.get('city', 'San Jose, CA')
    search = request.args.get('search', '')
    restaurants = scrape_yelp_restaurants(city, search)
    return jsonify(restaurants)

@app.route('/api/analytics')
def get_analytics_api():
    """API endpoint to get analytics data as JSON"""
    city = request.args.get('city', 'San Jose, CA')
    search = request.args.get('search', '')
    restaurants = scrape_yelp_restaurants(city, search)
    analytics = analyze_restaurant_data(restaurants)
    return jsonify(analytics)

@app.route('/submit_review', methods=['POST'])
def submit_review():
    """Handle review submission"""
    restaurant_name = request.form.get('restaurant_name')
    review_text = request.form.get('review_text')
    rating = request.form.get('rating', 5)
    
    # In a real app, you would save this to a database
    print(f"New review for {restaurant_name}: {review_text} (Rating: {rating})")
    
    # Redirect back to the restaurant page
    return redirect(url_for('home', restaurant=restaurant_name))

if __name__ == "__main__":
    app.run(debug=True)
