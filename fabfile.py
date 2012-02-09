"""Fabfile for the ``webfaction-django-boilerplate``.

Make sure to setup your ``fabric_settings.py`` first. As a start, just copy
``fabric_settings.py.sample``.

"""
from __future__ import with_statement

from fabric.api import (
    cd,
    env,
    lcd,
    local,
    run,
    settings,
)
from fabric.contrib.files import append, exists,  sed

import fabric_settings as fab_settings


env.hosts = fab_settings.ENV_HOSTS
env.user = fab_settings.ENV_USER


BASHRC_SETTING1 = 'export VIRTUALENVWRAPPER_PYTHON=/usr/local/bin/python2.7'
BASHRC_SETTING2 = 'export WORKON_HOME=$HOME/Envs'
BASHRC_SETTING3 = 'source /home/{0}/bin/virtualenvwrapper.sh'.format(env.user)
BASHRC_SETTING4 = 'export PIP_VIRTUALENV_BASE=$WORKON_HOME'
BASHRC_SETTING5 = 'export PIP_RESPECT_VIRTUALENV=true'


# ****************************************************************************
# HIGH LEVEL TASKS
# ****************************************************************************
def install_everything():
    install_local_repo()
    install_server()
    local_link_repo_with_remote_repo()
    first_deployment()


def first_deployment():
    run_clone_repo()
    run_install_scripts()
    run_prepare_wsgi()


def install_local_repo():
    local_create_new_repo()
    local_init_django_project()
    local_initial_commit()


def install_server():
    run_install_virtualenv()
    run_install_mercurial()
    run_add_bashrc_settings()
    run_create_virtualenv()
    run_create_git_repo()


# ****************************************************************************
# LOCAL TASKS
# ****************************************************************************
def local_link_repo_with_remote_repo():
    with lcd(fab_settings.PROJECT_ROOT):
        local('git config http.sslVerify false')
        local('git config http.postBuffer 524288000')
        local('git remote add origin'
                ' https://{0}@git.{0}.webfactional.com/{1}'.format(
                    fab_settings.ENV_USER, fab_settings.GIT_REPO_NAME))
        local('git push -u origin master')


def local_create_new_repo():
    with lcd(fab_settings.PROJECT_ROOT):
        local('rm -rf .git')
        local('rm .gitmodules')
        local('rm -rf website/webapps/django/project/submodules/Skeleton')
        local('git init')
        local('git submodule add git://github.com/dhgamache/Skeleton.git'
                ' website/webapps/django/project/submodules/Skeleton')


def local_init_django_project():
    with lcd(fab_settings.DJANGO_PROJECT_ROOT):
        local('cp settings/local/local_settings.py.sample'
                ' settings/local/local_settings.py')
        local('cp settings/local/gorun_settings.py.sample gorun_settings.py')
        local('python manage.py syncdb --all --noinput')
        local('python manage.py migrate --fake')
        local('python manage.py loaddata bootstrap_auth.json')


def local_initial_commit():
    with lcd(fab_settings.PROJECT_ROOT):
        local('git add .')
        local('git commit -am "Initial commit."')


# ****************************************************************************
# REMOTE TASKS
# ****************************************************************************
def run_add_bashrc_settings():
    with cd('$HOME'):
        append('.bashrc', BASHRC_SETTING1, partial=True)
        append('.bashrc', BASHRC_SETTING2, partial=True)
        append('.bashrc', BASHRC_SETTING3, partial=True)
        append('.bashrc', BASHRC_SETTING4, partial=True)
        append('.bashrc', BASHRC_SETTING5, partial=True)


def run_clone_repo():
    run('mkdir -p $HOME/src')
    cloned_repo_path = '$HOME/src/{0}'.format(fab_settings.PROJECT_NAME)
    if exists(cloned_repo_path):
        run('rm -rf {0}'.format(cloned_repo_path))
    with cd('$HOME/src'):
        run('git clone $HOME/webapps/git/repos/{0} {1}'.format(
            fab_settings.GIT_REPO_NAME, fab_settings.PROJECT_NAME))


def run_create_git_repo():
    run('rm -rf $HOME/webapps/git/repos/{0}'.format(
        fab_settings.GIT_REPO_NAME))
    with cd('$HOME/webapps/git'):
        run('git init --bare ./repos/{0}'.format(fab_settings.GIT_REPO_NAME))
    with cd('$HOME/webapps/git/repos/{0}'.format(fab_settings.GIT_REPO_NAME)):
        run('git config http.receivepack true')


def run_create_ssh_dir():
    with cd('$HOME'):
        with settings(warn_only=True):
            run('mkdir .ssh')
            run('touch .ssh/authorized_keys')
            run('chmod 600 .ssh/authorized_keys')
            run('chmod 700 .ssh')


def run_create_virtualenv():
    with cd('$HOME'):
        run('mkvirtualenv -p python2.7 {0}'.format(fab_settings.VENV_NAME))


def run_install_mercurial():
    with cd('$HOME'):
        run('easy_install-2.7 mercurial')


def run_install_scripts():
    with cd('$HOME/src/{0}/scripts'.format(fab_settings.PROJECT_NAME)):
        run('git pull origin master')
        run('cp deploy-website.sh $HOME/bin/deploy-website-{0}.sh'.format(
            fab_settings.PROJECT_NAME))
        run('cp mysql-backup.sh $HOME/bin/mysql-backup-{0}.sh'.format(
            fab_settings.PROJECT_NAME))
        run('cp restart-apache.sh $HOME/bin/restart-apache-{0}.sh'.format(
            fab_settings.PROJECT_NAME))
        run('cp show-memory.sh $HOME/bin/show-memory.sh')
        run('cp script_settings.sh $HOME/bin/script_settings.sh')

    with cd('$HOME/bin'):
        sed('script_settings.sh', 'INSERT_USERNAME', fab_settings.ENV_USER)
        sed('script_settings.sh', 'INSERT_DB_USER', fab_settings.MYSQL_DB_USER)
        sed('script_settings.sh', 'INSERT_DB_NAME', fab_settings.MYSQL_DB_NAME)
        sed('script_settings.sh', 'INSERT_DB_PASSWORD',
            fab_settings.MYSQL_DB_PASSWORD)
        sed('script_settings.sh', 'INSERT_PROJECT_NAME',
            fab_settings.PROJECT_NAME)
        sed('script_settings.sh', 'INSERT_DJANGO_APP_NAME',
            fab_settings.DJANGO_APP_NAME)


def run_install_virtualenv():
    with cd('$HOME'):
        run('mkdir -p $HOME/lin/python2.7')
        run('easy_install-2.7 virtualenv')
        run('easy_install-2.7 pip')
        run('pip install virtualenvwrapper')
        run('mkdir -p $HOME/Envs')


def run_prepare_wsgi():
    with cd('$HOME/webapps/{0}/lib/python2.7/'.format(
        fab_settings.DJANGO_APP_NAME)):
        run('rm -rf django')
        run('rm -rf Django*')
    with cd('$HOME/webapps/{0}'.format(fab_settings.DJANGO_APP_NAME)):
        run('cp $HOME/src/{0}/scripts/myproject.wsgi .'.format(
            fab_settings.PROJECT_NAME))
        sed('myproject.wsgi', 'ENV_USER', fab_settings.ENV_USER)
        sed('myproject.wsgi', 'VENV_NAME', fab_settings.VENV_NAME)
        sed('myproject.wsgi', 'DJANGO_APP_NAME', fab_settings.DJANGO_APP_NAME)
