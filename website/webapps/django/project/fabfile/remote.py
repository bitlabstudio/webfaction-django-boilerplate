"""Fabric commands that are run on the server."""
from fabric.api import (
    cd,
    env,
    run,
)

import fab_settings


env.hosts = fab_settings.ENV_HOSTS
env.user = fab_settings.ENV_USER


def run_deploy_website():
    with cd('$HOME/'):
        run('deploy-website-{0}.sh'.format(fab_settings.PROJECT_NAME))


def run_restart_apache():
    with cd('$HOME/'):
        run('restart-apache-{0}.sh'.format(fab_settings.PROJECT_NAME))
