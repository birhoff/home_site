__author__ = 'birhoff'

# encoding: utf-8
"""
"""
import os
import warnings

from fabric.api import env


def _set_remote_dir():
    project = os.path.split(env.real_fabfile)[0].split('/')[-1]
    try:
        remote_workspace = env.remote_workspace
    except AttributeError:
        remote_workspace = '/home/username'
        warnings.warn('Add "remote_workspace" setting to ~/.fabricrc. '
                      'Example: remote_workspace = /home/username')

    env.remote_dir = os.path.join(remote_workspace, project)


def _set_local_dir():
    env.local_dir = os.path.split(env.real_fabfile)[0]


def _set_is_local():
    env.is_local = not os.path.exists(env.remote_dir)


def setup():
    _set_local_dir()
    _set_remote_dir()
    _set_is_local()



