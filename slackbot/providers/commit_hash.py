import os
from github import Github

GH_USER = os.getenv('GH_USER')
GH_TOKEN = os.getenv('GH_TOKEN')
GH_ORGANISATION = 'riddlesio'


def get_microservice_repository_name(microservice_name):
    return 'microservices-nova'


def get_hash_in_repository(repository_name, tag_or_hash):
    g = Github(GH_TOKEN)
    riddlesio = g.get_organization(GH_ORGANISATION)
    repo = riddlesio.get_repo(repository_name)
    commit = repo.get_commit(tag_or_hash)
    return commit.sha


def get_commit_hash(microservice_name, tag_or_hash):
    repository = get_microservice_repository_name(microservice_name)
    return get_hash_in_repository(repository, tag_or_hash)
