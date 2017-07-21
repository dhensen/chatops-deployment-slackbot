defined_environments = [
    'test',
    'staging',
    'production'
]


def has_environment(name):
    return name in defined_environments