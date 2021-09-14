import os
import json

local_path = os.path.dirname(__file__)


def load_config_file(path):
    file = open(os.path.join(local_path, os.pardir, path))
    return json.load(file)


def load_loc():
    return load_config_file('config/loc.json')


def load_responses_config():
    return load_config_file('config/responses.json')


def load_bot_config():
    return load_config_file('config/config.json')


def load_emoji_config():
    file = open(os.path.join(local_path, os.pardir, 'config/emoji.json'), encoding="utf8")
    return json.load(file)


def load_gif_config():
    return load_config_file('config/gif.json')


def load_tokens():
    return load_config_file('config/token.json')