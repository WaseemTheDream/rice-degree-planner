#!/usr/bin/env python
#
# Copyright 2007 Google Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
#
import datetime
import os
import jinja2
import json
import logging
import webapp2

from models import models
from google.appengine.ext import db
from authentication import auth
from authentication.gaesessions import get_current_session

JINJA_ENV = jinja2.Environment(
    loader=jinja2.FileSystemLoader(os.path.dirname(__file__)))

class MainHandler(webapp2.RequestHandler):
    def get(self):
        page = self.request.path
        if page == '/':
            page = 'main'
        if page.startswith('/'):
            page = page[1:]
        if page.endswith('.html'):
            page = page[:-5]
        logging.info(page)
        template = JINJA_ENV.get_template('/views/%s.html' % page)
        self.response.out.write(template.render())

class AddCourseHandler(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        
        # Uncomment when we have the login page working
        # if not session.has_key('net_id'):
        #     return

        user = get_user(session['net_id'])
        data = jason.loads(self.request.get('json'))
        logging.info(data)

        course = data['course'].split()
        subject_entity = models.Subject('WHERE code=:1',)
        course_entity = models.Course('WHERE code=:1',201310)

        coursetaken = CourseTaken(user = user.key(),
                                  course = ,
                                  term = models.Term('WHERE code=:1',201310))

        # coursetaken = CourseTaken(user = user.key(),
        #                           course = data['course'],
        #                           term = data['term'])
        coursetaken.put()
        data['id'] = str(sticky.key())
        self.response.out.write(json.dumps(data))

        # {"term":"{term_id}","course":"COMP 140"}

        

        

app = webapp2.WSGIApplication([
    ('/.*', MainHandler)
    ('/addcourse', AddCourseHandler)
], debug=True)
