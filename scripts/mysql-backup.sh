#!/bin/bash
source script_settings.sh

KEEP=30
BACKUPS=`find /home/$USERNAME/backups -name "mysqldump-*.gz" | wc -l | sed 's/\ //g'`
while [ $BACKUPS -ge $KEEP ]
do
ls -tr1 /home/$USERNAME/backups/mysqldump-*.gz | head -n 1 | xargs rm -f
BACKUPS=`expr $BACKUPS - 1`
done
DATE=`date +%Y%m%d%H%M%S`
rm -f /home/$USERNAME/backups/.mysqldump-${DATE}.gz_INPROGRESS
mysqldump --opt -u$DBUSER -p$DBPASSWORD --opt $DBNAME | gzip -c -9 > /home/$USERNAME/backups/.mysqldump-${DATE}.gz_INPROGRESS
mv -f /home/$USERNAME/backups/.mysqldump-${DATE}.gz_INPROGRESS /home/$USERNAME/backups/mysqldump-${DATE}.gz
exit 0
