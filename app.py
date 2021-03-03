# dependencies
from flask_pymongo import PyMongo
from flask import Flask, render_template, redirect
import scrape_mars



# create instance of Flask app
app = Flask(__name__)


# Use flask_pymongo to set up mongo connection
mongo = PyMongo(app, uri="mongodb://localhost:27017/mars_app")


# create route that renders index.html template
@app.route("/")
def index():
    mars_scraped = mongo.db.collection.find_one()
    return render_template("index.html", mars_scraped=mars_scraped)


#scrape
@app.route("/scrape")
def scrape():
    mars_data = scrape_mars.scrape()
    mongo.db.collection.update({},mars_data, upsert=True)
    return redirect("/",code=302)


if __name__ == "__main__":
    app.run(debug=True)