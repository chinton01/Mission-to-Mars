from flask import Flask, render_template, redirect
from flask_pymongo import PyMongo
import scraping
app = Flask(__name__)
# Use flask_pymongo to set up mongo connection
app.config["MONGO_URI"] = "mongodb://localhost:27017/mars_app"
mongo = PyMongo(app)


@app.route("/")
def index():
   print("we at home!")
   mars = mongo.db.mars.find_one()
   return render_template("index.html", mars=mars)


@app.route("/scrape")
def scrape():
   print("in scraping")
   try: 
      mars = mongo.db.mars
      mars_data = scraping.scrape_all()
      mars.update({}, mars_data, upsert=True)
   except Exception as e:
      print(e)
   return redirect('/', code=302)


#@app.route("/test")
#def test():
   #print("test")
   #return "test route"
if __name__ == "__main__":
   app.run(debug=True)
