#!/bin/bash
source script-settings-INSERT_PROJECTNAME.sh
BACKUPFOLDER=$PROJECTNAME'_backups'

KEEP=30
BACKUPS=`find /home/$USERNAME/$BACKUPFOLDER -name "mysqldump-*.gz" | wc -l | sed 's/\ //g'`
while [ $BACKUPS -ge $KEEP ]
do
ls -tr1 /home/$USERNAME/$BACKUPFOLDER/mysqldump-*.gz | head -n 1 | xargs rm -f
BACKUPS=`expr $BACKUPS - 1`
done
DATE=`date +%Y%m%d%H%M%S`
rm -f /home/$USERNAME/$BACKUPFOLDER/.mysqldump-${DATE}.gz_INPROGRESS
mysqldump --opt -u$DBUSER -p$DBPASSWORD --opt $DBNAME | gzip -c -9 > /home/$USERNAME/$BACKUPFOLDER/.mysqldump-${DATE}.gz_INPROGRESS
mv -f /home/$USERNAME/$BACKUPFOLDER/.mysqldump-${DATE}.gz_INPROGRESS /home/$USERNAME/$BACKUPFOLDER/mysqldump-${DATE}.gz
exit 0
