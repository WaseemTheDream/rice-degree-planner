"""
Database storage for the app.
"""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class User(db.Model):
    net_id = db.StringProperty(required=True)

def get_user(net_id, create=False):
    user = User.gql('WHERE net_id=:1', net_id).get()
    if not user and create:
        user = User(net_id=net_id).put()
    return user

class Course(db.Model):
    subject = db.ReferenceProperty(Subject, required=True)
    number = db.StringProperty(required=True)     # E.g. 182
    term = db.ListProperty(db.Key)      # List of terms its been taught
    description = db.TextProperty()
    xlink = db.StringProperty()
    credit_hours = db.IntegerProperty(required=True)

class Term(db.Model):
    code = db.StringProperty(required=True) # E.g. 201320
    description = db.StringProperty()       # E.g. Spring 2013

class Department(db.Model):
    name = db.StringProperty(required=True)

class Subject(db.Model):
    code = db.StringProperty(required=True)     # E.g. COMP