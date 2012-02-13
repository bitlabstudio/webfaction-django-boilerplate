"""Fabfile for the ``webfaction-django-boilerplate``.

Make sure to setup your ``fabric_settings.py`` first. As a start, just copy
``fabric_settings.py.sample``.

"""
from __future__ import with_statement

import os

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
    run_delete_previous_attempts()
    run_clone_repo()
    run_install_scripts()
    run_install_crontab()
    run_prepare_wsgi()
    run_install_requirements()
    run_deploy_website(with_manage_py=False)
    run_prepare_local_settings()
    run_deploy_website()
    run_loaddata_auth()


def install_local_repo():
    local_create_new_repo()
    local_init_django_project()
    local_create_fab_settings()
    local_initial_commit()


def install_server():
    run_install_virtualenv()
    run_install_mercurial()
    run_add_bashrc_settings()
    run_create_virtualenv()
    run_create_git_repo()
    run_delete_index_files()


# ****************************************************************************
# LOCAL TASKS
# ****************************************************************************
def local_link_repo_with_remote_repo():
    with lcd(fab_settings.PROJECT_ROOT):
        local('git config http.sslVerify false')
        local('git config http.postBuffer 524288000')
        with settings(warn_only=True):
            local('git remote rm origin')
        local('git remote add origin'
                ' https://{0}@git.{0}.webfactional.com/{1}'.format(
                    fab_settings.ENV_USER, fab_settings.GIT_REPO_NAME))
        local('git push -u origin master')


def local_create_fab_settings():
    fabfile_dir = os.path.join(fab_settings.PROJECT_ROOT, 'website',
        'webapps', 'django', 'project', 'fabfile')
    print fabfile_dir
    with lcd(fabfile_dir):
        local('cp fab_settings.py.sample fab_settings.py')
        local("sed -i -r -e 's/INSERT_PROJECT_NAME/{0}/g'"
              " fab_settings.py".format(fab_settings.PROJECT_NAME))
        local("sed -i -r -e 's/INSERT_ENV_USER/{0}/g'"
              " fab_settings.py".format(fab_settings.ENV_USER))


def local_create_new_repo():
    with lcd(fab_settings.PROJECT_ROOT):
        local('rm -rf .git')
        local('rm -f .gitmodules')
        local('rm -rf website/webapps/django/project/submodules/Skeleton')
        local('git init')
        local('git submodule add git://github.com/dhgamache/Skeleton.git'
                ' website/webapps/django/project/submodules/Skeleton')


def local_init_django_project():
    with lcd(fab_settings.DJANGO_PROJECT_ROOT):
        local('cp settings/local/local_settings.py.sample'
                ' settings/local/local_settings.py')
        local('cp fabfile/fab_settings.py.sample'
                ' fabfile/fab_settings.py')
        local('cp settings/local/gorun_settings.py.sample gorun_settings.py')
        local('python manage.py syncdb --all --noinput')
        local('python manage.py migrate --fake')
        local('python manage.py loaddata bootstrap_auth.json')
        local("sed -i -r -e 's/XXXX/{0}/g' urls.py".format(
            fab_settings.ADMIN_URL))

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
    with cd('$HOME/src/{0}'.format(fab_settings.PROJECT_NAME)):
        run('git submodule init')
        run('git submodule update')


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
        run('rm -rf $HOME/Envs/{0}'.format(fab_settings.VENV_NAME))
        run('mkvirtualenv -p python2.7 --system-site-packages {0}'.format(
            fab_settings.VENV_NAME))


def run_delete_index_files():
    run('rm -f $HOME/webapps/{0}/index.html'.format(
        fab_settings.MEDIA_APP_NAME))
    run('rm -f $HOME/webapps/{0}/index.html'.format(
        fab_settings.STATIC_APP_NAME))


