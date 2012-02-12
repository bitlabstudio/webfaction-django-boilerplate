#!/bin/bash
source script-settings-INSERT_PROJECTNAME.sh

cd ~/webapps/$DJANGO_APP_NAME/apache2/bin
./restart
