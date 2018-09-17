---
slug: mathematics
title: Mathematics
github_slug: content/pages/mathematics.md
---

For as long as I can remember, I have had a love of learning math and problem
solving. In 7th grade, I participated in my first math competition (MathCounts)
and the rest is history.

From August 2013 to August 2018, I spent my time taking classes, teaching and
doing research as a graduate student at UC Berkeley. (See my post
["Graduated"]({filename}/2018-09-07-graduated.md) for a
retrospective.) This page is mostly intended as a place to gather some
things I made during that time.

### Code and Writing:

- Write-up and some code for generating the "optimal" finite difference
  [stencils][stencils] to compute a given derivative (November 2013)
- IPython notebook about [GMRES][gmres-gist] (October 2015)
- [Discussion][implicitizing] of parametric curves. In particular, how to
  classify cubics and how implicitization helps with conversion from a
  parametric curve to an algebraic curve. (April 2016)
- `bezier` [library][bez-docs] ([GitHub][bez-gh], published [in JOSS][bez-joss]
  in August 2017)
- `foreign-fortran` [project][foreign-fortran] ([GitHub][foreign-fortran-gh])
- Math 273 topics [course][m273] on numerical analysis ([GitHub][m273-gh])

### Papers:

- Compensated de Casteljau algorithm in `K` times the working precision
  ([arXiv][k-compensated], [GitHub][k-compensated-gh], submitted May 2016 to
  [AMC][AMC])
- A Curious Case of Curbed Condition ([arXiv][curbed-cond],
  [GitHub][curbed-cond-gh], June 2018)
- UC Berkeley [Dissertation][thesis] ([GitHub][thesis-gh], submitted August 2018)
- A 2-Norm Condition Number for B&#xe9;zier Curve Intersection
  ([arXiv][cond-num], [GitHub][cond-num-gh], August 2018)

### Talks:

- Butterfly Algorithm for Geometric Non-uniform FFT ([slides][butterfly],
  [GitHub][butterfly-github], given February 2015)
- Paper presentation on WENO [survey][weno-survey] ([slides][m273-talk],
  given February 2016 in Math 273 topics course)
- Paper presentation on [supermeshing][supermesh] / conservative
  [interpolation][local-supermesh] ([slides][m273-supermesh],
  given April 2016 in Math 273 topics course)
- Thesis talk ([slides][thesis-talk], given August 2018)

### Teaching:

- Teaching [page][teaching-page] used throughout graduate school
- Math 1A [Fall 2013][fa-2013]
- Math 1B [Spring 2014][sp-2014] (Professor's [page][sp-2014-prof])
- Math 128A [Fall 2014][fa-2014] (Professor's [page][fa-2014-prof])
- Math 228B [Spring 2015][sp-2015]
- Math 128A [Fall 2015][fa-2015] (Professor's [page][fa-2015-prof])
- Math 128A [Spring 2016][sp-2016]
- Math 128A [Fall 2016][fa-2016] (Professor's [page][fa-2016-prof])
- Math 128A [Spring 2017][sp-2017] (Professor's [page][sp-2017-prof])
- Math 54 [Spring 2018][sp-2018] (Professor's [page][sp-2018-prof])

[k-compensated]: https://arxiv.org/abs/1808.10387
[k-compensated-gh]: https://github.com/dhermes/k-compensated-de-casteljau
[cond-num]: https://arxiv.org/abs/1808.06126
[cond-num-gh]: https://github.com/dhermes/condition-number-bezier-curve-intersection
[curbed-cond]: https://arxiv.org/abs/1806.05145
[curbed-cond-gh]: https://github.com/dhermes/curious-case-curbed-condition
[thesis-talk]: https://github.com/dhermes/phd-thesis/blob/master/doc/thesis_talk.pdf
[thesis]: https://github.com/dhermes/phd-thesis/blob/master/doc/thesis.pdf
[thesis-gh]: https://github.com/dhermes/phd-thesis
[AMC]: https://www.journals.elsevier.com/applied-mathematics-and-computation
[butterfly-github]: https://github.com/dhermes/butterfly-algorithm
[butterfly]: https://www.bossylobster.com/butterfly-slides
[fa-2014]: https://drive.google.com/drive/u/0/folders/0B91542R0K_UPalprVm9ZdEwwamM
[fa-2014-prof]: https://math.berkeley.edu/~wilken/128A.F14/
[sp-2017]: https://drive.google.com/drive/folders/0B8el7dRo8mVOT0RoZ3BrQ1ZwTHM
[sp-2017-prof]: https://math.berkeley.edu/~mgu/MA128ASpring2017/index.html
[sp-2018]: https://drive.google.com/drive/folders/17UM4RMsVRP3rgTLHe6hGPnR6Iz2o1zua
[sp-2018-prof]: https://math.berkeley.edu/~apaulin/54_002(Spring2018).html
[fa-2016-prof]: https://people.eecs.berkeley.edu/~oholtz/128A/index.html
[fa-2016]: https://drive.google.com/drive/folders/0B8el7dRo8mVOdHp0ak5CdlhzWlk
[sp-2016]: https://drive.google.com/drive/folders/0B8el7dRo8mVOcDgwelZSeDQ3amM
[fa-2015-prof]: https://math.berkeley.edu/~mgu/MA128A2015F/index.html
[fa-2015]: https://drive.google.com/drive/folders/0B91542R0K_UPfjZ6RElBYUljM2hDclpsRElqYVROdUlYa0JsSlZUc3NicXNiQkhmT0ppUzg
[teaching-page]: https://docs.google.com/document/d/1EhOoMhzGariQui1c85AetcbT8R751p_nmzGe8A41Gsc/edit
[sp-2014-prof]: https://math.berkeley.edu/~reshetik/index1b-14.html
[sp-2014]: https://drive.google.com/drive/folders/0B8el7dRo8mVOTnlsVWU3eDZFUEU
[fa-2013]: https://drive.google.com/drive/folders/0B8el7dRo8mVOOHRYd2hQc1dLbjg
[sp-2015]: https://drive.google.com/drive/folders/1GEqta0uTlDS9v5UNnJbjiZ7PTwZEkmZ_
[bez-docs]: https://bezier.readthedocs.io/en/latest/
[bez-gh]: https://github.com/dhermes/bezier
[bez-joss]: http://joss.theoj.org/papers/10.21105/joss.00267
[foreign-fortran]: https://foreign-fortran.readthedocs.io/en/latest/
[foreign-fortran-gh]: https://github.com/dhermes/foreign-fortran/
[m273]: https://berkeley-math-273-spring-2016.readthedocs.io/en/latest/
[m273-gh]: https://github.com/dhermes/berkeley-m273-s2016
[m273-talk]: https://nbviewer.jupyter.org/format/slides/github/dhermes/berkeley-m273-s2016/blob/master/class_preso/weno_computations.ipynb
[weno-survey]: https://doi.org/10.1137/070679065
[supermesh]: https://doi.org/10.1016/j.cma.2009.03.004
[local-supermesh]: https://dx.doi.org/10.1016/j.cma.2010.07.015
[m273-supermesh]: https://nbviewer.jupyter.org/format/slides/gist/dhermes/59f4c4b79be4b53dbf84a7761c029f01
[stencils]: https://gist.github.com/dhermes/ba7276f20d5a4947cafbb911671ab8f1#file-finite_difference_order-pdf
[gmres-gist]: https://gist.github.com/dhermes/d72e36c40626bd93a4a02704ee79c7d1
[implicitizing]: [https://gist.github.com/dhermes/3551f053e3f81a85d488c7cdb22a18c8#file-implicitizing_curves-pdf]
