title: Graduated
description: Finishing my PhD
date: 2018-09-07
author: Danny Hermes (dhermes@bossylobster.com)
tags: Education, Research, Applied Mathematics, PhD
slug: graduated
comments: true
use_twitter_card: true
use_open_graph: true
use_schema_org: true
twitter_site: @bossylobster
twitter_creator: @bossylobster
social_image: images/graduation.png
github_slug: content/2018-09-07-graduated.md

After five years, I'm excited to say I've finished [my PhD][1]. I certainly
learned a lot and met a lot of great people along the way.

One of the biggest lessons I learned was about myself: I need to **say no**
more often. I continued to say yes, to [side projects][6], to coffee in SF, to
teaching Python training on the side, etc. Saying no a bit more frequently
would have allowed me to spend more time on research and to finish sooner as
I'd originally hoped.

While the many diversions did make me appreciate the need for **focus**, I am
also happy that my time in school gave me an opportunity to go down rabbit
holes and winding paths to learn.

For readers in a hurry, the TL;DR:

- [Advising and Peers](#advising): I was lucky to be in a great learning and
  research environment
- [Teaching](#teaching): I enjoyed teaching undergraduates but wish some things
  were different about the university model
- [Research](#research): I had a chance to make incremental progress on a tool
  that can be useful for physical simulations
- [Software](#software): I wrote a lot of code both for science and for Google;
  in particular, I learned to appreciate modern Fortran and struggled with
  building binary extensions for Python

### Advising and Peers {#advising}

I was lucky to have a great advisor, [Per-Olof Persson][2].
When I was deciding which graduate school to attend, a chat with Per
was one of the clinching factors in choosing UC Berkeley. Since his
research (CFD) was not quite in line with my interests (e.g. Numerical
Linear Algebra), I hesitated in asking him to advise me. However,
I gave the personality fit more weight than the research fit and am happy
about the outcome.

The UC Berkeley Math department is a very welcoming place and I really
enjoyed teaching undergraduates and taking classes with my fellow
graduate students. A few of my peers had somewhat inaccessible
advisors (e.g. they only met once a year) and these students did
feel a sense of [isolation][5]. It made a big difference having an advisor that
was easy to get in touch with and eager to help.

### Teaching {#teaching}

I really enjoyed teaching and had some great interactions with students:

> Danny manages to be relaxed, funny, and watchable AND very knowledgeable
> about the material AND a stickler about teaching it AND good at explaining
> it clearly and quickly. This is a combination of strengths so rare around
> here that I thought it was mythical.

Though the interactions were great, there were a few things I wished were
different.

- I wish the lower-division classes were changed to utilize computers both
  for rote computation and visualization of concepts. (I taught Calculus I and
  II and Linear Algebra.)
- I was a bit disappointed at the preparedness and more importantly the
  enthusiasm of students in upper-division courses (I taught Numerical Analysis
  five times). It seemed that for many, taking courses in their major was
  a chore rather than a joy. This is as much (if not more) a reflection on the
  system as it is on the students.
- Numerical Analysis is an opportunity to learn how "classical" algorithms
  break down on a computer (i.e. in the presence of rounding). Having the
  ability to program is a must to really solidify the concepts. However, once
  a class hits 150 students, the grading must be "standardized". In this case,
  that meant student evaluation was done via traditional pen and paper
  assignments and exams. Coupled with the absence of a programming
  prerequisite, this made the amount of **computing** in the class
  a small fraction of the course.
- I was continually frustrated by the prevalence of MATLAB usage in the
  math department. MATLAB certainly has strengths, but its kitchen sink
  approach to namespaces (similar to that of PHP) really makes it hard to
  teach. Its lack of a packaging story and reliance on a proprietary IDE
  makes it hard for students to understand what code "is" (or even **where**
  it is on their filesystem). The IPython notebook was created at UC
  Berkeley and I wish the math department would get on board. Perhaps more
  relevantly, using MATLAB does little to prepare students for the real world
  because it is used almost exclusively in academic or lab settings.

### Research {#research}

I enjoyed the research I did, but wish there was more time to keep doing it.
[ref]I suppose there would be if I were to stay in academia, but that path is
not for me[/ref] I thoroughly enjoyed diving into Numerical Linear Algebra
papers and implementing some of the more classical results. The most satisfying
of course were the ones that took a few attempts to get right.

In my dissertation, I describe a method for solution transfer between
curved meshes. In layman's terms:

- A **mesh** is an approximation of some physical domain, e.g. the surface
  of a frying pan (in 2D) or the wing of an airplane (in 3D)
- A mesh is composed of small **elements** that are well understood, e.g.
  triangles, rectangles, tetrahedra, cubes, etc.
- A **curved** mesh is one in which the edges / faces of the elements are
  allowed to curve
- A **solution** (or field) on a mesh is a numerical representation of
  some physical quantity, e.g. velocity, pressure, density or energy
- **Solution transfer** is the process of reintepreting (or interpolating)
  a solution from one mesh onto another

During commonly used simulation techniques, one or several physical quantities
are represented on a mesh and change over time according to some law
of physics (usually represented by a partial differential equation). When the
process involves a fluid (the F in CFD), it's common to allow the mesh to
"travel" over time with the fluid. For [example][8], when simulating blood flow
within a rigid cavity (e.g. a heart or vein) the mesh can represent a membrane
that flows as the blood moves.

In such simulations, the mesh can become tangled after a certain amount of
time moving along the flow. It is these cases where mesh quality begins to
deteroriate that benefit from **solution transfer**. Once a mesh becomes too
low-quality to use in simulation, a new mesh must be used to represent the
physical domain. Once the new mesh is chosen, the physical quantities being
tracked must be transferred from the low-quality mesh to the new one.

This work was certainly incremental, as much research is. Solution transfer
has already been [described][9] for straight sided meshes (i.e. meshes
where the elements are not curved). However, the work required to intersect
curved triangles is considerably more involved than that required to
intersect straight sided triangles. Peter Thiel would have you
believe (in [Zero to One][7]) that the hardest step is the initial idea and
everything else is incremental. However, I can say that the incremental
step from straight sided to curved elements was a **considerable** jump in
difficulty.

### Software {#software}

During graduate school, I wrote a lot of code, as I usually do. However,
two projects in particular stick out:

- The `google-cloud-python` [collection][6] of packages
- My `bezier` [library][3] ([published][4] in JOSS)

I've worked on Google client libraries in one form or another since 2011 and
somehow managed to keep doing this after leaving Google for UC Berkeley. I
had a great opportunity to be one of the main drivers of the
`google-cloud-python` library and it allowed me to stay current on how
software is built. Among other things I gained an appreciation for testing,
continuous integration and documentation that I didn't have before.

As part of my [research](#research), I needed to be able to intersect
millions of pairs of B&#xe9;zier curves in a single simulation. I was worried
that doing this in my language of choice (Python) would be too slow, so I
decided to write the computation in a compiled language and wrap the interface
with a [binary extension][10]. Building binary wheels for Linux, Mac OS X and
Windows was a struggle, to say the least, but I'm happy I went through the
process. If I can find the time, I hope to write a bit more about some of
the amusing packaging bugs I created and had to track down. I hope that
[scikit-build][11] or a similar effort can once and for all demystify the
process of invoking native code from Python.

I chose Fortran for the implementation, which is likely a shock to most
people outside of academia. In Silicon Valley, Fortran is usually a punchline
rather than a language choice. However, I discovered early in my program that
modern Fortran is a wonderful language. Writing vanilla Fortran is essentially
just like writing NumPy code with all square brackets (`[`) swapped
for parentheses (`(`). With the Fortran 90 specification, the FORTRAN (yes, all
caps) language was no more and the modern features actually make it an
appealing language.

I legitimately think people should consider Fortran first for computational
workloads, if not for more general purpose tasks. Having a sponsor has made
the Go (Google) and Rust (Firefox) communities vibrant places with great
documentation and ever-expanding choices for libraries. Intel is the closest
it comes to a Fortran steward due to their forums for the wonderful
`ifort` compiler. However, there is no community-led Fortran
documentation[ref]An equivalent of `golang.org` or `docs.python.org`[/ref]
and this makes it a bit hard to develop code in Fortran. The amazing
`fortran90` [site][13] from Ond&#x159;ej &#x10c;ert&#xed;k fills many gaps, but
is mostly a one-person effort.

I started the `foreign-fortran` [project][12] to make my little contribution
back to the Fortran community. The project is essentially documentation only
and gives examples of how Fortran libraries can be used from other programming
languages.

## Parting Words

I really enjoyed my time in graduate school and wish I was able to better
utilize the awesome communities on UC Berkeley's campus. Though I'm happy I
did it, I'm equally happy that I spent three years in the real world working
at companies[ref]Or "industry" as it's called in academia[/ref] before
starting. I would recommend that all undergraduate students go get a "real job"
before deciding to commit several years of their life to a PhD. There's a whole
world out there outside of the ivory tower and too often it's not clear to
students what their options are if they don't end up in that tenure track
job.

As I said, my fellow graduate students with and from whom I have learned were
a great part of the experience. In particular Will Pazner[ref]Thanks to Will
for reviewing this post[/ref], Chris Miller and Qiaochu Yuan as well as my
undergraduate classmate Wade Hindes have been a source of many great
discussions.

[1]: https://github.com/dhermes/phd-thesis
[2]: http://persson.berkeley.edu
[3]: https://bezier.readthedocs.io/en/latest/
[4]: http://joss.theoj.org/papers/10.21105/joss.00267
[5]: http://www.fast.ai/2018/08/27/grad-school/
[6]: https://github.com/GoogleCloudPlatform/google-cloud-python/
[7]: https://en.wikipedia.org/wiki/Zero_to_One
[8]: https://www.cs.cmu.edu/~tp517/papers/cardoze04bezier-b.pdf
[9]: https://doi.org/10.1016/j.cma.2010.07.015
[10]: https://packaging.python.org/guides/packaging-binary-extensions/#an-overview-of-binary-extensions
[11]: https://scikit-build.readthedocs.io/en/latest/
[12]: https://foreign-fortran.readthedocs.io/en/latest/
[13]: https://www.fortran90.org/
