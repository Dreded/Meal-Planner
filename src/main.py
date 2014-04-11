import webapp2
from views import CreatePlan,MainPage, CreateMeal, DeleteMeal, EditMeal

app = webapp2.WSGIApplication([
        ('/', MainPage), 
        ('/create', CreateMeal), 
        ('/edit/([\d]+)', EditMeal),
        ('/delete/([\d]+)', DeleteMeal),
        ('/plan', CreatePlan)
        ],
        debug=True)
