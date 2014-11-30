# coding: utf-8

__author__ = 'birhoff'

"""
fab <команда>[:agr1[,arg2[,...]]]

TODO: понять что мы хотим запускать локально, что удаленно, возможно нужно
делать таски так, чтобы они запускались и так, и так.
"""


from fablib.build import *
# from fablib.db import *
# from fablib.graph import *
# from fablib.i18n import *
# from fablib.test import *


def help():
    """ХЁЛП"""
    from fabric.api import local
    local('fab -l')
