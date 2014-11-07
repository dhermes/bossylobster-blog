Title: The Lesson V8 Can Teach Python and Other Dynamic Languages
date: 2011-08-17
author: Danny Hermes (dhermes@bossylobster.com)
tags: Benchmark, Comparison, Dynamic Language, Javascript, Javascript Engine, JIT, Just-in Time Compile, node.js, Performance, Project Euler, PyPy, Python, V8
slug: lesson-v8-can-teach-python-and-other

Being unable to completely give up math for computers, I am naturally
drawn to [Project Euler](http://projecteuler.net/) and as a result
solved a [ridiculous
number](http://code.google.com/p/dhermes-project-euler/source/browse/#git%2Fpython_code%2Fcomplete)
of the problems posted there while learning Python. A few months
ago (March 13), after reading [Secrets of a Javascript
Ninja](http://jsninja.com/), I decided to begin converting my [solutions
to
Javascript](https://github.com/dhermes/ProjectEuler/commit/663ee638c6b8255d00b84173b0ecad1af2c53af1). A
month and a half later I [came
back](https://github.com/dhermes/ProjectEuler/commit/72c092ccf82c3933944584c2479d2e7ca0ef06f7)
to it, and then finally two months after that, I [began to take it
seriously](https://github.com/dhermes/ProjectEuler/commit/f19f85978aeeac3310b2175812d53bbea884d73b).

After making this decision, I noticed the prime Sieve of Eratosthenes
was mighty fast when I ran it in Chrome, maybe even faster than my
beloved Python. I tabled the thought for a little, but never really
forgot it. So a few weeks ago (early August 2011), I *finally* got a
working install of [node](http://nodejs.org/) running on my machine and
was able to make more of this thought. (I say *finally installed*
because on two previous tries I gave up because of conflicts with my
version of gcc, coupled with the fact that I had no good reason to use
node.)

When I originally did the conversion, I had skipped problem 8, because
my implementation required pulling in the problem data as text from a
file. While hanging out with [Boris](http://twitter.com/#!/borismus) and
[Eric](https://twitter.com/#!/ebidel) from on the Chrome Developer
Relations team, I decided to give it another go on node (xhr requests
not allowed) and found it to be quite simple with <span
class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">readFileSync</span>
in the node native <span class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">fs</span>
module. After witnessing this, over this weekend, I decided to harness
the power of [V8](http://code.google.com/p/v8/) -- the Javascript engine
that powers Chrome and node -- and run all my scripts locally with node.
So over a two day period, I
[hack-hack-hacked](http://code.google.com/p/dhermes-project-euler/source/detail?r=87b2cf2128be9d13d3b374d8eba9cb4ad808c982)
my way into converting the Python solutions for problems 11 through 50
(the remaining unconverted) into their Javascript equivalents, while
also converting a good portion of my hefty
[functions](http://code.google.com/p/dhermes-project-euler/source/browse/python_code/functions.py)
module.

Once this was done, I had also found I could replace most of the nice
parts about Python with my own equivalent. For example, I was able to
replace functionality I needed from the Python <span
class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">set</span>
datatype with

~~~~ {.prettyprint style="background-color: white;"}
function uniq(arr) {  var result = {};  for (var i = 0, val; val = arr[i]; i++) {    result[val] = true;  }  return Object.keys(result);};
~~~~

and I was able to replace the (amazingly) useful Python handling of
<span class="Apple-style-span"
style="color: lime; font-family: 'Courier New', Courier, monospace;">long</span>
integers with a non-native node package called
[bigint](https://github.com/substack/node-bigint) that uses libgmp among
other usings. Of course, for Python's secret sauce -- the list
comprehension -- I was able to substitute enough <span
class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">filter</span>,
<span class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">reduce</span>
and <span class="Apple-style-span"
style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">map</span>
statements to almost make it seem like I had never left Pythonland.
After doing all this, I also ended up writing my own
[operator.js](http://code.google.com/p/dhermes-project-euler/source/browse/js/operator.js)
to replace the wonderful Python native
module [operator](http://docs.python.org/library/operator.html), and my
own
[timer.js](http://code.google.com/p/dhermes-project-euler/source/browse/js/timer.js)
to stand in for the Python native
module [time](http://docs.python.org/library/time.html).

Finally, I had working code and could do a side by side comparison of V8
and the Python interpreter. **Update**: *I added a column
for [PyPy](http://pypy.org/), a just in time implementation of
Python. *Here is what I found (averaging the runtime over 10 separate
calls to each function, the results are):


<center>
<table border="1" style="border-collapse: collapse;">
<tbody>
<tr>
<th align="left">
Problem

</th>
<th align="left">
Answer

</th>
<th align="left">
Python

</th>
<th align="left">
Javascript

</th>
<th align="left">
Ratio (PY/JS)

</th>
<th align="left">
PyPy

</th>
</tr>
<tr>
<td>
1\*

</td>
<td>
233168

</td>
<td>
1804ms

</td>
<td>
1215ms

</td>
<td>
1.48

</td>
<td>
385ms

</td>
</tr>
<tr>
<td>
2\*

</td>
<td>
4613732

</td>
<td>
247ms

</td>
<td>
102ms

</td>
<td>
2.42

</td>
<td>
85ms

</td>
</tr>
<tr>
<td>
3\*

</td>
<td>
6857

</td>
<td>
4725ms

</td>
<td>
1508ms

</td>
<td>
3.13

</td>
<td>
582ms

</td>
</tr>
<tr>
<td>
4

</td>
<td>
906609

</td>
<td>
8708ms

</td>
<td>
149ms

</td>
<td>
58.44

</td>
<td>
282ms

</td>
</tr>
<tr>
<td>
5\*

</td>
<td>
232792560

</td>
<td>
136ms

</td>
<td>
186ms

</td>
<td>
0.73

</td>
<td>
114ms

</td>
</tr>
<tr>
<td>
6\*

</td>
<td>
25164150

</td>
<td>
10ms

</td>
<td>
4ms

</td>
<td>
2.50

</td>
<td>
6ms

</td>
</tr>
<tr>
<td>
7

</td>
<td>
104743

</td>
<td>
656ms

</td>
<td>
12ms

</td>
<td>
54.67

</td>
<td>
11ms

</td>
</tr>
<tr>
<td>
8\*

</td>
<td>
40824

</td>
<td>
18045ms

</td>
<td>
5014ms

</td>
<td>
3.60

</td>
<td>
7042ms

</td>
</tr>
<tr>
<td>
9

</td>
<td>
31875000

</td>
<td>
610ms

</td>
<td>
3ms

</td>
<td>
203.33

</td>
<td>
8ms

</td>
</tr>
<tr>
<td>
10

</td>
<td>
142913828922

</td>
<td>
6628ms

</td>
<td>
167ms

</td>
<td>
39.69

</td>
<td>
116ms

</td>
</tr>
<tr>
<td>
11

</td>
<td>
70600674

</td>
<td>
49ms

</td>
<td>
2ms

</td>
<td>
24.50

</td>
<td>
11ms

</td>
</tr>
<tr>
<td>
12

</td>
<td>
76576500

</td>
<td>
5127ms

</td>
<td>
203ms

</td>
<td>
25.26

</td>
<td>
100ms

</td>
</tr>
<tr>
<td>
13\*

</td>
<td>
5537376230

</td>
<td>
1795ms

</td>
<td>
10710ms

</td>
<td>
0.17

</td>
<td>
1423ms

</td>
</tr>
<tr>
<td>
14

</td>
<td>
837799

</td>
<td>
5572ms

</td>
<td>
1712ms

</td>
<td>
3.25

</td>
<td>
362ms

</td>
</tr>
<tr>
<td>
15\*

</td>
<td>
137846528820

</td>
<td>
54ms

</td>
<td>
18ms

</td>
<td>
3.00

</td>
<td>
55ms

</td>
</tr>
<tr>
<td>
16\*

</td>
<td>
1366

</td>
<td>
1844ms

</td>
<td>
265ms

</td>
<td>
6.96

</td>
<td>
462ms

</td>
</tr>
<tr>
<td>
17

</td>
<td>
21124

</td>
<td>
87ms

</td>
<td>
4ms

</td>
<td>
21.75

</td>
<td>
7ms

</td>
</tr>
<tr>
<td>
18\*

</td>
<td>
1074

</td>
<td>
2291ms

</td>
<td>
1790ms

</td>
<td>
1.28

</td>
<td>
1090ms

</td>
</tr>
<tr>
<td>
19\*

</td>
<td>
171

</td>
<td>
2254ms

</td>
<td>
336ms

</td>
<td>
6.71

</td>
<td>
342ms

</td>
</tr>
<tr>
<td>
20\*

</td>
<td>
648

</td>
<td>
1061ms

</td>
<td>
9154ms

</td>
<td>
0.12

</td>
<td>
374ms

</td>
</tr>
<tr>
<td>
21

</td>
<td>
31626

</td>
<td>
18910ms

</td>
<td>
1038ms

</td>
<td>
18.22

</td>
<td>
728ms

</td>
</tr>
<tr>
<td>
22

</td>
<td>
871198282

</td>
<td>
188ms

</td>
<td>
7ms

</td>
<td>
26.86

</td>
<td>
8ms

</td>
</tr>
<tr>
<td>
23

</td>
<td>
4179871

</td>
<td>
83318ms

</td>
<td>
1120ms

</td>
<td>
74.39

</td>
<td>
1295ms

</td>
</tr>
<tr>
<td>
24\*

</td>
<td>
2783915460

</td>
<td>
206ms

</td>
<td>
210ms

</td>
<td>
0.98

</td>
<td>
139ms

</td>
</tr>
<tr>
<td>
25

</td>
<td>
4782

</td>
<td>
5865ms

</td>
<td>
35ms

</td>
<td>
167.57

</td>
<td>
232ms

</td>
</tr>
<tr>
<td>
26

</td>
<td>
983

</td>
<td>
28ms

</td>
<td>
18ms

</td>
<td>
1.56

</td>
<td>
4ms

</td>
</tr>
<tr>
<td>
27

</td>
<td>
-59231

</td>
<td>
645738ms

</td>
<td>
22536ms

</td>
<td>
28.65

</td>
<td>
28288ms

</td>
</tr>
<tr>
<td>
28\*

</td>
<td>
669171001

</td>
<td>
8509ms

</td>
<td>
1037ms

</td>
<td>
8.21

</td>
<td>
981ms

</td>
</tr>
<tr>
<td>
29

</td>
<td>
9183

</td>
<td>
184ms

</td>
<td>
96ms

</td>
<td>
1.92

</td>
<td>
20ms

</td>
</tr>
<tr>
<td>
30

</td>
<td>
443839

</td>
<td>
52167ms

</td>
<td>
1037ms

</td>
<td>
50.31

</td>
<td>
877ms

</td>
</tr>
<tr>
<td>
31

</td>
<td>
73682

</td>
<td>
9606ms

</td>
<td>
257ms

</td>
<td>
37.38

</td>
<td>
154ms

</td>
</tr>
<tr>
<td>
32

</td>
<td>
45228

</td>
<td>
206888ms

</td>
<td>
12096ms

</td>
<td>
17.10

</td>
<td>
4266ms

</td>
</tr>
<tr>
<td>
33

</td>
<td>
100

</td>
<td>
300ms

</td>
<td>
6ms

</td>
<td>
50.00

</td>
<td>
15ms

</td>
</tr>
<tr>
<td>
34

</td>
<td>
40730

</td>
<td>
7462ms

</td>
<td>
2447ms

</td>
<td>
3.05

</td>
<td>
247ms

</td>
</tr>
<tr>
<td>
35

</td>
<td>
55

</td>
<td>
8617ms

</td>
<td>
848ms

</td>
<td>
10.16

</td>
<td>
242ms

</td>
</tr>
<tr>
<td>
36

</td>
<td>
872187

</td>
<td>
189788ms

</td>
<td>
2183ms

</td>
<td>
86.94

</td>
<td>
3532ms

</td>
</tr>
<tr>
<td>
37

</td>
<td>
748317

</td>
<td>
2389022ms

</td>
<td>
71845ms

</td>
<td>
33.25

</td>
<td>
61551ms

</td>
</tr>
<tr>
<td>
38

</td>
<td>
932718654

</td>
<td>
506ms

</td>
<td>
10ms

</td>
<td>
50.60

</td>
<td>
12ms

</td>
</tr>
<tr>
<td>
39

</td>
<td>
840

</td>
<td>
178ms

</td>
<td>
6ms

</td>
<td>
29.67

</td>
<td>
12ms

</td>
</tr>
<tr>
<td>
40\*

</td>
<td>
210

</td>
<td>
326ms

</td>
<td>
202ms

</td>
<td>
1.61

</td>
<td>
119ms

</td>
</tr>
<tr>
<td>
41

</td>
<td>
7652413

</td>
<td>
2627ms

</td>
<td>
133ms

</td>
<td>
19.75

</td>
<td>
65ms

</td>
</tr>
<tr>
<td>
42

</td>
<td>
162

</td>
<td>
65ms

</td>
<td>
7ms

</td>
<td>
9.29

</td>
<td>
8ms

</td>
</tr>
<tr>
<td>
43

</td>
<td>
16695334890

</td>
<td>
38ms

</td>
<td>
2ms

</td>
<td>
19.00

</td>
<td>
2ms

</td>
</tr>
<tr>
<td>
44

</td>
<td>
5482660

</td>
<td>
384013ms

</td>
<td>
27744ms

</td>
<td>
13.84

</td>
<td>
6621ms

</td>
</tr>
<tr>
<td>
45\*

</td>
<td>
1533776805

</td>
<td>
17ms

</td>
<td>
4ms

</td>
<td>
4.25

</td>
<td>
8ms

</td>
</tr>
<tr>
<td>
46

</td>
<td>
5777

</td>
<td>
2864ms

</td>
<td>
202ms

</td>
<td>
14.18

</td>
<td>
65ms

</td>
</tr>
<tr>
<td>
47

</td>
<td>
134043

</td>
<td>
400967ms

</td>
<td>
12838ms

</td>
<td>
31.23

</td>
<td>
4425ms

</td>
</tr>
<tr>
<td>
48

</td>
<td>
9110846700

</td>
<td>
46ms

</td>
<td>
16ms

</td>
<td>
2.88

</td>
<td>
6ms

</td>
</tr>
<tr>
<td>
49

</td>
<td>
296962999629

</td>
<td>
115ms

</td>
<td>
8ms

</td>
<td>
14.38

</td>
<td>
13ms

</td>
</tr>
<tr>
<td>
50

</td>
<td>
997651

</td>
<td>
3277ms

</td>
<td>
80ms

</td>
<td>
40.96

</td>
<td>
51ms

</td>
</tr>
<tr>
<td colspan="6">
\*These were very quick to run, so the runtimes are the time taken to
run 10000 times.

</td>
</tr>
</tbody>
</table>
</center>

As you'll notice, standard Python gets its butt kicked. I was kind of
saddened by this, but in the end, just giddy that our web is faster
because of it (90% of my life is digital) and also that we can do
scripting faster on the server side (attribute to [Boris
Smus](http://twitter.com/#!/borismus)) because of the node project
(thanks Ryan Dahl).

Standard Python is actually slower in 46 of the 50 problems. In 28 of
the 46 node is faster by a factor of 10 or greater, in 9 of those 28 by
a factor of 50 or greater and in 2 of the 9 by a factor of 100 or
greater! The only 4 in which Python was faster were from the ***n =
10000*** sample. In fact, I was able to pinpoint exactly why:

-   \#5 - My own Javascript implementation of <span
    class="Apple-style-span"
    style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">gcd</span>
    is slower than the native (<span class="Apple-style-span"
    style="color: lime; font-family: 'Courier New', Courier, monospace;">from
    fractions import gcd</span>) Python library (resulting in a
    difference of 50 ms over 10000 iterations)
-   \#13 - The node package <span class="Apple-style-span"
    style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">bigint</span>
    is slower than the Python native <span class="Apple-style-span"
    style="color: lime; font-family: 'Courier New', Courier, monospace;">long
    int</span> (Javascript is slower by a factor of 6)
-   \#20 - The node package <span class="Apple-style-span"
    style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">bigint</span> is
    slower than the Python native <span class="Apple-style-span"
    style="color: lime; font-family: 'Courier New', Courier, monospace;">long
    int</span> (Javascript is slower by a factor of 8.5)
-   \#24 - Having to perform two <span class="Apple-style-span"
    style="background-color: white; color: purple; font-family: 'Courier New', Courier, monospace;">slice</span>s
    is slower in Javascript than in Python and there is no good way to
    just remove one element (resulting in a difference of 4 ms over
    10000 iterations; a little bit about that
    [here](http://ejohn.org/blog/javascript-array-remove/))

<div>

So what, you ask, is that lesson I speak of? Well, Javascript didn't
used to be this fast. How did it get that way? The brilliant and
inspired people behind V8 rethought the Javascript compile steps and
after much work, we now have code that is closer to the metal (attribute
to: [Eric Bidelman](https://twitter.com/#!/ebidel), i.e. closer to
machine code) than we had ever had before. The use of just-in-time
compilation and other incredible techniques has taken a formerly slow
and clunky language (Javascript) which was used well beyond its original
intended scope, and turned it into a damn fast dynamic language.
Hopefully, this movement will make its way to Python and other dynamic
languages and we can all have our code end up this close to the metal.

**Update**: *In response to the comments, I ran the same code on the
same machine, but with PyPy in place of Python. This is the direction I
hope standard Python goes in and commend the guys pumping out faster and
faster just in time implementations over at PyPy. I went through and
counted 20 node wins, 29 PyPy wins and 1 tie. (I reserve the right to
update the post with more detailed metrics.) While I do commend them,
the results don't really belong in this post because PyPy is still an
offshoot. (However, as I understand, they both have ties to C, as PyPy
uses GCC to compile to bytecode and V8 is written in C++. Feel free to
supplement my knowledge in the comments.)*

**Update**: *All benchmarking was run on my Mac Pro Desktop with a 3.2
GHz Quad-Core Intel Xeon processor and 4 cores for a total of 12 GB 1066
MHz DDR3 memory. I used Python version 2.6.1, node version 0.4.9, and
PyPy version 1.5 (running on top of Python 2.7.1 with GCC 4.0.1).*

</div>

<a href="https://profiles.google.com/114760865724135687241" rel="author" style="display: none;">About Bossy Lobster</a>
