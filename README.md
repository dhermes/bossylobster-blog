# Bossy Lobster Blog

This repository houses the [content][1] of my blog [posts][2]
as markdown. The blog is built with [Pelican][8] and I followed
[jakevdp][10]'s [`PythonicPerambulations`][9] while getting started.

After cloning, local dev can be done via

```
nox -s clean
nox -s html
nox -s serve &
nox -s stopserver
```

This relies on heavily on the [`pelican-octopress-theme`][6] with
a few of my own [tweaks][7]. (Hopefully they will just land in
`master`.)

## Publish Instructions

Build with the `PUBLISH` environment variable set to `true` and then
replace the content on [`dhermes.github.io`][3] with the contents
of `output/`. (Be careful not to write over the `CNAME` file.)

## Content Attribution

- `abraham-de-moivre.jpg` - From [Wikipedia Commons][11]
- `abraham-lincoln.jpg` - From [Wikipedia Commons][12]
- `baby_lobster.jpg` - From [Flickr][19], via [Creative Commons][14]
- `cluttered_desk.jpg` - From [Flicker][20], via [Creative Commons][17]
- `horse.jpg` - From [Flickr][16], via [Creative Commons][17]
- `magician.jpg` - From [Flickr][18], via [Creative Commons][17]
- `nerd-out.jpg` - From [Flickr][22], via [Creative Commons][17]
- `prepare-yourself.jpg` - From [Flickr][15], via [Creative Commons][14]
- `sleeping_in_class.jpg` - From [Flickr][21], via [Creative Commons][17]
- `TI-83.png` - From [Wikipedia Commons][13]
- `elon-musk-criticism-thumbnail.jpg` - From [YouTube][23],
  via [Standard YouTube License][24]
- `generic-football.png` - From [openclipart][26] via
  [Unlimited Commerical Use][25]
- `graduation.png` - From [openclipart][27] via
  [Unlimited Commerical Use][25]
- `fail-whale.png` - From [Wikipedia][28], via fair use
- A community logo for TypeScript `ts-logo.png`, via [Remo Jansen][29] and
  provided with the MIT [license][30]

[1]: https://github.com/dhermes/dhermes.github.io
[2]: https://blog.bossylobster.com
[3]: https://github.com/dhermes/dhermes.github.io
[6]: https://github.com/duilio/pelican-octopress-theme
[7]: https://github.com/dhermes/pelican-octopress-theme
[8]: http://docs.getpelican.com/en/3.5.0/
[9]: https://github.com/jakevdp/PythonicPerambulations
[10]: https://twitter.com/jakevdp
[11]: http://upload.wikimedia.org/wikipedia/commons/1/1b/Abraham_de_moivre.jpg
[12]: http://en.wikipedia.org/wiki/File:Abraham_Lincoln_November_1863.jpg
[13]: http://en.wikipedia.org/wiki/File:TI-83.png
[14]: https://creativecommons.org/licenses/by/2.0/
[15]: https://flic.kr/p/65i1j
[16]: https://flic.kr/p/5ccWFq
[17]: https://creativecommons.org/licenses/by-sa/2.0/
[18]: https://flic.kr/p/9hBrtv
[19]: https://flic.kr/p/h9PhFv
[20]: https://flic.kr/p/n4XLG
[21]: https://flic.kr/p/E8Mz7
[22]: https://flic.kr/p/EWAVi
[23]: http://img.youtube.com/vi/NU7W7qe2R0A/0.jpg
[24]: https://www.youtube.com/static?template=terms
[25]: https://openclipart.org/unlimited-commercial-use-clipart
[26]: https://openclipart.org/detail/102853/football
[27]: https://openclipart.org/detail/178476/graduation-penguin
[28]: https://en.wikipedia.org/wiki/File:Failwhale.png
[29]: https://github.com/remojansen/logo.ts
[30]: https://github.com/remojansen/logo.ts/blob/5b4f0df433a5301aee0180582a8782bfbc9a0739/LICENSE
