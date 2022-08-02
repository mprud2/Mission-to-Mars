from flask import Flask, render_template, redirect, url_for
from flask_pymongo import PyMongo
import scraping

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
    # tell Python that our app will connect to Mongo using a URI, a uniform resource identifier similar to a URL.
        # Set up URI we'll be using to connect our app to Mongo. 
        # This URI is saying that the app can reach Mongo through our localhost server, 
        # using port 27017, using a database named "mars_app"
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"

mongo = PyMongo(app)

# This route, @app.route("/"), tells Flask what to display when we're looking at the home page, index.html 
# (index.html is the default HTML file that we'll use to display the content we've scraped)
@app.route("/")
def index():
    # mars = mongo.db.mars.find_one() uses PyMongo to find the "mars" collection in our database
    # return render_template("index.html" tells Flask to return an HTML template using an index.html file. 
    # , mars=mars) tells Python to use the "mars" collection in MongoDB.
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)
# ^ This function is what links our visual representation of our work, our web app, to the code that powers it.

# define the route that Flask will be using. This route, “/scrape”, will run the function that we create just beneath it.
@app.route("/scrape")
def scrape():
   #assign a new variable that points to our Mongo database
   mars = mongo.db.mars
   # create a new variable to hold the newly scraped data
   mars_data = scraping.scrape_all()
   # Now that we've gathered new data, update the database
        # syntax we'll use: .update_one(query_parameter, {"$set": data}, options)
        # modify document ("$set") with the data in question
        # upsert=True tells Mongo to create a new document if one doesn't already exist
   mars.update_one({}, {"$set":mars_data}, upsert=True)
   # After scraping data, navigate back to homepage to see updated content
   return redirect('/', code=302)

# Provide code to tell Flask to run
if __name__ == "__main__":
app.run()