"""
Handler for deleting stickies.
"""

import webapp2
import models
import logging

from authentication import auth
from authentication.gaesessions import get_current_session
from main import JINJA_ENV

class GarbageHandler(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            return
        user = models.get_user(session['net_id'])
        logging.info(user)
        sticky_id = self.request.get('id')
        logging.info(sticky_id)
        sticky = models.Sticky.get(sticky_id)
        logging.info(sticky.user)
        assert sticky.user.key() == user.key()
        sticky.delete()
        self.response.out.write('Success!')