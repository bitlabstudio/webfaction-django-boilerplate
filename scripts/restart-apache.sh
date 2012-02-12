#!/bin/bash
source $HOME/bin/script-settings-INSERT_PROJECTNAME.sh

cd ~/webapps/$DJANGO_APP_NAME/apache2/bin
./restart
