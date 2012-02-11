"""Fabric commands that are run locally."""
import os

from coverage.misc import CoverageException
from fabric.api import local, settings
from fabric.colors import _wrap_with

from settings import TEST_APPS, MEDIA_ROOT, PROJECT_ROOT
from fab_settings import WWW_OPEN


green_bg = _wrap_with('42')
red_bg = _wrap_with('41')


def check():
    """Checks if the current state can be pushed."""
    flake8()
    test()
    coverage(0)


def coverage(html=1):
    """Runs coverage with html output or returns percentage of coverage::

        fab coverage:1      # will create html output (default)
        fab coverage:0      # will return percentage

    """
    not_html = not int(html)
    settings_file = (not_html and 'settings.coverage_nohtml_settings'
                     or 'settings.coverage_settings')
    try:
        results = local('./manage.py test_coverage --settings={0} {1}'.format(
             settings_file, ' '.join(TEST_APPS)), capture=not_html)
    except:
        raise CoverageException(
            red_bg("You have failing tests, run 'fab test' for more details"))

    if not_html:
        global_percentage = int(results.split("\n")[-3].split()[-1][:-1])
        files_percents = dict((
                line.split()[0],  # filename
                int(line.split()[3][:-1]),  # file percentage
            ) for line in results.split("-" * 45)[1].split("\n")[1:-1])

        errors = []
        for name, percentage in files_percents.iteritems():
            if percentage < 80:
                errors.append(red_bg(
                    'The file {0} is only covered to {1}%'.format(
                        name, percentage)))
        if errors:
            raise CoverageException(
                "\nThere isn't enought coverage:\n{0}".format(
                    "\n\t".join(errors)))
        else:
            print(green_bg('{0}% of the code is covered'.format(
                global_percentage)))
    else:
        local('{0} coverage_html/index.html'.format(WWW_OPEN))


def dumpdata():
    """Dumps everything.

    Remember to add new dumpdata commands for new apps here so that you always
    get a full initial dump when running this task.

    """
    local('python2.7 ./manage.py dumpdata --indent 4 --natural auth --exclude auth.permission > _global/fixtures/bootstrap_auth.json')  # NOQA
    local('python2.7 ./manage.py dumpdata --indent 4 --natural sites > _global/fixtures/bootstrap_sites.json')  # NOQA
    local('python2.7 ./manage.py dumpdata --indent 4 --natural cms > _global/fixtures/bootstrap_cms.json') # NOQA
    local('python2.7 ./manage.py dumpdata --indent 4 --natural text > _global/fixtures/bootstrap_cms_plugins_text.json') # NOQA
    local('python2.7 ./manage.py dumpdata --indent 4 --natural cmsplugin_blog > _global/fixtures/bootstrap_cmsplugin_blog.json') # NOQA
    local('python2.7 ./manage.py dumpdata --indent 4 --natural tagging > _global/fixtures/bootstrap_tagging.json') # NOQA


def flake8():
    """Searches for PEP8 errors in all project files."""
    local("flake8 --statistics .")


def push():
    """git push after checking tests and syntax"""
    check()
    local("git push")


def rebuild():
    """Deletes the database and recreates the database.

    Does not work with PostgreSQL. TODO: Create a new manage.py command
    that deletes all tables instead of the whole database.
    """
    rebuild_db()
    rebuild_media()


def rebuild_db():
    """Syncdb localhost or remote server."""
    local('python2.7 manage.py reset_db --router=default --noinput')
    local('python2.7 manage.py syncdb --all --noinput')
    local('python2.7 manage.py migrate --fake')
    local('python2.7 manage.py loaddata bootstrap_auth.json')
    local('python2.7 manage.py loaddata bootstrap_sites.json')
    local('python2.7 manage.py loaddata bootstrap_cms.json')
    local('python2.7 manage.py loaddata bootstrap_cms_plugins_text.json')
    local('python2.7 manage.py loaddata bootstrap_cmsplugin_blog.json')
    local('python2.7 manage.py loaddata bootstrap_tagging.json')
    local('python2.7 manage.py loaddata bootstrap.json')


def rebuild_media():
    """Copies media fixtures into your media_root."""
    files_to_delete = os.path.join(MEDIA_ROOT, '*')
    local('rm -rf %s' % files_to_delete)
    media_fixtures_path = os.path.join(PROJECT_ROOT,
            'test_media/fixtures/media/*')
    local('cp -rf %s %s' % (media_fixtures_path, MEDIA_ROOT))


def test(apps=' '.join(TEST_APPS), options=None):
    """Runs manage.py tests::

        $ fab test                          # will run all unit tests
        $ fab test:app1                     # will run tests only for app1

    """
    command = ('./manage.py test -v 2 --traceback --failfast'
               ' --settings=settings.test_settings')
    if options:
        command += ' {0}'.format(options)

    with settings(warn_only=True):
        result = local('%s %s' % (command, apps), capture=False)
    if result.failed:
        print red_bg('Some tests failed')
    else:
        print green_bg('All tests passed')
