# coding: utf-8
"""
Про сборку проекта/виртуалэнв/дебиан пакета.
"""
import tempfile
from functools import partial
from itertools import islice

from fabric.operations import local, abort


PYPI = 'https://pypi.python.org/simple/'


def update_packages(where='venv/home', env='development'):
    install_requirements_cmd = ' '.join([
        'PIP_DOWNLOAD_CACHE=/tmp/.pip/download-cache',
        'PIP_ACCEL_CACHE=/tmp/.pip-accel/',
        '%s/bin/pip-accel install' % where,
        '--index-url %s' % PYPI,
        '--requirement requirements-%s' % env,
        '--upgrade'
    ])

    local(' && '.join([
        '. %s/bin/activate' % where,
        install_requirements_cmd,
        'deactivate',
    ]))


def build_virtualenv(
        where='venv/home',
        global_site_packages=True,
        env='production'):
    """
    Создание virtualenv.
    where -- где создавать virtualenv
    global_site_packages -- если True, происходит фолбэк на системные
        site-packages
    env -- ('production'|'testing'|'development') -- выбор файла с зависимостями
    (.pth с ссылкой на директорию).
    """

    if local('(pip list | grep virtualenv) || echo false', capture=True) != 'false':
        local('virtualenv %s' % where)
    else:
        local('pip install virtualenv -i %s' % PYPI)
        local('virtualenv %s' % where)
        local('ln -sf /usr/lib/python2.7/distutils %s/local/lib/python2.7/distutils' % where)

    local(' && '.join([
        '. %s/bin/activate' % where,
        '%s/bin/pip install -i %s pip-accel' % (where, PYPI),
    ]))

    development_flag = '-e' if env == 'development' else ''

    install_requirements_cmd = ' '.join([
        'PIP_DOWNLOAD_CACHE=/tmp/.pip/download-cache',
        'PIP_ACCEL_CACHE=/tmp/.pip-accel/',
        '%s/bin/pip-accel install' % where,
        '-i %s' % PYPI,
        '-r requirements-%s' % env,
    ])

    local(' && '.join([
        '. %s/bin/activate' % where,
        install_requirements_cmd,
        '%s/bin/pip install %s .' % (where, development_flag),
        'deactivate',
    ]))

    if global_site_packages:
        # делаем неизолированным,
        local('rm %s/lib/python2.7/no-global-site-packages.txt' % where)


# девелоперская сборка
develop = partial(build_virtualenv, env='development')
