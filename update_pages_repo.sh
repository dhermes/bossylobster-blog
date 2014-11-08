#!/bin/bash
set -ev

#################################
# Build static site in output/. #
#################################
make clean && make html

#######################################
# Checkout the repository Pages repo. #
#######################################
PAGES_REPO="${GH_OWNER}.github.io"
git clone --branch=master \
    "https://${GH_OAUTH_TOKEN}@github.com//${GH_OWNER}/${PAGES_REPO}" \
    "${PAGES_REPO}"

##############################################
# Remove the old content from ${PAGES_REPO}. #
##############################################
cd "${PAGES_REPO}"
git rm -r *

########################################################
# Put the cleanly built output into the ${PAGES_REPO}. #
########################################################
cp -r ../output/* .

##################################
# Add the commits and push them. #
##################################
git config --global user.email "travis@travis-ci.org"
git config --global user.name "travis-ci"

git add .
git status  # To see what has changed.

git commit -m "Update ${PAGES_REPO} after blog commit in ${GH_PROJECT_NAME}."
git push origin master
