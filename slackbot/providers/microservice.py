defined_microservices = [
    'chronicler',
    'player-front-end',
    'match-runner'
]


def has_microservice(name):
    return name in defined_microservices