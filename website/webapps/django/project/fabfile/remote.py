"""Fabric commands that are run on the server."""
from fabric.api import (
    cd,
    env,
    local,
    run,
)

import fab_settings
from settings import DATABASES


env.hosts = fab_settings.ENV_HOSTS
env.user = fab_settings.ENV_USER


def run_deploy_website():
    with cd('$HOME/'):
        run('deploy-website-{0}.sh'.format(fab_settings.PROJECT_NAME))


def run_download_db():
    db_engine = DATABASES['default']['ENGINE']
    db_name = DATABASES['default']['NAME']
    if 'sqlite' in db_engine:
        print('Download of sqlite database is not supported.')
    db_type = None
    if 'postgre' in db_engine:
        db_type = 'psql'
    if 'mysql' in db_engine:
        db_type = 'mysql'
    local('scp {2}@{2}.webfactional.com:/home/{2}/{0}_{1}.sql .'.format(
        db_name, db_type, fab_settings.ENV_USER))


def run_download_media():
    """Downloads the latest media files from the server."""
    with cd('$HOME/webapps/{0}_media/'.format(fab_settings.PROJECT_NAME)):
        run('tar -cvjf ../../{0}_media.tar.bz2 .'.format(
            fab_settings.PROJECT_NAME))
    local('scp {0}@{0}.webfactional.com:/home/{0}/{1}_media.tar.bz2'
          ' ../../'.format(fab_settings.ENV_USER, fab_settings.PROJECT_NAME))


def run_restart_apache():
    with cd('$HOME/'):
        run('restart-apache-{0}.sh'.format(fab_settings.PROJECT_NAME))


def run_upload_db():
    db_engine = DATABASES['default']['ENGINE']
    db_name = DATABASES['default']['NAME']
    if 'sqlite' in db_engine:
        print('Upload of sqlite database is not supported.')
    db_type = None
    if 'postgre' in db_engine:
        db_type = 'psql'
    if 'mysql' in db_engine:
        db_type = 'mysql'
    local('scp {0}_{1}.sql {2}@{2}.webfactional.com:/home/{2}/'.format(
        db_name, db_type, fab_settings.ENV_USER))
