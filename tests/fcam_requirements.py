"""
Shows you how to use requirements code for FCAM Minor.

Assumes you ran setup.py


FCAM Minor
3 of ECON 211 ECON 370 STAT 310 ECON 400 STAT 410 
3 of ECON 255 ECON 243 ECON 443 STAT 421 STAT 449 STAT 486

Used a combined requirement from options of:
STAT 310
STAT 410
ECON 243
ECON 443
STAT 421
STAT 449
STAT 486
Because the above were the only ones found in the database of fall12 and spring13.


last print in main prints:
{'courses_matching': [<models.models.Course object at 0x1da7af0>, <models.models.Course object at 0x2caff70>], 'max_credits_required': 13L, 'min_credits_required': 12L, 'credits_taken': 7L}
"""

from models import models

def main():
    options_names = [
        'STAT 310',
        'STAT 410',
        'ECON 243',
        'ECON 443',
        'STAT 421',
        'STAT 449',
        'STAT 486']
    options = []
    for course_name in options_names:
        course = models.get_course(course_name)
        if course:
            options.append(course)

    fcam_requirements = models.RequirementsFromCourses(
        name='FCAM Requirements',
        options=options,
        num_required=4)

    courses_taken_names = ['STAT 310', 'COMP 182', 'STAT 410']
    courses_taken = []
    for course_name in courses_taken_names:
        course = models.get_course(course_name)
        if course:
            courses_taken.append(course)

    print fcam_requirements.progress(courses_taken)

if __name__ == '__main__':
    main()