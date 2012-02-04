#!/bin/bash
source script_settings.sh

cd ~/webapps/$DJANGO_APP_NAME/apache2/bin
./restart
