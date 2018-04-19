defined_environments = [
    'test',
    'production'
]


def has_environment(name):
    return name in defined_environments
