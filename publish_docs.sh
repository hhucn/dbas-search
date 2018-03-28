#!/usr/bin/env bash

# build the docs
cd docs
make clean
make html
# package the docs
cd _build/html
tar czf ~/html.tgz .
cd ../../..
# checkout doc branch
git checkout gh-pages

# make sure the checkout was successful
current_branch=$(git branch | grep \* | cut -d ' ' -f2-)
if [ $current_branch = "gh-pages" ]; then
    git rm -rf .
    rm -fr docs
    rm -fr .idea

    tar xzf ~/html.tgz
    git add .
    git commit -a -m "update the docs"
    git push origin gh-pages

    git checkout master
fi
