# import the Flask class from the flask module
from flask import Flask

# import the render_template function
from flask import render_template, request


app = Flask(__name__)

@app.route("/")
@app.route("/home")



if __name__ == '__main__':
    app.run(debug=True)