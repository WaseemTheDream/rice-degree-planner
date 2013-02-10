"""
Database storage for the app.
"""

from google.appengine.ext import db
from google.appengine.ext.db import polymodel

class Term(db.Model):
    code = db.StringProperty(required=True) # E.g. 201320
    description = db.StringProperty()       # E.g. Spring 2013

class User(db.Model):
	net_id = db.StringProperty(required=True)
	terms = db.ListProperty(db.Key)

class DistributionGroup(db.Model):
    name = db.StringProperty()

class Subject(db.Model):
    code = db.StringProperty(required=True,    # E.g. COMP
                             indexed=True)

class Course(db.Model):
    subject = db.ReferenceProperty(Subject,
                                   required=True,
                                   collection_name='courses')
    number = db.StringProperty(required=True)     # E.g. 182
    terms = db.ListProperty(db.Key)      # List of terms its been taught
    distribution = db.ReferenceProperty(DistributionGroup) # ref to distribution entity
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


class CoursesRequirement(Requirement):
    options = db.ListProperty(db.Key)
    num_required = db.IntegerProperty(required=True)

    def load_courses(self, options):
        """
        options {List<Course>}: list of options
        """
        for course in options:
            self.options.append(course.key())

    def progress(self, courses_taken):
        # Load up the courses and get their credit values
        credits_list = []
        options = [Course.get(key) for key in self.options]
        for course in options:
            credits_list.append(course.credit_hours)
        credits_list.sort()
        print credits_list
        min_credits_required = sum(credits_list[:self.num_required])
        max_credits_required = sum(credits_list[-self.num_required:])
        
        courses_matching = []       # Courses taken fulfill this requirement
        for course_taken in courses_taken:
            if course_taken.key() in self.options:
                courses_matching.append(course_taken)
        credits_taken = sum([course.credit_hours for course in courses_matching])
        return {
            'name': self.name,
            'max_credits_required': max_credits_required,
            'min_credits_required': min_credits_required,
            'credits_taken': credits_taken,
            'courses_matching': courses_matching
        }

class CourseRangeRequirement(Requirement):
    subject_options = db.ListProperty(db.Key)
    excluded_courses = db.ListProperty(db.Key)      # Courses that can't be used towards progress
    any_subject = db.BooleanProperty(default=False)  # If true, doesn't check for subject_options matching
    num_required = db.IntegerProperty(required=True)
    lower_range = db.IntegerProperty(required=True)
    upper_rage = db.IntegerProperty(required=True)
        
    def load_subjects(self, subject_options):
        """
        subject_options {List<Subject>}: list of possible subject_options
        """
        for subject in subject_options:
            self.subject_options.append(subject.key())

    def load_excluded_courses(self, excluded_courses):
        """
        excluded_courses {List<Course>}: Courses that can't be used towards progress
        """
        for course in excluded_courses:
            self.excluded_courses.append(course.key())

    def progress(self, courses_taken):
        # Load up the courses and get their credit values
        credits_list = []
        min_credits_required = 3 * self.num_required
        max_credits_required = 4 * self.num_required
        courses_matching = []       # Courses taken that fulfill this requirement
        for course in courses_taken:
            number = try_parse_int(course.number, 0)
            if course.subject not in self.subject_options and not self.any_subject:
                continue
            if course.key() in self.excluded_courses:
                continue
            if self.lower_range <= number and number <= self.upper_rage:
                courses_matching.append(course)
        credits_taken = sum([course.credit_hours for course in courses_matching])
        return {
            'name': self.name,
            'max_credits_required': max_credits_required,
            'min_credits_required': min_credits_required,
            'credits_taken': credits_taken,
            'courses_matching': courses_matching
        }


class DistributionRequirement(db.Model):
    distribution = db.ReferenceProperty(DistributionGroup,
                                        required=True)
    credits_required = db.IntegerProperty(required=True)

    def progress(self, courses_taken):
        credits_taken = 0
        courses_matching = []
        for course in courses_taken:
            if course.distribution.key() == self.distribution.key():
                credits_taken += course.credits
                courses_matching.append(course)
        return {
            'name': self.name,
            'max_credits_required': self.credits_required,
            'min_credits_required': self.credits_required,
            'credits_taken': credits_taken,
            'courses_matching': courses_matching
        }

class RequirementGroup(db.Model):
    name = db.StringProperty(required=True)
    requirements = db.ListProperty(db.Key)

    def progress_summary(self, courses_taken):
        """
        Returns the summary of progress made within the requirement group.

        Args:
            courses_taken {List<Course>}: list of courses taken by user.

        Returns:
            A dictionary with the following key value pairs.
            name {String}: the name of the requirement
            min_credits_required: the minimum credits required to fulfill requirements
            max_credits_required: the maximum credits required to fulfill requirements
            credits_taken: the number of relevant credits taken
            overall_progress: list of progress objects for each requirement of this group
        """
        requirements = [Requirement.get(req) for req in self.requirements]
        overall_progress = [req.progress(courses_taken) for req in requirements]
        credits_taken = sum([prog['credits_taken'] for prog in overall_progress])
        min_credits_required = sum([prog['min_credits_required'] for prog in overall_progress])
        max_credits_required = sum([prog['max_credits_required'] for prog in overall_progress])
        return {
            'name': self.name,
            'min_credits_required': min_credits_required,
            'max_credits_required': max_credits_required,
            'credits_taken': credits_taken,
            'overall_progress': overall_progress
        }

class DegreeRequirement(db.Model):
    name = db.StringProperty(required=True)
    requirement_groups = db.ListProperty(db.Key)

    def progress_summaries(self, courses_taken):
        """
        Returns a list of progress summaries for each requirement group in the 
        degree requirement.

        Args:
            course_taken {List<Course>}: list of courses taken by the user.

        Returns:
            A dictionary with the following key value pairs
            name: the name of the degree
            progress_summaries {List<progress_summary>}: returns list of progress summaries
        """
        groups = [RequirementGroup.get(grp) for grp in self.requirement_groups]
        summaries = [grp.progress_summary(courses_taken) for grp in groups]
        return {
            'name': self.name,
            'progress_summaries': summaries
        }


def get_user(net_id, create=False):
	user = User.gql('WHERE net_id=:1', net_id).get()
	if not user:
		if create:
			user = User(net_id=net_id).put()
		else:
			return False
	return user


def get_subject(code, create=False):
    subject = Subject.gql('WHERE code=:1', code).get()
    if not subject and create:
        subject = Subject(code=code)
        subject.put()
    return subject

def get_distribution_group(name, create=False):
    dist = DistributionGroup.gql('WHERE name=:1', name).get()
    if not dist and create:
        dist = DistributionGroup(name=name)
        dist.put()
    return dist

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

def get_courses_above(name,number):
	"""
	Returns list of courses for a specified subject above a specified level
	
	Args:
		name {String}: e.g. COMP
	"""
	subject = Subject.gql('WHERE code=:1',name).get()
	courses = Course.gql(
			'Where subject=:1 AND number>=:2', subject, course_number).run(batch_size=200)
	for course in courses:
		return_courses.append(course)
	return return_courses
	
def try_parse_int(string, val=None):
    """
    Tries to parse the given string, if it fails returns val.
    """
    try:
        return int(string)
    except ValueError:
        return val

