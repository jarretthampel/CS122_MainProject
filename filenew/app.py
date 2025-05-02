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

os.makedirs('templets', exist_ok=True)



@app.route("/")
@app.route("/home")

def home():
    try:
        url = 'https://www.yelp.com/search?find_desc=+Restaurants&find_loc=San+Jose%2C+CA'
        headers = {'User-Agent': 'Mozilla/5.0'}
        response = requests.get(url, headers=headers)

        return render_template('webscraping.html')
    
        if 'You have been blocked' in reposne.text:
            print('You have been blocked, resorting to mock data instead')
            returants = resturant_data()
        else:
            soup = BeautifulSoup(response.content, "html.parser")
            resturant = []
            # this is looking for resturant listings
            resturant_elements = soup.select('div[data-testid="serp-ia-card"]')
        # this is going to lok for the 10 resturants
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
                        categgory = random.choice(categories)

                        resturant.append({
                            'name': name,
                            'rating': rating,
                            'price': price,
                            'category': category,
                            'address': f'{random.randint(100, 999)} Main St, San Jose, CA',
                            "phone": f"(408) {random.randint(200, 999)}-{random.randint(1000, 9999)}",
                            "image_url": f"https://via.placeholder.com/150?text={name.replace(' ', '+')}"
                            # 'reviews': ['Could be better']
                        })
        if not resturants:
            print('no resturant was successfullt extracted')
        resturant = get_resturant_data()
    except Exception as e:
        print(f'Error scraping Yelp: {e}')
        resturant = get_resturant_data()
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
