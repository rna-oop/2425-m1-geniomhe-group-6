#!/bin/bash

#this script will take the lib name which should be a directory
#it will open this drectory's files and change the name of the library
#e.g., if im changing from lib to lib2, it will change: 
    # from lib import ... -> from lib2 import ...
    # from lib. import ... -> from lib2. import ..
#it will also change its name in setup.py
# Usage: ./dev/change-libname.sh

# -- take lib path from user
read -p ">>> Enter the library relative path: " LIB_PATH
LIB_PATH=$(pwd)/$LIB_PATH
LIB_PATH=$(realpath "$LIB_PATH")
LIB_NAME=$(basename "$LIB_PATH")

read -p ">>> Enter the new library name: " NEW_LIB_NAME

echo  ""
echo ">>> Changing library name from '$LIB_NAME' to '$NEW_LIB_NAME'"
echo ""

# -- check if the path is valid
if [ ! -d "$LIB_PATH" ]; then
    echo "<<< '$LIB_PATH' is not a valid path, exiting"
    exit 1
fi

# -- updated imports in all python files
for file in $(find "$LIB_PATH" -type f -name "*.py"); do
    sed -i "s/$LIB_NAME/$NEW_LIB_NAME/g" "$file"
    echo "  >>> '$file' is updated"
done

# -- update the library name in setup.py
lib_parent=$(dirname "$LIB_PATH")
SETUP_PATH=$lib_parent/setup.py

if [ -f $SETUP_PATH ]; then
    sed -i "s/$LIB_NAME/$NEW_LIB_NAME/g" $SETUP_PATH
    # sed -i "s/\(name=\)\(['\"].*['\"]\)/\1\"$NEW_LIB_NAME\"/g" $SETUP_PATH
    echo "  >>> '$SETUP_PATH' is updated"
else
    echo "<<< '$SETUP_PATH' is not found"
fi

# -- rename the library directory
mv $LIB_PATH $lib_parent/$NEW_LIB_NAME

echo ""
echo " >>> Library name is updated from '$LIB_NAME' to '$NEW_LIB_NAME' <<<"