def run_delete_previous_attempts():
    run('rm -rf $HOME/webapps/{0}/project'.format(
        fab_settings.DJANGO_APP_NAME))
    run('rm -rf $HOME/Envs/{0}/'.format(fab_settings.VENV_NAME))
    run('rm -rf $HOME/src/{0}/'.format(fab_settings.PROJECT_NAME))
    run('rm -rf $HOME/bin/*{0}*.*'.format(fab_settings.PROJECT_NAME))
    # TODO remove crontab jobs


def run_deploy_website(with_manage_py=True):
    args = ' 1'
    if with_manage_py:
        args = ''

    run('workon {0} && deploy-website-{1}.sh{2}'.format(fab_settings.VENV_NAME,
        fab_settings.PROJECT_NAME, args))


def run_install_crontab():
    with cd('$HOME/bin/'):
        run('crontab -l > crontab_tmp')
        run('cat crontab-{0}.txt >> crontab_tmp'.format(
            fab_settings.PROJECT_NAME))
        run('crontab crontab_tmp')
        run('rm crontab_tmp')


def run_install_mercurial():
    with cd('$HOME'):
        run('easy_install-2.7 mercurial')


def run_install_requirements():
    run('workon {0} && pip install -r $HOME/src/{1}/website/webapps/django/'
        'project/requirements.txt --upgrade'.format(
            fab_settings.VENV_NAME, fab_settings.PROJECT_NAME))


def run_install_scripts():
    project_name = fab_settings.PROJECT_NAME
    script_settings_name = 'script-settings-{0}.sh'.format(project_name)
    deploy_website_name = 'deploy-website-{0}.sh'.format(project_name)
    mysql_backup_name = 'mysql-backup-{0}.sh'.format(project_name)
    pg_backup_name = 'pg-backup-{0}.sh'.format(project_name)
    restart_apache_name = 'restart-apache-{0}.sh'.format(project_name)
    django_cleanup_name = 'django-cleanup-{0}.sh'.format(project_name)
    crontab_name = 'crontab-{0}.txt'.format(project_name)
    with cd('$HOME/src/{0}/scripts'.format(project_name)):
        run('git pull origin master')
        run('cp deploy-website.sh $HOME/bin/{0}'.format(deploy_website_name))
        run('cp mysql-backup.sh $HOME/bin/{0}'.format(mysql_backup_name))
        run('cp restart-apache.sh $HOME/bin/{0}'.format(restart_apache_name))
        run('cp django-cleanup.sh $HOME/bin/{0}'.format(django_cleanup_name))
        run('cp script-settings.sh $HOME/bin/{0}'.format(script_settings_name))
        run('cp crontab.txt $HOME/bin/{0}'.format(crontab_name))
        run('cp show-memory.sh $HOME/bin/show-memory.sh')

    with cd('$HOME/bin'):
        sed(script_settings_name, 'INSERT_USERNAME', fab_settings.ENV_USER)
        sed(script_settings_name, 'INSERT_DB_USER', fab_settings.DB_USER)
        sed(script_settings_name, 'INSERT_DB_NAME', fab_settings.DB_NAME)
        sed(script_settings_name, 'INSERT_DB_PASSWORD',
            fab_settings.DB_PASSWORD)
        sed(script_settings_name, 'INSERT_PROJECT_NAME', project_name)
        sed(script_settings_name, 'INSERT_DJANGO_APP_NAME',
            fab_settings.DJANGO_APP_NAME)
        sed(script_settings_name, 'INSERT_VENV_NAME', fab_settings.VENV_NAME)
        sed(deploy_website_name, 'INSERT_PROJECTNAME', project_name)
        sed(mysql_backup_name, 'INSERT_PROJECTNAME', project_name)
        sed(pg_backup_name, 'INSERT_PROJECTNAME', project_name)
        sed(restart_apache_name, 'INSERT_PROJECTNAME', project_name)
        sed(django_cleanup_name, 'INSERT_PROJECTNAME', project_name)
        sed(crontab_name, 'INSERT_PROJECTNAME', project_name)
        run('rm -f *.bak')


