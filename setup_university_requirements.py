"""
Run this setup file to add university requirements to the degree requirements table.
"""

from models import models
from tasks import course_processor

def distribution_group_requirement():
    distribution_names = ['I', 'II', 'III'] # TODO: Make sure this is correct
    distributions = []
    for dist_name in distribution_names:
        dist = models.DistributionGroup.gql('WHERE name=:1', dist_name).get()
        assert (dist!=None)
        distributions.append(dist)

    distribution_requirements = []
    for dist in distributions:
        dist_req = models.DistributionRequirement(
            name='Distribution Requirement Group %s' % dist.name,
            distribution=dist,
            credits_required=12)
        dist_req.put()
        distribution_requirements.append(dist_req)

    distribution_group_requirement = models.RequirementGroup(
        name='Distribution Requirements Group')
    for dist_req in distribution_requirements:
        distribution_group_requirement.requirements.append(dist_req)
    distribution_group_requirement.put()

    return distribution_group_requirement

def university_degree_requirement():
    university_degree_requirement = models.DegreeRequirement(
        name='University Requirements')
    university_degree_requirement.requirement_groups.append(
        distribution_group_requirement().key())
    university_degree_requirement.put()
    return university_degree_requirement


def main():
    university_degree_requirement()

if __name__ == '__main__':
    main()