# import the Flask class from the flask module
from flask import Flask, render_template, request, render_template_string

from os import access
import requests
from bs4 import BeautifulSoup
import os 
import shutil

app = Flask(__name__)


@app.route("/")
@app.route("/home")

def home():
    url = 'https://www.yelp.com/search?find_desc=+Restaurants&find_loc=San+Jose%2C+CA'
    headers = {'User-Agent': 'Mozilla/5.0'}
    response = requests.get(url, headers=headers)
    print(response)
    soup = BeautifulSoup(response.content, "html.parser")
    businesses = soup.find_all('a', class_='css-19v1rkv')

    names = []
    for biz in businesses:
        name = biz.get_text()
        if name and name not in names:
            names.append(name)

    return render_template_string('webscraping.html', restaurants=names)


if __name__ == "__main__":
    app.run(debug=True)