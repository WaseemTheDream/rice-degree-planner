"""
Main controller for application.
"""


import webapp2
from models import delete, stickies
from main import MainHandler

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
], debug=True)