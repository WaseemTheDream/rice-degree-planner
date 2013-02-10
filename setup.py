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

    probability = [models.get_course(course) for course in ['STAT 310','STAT 331']]
    assert (None not in probability)
    probability_requirement = models.CoursesRequirement(
        name='Probability',
        num_required=1)
    probability_requirement.load_courses(probability)
    probability_requirement.put()

    # linear_algebra = [models.get_course(course) for course in ['MATH 355','MATH 354','CAAM 335']]
    # assert (None not in linear_algebra)
    # linear_algebra_requirement = models.CoursesRequirement(
    #     name='Linear Algebra',
    #     num_required=1)
    # linear_algebra_requirement.load_courses(linear_algebra)
    # linear_algebra_requirement.put()
    
    physics1 = [models.get_course(course) for course in ['PHYS 101', 'PHYS 111','PHYS 125']]
    assert (None not in physics1)
    physics1_requirement = models.CoursesRequirement(
        name='Physics Mechanics',
        num_required=1)
    physics1_requirement.load_courses(physics1)
    physics1_requirement.put()

    physics2 = [models.get_course(course) for course in ['PHYS 102', 'PHYS 112','PHYS 126']]
    assert (None not in physics2)
    physics2_requirement = models.CoursesRequirement(
        name='Physics E+M',
        num_required=1)
    physics2_requirement.load_courses(physics2)
    physics2_requirement.put()
    
    math_and_science_group = models.RequirementGroup(name='Math and Science')
    # for req in [calculus_requirement, advanced_calculus_requirement, probability_requirement, linear_algebra_requirement, physics1_requirement, physics2_requirement]:
    for req in [calculus_requirement, advanced_calculus_requirement, probability_requirement, physics1_requirement, physics2_requirement]:
        math_and_science_group.requirements.append(req.key())
    math_and_science_group.put()

    return math_and_science_group

def comp_sci_core_group():
    # Compute CS Core requirements
    intro = [models.get_course(course) for course in ['COMP 140', 'COMP 160']]
    assert (None not in intro)
    intro_requirement = models.CoursesRequirement(
        name='Introductory CS',
        num_required=1)
    intro_requirement.load_courses(intro)
    # intro_requirement.load_excluded()
    intro_requirement.put()


    algorithms = [models.get_course('COMP 182')]
    assert (None not in algorithms)
    algorithms_requirement = models.CoursesRequirement(
        name='Algorithms',
        num_required=1)
    algorithms_requirement.load_courses(algorithms)
    algorithms_requirement.put()


    programming = [models.get_course('COMP 215')]
    assert (None not in programming)
    programming_requirement = models.CoursesRequirement(
        name='Programming',
        num_required=1)
    programming_requirement.load_courses(programming)
    programming_requirement.put()
    
    hardware = [models.get_course('ELEC 220')]
    assert (None not in hardware)
    hardware_requirement = models.CoursesRequirement(
        name='Hardware',
        num_required=1)
    hardware_requirement.load_courses(hardware)
    hardware_requirement.put()

    systems = [models.get_course('COMP 221')]
    assert (None not in systems)
    systems_requirement = models.CoursesRequirement(
        name='Systems',
        num_required = 1)
    systems_requirement.load_courses(systems)
    systems_requirement.put()
    
    object_programming = [models.get_course('COMP 310')]
    assert (None not in object_programming)
    object_programming_requirement = models.CoursesRequirement(
        name='Object Oriented Programming',
        num_required=1)
    object_programming_requirement.load_courses(object_programming)
    object_programming_requirement.put()
    
    parallel = [models.get_course('COMP 322')]
    assert (None not in parallel)
    parallel_requirement = models.CoursesRequirement(
        name='Parallel Programming',
        num_required=1)
    parallel_requirement.load_courses(parallel)
    parallel_requirement.put()
    
    
    programming_languages = [models.get_course(course) for course in ['COMP 411', 'COMP 412']]
    assert (None not in programming_languages)
    programming_languages_requirement = models.CoursesRequirement(
        name='Programming Languages',
        num_required=1)
    programming_languages_requirement.load_courses(programming_languages)
    programming_languages_requirement.put()

    os = [models.get_course('COMP 421')]
    assert (None not in os)
    os_requirement = models.CoursesRequirement(
        name='Operating Systems',
        num_required=1)
    os_requirement.load_courses(os)
    os_requirement.put()

    cs_theory = [models.get_course(course) for course in ['COMP 481', 'COMP 482']]
    assert (None not in cs_theory)
    cs_theory_requirement = models.CoursesRequirement(
        name='Computer Science Theory',
        num_required=1)
    cs_theory_requirement.load_courses(cs_theory)
    cs_theory_requirement.put()


    core_group = models.RequirementGroup(name='CS Core')
    for req in [intro_requirement, algorithms_requirement, programming_requirement, hardware_requirement, systems_requirement, object_programming_requirement, programming_languages_requirement, os_requirement, cs_theory_requirement]:
        core_group.requirements.append(req.key())
    core_group.put()
    return core_group

def comp_sci_major():
    math_and_science_group = comp_sci_math_and_science_group()
    core_group = comp_sci_core_group()

    # Set up elective requirement group 
    elective_group = models.RequirementGroup(name='CS Electives')
    courserange = models.CourseRangeRequirement(name='electives', num_required=2, lower_range=300, upper_range=999)
    comp = models.Subject.gql('WHERE code=:1', 'COMP').get()
    courserange.load_subjects([comp])
    courserange.put()

    #
    major_requirement = models.DegreeRequirement(name='Computer Science')
    for grp in [math_and_science_group, core_group]:
        major_requirement.requirement_groups.append(grp.key())
    major_requirement.put()
    return major_requirement

if __name__ == '__main__':
    main()