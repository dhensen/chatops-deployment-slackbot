from queue import Queue

MAX_QUEUE_SIZE = 10


class Deployment(object):
    def __init__(self, microservice_name, commit_hash, environment, user=None):
        self.microservice_name = microservice_name
        self.commit_hash = commit_hash
        self.environment = environment
        self.user = user


class DeploymentQueue(Queue):
    def __init__(self):
        super().__init__(maxsize=MAX_QUEUE_SIZE)

    def enqueue_deployment(self, deployment: Deployment):
        print("enqueue: {}".format(deployment))
        self.put(deployment, block=False)
