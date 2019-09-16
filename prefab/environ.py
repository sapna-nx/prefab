
import json
import os

from fabric.api import env
from fabric.contrib import django
import collections


DEFAULTS = {
    "django_settings": os.environ.get("DJANGO_SETTINGS_MODULE", ""),
}


def fabenv(environ, path='environ.json'):
    with open(path) as configfile:
        conf = json.load(configfile)[environ]
        defaults = DEFAULTS.copy()

        django.settings_module(conf['django_settings'])

        # for now, also use env to store other global state
        env.update(defaults)
        env.update(conf)

        # and finally update with the env dict
        env.update(conf.pop('env', {}))


def register(name, defaults):
    """
    """
    env.envvars[name] = defaults


def gather(name, **kwargs):
    """
    """
    envvars = env.envvars[name]
    envvars.update(kwargs)

    for key, value in list(envvars.items()):
        if isinstance(value, collections.Callable):
            envvars[key] = value()

    return envvars


if 'envvars' not in env:
    env.envvars = {}
