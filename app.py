from flask import Flask, request, render_template, jsonify, json, make_response, render_template_string
from bs4 import BeautifulSoup
import requests
from requests import status_codes
import main

app = Flask(__name__)
app.config["DEBUG"] = True

def getReviews(url):
    try:
        soup = main.setup(url)
        if (soup == 0):
            return render_template('home.html', data = "Please enter a valid URL beginning with https://www.")
    except:
        return render_template_string("{{ e }}")
    try:
        json = main.extractsoup(soup)                
        if (json == 0):
            return render_template('home.html', data = "Uh oh. Three things could have happened here. <br> 1. You entered the wrong URL, <br> 2. This lender has no reviews, <br> 3. You have entered a page number passed the max")
    except:
        return render_template_string("{{ e }}")
    return render_template('home.html', data = json)

@app.route('/', methods = ["GET", "POST"])
def get_data():
    if request.method == "POST":
        url = request.form['url']
        return getReviews(url)
    elif request.args.get("url"):
        url = request.args.get("url")
        return getReviews(url)
    else:
        return render_template('home.html')


@app.errorhandler(403)
def forbidden(e):
    return jsonify(error=str(e)), 403
@app.errorhandler(404, )
def resource_not_found(e):
    app.logger.info(f"Page not found: {request.url}")
    return jsonify(error=str(e)), 404
@app.errorhandler(500)
def server_error(e):
    app.logger.error(f"Server error: {request.url}")
    return jsonify(error=str(e)), 500

app.run()