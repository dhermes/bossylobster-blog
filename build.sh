#!/bin/bash
set -ev

################################################################
# Only make and push new build on a commit (non PR) to master. #
################################################################
if [[ "${TRAVIS_BRANCH}" == "master" ]] && \
       [[ "${TRAVIS_PULL_REQUEST}" == "false" ]]; then
  ./update_pages_repo.sh
  # ./check_octopress_plugin.sh
else
  echo "Not in master on a non-pull request. Doing nothing."
fi
