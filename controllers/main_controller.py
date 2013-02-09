"""
Main controller for application.
"""


import webapp2
from models import delete, stickies
from main import MainHandler

app = webapp2.WSGIApplication([
    ('/stickies', stickies.StickyNotesHandler),
    ('/delete', delete.GarbageHandler),
    ('/.*', MainHandler)
], debug=True)