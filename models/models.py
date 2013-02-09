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

class Term(db.Model):
    code = db.StringProperty(required=True) # E.g. 201320
    description = db.StringProperty()       # E.g. Spring 2013

class Department(db.Model):
    name = db.StringProperty(required=True,
                             indexed=True)

def get_department(name, create=False):
    department = Department.gql('WHERE name=:1', name).get()
    if not department and create:
        department = Department(name=name)
        department.put()
    return department

class Subject(db.Model):
    code = db.StringProperty(required=True,    # E.g. COMP
                             indexed=True)

def get_subject(code, create=False):
    subject = Subject.gql('WHERE code=:1', code).get()
    if not subject and create:
        subject = Subject(code=code)
        subject.put()
    return subject

class Course(db.Model):
    subject = db.ReferenceProperty(Subject,
                                   required=True,
                                   collection_name='courses')
    number = db.StringProperty(required=True)     # E.g. 182
    terms = db.ListProperty(db.Key)      # List of terms its been taught
    xlink = db.StringProperty()
    credit_hours = db.IntegerProperty(required=True)

class CourseTaken(db.Model):
    user = db.ReferenceProperty(User, required=True ,
                                collection_name='courses_taken')
    course = db.ReferenceProperty(Course,required=True)
    term = db.ReferenceProperty(Term,required=True)