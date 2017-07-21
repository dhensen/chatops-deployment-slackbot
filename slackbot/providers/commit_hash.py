def get_microservice_repository_root_path(microservice_name):
    return '/path/to/microservice/repository'


def get_hash_in_repository(repo, tag_or_hash):
    return 'afefbdeeefffffffff267276d6eee2f7e7be27f'


def get_commit_hash(microservice_name, tag_or_hash):
    repository_path = get_microservice_repository_root_path(microservice_name)
    return get_hash_in_repository(repository_path, tag_or_hash)