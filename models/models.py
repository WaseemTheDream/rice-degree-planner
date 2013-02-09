"""
Database storage for the app.
"""

from google.appengine.ext import db

class User(db.Model):
    net_id = db.StringProperty(required=True)

class Sticky(db.Model):
    user = db.ReferenceProperty(User,
                                required=True)
    time_added = db.DateTimeProperty(auto_now=True)
    title = db.StringProperty(required=True)
    note = db.TextProperty()

def get_user(net_id, create=False):
    user = User.gql('WHERE net_id=:1', net_id).get()
    if not user and create:
        user = User(net_id=net_id).put()
    return user