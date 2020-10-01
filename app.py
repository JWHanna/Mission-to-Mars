# Import dependencies 
from flask import Flask, render_template
from flask_pymongo import PyMongo
import scraping.py

# Flask setup
app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
    # Tells Python that our app will connect to Mongo using a URI, 
    # a uniform resource identifier similar to a URL
mongo = PyMongo(app)

# Setup App Routes

# Welcome route
@app.route("/")
def index():
   mars = mongo.db.mars.find_one()
    # Uses PyMongo to find the “mars” collection in database
   return render_template("index.html", mars=mars)
    # tells Flask to return an HTML template using an index.html file
    # mars=mars tells python to use "mars" collection

# Scrape route
@app.route("/scrape")
def scrape():
   mars = mongo.db.mars
   mars_data = scraping.scrape_all()
   mars.update({}, mars_data, upsert=True)
   return "Scraping Successful!"

# Run Flask
if __name__ == "__main__":
   app.run()