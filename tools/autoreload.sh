#!/bin/bash

# wrap a command in a auto reload watchdog to restart it if files change, useful for debugging inside docker

exec /usr/bin/watchmedo auto-restart -d /source/websecmap -p "*.py" -R --signal SIGKILL -- "$@"
