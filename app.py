from flask import Flask, request, render_template, jsonify, render_template_string
import main

app = Flask(__name__)

# get reviews from url
def getReviews(url):
    try:
        soup = main.setup(url)
        # when URL informat is invalid
        if (soup == 0):
            return render_template('home.html', data = "Please enter a valid URL beginning with https://www.")
    except:
        return render_template_string("{{ e }}")
    try:
        json = main.extractsoup(soup)
        # When json output is invalid                 
        if (json == 0):
            return render_template('home.html', data = "Uh oh. Three things could have happened here. <br> 1. You entered the wrong URL, <br> 2. This lender has no reviews, <br> 3. You have entered a page number passed the max")
    except:
        return render_template_string("{{ e }}")
    return json

@app.route('/', methods = ["GET", "POST"])
def get_data():
    #Post method for using the testing functionality
    if request.method == "POST":
        url = request.form['url']
        json = getReviews(url)
        return render_template('home.html', data=json)
    #Get method for returning full json output
    elif request.args.get("url"):
        #Append optional paramaters in url with /?url=
        url = request.args.get("url")
        json =  getReviews(url)
        return jsonify(json)
    else:
        return render_template('home.html')

#Generic error handling
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

# uncomment for local testing.
# app.run()