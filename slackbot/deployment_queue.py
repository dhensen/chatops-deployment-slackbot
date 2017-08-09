"""
DeploymentQueue and Deployment
"""
from queue import Queue

MAX_QUEUE_SIZE = 10


class DeploymentQueue(Queue):
    """ DeploymentQueue """
    def __init__(self):
        super().__init__(maxsize=MAX_QUEUE_SIZE)

    def enqueue_deployment(self, deployment):
        """ put a deployment on the queue non-blocking """
        print("enqueue: {}".format(deployment))
        self.put(deployment, block=False)
