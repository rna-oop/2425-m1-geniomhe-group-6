#!/bin/bash

read -p "Enter library name: " lib_name

cp -r ./lab4/src $lib_name
cd $lib_name
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

make clean html

echo check out $lib_name/focs/build/html/index.html for read.the.docs styles doucumentation of the library