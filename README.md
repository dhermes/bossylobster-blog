# bossylobster-blog

[![Travis Build Status](https://travis-ci.org/dhermes/bossylobster-blog.svg)](https://travis-ci.org/dhermes/bossylobster-blog/)

This will house the content of my [blog][1] [posts][2]
and will (eventually) use Travis to build and push updates.

## [Travis][3] Instructions

1. [Install][5] the `travis` command-line tool.

1. Visit your GitHub [Applications settings][4] to generate an OAuth token
   to use with the `travis` CLI tool. Be sure to select `public_repo`
   and `user:email` (or `user`) for the token scopes.

1. Copy the token and save it in a read-only file called `travis.token`.

1. Log in to Travis via the CLI tool:

   ```
   travis login --github-token=`cat travis.token`
   ```

1. Define and export the following environment variables:

   ```
   # Variables used to push new commits to the wheelhouse.
   export GH_OWNER="dhermes"
   export GH_PROJECT_NAME="bossylobster-blog"
   ```

1. Set the Travis environment variables:

   ```
   # Variables used to push new commits to the wheelhouse.
   travis env set GH_OWNER "${GH_OWNER}" --repo "${GH_OWNER}/${GH_PROJECT_NAME}"
   travis env set GH_PROJECT_NAME "${GH_PROJECT_NAME}" --repo "${GH_OWNER}/${GH_PROJECT_NAME}"
   travis env set GH_OAUTH_TOKEN `cat travis.token` --repo "${GH_OWNER}/${GH_PROJECT_NAME}"
   ```

1. Log out of Travis:

   ```
   travis logout
   ```

[1]: https://github.com/dhermes/dhermes.github.io
[2]: http://dhermes.github.io/
[3]: https://travis-ci.org
[4]: https://github.com/settings/tokens/new
[5]: https://github.com/travis-ci/travis.rb#installation
