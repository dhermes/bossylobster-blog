#!/bin/bash
set -ev

cd pelican-octopress-theme
git remote add official https://github.com/duilio/pelican-octopress-theme
git fetch official

OFFICIAL_HEAD=$(git log -1 official/master --pretty=%H)
MERGE_BASE=$(git merge-base "${OFFICIAL_HEAD}" origin/master)
if [[ "${OFFICIAL_HEAD}" == "${MERGE_BASE}" ]]; then
  echo "Octopress theme fork still refers to most recent."
else
  echo "Octopress theme fork out of date. Needs rebase."
  exit 1
fi
