# Webfaction Django Boilerplate

## Use it, if you know what you are doing

This boilerplate has been tested with a fresh Webfaction server on March 23 2012.
It worked without any issues. However, if you use it and ``fab install_everything``
crashes you will have read the fabric error message carefully, think hard about what
might have gone wrong, probably fix the fabfile (and open an issue here) and try again.
The fab task is setup in such a way that it deletes previous failed attempts on the
server so that it can be run over and over again. Unfortunately there might be some 
TODOs left (check the TODO section at the bottom of this file), for example if you
run the fab task again, you will end up having the crontabs twice. I will try to fix
this ASAP.

This project will help you to start new
[Django](https://www.djangoproject.com/) projects on
[Webfaction](http://www.webfaction.com/) servers.

## Naming conventions

Throughout the instructions we will stick to the following naming conventions:

* ``username`` is your webfaction username. You will want to chose a username
  as short as possible since database names have to start with ``username_``
  and are quite limited in length.
* ``yourproject`` is the name of your project. You will probably name your
  folder on your local development environment like this. It should be a short
  name as well.
* We will prepend or append ``yourproject`` at many places. We _could_ just
  name your apps ``django``, ``static`` and ``media`` etc. but we want to make
  sure that you are able to host several projects on one machine in a clean and
  manageable way. Most likely ``yourproject`` and ``username`` will be the same
  for your first site.
* ``yourdomain.com`` is the domain that you want to use.

## Webfaction panel

Before you can start to deploy your Django site on your Webfaction server,
you need to add various settings at your Webfaction control panel:

* First, change your
  [control panel password](https://my.webfaction.com/change_password/create)
* Next, change your
  [SSH/FTP password](https://my.webfaction.com/change_ssh_password/create)
* Go to
  [domains management](https://my.webfaction.com/domains)
* Add the domain ``git.username.webfactional.com``
* Add the domain ``yourdomain.com`` and ``www.yourdomain.com``
* Go to [applications management](https://my.webfaction.com/app_/list)
* Create a new ``Django`` app ``Django X.X.X (mod_wsgi 3.3/Python 2.7)``. Call it
* ``yourproject_django``. Just select the latest release. It doesn't really
  matter because we will use a virtualenv anyways.
* Create a new ``Static`` app ``Static only (no .htaccess)``. Call it
  ``yourproject_media`` and enable ``expires max``.
* Create a new ``Static`` app ``Static only (no .htaccess)``. Call it
  ``yourproject_static`` and enable ``expires max``.
* Create a new app ``Static/CGI/PHP-5.3``. Call it ``yourproject_www``.
* Create a new app ``Git``. Call it ``git`` and enter a password.
* Go to [website management](https://my.webfaction.com/site/list)
* Add a new site called ``yourproject`` and map ``yourproject_django`` to
  ``/``, ``yourproject_media`` to ``/media`` and ``yourproject_static`` to
  ``/static``.
* Use the subdomains ``username.webfactional.com``, ``yourdomain.com`` and
  ``www.yourdomain.com``.
* Add a new site called ``git`` and map ``git`` to ``/``.
* Mark it as ``HTTPS``
* Use the subdomain ``git.username.webfactional.com``
* Go to [database management](https://my.webfaction.com/database/create)
* Create your database (``username_yourproject``) and note down the password.
  You should create a PostgreSQL database as the latest MySQL has problems with
  south migrations of ``easy_thumbnails``.
* Got to [email management](https://my.webfaction.com/mailboxes)
* Crate a new mailbox (``username_yourproject``) and note down the password.

## Local machine

First setup your local virtualenv. If you are not familiar with
[virtualenv](http://pypi.python.org/pypi/virtualenv) and
[virtualenvwrapper](http://www.doughellmann.com/projects/virtualenvwrapper/)
we strongly recommend to have a look at those first:

    mkvirtualenv -p python2.7 yourproject
    workon yourproject

Next ``cd`` into your desired project folder and clone this repository:

    cd $HOME/Projects
    mkdir yourproject
    cd yourproject
    git clone git://github.com/bitmazk/webfaction-django-boilerplate.git src

Now you can install some requirements that we need to run fabric. We also added
some useful tools that will help you to develop and debug your project more
efficiently. You should also install the requirements of the actual Django
project. Please note that if you are on Linux and want to use gorun for continuous
testing, you should uncomment a few lines in the first ``requirements.txt``:

    cd src
    pip install -r requirements.txt --upgrade
    pip install -r website/webapps/django/project/requirements.txt --upgrade

Next you need to copy ``fabric_settings.py.sample`` and modify it for your needs.
Basically you just need to modify your webfaction username and your desired
project name. Usually both will be the same unless you are hosting several
Django apps on the same Webfaction server. It also holds some values that will
be inserted into your server's ``local_settings.py``.

    cp fabric_settings.py.sample fabric_settings.py

You might want to create a ``.ssh`` directory on your Webfaction server with 
permissions setup properly. Once you have done that, copy your public key, ssh 
into your Webfaction server and append your key to ``.ssh/authorized_keys``. If
you have already done sone, you can skip this step. It will setup the ``.ssh``
folder on your server according to the Webfaction user guide on
[accessing your data using SSH keys](https://docs.webfaction.com/user-guide/access.html#using-ssh-keys):

    fab run_create_ssh_dir
    
Since you are on the server now anyways, you might consider to install our
[Webfaction dotfiles](https://github.com/bitmazk/webfaction-dotfiles).

From now on we will use a fabric file that will setup your local repository and
deploy it on your webfaction server. First it will prepare your local repository.
Obviously you cloned this boilerplate repository but you don't want our history
in your new project's history. So first the fabfile delete the ``.git`` folder and
``.gitmodules``, run ``git init``, add submodules, copy local settings files
and run ``syncdb`` and ``loaddata``.

After this you should be able to ``cd`` into the ``project`` folder, run
``./manage.py runserver`` and login to ``/admin-XXXX/`` with username ``admin``
and password ``test123``.

Next it will login to your Webfaction server and create a git repository, hook
up your local repo with the one on the server and do a push. It will install many
useful scripts for django-cleanup, database backups, media-files backups and 
translation catalogues backups. It will install cronjobs, place a .pgpass file,
install virtualenv and virtualenvwrapper, make changes to the .bashrc file,
clone your repo into the folder ``/src``, install the ``requirements.txt`` and
do a first deployment, which will run ``syncdb``, ``migrate``, ``collectstatic`` and
``makemessages``. And for all this goodness you only need one command:

    # The task will only halt once and ask for your git password
    fab install_everything

This will run for up to 20 minutes or so. Afterwards you will have a ready to go local
project that is also deployed on your Webfaction server.

We even went one step further and provided initial fixtures which should give
you everything you need for a normal website. In order to install the fixtures
locally do the following. If you just want to create your own CMS pages and
start creating your templates, you can skp this step:

    cd website/webapps/django/project
    fab rebuild
    ./manage.py runserver
    
The idea behind this rebuild command is that a new developer should never be forced
to download the lates database from production in order to get started. Instead
we should always provide fixtures that setup enough test data so that a new developer
can run ``fab rebuild`` and as a result he will see a fresh database that has all
needed CMS pages and apphooks and lorem ipsum blog posts and other test data inside.

Your development workflows might differ, so you can just ignore this command.

## Webfaction server

At this point you are able to browse to ``username.webfactional.com`` and see
the django-cms welcome screen. First you should login at ``/admin-XXXX/``
with username ``admin`` and password ``test123``  and change your password.

The next thing you should do is ssh into your Webfaction server and change
the secret key in
``$HOME/webapps/yourproject_django/project/settings/local/local_settings.py``.

If you want to make use of the ``fab rebuild`` command on your server as well,
you should run:

    workon yourproject
    pip install fabric
    pip install coverage
    cd $HOME/webapps/yourproject_django/project/
    fab rebuild

This setup assumes that you are deploying a multilingual project, so you would
want to create your first translation catalogues now:

    cd $HOME/webapps/yourproject_django/project/
    workon yourproject
    ./manage.py makemessages -l ch_ZN

If you don't intend to use i18n, you can remove the scheduled backups from
crontab:

    crontab -e
    # remove the line about locale-backup.sh

## Misc

In your local project you should change the recepients for the contact form
app. Usually this should be your customers ``info@yourdomain.com`` address.
You can find the file at
``../project/settings/installed_apps/contact_form.py``.

You should also have a look at ``../project/templates/base.html`` and change
the site name that gets appended to the title. If you are using Google
Analytics, you should enter your ID, if not, you should delete the analytics
code snippet.


## TODO

* Document what gets changed and how to revert in case of failure
* fab rebuild does not work because there is no test_media
* Why is there a ``fabfile_settings.py-r`` and ``urls.py-r`` after install everything?
* Add ``pg_backup.sh`` script (test this)
* News text is not displayed
* Add ``delete_project`` task
* Only add cronjobs if not there already
* Make sure django forwards to www
* Bug: Stuff gets appended to .bashrc even if it is already there
* Autogenerate secret key
* Use ssh for git authentication
