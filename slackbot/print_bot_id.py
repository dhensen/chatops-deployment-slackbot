import os
from slackclient import SlackClient
from slackbot.settings import SLACK_BOT_NAME, SLACK_API_TOKEN

slack_client = SlackClient(SLACK_API_TOKEN)

if __name__ == "__main__":
    api_call = slack_client.api_call("users.list")
    if not api_call.get('ok'):
        print("could not find bot user with the name " + SLACK_BOT_NAME)
        exit(1)

    # retrieve all users so we can find our bot
    users = api_call.get('members')
    for user in users:
        if 'name' in user and user.get('name') == SLACK_BOT_NAME:
            print(f"Bot ID for '{user['name']}' is {user.get('id')}")
            print(f"export BOT_ID={user.get('id')}")
    exit(0)
