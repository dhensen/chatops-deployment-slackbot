import os
from github import Github

GH_USER = os.getenv('GH_USER')
GH_TOKEN = os.getenv('GH_TOKEN')
GH_ORGANISATION = os.getenv('GH_ORGANISATION')


def get_microservice_repository_name(microservice_name):
    # todo: create a config map that maps a microservice onto a repository, for now we use a mono-repo so this is easy
    return 'microservices-nova'


def get_hash_in_repository(repository_name, tag_or_hash):
    g = Github(GH_TOKEN)
    organisation = g.get_organization(GH_ORGANISATION)
    repo = organisation.get_repo(repository_name)
    commit = repo.get_commit(tag_or_hash)
    return commit.sha


def get_commit_hash(microservice_name, tag_or_hash):
    repository = get_microservice_repository_name(microservice_name)
    return get_hash_in_repository(repository, tag_or_hash)
