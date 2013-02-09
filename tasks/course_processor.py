"""
Processes raw courses data into the datastore.
"""

import logging

from models import models
from xml.etree import ElementTree as etree


def process_xml(xml):
    """
    Processes the specified xml file to load courses into the datastore.
    """

    tree = etree.parse(xml)

    courses = tree.findall('.//course')

    for course in courses:
        # Get a key-value set of tag to text for each course
        data = (dict(zip([x.tag for x in course.getchildren()],
                         [x.text for x in course.getchildren()])))
        
        process_course(data)

def process_course(data):
    """
    Processes a given data dictionary of a course into the datastore.
    """

    # Get the term of the course
    term_code = data['term-code']
    term = models.Term.gql('WHERE code=:1', term_code).get()
    if not term:        # Create term if it doesn't exist
        term = models.Term(code=term_code, description=data['term-description'])
        term.put()

    department = models.get_department(data['department'], create=True)
    subject = models.get_subject(data['subject'], create=True)
    credit_hours = try_parse_int(data['credit-hours'], 0)
    xlink = data['xlink-course']
    number = data['course-number']

    # Create or update course
    course = models.Course.gql(
        'WHERE subject=:1 and number=:2', subject, number).get()
    if not course:  
        course = models.Course(subject=subject,
                               number=number,
                               credit_hours=credit_hours)

    if term not in course.terms:
        course.terms.append(term.key())
    course.xlink = xlink
    course.put()
    logging.info('Processed %s %s', course.subject.code, course.number)



def try_parse_int(string, val=None):
    """
    Tries to parse the given string, if it fails returns val.
    """
    try:
        return int(string)
    except ValueError:
        return val
