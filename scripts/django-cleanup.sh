#!/bin/bash
source $HOME/bin/script-settings-INSERT_PROJECTNAME.sh
source $HOME/Envs/$VENV_NAME/bin/activate

$HOME/webapps/$DJANGO_APP_NAME/project/manage.py cleanup
