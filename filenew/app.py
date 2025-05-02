# import the Flask class from the flask module
from flask import Flask, render_template, request, redirect, url_for
import json
import os
import requests
from bs4 import BeautifulSoup
import os 
import shutil
import time 
import re 

app = Flask(__name__)

os.makedirs('templets', exist_ok=True)

# returant data will run if the scraping fails
resturants = [
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

@app.route("/")
@app.route("/home")

def home():
    try:
        url = 'https://www.yelp.com/search?find_desc=+Restaurants&find_loc=San+Jose%2C+CA'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)
        
        businesses = soup.find_all('a', class_='css-19v1rkv')
        names = []
        for biz in businesses:
            name = biz.get_text()
            if name and name not in names:
                names.append(name)

        return render_template('webscraping.html', restaurants=names)
    
        if 'You have been blocked' in reposne.text:
            print('You have been blocked, resorting to mock data instead')
            returants = resturant_data()
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            resturant = []
            resturant_elements = soup.select('div[data-testid="serp-ia-card"]')
            


if __name__ == "__main__":
    app.run(debug=True)
