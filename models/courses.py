"""
Courses Request Handler
"""

import logging
import json
import webapp2
import models

MAX_STRING = u"\ufffd"

class CoursesHandler(webapp2.RequestHandler):

    def get(self):
        query_string = self.request.get('query')
        if not query_string:
            self.response.out.write('No query provided')
            return
        
        subject_code = self.request.get('subject')
        course_number = self.request.get('number')
        # db.GqlQuery("SELECT * FROM MyModel WHERE prop >= :1 AND prop < :2", "abc", u"abc" + MAX_STRING)
        subject = models.Subject.gql('WHERE code=:1', subject_code).get()
        if not subject:
            logging.error('Subject not found')
            self.response.out.write(json.dumps({'courses': []}))
            return
        courses = models.Course.gql(
            'WHERE subject=:1 AND number=:2', subject, course_number)
        courses_json = []
        for course in courses:
            courses_json.append({
                    'id': str(course.key()),
                    'label': '%s %s' % (course.subject.code, course.number)
                })
        self.response.out.write(json.dumps({'courses': courses_json}))