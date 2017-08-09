import os
import random
import subprocess
from queue import Full
from tempfile import TemporaryDirectory
from time import sleep

from parse import parse

from slackbot.deployment_queue import DeploymentQueue
from slackbot.providers.commit_hash import get_commit_hash, GH_TOKEN, GH_USER

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

    if commit_hash is None:
        return "A commit hash is not found for short hash or tag {}, did you forget to push it?".format(hash_or_tag)

    try:
        deployment_queue.enqueue_deployment(
            {'microservice_name': microservice_name, 'commit_hash': commit_hash, 'environment': environment, 'user': user})
    except Full:
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

            send_message(slack_client, deployment,
                         "<@{user}> Started deploying {microsevice_name}:{commit_hash} to {environment}")

            # perform steps 2-5

            with TemporaryDirectory() as tmpdirname:
                os.chdir(tmpdirname)
                username = GH_USER
                password = GH_TOKEN
                organisation = 'riddlesio'
                subprocess.run("git clone https://{}:{}@github.com/{}}/{}".format(
                    username, password, organisation, deployment.microservice_name))

            send_message(slack_client, deployment,
                         "<@{user}> Deploying {microservice_name}:{commit_hash} to {environment} done :+1:")

            deployment_queue.task_done()

    return handler


def send_message(slack_client, deployment, message):

    slack_client.api_call(
        "chat.postMessage",
        channel="#general",
        text=message.format(**deployment),
        as_user=True
    )
