"""
Run this setup file only once from remote_api to fill your database


Introductory calculus: MATH 101-102
Advanced calculus: MATH 211, 212, 221, or 222
Probability: STAT 310 or 331
Linear Algebra: MATH 355, MATH 354, or CAAM 335
Physics (B.S. only): PHYS 101-102, PHYS 111-112, or PHYS 125-126
"""

from models import models
from tasks import course_processor

def main():
    term = models.Term(code='TRANSFER', description='Transfer Credit')
    term.put()

    course_processor.process_xml('courses_data/fall12.xml')
    course_processor.process_xml('courses_data/spring13.xml')

def add_comp_sci_major():
    calculus = [models.get_course(course) for course in ['MATH 101', 'MATH 102']]
    assert (None not in calculus)
    culculus_requirement = models.CoursesRequirement(
        name='Introductory calculus',
        options=calculus,
        num_required=2)

    advanced_calculus = [models.get_course(course) for course in ['MATH 211', 'MATH 212', 'MATH 221', 'MATH 222']]
    assert (None not in advanced_calculus)
    advanced_calculus_requirement = models.CoursesRequirement(
        name='Advanced calculus',
        options=advanced_calculus,
        num_required=1)

if __name__ == '__main__':
    main()