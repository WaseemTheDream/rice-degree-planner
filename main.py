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
        requiredTerm = models.Term.gql('WHERE code=:1', '201320').get()
        #if requiredTerm.key() not in user.terms:
        #    user.terms.append(requiredTerm.key())
        #    user.put()        
        
        sorted_terms = sorted(models.Term.get(user.terms), key=lambda t:t.code)
        for term in sorted_terms:
            thisTerm = {
                'code': term.code,
                'description':term.description
            }        
            courseTakens = models.CourseTaken.gql('WHERE user=:1 AND term=:2', user, term)
            thisTerm['courses'] = []
            for courseTaken in courseTakens:
                thisTerm['courses'].append({
                    'name': courseTaken.course.subject.code + " " + courseTaken.course.number,
                    'term': courseTaken.term.code,
                    'id' : courseTaken.key()
                })
            page_data['terms'].append(thisTerm)
        
        degree = models.DegreeRequirement.gql('WHERE name=:1', 'Computer Science').get()
        courses_takens = models.CourseTaken.gql('WHERE user=:1', user)
        
        courses = []
        for courses_taken in courses_takens:
        	courses.append(courses_taken.course)
        
        page_data['progress'] = degree.progress_summaries(courses)
        self.response.out.write(page_data['progress'])
        self.response.out.write(template.render(page_data))

class AddCourseHandler(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            return
        user = models.get_user(session['net_id'])

        if not user:
            data['error'] = "Invalid User"
            self.response.out.write(json.dumps(data))
            return

        data = json.loads(self.request.get('json'))
        logging.info(data)

        course = models.get_course(data['course'])

        if not course:
            data['error'] = "Invalid Course"
            self.response.out.write(json.dumps(data))
            return

        term = models.Term.gql('WHERE code=:1', str(data['term'])).get()


        if not term:
            data['error'] = "Invalid Term"
            self.response.out.write(json.dumps(data))
            return

        coursetaken = models.CourseTaken(user = user, course = course, term = term)
        coursetaken.put()
        data['id'] = str(coursetaken.key())
        self.response.out.write(json.dumps(data))

class DeleteCourseHandler(webapp2.RequestHandler):
    def post(self):
        session = get_current_session()
        if not session.has_key('net_id'):
            return
        user = models.get_user(session['net_id'])

        if not user:
            data['error'] = "Invalid User"
            self.response.out.write(json.dumps(data))
            return

        data = json.loads(self.request.get('json'))

        course_taken = models.CourseTaken.get(data['id'])
        if not course_taken:
            data['error'] = "Course Taken not found!"
            self.response.out.write(json.dumps(data))
            return

        course_taken.delete()
        self.response.out.write('Deleted')

        