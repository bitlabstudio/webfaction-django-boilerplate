#!/bin/bash
source $HOME/bin/script-settings-INSERT_PROJECTNAME.sh
BACKUPFOLDER='backups_locale_'$PROJECTNAME
mkdir -p $HOME/$BACKUPFOLDER

KEEP=60
ls -tr1 $HOME/$BACKUPFOLDER/locale-*.tgz | head -n 1 | xargs rm -f
BACKUPS=`expr $BACKUPS - 1`
done
DATE=`date +%Y%m%d%H%M%S`
rm -f $HOME/$BACKUPFOLDER/.locale-${DATE}.tgz_INPROGRESS
tar -cvzpf $HOME/$BACKUPFOLDER/.locale-${DATE}.tgz_INPROGRESS ~/webapps/$DJANGO_APP_NAME/project/locale
mv -f $HOME/$BACKUPFOLDER/.locale-${DATE}.tgz_INPROGRESS $HOME/$BACKUPFOLDER/locale-${DATE}.tgz
exit 0
