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
    	session = get_current_session()
        if not session.has_key('net_id'):
            auth.require_login(self)
        user = models.get_user(session['net_id'], True)    
        page = self.request.path
        if page == '/':
            page = 'main'
        if page.startswith('/'):
            page = page[1:]
        if page.endswith('.html'):
            page = page[:-5]
        logging.info(page)
        template = JINJA_ENV.get_template('/views/%s.html' % page)
        page_data = {}
        page_data['net_id'] = user.net_id
    	page_data['terms'] = []	    
        terms = models.Term.gql('LIMIT 10')
        for term in terms:
        	page_data['terms'].append({   ## if terms_data is an array, it is integer-indexed. Therefore list['a string'] is invalid
        			'code': term.code,
        			'description' : term.description
        		})
        self.response.out.write(template.render(page_data))

class AddCourseHandler(webapp2.RequestHandler):
	def post(self):
		session = get_current_session()
		if not session.has_key('net_id'):
			return
		user = models.get_user(session['net_id'])
		data = json.loads(self.request.get('json'))
		logging.info(data)
		
		course = models.get_course(data['course'])
		
		if not course:
			data['error'] = "Invalid Course"
			self.response.out.write(json.dumps(data))
			return
		
		term = models.Term.gql('WHERE code=:1', str(data['term']))
		
		if not term:
			data['error'] = "Invalid Term"
			self.response.out.write(json.dumps(data))
			return
		
		coursetaken = models.CourseTaken(user = user.key(), course = course, term = term)
		#coursetaken.put()
		#data['id'] = str(coursetaken.key())
		self.response.out.write(json.dumps(data))
