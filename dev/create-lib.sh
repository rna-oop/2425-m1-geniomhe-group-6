#!/bin/bash

read -p "Enter library name: " lib_name

if [ ! -d backup ]; then
   mkdir backup
   echo "Created backup directory"
fi

# if [ -d $lib_name ]; then
#    echo "Directory $lib_name already exists => moving it to backup"
#    counter=1
#    while [ -d "backup/${lib_name}_$counter" ]; do
#        counter=$((counter + 1))
#    done
#    sudo mv $lib_name backup/${lib_name}_$counter
#    echo "Moved existing $lib_name directory to backup/${lib_name}_$counter"
# fi

# mkdir $lib_name


# cp -r ./lab4/src/* $lib_name/

if [ -d docs ]; then
   echo "docs directory already exists, moving it"
    
   counter=1
   while [ -d "backup/docs_$counter" ]; do
      counter=$((counter + 1))
   done
    
   sudo mv docs/ backup/docs_$counter
   echo "Moved existing docs directory to docs_$counter"
fi

mkdir docs
cd docs

printf "y\n ${lib_name} \nm1geniomhe2425-rna-oop-group6\n0\nen" | sphinx-quickstart

# sphinx-quickstart
# echo multiline string
echo '''
extensions = [
   "sphinx_rtd_theme",
   "sphinx.ext.autodoc"
]


import sphinx_rtd_theme

html_theme = "sphinx_rtd_theme"
''' >> source/conf.py

sphinx-apidoc -o . ../$lib_name

make clean html
make html

echo check out docs/build/html/index.html for read.the.docs styles doucumentation of the library