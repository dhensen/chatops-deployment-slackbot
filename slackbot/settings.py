import os
def get_config_value(env_key, cls=str, default=None):
    return cls(os.environ.get(env_key))

BOT_ID = get_config_value('BOT_ID')
SLACK_API_TOKEN = get_config_value('SLACK_API_TOKEN')
SLACK_BOT_NAME = get_config_value('SLACK_BOT_NAME')
GH_USER = get_config_value('GH_USER')
GH_TOKEN = get_config_value('GH_TOKEN')
GH_ORGANISATION = get_config_value('GH_ORGANISATION')
