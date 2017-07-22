import os
import threading
import time

from slackclient import SlackClient

from slackbot.tasks.deploy import deploy_handler, parse_deploy_message, deployment_queue, schedule_deployment

# starterbot's ID as an environment variable
BOT_ID = os.environ.get("BOT_ID")

# constants
AT_BOT = "<@" + BOT_ID + ">"
DEPLOY_COMMAND = "deploy"
STATUS_COMMAND = "status"

# instantiate Slack client
slack_token = os.environ["SLACK_API_TOKEN"]
slack_client = SlackClient(slack_token)


def handle_command(command, channel, user):
    """
        Receives commands directed at the bot and determines if they
        are valid commands. If so, then acts on the commands. If not,
        returns back what it needs for clarification.
    """
    response = "Not sure what you mean. Use the *" + DEPLOY_COMMAND + \
               "* command with numbers, delimited by spaces."
    if command.startswith(DEPLOY_COMMAND):
        response = schedule_deployment(*parse_deploy_message(command), user)
    elif command.startswith(STATUS_COMMAND):
        size = deployment_queue.qsize()
        if size:
            response = "Processing {} deployments".format(size)
        else:
            response = "Just idling boss!"

    # response = "<@{}> ".format(user) + response
    slack_client.api_call("chat.postMessage", channel=channel,
                          text=response, as_user=True)


def parse_slack_output(slack_rtm_output):
    """
        The Slack Real Time Messaging API is an events firehose.
        this parsing function returns None unless a message is
        directed at the Bot, based on its ID.
    """
    output_list = slack_rtm_output
    if output_list and len(output_list) > 0:
        for output in output_list:
            if output and 'text' in output and AT_BOT in output['text']:
                # return text after the @ mention, whitespace removed
                return output['text'].split(AT_BOT)[1].strip().lower(), \
                       output['channel']
    return None, None


def start_workers(num_worker_threads):
    threads = []
    for i in range(num_worker_threads):
        t = threading.Thread(target=deploy_handler(slack_client))
        t.start()
        threads.append(t)
    return threads


def stop_workers(threads):
    print("stopping workers")
    for thread in threads:
        deployment_queue.put(None)
    for thread in threads:
        thread.join()


def main_loop():
    while True:
        print("event loop iteration")
        slack_rtm_output = slack_client.rtm_read()
        command, channel = parse_slack_output(slack_rtm_output)
        if command and channel:
            handle_command(command, channel, slack_rtm_output[0]['user'])
        time.sleep(READ_WEBSOCKET_DELAY)


if __name__ == "__main__":
    READ_WEBSOCKET_DELAY = 1 # 1 second delay between reading from firehose
    if slack_client.rtm_connect():
        print("StarterBot connected and running!")
        threads = start_workers(1)
        try:
            main_thread = threading.Thread(target=main_loop)
            main_thread.start()
        except Exception as e:
            print(str(e))
            stop_workers(threads)
        finally:
            pass
    else:
        print("Connection failed. Invalid Slack token or bot ID?")