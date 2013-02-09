"""
Courses Request Handler
"""

import logging
import json
import webapp2
import models


class CoursesHandler(webapp2.RequestHandler):

    def get(self):
        subject_code = self.request.get('subject')
        course_number = self.request.get('number')
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