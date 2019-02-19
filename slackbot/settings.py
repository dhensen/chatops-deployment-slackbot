import os


def get_config_value(env_key, cls=str, required=False, default=None):
    try:
        return cls(os.environ[env_key])
    except KeyError:
        if required:
            raise RuntimeError(f'environment variable {env_key} is required')
        return default
    except TypeError:
        raise


BOT_ID = get_config_value('BOT_ID', required=True)
SLACK_API_TOKEN = get_config_value('SLACK_API_TOKEN', required=True)
SLACK_BOT_NAME = get_config_value('SLACK_BOT_NAME', required=True)
GH_USER = get_config_value('GH_USER')
GH_TOKEN = get_config_value('GH_TOKEN')
GH_ORGANISATION = get_config_value('GH_ORGANISATION')
