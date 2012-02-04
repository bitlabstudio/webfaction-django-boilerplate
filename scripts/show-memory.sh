#!/bin/bash
source script_settings.sh

ps -u $USERNAME -o pid,rss,command | awk '{print $0}{sum+=$2} END {print "Total", sum}'
