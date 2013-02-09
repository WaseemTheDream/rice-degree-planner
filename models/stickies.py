"""
Sticky notes handler.
"""

import webapp2
import models
import json
import logging

from authentication import auth
from authentication.gaesessions import get_current_session
from main import JINJA_ENV


class StickyNotesHandler(webapp2.RequestHandler):
    def get(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            auth.require_login(self)
        user = models.get_user(session['net_id'], create=True)
        stickies = models.Sticky.gql('WHERE user=:1', user)
        stickies_data = []
        for sticky in stickies:
            stickies_data.append({
                    'id': str(sticky.key()),
                    'title': sticky.title,
                    'note': sticky.note
                })


        page_data = {'stickies': stickies_data}
        template = JINJA_ENV.get_template('/views/stickies.html')
        self.response.out.write(template.render(page_data))

    def post(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            return
        user = models.get_user(session['net_id'])
        data = json.loads(self.request.get('json'))
        logging.info(data)
        sticky = models.Sticky(user=user.key(),
                        title=data['title'],
                        note=data['note'])
        sticky.put()
        data['id'] = str(sticky.key())
        self.response.out.write(json.dumps(data))