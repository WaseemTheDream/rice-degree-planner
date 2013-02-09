"""
Main controller for application.
"""


import webapp2
from main import MainHandler
from models import courses

app = webapp2.WSGIApplication([
    ('/courses', courses.CoursesHandler),
    ('/.*', MainHandler)
], debug=True)