# Webfaction Django Boilerplate

## DO NOT USE THIS!

This repo is a work in progress. Do not use it as long as this warning message
is in the readme.

This project will help you to start new
[Django](https://www.djangoproject.com/) projects on
[Webfaction](http://www.webfaction.com/) servers.

## Naming conventions

Throughout the instructions we will stick to the following naming conventions:

* ``username`` is your webfaction username. You will want to chose a username
  as short as possible since database names have to start with ``username_``
  and are quite limited in lenght.
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
  [channel password](https://my.webfaction.com/change_password/create)
* Next, change your
  [SSH/FTP password](https://my.webfaction.com/change_ssh_password/create)
* Go to
  [domains management](https://my.webfaction.com/change_ssh_password/create)
* Add the domain ``git.username.webfactional.com``
* Add the domain ``yourdomain.com`` and ``www.yourdomain.com``
* Go to [applications management](https://my.webfaction.com/app_/list)
* Create a new app ``Django X.X.X (mod_wsgi 3.3/Python 2.7)``. Call it
* ``yourproject_django``. Just select the latest release. It doesn't really
  matter because we will use a virtualenv anyways.
* Create a new app ``Static only (no .htaccess)``. Call it
  ``yourproject_media`` and enable ``expires max``.
* Create a new app ``Static only (no .htaccess)``. Call it
  ``yourproject_static`` and enable ``expires max``.
* Create a new app ``Static/CGI/PHP-5.3``. Call it ``yourproject_www``.
* Create a new app ``Git`` and enter a password.
* Go to [website management](https://my.webfaction.com/site/list)
* Add a new site called ``yourproject`` and map ``yourproject_django`` to
  ``/``, ``yourproject_media`` to ``/media`` and ``yourproject_static`` to
  ``/static``.
* Use the subdomains ``yourproject.wefactional.com``, ``yourdomain.com`` and
  ``www.yourdomain.com``.
* Go to [database management](https://my.webfaction.com/database/create)
* Create your database (``username_yourproject``) and note down the password.
* Got to [email management](https://my.webfaction.com/mailbox/create)
* Crate a new mailbox (``username_yourproject``) and note down the password.

## Local machine

First setup your local virtualenv. If you are not familiar with virtualenv and
virtualenvwrapper we strongly recommend to have a look at those first:

    mkvirtualenv -p python2.7 yourproject
    workon yourproject

Next ``cd`` into your desired project folder and clone this repository:

    cd $HOME/Projects
    mkdir yourproject
    cd yourproject
    git clone git clone git://github.com/bitmazk/webfaction-django-boilerplate.git src

Now you can install some requirements that we need to run fabric. We also added
some useful tools that will help you to develop and debug your project more
efficiently. You should also install the requirements of the actual Django
project. Please note that if you are on OSX you should comment out a line in
the first ``requirements.txt``:

    cd src
    pip install -r requirements.txt --upgrade
    pip install -r website/webapps/django/project/requirements.txt --upgrade

Next you need to copy ``fab_settings.py.sample`` and modify it for your needs.
Basically you just need to modify your webfaction username and your desired
project name. Usually both will be the same unless you are hosting several
Django apps on the same Webfaction server. It also holds some values that will
be inserted into your server's ``local_settings.py``.

    cp fabric_settings.py.sample fabric_settings.py

You might want to create a ``.ssh`` directory on your server with permissions
setup properly. Once you have done that, copy your public key, ssh into your
server and append your key to ``.ssh/authorized_keys``:

    fab run_create_ssh_dir

From now on we will use a fabric file that will setup your local repository and
deploy it on your webfaction server. First let's prepare your local repository.
Obviously you cloned this boilerplate repository but you don't want our history
in your new project's history. So first we will delete the ``.git`` folder and
``.gitmodules``, run ``git init``, add submodules, copy local settings files
and run ``syncdb`` and ``loaddata``.

After this you should be able to ``cd`` into the ``project`` folder, run
``./manage.py runserver`` and login to ``/admin-XXXX/`` with username ``admin``
and password ``test123``:

    fab install_everything

We even went one step further and provided initial fixtures which should give
you everything you need for a normal website:

    cd website/webapps/django/project
    fab rebuild
    ./manage.py runserver


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

* News text is not displayed
* Add delete_project task
* Only add cronjobs if not there already
* Make sure django forwards to www
