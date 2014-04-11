from google.appengine.ext import db

class Meals(db.Model):
    name = db.StringProperty()
    price = db.StringProperty()
    type = db.StringListProperty()
    ingredients = db.StringListProperty()
    recipe = db.StringListProperty()
    nutritional = db.StringListProperty()