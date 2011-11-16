
from google.appengine.ext import db

class User(db.Model):
    name = db.StringProperty()
    update_time = db.DateTimeProperty()
    url = db.TextProperty()
    is_active = db.BooleanProperty()