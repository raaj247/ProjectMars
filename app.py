from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scrape_mars

app = Flask(__name__)

# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/craigslist_app"
mongo = PyMongo(app)



@app.route("/")
def index():
    marsDetails = mongo.db.marsDetails.find_one()
    return render_template("index.html", marsDetails=marsDetails)


@app.route("/scrape")
def scraper():
    marsDetails = scrape_mars.scrape()
    mongo.db.marsDetails.update({}, marsDetails, upsert=True)
    return redirect("/", code=302)


if __name__ == "__main__":
    app.run(debug=True)
