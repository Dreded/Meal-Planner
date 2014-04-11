import jinja2
import os
import webapp2
from time import sleep
from datetime import datetime
from google.appengine.ext import db

from models import Meals
DEFAULT_KEY = 'MealLists';
TEMPLATE_DIR = os.path.join(os.path.dirname(__file__), 'templates')
jinja_environment = \
    jinja2.Environment(loader=jinja2.FileSystemLoader(TEMPLATE_DIR))


class BaseHandler(webapp2.RequestHandler):

    @webapp2.cached_property
    def jinja2(self):
        return jinja2.get_jinja2(app=self.app)

    def render_template(
        self,
        filename,
        template_values,
        **template_args
        ):
        template = jinja_environment.get_template(filename)
        self.response.out.write(template.render(template_values))


class MainPage(BaseHandler):

    def get(self):
        meals = Meals.all()
        self.render_template('index.html', {'meals': meals})


class CreatePlan(BaseHandler):
    def get(self):
        meals = Meals.all()
        lunch = []
        breakfast = []
        dinner = []
        snack = []
        for meal in meals:
            if "Lunch" in meal.type:
                lunch.append(meal)
            if "Breakfast" in meal.type:
                breakfast.append(meal)
            if "Dinner" in meal.type:
                dinner.append(meal.name)
            if "Snack" in meal.type:
                '''snack.append(meal.key().id())'''
                snack.append(meal.name)
        self.render_template('plan.html', {'lunch': lunch,'breakfast': breakfast,'dinner': dinner,'snack': snack,'meals': meals})
        


class CreateMeal(BaseHandler):

    def post(self):
        n = Meals(name=self.request.get('name'),
                  price=self.request.get('price'),
                  type=self.request.get_all('type'),
                  ingredients=self.request.get_all('ingredients'),
                  recipe=self.request.get_all('recipe'),
                  nutritional=self.request.get_all('nutritional'))
        n.put()
        sleep(0.1)
        return webapp2.redirect('/')

    def get(self):
        self.render_template('create.html', {})


class EditMeal(BaseHandler):

    def post(self, meal_id):
        iden = int(meal_id)
        meal = db.get(db.Key.from_path('Meals', iden))
        meal.name = self.request.get('name')
        meal.price = self.request.get('price')
        meal.type = self.request.get_all('type')
        meal.ingredients = self.request.get_all('ingredients')
        meal.recipe = self.request.get_all('recipe')
        meal.nutritional = self.request.get_all('nutritional')
        meal.put()
        sleep(0.1)
        return webapp2.redirect('/')

    def get(self, meal_id):
        iden = int(meal_id)
        meal = db.get(db.Key.from_path('Meals', iden))
        self.render_template('edit.html', {'meal': meal})


class DeleteMeal(BaseHandler):

    def get(self, meal_id):
        iden = int(meal_id)
        meal = db.get(db.Key.from_path('Meals', iden))
        db.delete(meal)
        sleep(0.1)
        return webapp2.redirect('/')
