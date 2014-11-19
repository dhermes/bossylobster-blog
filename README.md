# bossylobster-blog

[![Travis Build Status](https://travis-ci.org/dhermes/bossylobster-blog.svg)](https://travis-ci.org/dhermes/bossylobster-blog/)

This repository houses the content of my [blog][1] [posts][2]
as markdown. The blog is built with [Pelican][8] and I followed
[jakevdp][10]'s [`PythonicPerambulations`][9] while getting started.

After cloning, local dev can be done via

```
make clean && make html
make serve &
# Do some stuff
make stopserver
```

This depends on locally installing

```
[sudo] pip install --upgrade pelican markdown
```

This relies on heavily on the [`pelican-octopress-theme`][7] with
a few of my own [tweaks][8]. (Hopefully they will just land in
`master`.)

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

## Content Attribution

- `abraham-de-moivre.jpg` - From [Wikipedia Commons][11]
- `abraham-lincoln.jpg` - From [Wikipedia Commons][12]
- `TI-83.png` - From [Wikipedia Commons][13]

[1]: https://github.com/dhermes/dhermes.github.io
[2]: http://dhermes.github.io/
[3]: https://travis-ci.org
[4]: https://github.com/settings/tokens/new
[5]: https://github.com/travis-ci/travis.rb#installation
[6]: https://github.com/duilio/pelican-octopress-theme
[7]: https://github.com/dhermes/pelican-octopress-theme
[8]: http://docs.getpelican.com/en/3.5.0/
[9]: https://github.com/jakevdp/PythonicPerambulations
[10]: https://twitter.com/jakevdp
[11]: http://upload.wikimedia.org/wikipedia/commons/1/1b/Abraham_de_moivre.jpg
[12]: http://en.wikipedia.org/wiki/File:Abraham_Lincoln_November_1863.jpg
[13]: http://en.wikipedia.org/wiki/File:TI-83.png
