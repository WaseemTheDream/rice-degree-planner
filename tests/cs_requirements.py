"""
Test code for RequirementsFromCoursesRange.

Uses CS Upperlevel requirements to check for that


"""

from models import models

def main():
    subject = models.Subject.gql('WHERE code=:1', 'COMP').get()

    upper_level = models.CourseRangeRequirement(
        name='Upper-Level Requirements',
        subject_options=[subject],
        num_required=2,
        lower_range=447,
        upper_range=999)

    comp_450 = models.get_course('COMP 450')
    comp_446 = models.get_course('COMP 446')
    courses_taken = [comp_450, comp_446]

    print upper_level.progress(courses_taken)

if __name__ == '__main__':
    main()