#!/bin/sh
USERNAME='INSERT_USERNAME'

ps -u $USERNAME -o pid,rss,command | awk '{print $0}{sum+=$2} END {print "Total", sum}'
