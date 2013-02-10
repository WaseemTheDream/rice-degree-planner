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

def comp_sci_math_and_science_group():
    # Compute Math and Science Requirements
    calculus = [models.get_course(course) for course in ['MATH 101', 'MATH 102']]
    assert (None not in calculus)
    calculus_requirement = models.CoursesRequirement(
        name='Introductory calculus',
        num_required=2)
    calculus_requirement.load_courses(calculus)
    calculus_requirement.put()

    advanced_calculus = [models.get_course(course) for course in ['MATH 211', 'MATH 212', 'MATH 221', 'MATH 222']]
    assert (None not in advanced_calculus)
    advanced_calculus_requirement = models.CoursesRequirement(
        name='Advanced calculus',
        num_required=1)
    advanced_calculus_requirement.load_courses(advanced_calculus)
    advanced_calculus_requirement.put()

    math_and_science_group = models.RequirementGroup(name='Math and Science')
    for req in [calculus_requirement, advanced_calculus_requirement]:
        math_and_science_group.requirements.append(req.key())
    math_and_science_group.put()

    # TODO: Finish this

    return math_and_science_group

def comp_sci_core_group():
    # Compute CS Core requirements
    intro = [models.get_course(course) for course in ['COMP 140', 'COMP 160']]
    assert (None not in intro)
    intro_requirement = models.CoursesRequirement(
        name='Introductory CS',
        num_required=1)
    intro_requirement.load_courses(intro)
    intro_requirement.put()

    algorithms = [models.get_course('COMP 182')]
    assert (None not in algorithms)
    algorithms_requirement = models.CoursesRequirement(
        name='Algorithms',
        num_required=1)
    algorithms_requirement.load_courses(algorithms)
    algorithms_requirement.put()

    programming_languages = [models.get_course(course) for course in ['COMP 411', 'COMP 412']]
    assert (None not in programming_languages)
    programming_languages_requirement = models.CoursesRequirement(
        name='Programming Languages',
        num_required=1)
    programming_languages_requirement.load_courses(programming_languages)
    programming_languages_requirement.put()


    cs_theory = [models.get_course(course) for course in ['COMP 481', 'COMP 482']]
    assert (None not in cs_theory)
    cs_theory_requirement = models.CoursesRequirement(
        name='Computer Science Theory',
        num_required=1)
    cs_theory_requirement.load_courses(programming_languages)
    cs_theory_requirement.put()


    core_group = models.RequirementGroup(name='CS Core')
    for req in [intro_requirement, algorithms_requirement]:
        core_group.requirements.append(req.key())
    core_group.put()
    return core_group

def comp_sci_major():
    math_and_science_group = comp_sci_math_and_science_group()
    core_group = comp_sci_core_group()

    major_requirement = models.DegreeRequirement(name='Computer Science')
    for grp in [math_and_science_group, core_group]:
        major_requirement.requirement_groups.append(grp.key())
    major_requirement.put()
    return major_requirement

if __name__ == '__main__':
    main()