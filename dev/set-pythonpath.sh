#!/bin/bash

# -- a script to export PYTHONPATH w user given path
#       if no given path then export current directory
#       need to rerun everytime a terminla session is started 
# Usage:
#       set-pythonpath.sh                       # --> adds current directory to PYTHONPATH
#       set-pythonpath.sh [path]                # --> adds given path to PYTHONPATH


PATH_TO_EXPORT=$1

if [ -z "$1" ]; then
    PATH_TO_EXPORT=$(pwd)
    echo ">>> No path is given, exporting current directory"
else
    PATH_TO_EXPORT=$(realpath "$1")
fi


# -- check if teh path is already in PYTHONPATH
if [ -z "$PYTHONPATH" ]; then
    export PYTHONPATH="$PATH_TO_EXPORT"
    echo ">>> empty PYTHONPATH is exported with '$PATH_TO_EXPORT'"
elif [[ ":$PYTHONPATH:" != *":$PATH_TO_EXPORT:"* ]]; then
    export PYTHONPATH="$PATH_TO_EXPORT:$PYTHONPATH"
    echo ">>> PYTHONPATH is exported with '$PATH_TO_EXPORT'"
else
    echo ">>> '$PATH_TO_EXPORT' is already in PYTHONPATH"
fi
 
echo " <> Current PYTHONPATH: $PYTHONPATH <>"