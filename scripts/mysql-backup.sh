#!/bin/bash
source $HOME/bin/script-settings-INSERT_PROJECTNAME.sh
BACKUPFOLDER='backups_'$PROJECTNAME

mkdir -p $HOME/$BACKUPFOLDER

KEEP=30
BACKUPS=`find $HOME/$BACKUPFOLDER -name "mysqldump-*.gz" | wc -l | sed 's/\ //g'`
while [ $BACKUPS -ge $KEEP ]
do
ls -tr1 $HOME/$BACKUPFOLDER/mysqldump-*.gz | head -n 1 | xargs rm -f
BACKUPS=`expr $BACKUPS - 1`
done
DATE=`date +%Y%m%d%H%M%S`
rm -f $HOME/$BACKUPFOLDER/.mysqldump-${DATE}.gz_INPROGRESS
mysqldump --opt -u$DBUSER -p$DBPASSWORD --opt $DBNAME | gzip -c -9 > $HOME/$BACKUPFOLDER/.mysqldump-${DATE}.gz_INPROGRESS
mv -f $HOME/$BACKUPFOLDER/.mysqldump-${DATE}.gz_INPROGRESS $HOME/$BACKUPFOLDER/mysqldump-${DATE}.gz
exit 0
