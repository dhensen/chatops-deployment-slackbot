from slackbot.providers.commit_hash import get_commit_hash


def test_get_commit_hash():
    short_hash = 'ca3ed'
    assert 'ca3ed3480b32b0082ffeb46090ada973cfb87e10' == get_commit_hash(
        "match-runner", short_hash)
