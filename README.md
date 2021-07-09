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
- The `grpc-logo.png` [for gRPC][31] from the (archived) `grpc.github.io`
  repo, licensed as [Apache 2.0][32]
- A screenshot `tcp-packet.png` from the [Transmission Control Protocol][33]
  Wikipedia page, which is under the
  [Creative Commons Attribution-ShareAlike License][34]
- The `requests-python-logo.png` from the [Requests][35] Wikipedia page, has
  the same license as the project, which is Apache 2.0
- `Lock-Up-The-Forest.jpg` - From [Flickr][37], via [Public Domain][36]
- `istio-whitelogo-bluebackground-framed.svg` from Istio [Media Resources][38]
  which says "Cool: Use the Istio logo in a blog post or news article about
  Istio" and converted to `.png` via
  ```
  cd content/images/
  convert -density 288 -background none -size 300x300 \
    ./istio-whitelogo-bluebackground-framed.svg ./istio-logo.png
  ```
- `broken-pipe.jpg` - From [Flickr][39], via [CC BY-NC-ND 2.0][40]
- `door-nowhere.jpg` - From Panoramio via [Wikimedia][41], via [CC BY 3.0][42]
- `heavy-duty-patch.png` - From Miniature Rhino [blog][43]
- `Vault_PrimaryLogo_Black_RGB.png` - From Hashicorp brand [page][44], which
  states
  > Please don't modify the marks or use them in a confusing way, including
  > suggesting sponsorship or endorsement by HashiCorp, or in a way that
  > confuses HashiCorp with another brand (including your own).

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
[31]: https://github.com/grpc/grpc.github.io/blob/80f02e605ca324131c21335087fd3189a1854cb2/img/grpc_square_reverse_4x.png
[32]: https://github.com/grpc/grpc.github.io/blob/80f02e605ca324131c21335087fd3189a1854cb2/LICENSE
[33]: https://en.wikipedia.org/wiki/Transmission_Control_Protocol
[34]: https://en.wikipedia.org/wiki/Wikipedia:Text_of_Creative_Commons_Attribution-ShareAlike_3.0_Unported_License
[35]: https://en.wikipedia.org/wiki/File:Requests_Python_Logo.png
[36]: https://creativecommons.org/publicdomain/zero/1.0/
[37]: https://flic.kr/p/X1cKzX
[38]: https://istio.io/latest/about/media-resources/
[39]: https://flic.kr/p/2zaGo
[40]: https://creativecommons.org/licenses/by-nc-nd/2.0/
[41]: https://commons.wikimedia.org/wiki/File:A_Door_In_The_Middle_Of_Nowhere_-_panoramio.jpg
[42]: https://creativecommons.org/licenses/by/3.0/deed.en
[43]: https://miniaturerhino.myshopify.com/blogs/news/easy-patching-for-heavy-duty-fabrics
[44]: https://www.hashicorp.com/brand
