"""
Main controller for application.
"""


import webapp2
from main import MainHandler
from main import AddCourseHandler
from main import DeleteCourseHandler
from models import courses

app = webapp2.WSGIApplication([
    ('/courses', courses.CoursesHandler),
    ('/addCourse', AddCourseHandler),
    ('/deleteCourse', DeleteCourseHandler),
    ('/.*', MainHandler)
], debug=True)