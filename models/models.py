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
            A dictionary with the following key value pairs
            max_credits_required: maximum number of total credits required to fulfill
            min_credits_required: minimum number of total credits required to fulfill
            credits_taken: number of credits taken towards degree
            courses_matching: courses taken that fulfill requirements
        """
        raise NotImplementedError('Abstract function')


class RequirementsFromCourses(Requirement):
    _options = db.ListProperty(db.Key)
    _num_required = db.IntegerProperty(required=True)

    def __init__(self, name, options, num_required):
        """
        Constructor.

        Args:
            name {String}: the name of the requirement
            options {List<Course>}: list of options
            num_required {Integer}: number of courses required
        """
        super(RequirementsFromCourses, self).__init__(name=name, _num_required=num_required)
        assert(num_required < len(options))
        self._options = []
        for course in options:
            self._options.append(course.key())

    def progress(self, courses_taken):
        # Load up the courses and get their credit values
        credits_list = []
        options = [Course.get(key) for key in self._options]
        for course in options:
            credits_list.append(course.credit_hours)
        credits_list.sort()
        print credits_list
        min_credits_required = sum(credits_list[:self._num_required])
        max_credits_required = sum(credits_list[-self._num_required:])
        
        courses_matching = []       # Courses taken fulfill this requirement
        for course_taken in courses_taken:
            if course_taken.key() in self._options:
                courses_matching.append(course_taken)
        credits_taken = sum([course.credit_hours for course in courses_matching])
        return {
            'max_credits_required': max_credits_required,
            'min_credits_required': min_credits_required,
            'credits_taken': credits_taken,
            'courses_matching': courses_matching
        }

class RequirementsFromCoursesRange(Requirement):
    _subject_options = db.ListProperty(db.Key)
    _num_required = db.IntegerProperty(required=True)
    _lower_range = db.IntegerProperty(required=True)
    _upper_range = db.IntegerProperty(required=True)

    def __init__(
        self, 
        name, 
        subject_options, 
        num_required, 
        lower_range, 
        upper_range):
        """
        Constructor.

        Args:
            name {String}: the name of the requirement
            subject_options {List<Subject>}: list of possible subject_options
            num_required {Integer}: the number of courses you have to take
            lower_range {Integer}: the lower range of the requirement e.g. 150
            upper_range {Integer}: the upper range of the requirement e.g. 300
        """
        super(RequirementsFromCoursesRange, this).__init__(
            name=name,
            _num_required=num_required,
            _lower_range=lower_range,
            _upper_range=upper_range)
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

def get_course(name):
    """
    Returns the course specified with the name.

    Args:
        name {String}: e.g. COMP 182
    """
    subject_code, course_number = tuple(name.split(' '))
    subject = Subject.gql('WHERE code=:1', subject_code).get()
    course = Course.gql(
            'WHERE subject=:1 AND number=:2', subject, course_number).get()
    return course