def run_install_virtualenv():
    with cd('$HOME'):
        run('mkdir -p $HOME/lib/python2.7')
        run('easy_install-2.7 virtualenv')
        run('easy_install-2.7 pip')
        run('pip install virtualenvwrapper')
        run('mkdir -p $HOME/Envs')


def run_loaddata_auth():
    with cd('$HOME/webapps/{0}/project/'.format(fab_settings.DJANGO_APP_NAME)):
        run('workon {0} && ./manage.py loaddata bootstrap_auth.json'.format(
            fab_settings.VENV_NAME))


def run_prepare_local_settings():
    with cd('$HOME/webapps/{0}/project/settings/local'.format(
        fab_settings.DJANGO_APP_NAME)):
        run('cp local_settings.py.sample local_settings.py')
        sed('local_settings.py', 'backends.sqlite3',
            'backends.postgresql_psycopg2')
        sed('local_settings.py', 'db.sqlite', fab_settings.DB_NAME)
        sed('local_settings.py', '"USER": ""', '"USER": "{0}"'.format(
            fab_settings.DB_USER))
        sed('local_settings.py', '"PASSWORD": ""', '"PASSWORD": "{0}"'.format(
            fab_settings.DB_PASSWORD))
        sed('local_settings.py', 'yourproject', '{0}'.format(
            fab_settings.PROJECT_NAME))
        sed('local_settings.py', 'FROM_EMAIL = "info@example.com"',
            'FROM_EMAIL = "{0}"'.format(fab_settings.EMAIL_DEFAULT_FROM_EMAIL))
        sed('local_settings.py', 'EMAIL_BACKEND', '#EMAIL_BACKEND')
        sed('local_settings.py', '##EMAIL_BACKEND', 'EMAIL_BACKEND')
        sed('local_settings.py', '#EMAIL_HOST', 'EMAIL_HOST')
        sed('local_settings.py', '#EMAIL_HOST_USER', 'EMAIL_HOST_USER')
        sed('local_settings.py', 'EMAIL_HOST_USER = ""',
            'EMAIL_HOST_USER = "{0}"'.format(fab_settings.EMAIL_INBOX))
        sed('local_settings.py', '#EMAIL_HOST_PASSWORD', 'EMAIL_HOST_PASSWORD')
        sed('local_settings.py', 'EMAIL_HOST_PASSWORD = ""',
            'EMAIL_HOST_PASSWORD = "{0}"'.format(fab_settings.EMAIL_PASSWORD))
        sed('local_settings.py', '#EMAIL_USE_TLS', 'EMAIL_USE_TLS')
        sed('local_settings.py', '#EMAIL_PORT', 'EMAIL_PORT')
        sed('local_settings.py', 'MEDIA_APP_NAME', fab_settings.MEDIA_APP_NAME)
        sed('local_settings.py', 'STATIC_APP_NAME',
            fab_settings.STATIC_APP_NAME)
        sed('local_settings.py', 'yourname', fab_settings.ADMIN_NAME)
        sed('local_settings.py', 'info@example.com', fab_settings.ADMIN_EMAIL)
        run('rm -f *.bak')


def run_prepare_wsgi():
    with cd('$HOME/webapps/{0}/lib/python2.7/'.format(
        fab_settings.DJANGO_APP_NAME)):
        run('rm -rf django')
        run('rm -rf Django*')
    with cd('$HOME/webapps/{0}'.format(fab_settings.DJANGO_APP_NAME)):
        run('rm -rf myproject')
        run('cp $HOME/src/{0}/scripts/myproject.wsgi .'.format(
            fab_settings.PROJECT_NAME))
        sed('myproject.wsgi', 'ENV_USER', fab_settings.ENV_USER)
        sed('myproject.wsgi', 'VENV_NAME', fab_settings.VENV_NAME)
        sed('myproject.wsgi', 'DJANGO_APP_NAME', fab_settings.DJANGO_APP_NAME)
        run('rm -f *.bak')
