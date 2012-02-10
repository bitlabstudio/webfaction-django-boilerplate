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
* Add new site called ``yourproject_www`` and map it to the ``yourproject_www``
  app. Attach the top level domain of your project to it (the one without
  ``www``).
* Add a new site called ``yourproject`` and map ``yourproject_django`` to
  ``/``, ``yourproject_media`` to ``/media`` and ``yourproject_static`` to
  ``/static``.
* Use the subdomains ``yourproject.wefactional.com`` and
  ``www.yourdomain.com``.
* Go to [database management](https://my.webfaction.com/database/create)
* Create your database (``username_yourproject``) and note down the password.
* Got to [email management](https://my.webfaction.com/mailbox/create)
* Crate a new mailbox (``username_yourproject``) and note down the password.

## Local machine

First setup your local virtualenv. If you are not familiar with virtualenv and
virtualenvwrapper we strongly recommend to have a look at those first:

    mkvirtualenv yourproject -p python2.7
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
Django apps on the same Webfaction server.

    cp fab_settings.py.sample fab_settings.py

You might want to create a ``.ssh`` directory on your server with permissions
setup properly. Once you have done that, copy your public key, ssh into your
server and append your key to ``.ssh/authorized_keys``:

    fab create_ssh_dir

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

## Webfaction server

* Change secret key
