"""
Processes raw courses data into the datastore.
"""

from models import models

from xml.etree import ElementTree as etree


def process_xml(xml):
    """
    Processes the specified xml file to load courses into the datastore.
    """

    tree = etree.parse(xml)

    courses = tree.findall('//course')

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
    term = models.Term('WHERE code=:1', term_code).get()
    if not term:        # Create term if it doesn't exist
        term = models.Term(code=term_code, description=data['term-description'])
        term.put()

    