import random
from queue import Full
from time import sleep

from parse import parse

from slackbot.deployment_queue import DeploymentQueue, Deployment
from slackbot.providers.commit_hash import get_commit_hash

deployment_queue = DeploymentQueue()


def parse_deploy_message(message):
    """
    deploy <microservice_name> <hash_or_tag> to <environment>
    """
    message_format = "deploy {microservice_name} {hash_or_tag} to {environment}"
    res = parse(message_format, message)

    if res is None:
        raise ValueError("message format should be: {}".format(message_format))

    return res['microservice_name'], res['hash_or_tag'], res['environment']


def schedule_deployment(microservice_name, hash_or_tag, environment, user):
    # get commit_hash via hash_or_tag for microservice_name
    # enqueue a deployment on a deployment queue
    commit_hash = get_commit_hash(microservice_name, hash_or_tag)

    try:
        deployment_queue.enqueue_deployment(Deployment(microservice_name, commit_hash, environment, user))
    except Full as e:
        return "The deployment queue is full, your deployment is not scheduled, please try again later :cry:"

    sleep(1)

    size = deployment_queue.qsize()
    if size > 5:
        return "Your deployment is scheduled :stopwatch:, there are {} deployments to be done first so you better get " \
               "some :coffee:".format(size)
    elif size > 0:
        return "Your deployment is scheduled :stopwatch:, there are {} deployments to be done first".format(size)
    return "Your deployment request will be processed right away :facepunch::skin-tone-5:"


def deploy_handler(slack_client):
    # pop a deployment off the deployment queue:
    #   1 checkout the repo at commit_hash
    #   2 jarvis build microservice_name TODO: jarvis can not build for a commit_hash yet, so checkout at commit_hash
    #   3 jarvis publish microservice_name commit_hash
    #   4 overwrite the microservice version in the proper dotenv
    #   5 jarvis deploy microservice_name to environment
    def handler():
        while True:
            deployment = deployment_queue.get()
            print("deployment: {}".format(deployment))
            if deployment is None:
                print("handler done")
                break

            # sleep 2 second to receive deployment scheduling/processing message first
            sleep(2)

            slack_client.api_call(
                "chat.postMessage",
                channel="#general",
                text="<@{}> Started deployment {}:{}@{}...".format(deployment.user, deployment.microservice_name,
                                                                   deployment.commit_hash,
                                                                   deployment.environment),
                as_user=True
            )

            # perform steps 2-5
            sleep(random.randint(30, 60))

            slack_client.api_call(
                "chat.postMessage",
                channel="#general",
                text="<@{}> Deployment {}:{}@{} done :+1:".format(deployment.user, deployment.microservice_name, deployment.commit_hash,
                                                                  deployment.environment),
                as_user=True
            )

            deployment_queue.task_done()

    return handler
