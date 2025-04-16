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

printf "n\n ${lib_name} \nJoelle ASSY & Rayane ADAM\n0\nen" | sphinx-quickstart

# sphinx-quickstart
# echo multiline string
echo '''

import sphinx_rtd_theme

html_theme = "sphinx_rtd_theme"

extensions = [
   "sphinx_rtd_theme",
   "sphinx.ext.autodoc"
]
''' >> conf.py

make html

sphinx-apidoc -o . ../$lib_name

make html

echo '''
def skip(app, what, name, obj, would_skip, options):
    if name == "__init__":
        return False
    return would_skip

def setup(app):
    app.connect("autodoc-skip-member", skip)
''' >> conf.py


cat <<EOF > index.rst
Welcome to ${lib_name}'s documentation!
=================================


.. toctree::
   :maxdepth: 2
   :caption: Contents:

   modules.rst

Indices and tables
==================

* :ref:\`genindex\`
* :ref:\`modindex\`
* :ref:\`search\`
EOF

echo "dixed index.rst to have links to genindex, modindex and search => allows for a small table of contents on main page"


make clean html
make html

plot_file="../assets/1r7w_cg_transparent.html"
index_file="_build/html/index.html"

plot_to_html_content="<section id=\"embedded-content\">
  <iframe src=\"${plot_file}\" style=\"border: none;\" width=\"600\" height=\"400\"></iframe>
</section>"
escaped_content=$(echo "$plot_to_html_content" | sed -e 's/[&/\]/\\&/g' -e 's/</\\</g' -e 's/>/\\>/g')


# sed -i "/<section id=\"indices-and-tables\">/i $escaped_content" $index_file
# # awk -v content="$plot_to_html_content" '/<section id="indices-and-tables">/ {print content}1' "_build/html/index.html" > temp.html && mv temp.html "_build/html/index.html"
# awk 'NR==85 {print "<section id=\"embedded-content\">\n  <iframe src=\"../../../assets/1r7w_cg_transparent.html\" style=\"border: none;\" width=\"600\" height=\"400\"></iframe>\n</section>"}1'   > temp.html && mv temp.html index.html

awk -v content="$plot_to_html_content" '/<section id="indices-and-tables">/ {print content}1' "$index_file" > temp.html && mv temp.html "$index_file"

echo 'added plot to main page'

# -- putting index file in docs directory
cd ..
cp docs/_build/html/* docs/

echo check out docs/index.html for read.the.docs styles doucumentation of the library