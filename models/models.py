"""
Database storage for the app.
"""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class User(db.Model):
    net_id = db.StringProperty(required=True)


class Term(db.Model):
    code = db.StringProperty(required=True) # E.g. 201320
    description = db.StringProperty()       # E.g. Spring 2013


class Department(db.Model):
    name = db.StringProperty(required=True,
                             indexed=True)


class Subject(db.Model):
    code = db.StringProperty(required=True,    # E.g. COMP
                             indexed=True)


class Course(db.Model):
    subject = db.ReferenceProperty(Subject,
                                   required=True,
                                   collection_name='courses')
    number = db.StringProperty(required=True)     # E.g. 182
    terms = db.ListProperty(db.Key)      # List of terms its been taught
    xlink = db.StringProperty()
    credit_hours = db.IntegerProperty(required=True)


class CourseTaken(db.Model):
    user = db.ReferenceProperty(User,
                                required=True,
                                collection_name='courses_taken')
    course = db.ReferenceProperty(Course,
                                  required=True)
    term = db.ReferenceProperty(Term,required=True)


class Requirement(polymodel.PolyModel):
    name = db.StringProperty(required=True)     # Requirement name
    description = db.StringProperty()

    def progress(self, courses_taken):
        """
        Determines the progress of the user in a certain requirement.

        Args:
            courses_taken {List<Course>}: list of courses taken

        Returns:
            max_credits_required: maximum number of total credits required to fulfill
            min_credits_required: minimum number of total credits required to fulfill
            credits_taken: number of credits taken towards degree
            courses_taken: courses taken that fulfill requirements
        """
        raise NotImplementedError('Abstract method')


class RequirementFromCourses(Requirement):
    _options = db.ListProperty(db.Key)
    _num_required = db.IntegerProperty(required=True)

    def __init__(self, num_required, options):
        """
        Constructor.

        Args:
            num_required {Integer}: number of courses required
            options {List<Course>}: list of options
        """
        assert(num_required < len(options))
        self._num_required = num_required
        for course in options:
            self._options.append(course.key())

    def progess(self, courses_taken):
        credit_list = []
        return None


def get_user(net_id, create=False):
    user = User.gql('WHERE net_id=:1', net_id).get()
    if not user and create:
        user = User(net_id=net_id).put()
    return user


def get_department(name, create=False):
    department = Department.gql('WHERE name=:1', name).get()
    if not department and create:
        department = Department(name=name)
        department.put()
    return department


def get_subject(code, create=False):
    subject = Subject.gql('WHERE code=:1', code).get()
    if not subject and create:
        subject = Subject(code=code)
        subject.put()
    return subject
