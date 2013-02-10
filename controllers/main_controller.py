"""
Main controller for application.
"""


import webapp2
from main import MainHandler
from main import AddCourseHandler
from models import courses

app = webapp2.WSGIApplication([
    ('/courses', courses.CoursesHandler),
    ('/addcourse', AddCourseHandler),
    ('/.*', MainHandler)
], debug=True)