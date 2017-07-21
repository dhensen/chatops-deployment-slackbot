import pytest

from slackbot.tasks.deploy import parse_deploy_message


def test_deploy_parser():
    microservice_name, sha, environment = parse_deploy_message("deploy player-front-end 2.7.11 to production")
    assert microservice_name == 'player-front-end'
    assert sha == '2.7.11'
    assert environment == 'production'


def test_deploy_parser_raises_on_false_formatted_message():
    with pytest.raises(ValueError) as excinfo:
        parse_deploy_message("deploy player-front-end to production")
        assert 'message format should be' in excinfo.value

