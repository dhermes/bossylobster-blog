Title: Reverse Calculating An Interest Rate
Date: 2012-05-16 02:44
Author: Danny Hermes (noreply@blogger.com)
Tags: Finance, Interest Rate, Mortgage, Newton-Raphson Method, Numerical Analysis, Python
Slug: reverse-calculating-an-interest-rate

I was recently playing around with some loan data and only happened to
have the term (or length, or duration) of the loan, the amount of the
recurring payment (in this case monthly) and the remaining principal
owed on the loan. I figured there was an easy way to get at the interest
rate, but wasn't sure how. After some badgering from my coworker
[+Paul](https://plus.google.com/104679465567407024302), I searched the
web and found a
[tool](http://www.calcamo.net/loancalculator/quickcalculations/loan-rate.php5)
from [CALCAmo](http://www.calcamo.net/) (a site just for calculating
amortizations).  
  
Problem solved, right? Wrong. I wanted to know why; I had to [go
deeper](http://t.qkme.me/35co7h.jpg). So I did a bit of math and a bit
of programming and I was where I needed to be. I'll break the following
down into parts before going on full steam.  

-   Break down the amortization schedule in terms of the variables we
    have and the one we want
-   Determine a function we want to find zeroes of
-   Write some code to implement the Newton-Raphson method
-   Utilize the Newton-Raphson code to find an interest rate
-   Bonus: Analyze the function to make sure we are right

**<span style="font-size: large;">Step I: Break Down the [Amortization
Schedule](http://en.wikipedia.org/wiki/Amortization_schedule)</span>**  
  
We can do this using the series \\(\\left\\{P\_i\\right\\}\_i\\) of
principal owed, which varies over time and will go to zero once paid
off. In this series, \\(P\_0\\) is the principal owed currently and
\\(P\_i\\) is the principal owed after \\(i\\) payments have been made.
(Assuming monthly payments, this will be after \\(i\\) months.) If the
term is \\(T\\) periods, then we have \\(P\_T = 0\\).  
  
We have already introduced the term (\\(T\\)); we also need the value
of the recurring (again, usually monthly) payment \\(R\\), the interest
rate \\(r\\) and the initial principal owed \\(P\_0 = P\\).  
  
**Time-Relationship between Principal Values**  
  
If after \\(i\\) periods, \\(P\_i\\) is owed, then after one period has
elapsed, we will owe \\(P\_i \\cdot m\\) where \\(m = m(r)\\) is some
multiplier based on the length of the term. For example if each period
is one month, then we divide our rate by \\(12\\) for the interest and
add \\(1\\) to note that we are adding to existing principal: \\[m(r) =
1 + \\frac{r}{12}.\\] In addition to the interest, we will have paid off
\\(R\\) hence \\[P\_{i + 1} = P\_i \\cdot m - R.\\] **Formula for
\\(P\_i\\)**  
  
Using this, we can actually determine \\(P\_i\\) strictly in terms of
\\(m, R\\) and \\(P\\). First, note that \\[P\_2 = P\_1 \\cdot m - R =
(P\_0 \\cdot m - R) \\cdot m - R = P \\cdot m\^2 - R(m + 1)\\] since
\\(P\_0 = P\\). We can show inductively that \\[P\_i = P \\cdot m\^i - R
\\cdot \\sum\_{j = 0}\^{i - 1} m\^j.\\] We already have the base case
\\(i = 1\\), by definition. Assuming it holds for \\(i\\), we see that
\\[P\_{i + 1} = P\_i \\cdot m - R =  m \\cdot \\left(P \\cdot m\^i - R
\\cdot \\sum\_{j = 0}\^{i - 1} m\^j\\right) - R = P \\cdot m\^{i + 1} -
R \\cdot \\sum\_{j = 1}\^{i} m\^j - R,\\] and our induction is complete.
(We bump the index \\(j\\) since we are multiplying each \\(m\^j\\) by
\\(m\\).)  
Each term in the series is related to the previous one (except
\\(P\_0\\), since time can't be negative in this case).   
  
**<span style="font-size: large;">Step II: Determine a Function we want
to find Zeroes of</span>**  
  
Since we know \\(P\_T = 0\\) and \\(P\_T = P \\cdot m\^T - R \\cdot
\\sum\_{j = 0}\^{T - 1} m\^j\\), we actually have a polynomial in place
that will let us solve for \\(m\\) and in so doing, solve for \\(r\\).  
  
To make our lives a tad easier, we'll do some rearranging. First, note
that \\[\\sum\_{j = 0}\^{T - 1} m\^j = m\^{T - 1} + \\cdots + m + 1 =
\\frac{m\^T - 1}{m - 1}.\\] We calculate this sum of a geometric series
here, but I'll just refer you to the [Wikipedia
page](http://en.wikipedia.org/wiki/Geometric_series) instead. With this
reduction we want to solve \\[0 = P \\cdot m\^T - R \\cdot \\frac{m\^T -
1}{m - 1} \\Longleftrightarrow P \\cdot m\^T \\cdot (m - 1) = R
\\cdot (m\^T - 1).\\] With that, we have accomplished Step II, we have
found a function (parameterized by \\(P, T\\) and \\(R\\) which we can
use zeroes from to find our interest rate: \\[f\_{P, T, R}(m) = P \\cdot
m\^T \\cdot (m - 1) - R \\cdot (m\^T - 1) = P \\cdot m\^{T + 1} - (P +
R) \\cdot m\^T + R.\\] **<span style="font-size: large;">Step III: Write
some code to implement the [Newton-Raphson
method](http://en.wikipedia.org/wiki/Newton's_method)</span>**  
  
We use the Newton-Raphson method to get super-duper-close to a zero of
the function. For in-depth coverage, see the Wikipedia page on the
Newton-Raphson method, but I'll give some cursory coverage below. The
methods used to show that a fixed point is found are not necessary for
the intuition behind the method.  
  
**Intuition behind the method**  
  
For the intuition, assume we know (and can compute) a function \\(f\\),
its derivative \\(f'\\) and a value \\(x\\). Assume there is some zero
\\(y\\) nearby \\(x\\). Since they are close, we can approximate the
slope of the line between the points \\((x, f(x)\\) and \\((y, f(y)\\)
with the derivative nearby. Since we know \\(x\\), we use \\(f'(x)\\)
and intuit that \\[f'(x) = \\text{slope} = \\frac{f(y) - f(x)}{y - x}
\\Rightarrow y - x = \\frac{f(y) - f(x)}{f'(x)}.\\] But, since we know
that \\(y\\) is a zero, \\(f(y) - f(x) = -f(x)\\) hence \\[y - x =
\\frac{-f(x)}{f'(x)} \\Rightarrow y = x - \\frac{f(x)}{f'(x)}.\\] Using
this method, one can start with a given value \\(x\_0 = x\\) and compute
better and better approximations of a zero via the iteration above that
determines \\(y\\). We use a sequence to do so: \\[x\_{i + 1} = x\_i -
\\frac{f(x\_i)}{f'(x\_i)}\\] and stop calculating the \\(x\_i\\) either
after \\(f(x\_i)\\) is below a preset threshold or after the fineness of
the approximation \\(\\left|x\_i - x\_{i + 1}\\right|\\) goes below a
(likely different) preset threshold. Again, there is much that can be
said about these approximations, but we are trying to accomplish things
today, not theorize.  
  
**Programming Newton-Raphson**  
  
To perform Newton-Raphson, we'll implement a Python function that takes
the initial guess (\\(x\_0\\)) and the functions \\(f\\) and \\(f'\\).
We'll also (arbitrarily) stop after the value \\(f(x\_i)\\) drops below
\\(10\^{-8}\\) in absolute value.  

~~~~ {.prettyprint style="background-color: white;"}
def newton_raphson_method(guess, f, f_prime):    def next_value(value):        return value - f(value)*1.0/f_prime(value)    current = guess    while abs(f(current)) > 10**(-8):        current = next_value(current)    return current
~~~~

As you can see, once we have <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">f</span>
 and <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">f\_prime</span>,
everything else is easy because all the work in calculating the next
value (via <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">next\_value</span>)
is done by the functions.  
  
**<span style="font-size: large;">Step IV: Utilize the Newton-Raphson
code to find an Interest Rate</span>**  
  
We first need to implement \\(f\_{P, T, R}(m) = P \\cdot m\^{T + 1} - (P
+ R) \\cdot m\^T + R\\) and \\(f'\_{P, T, R}\\) in Python. Before doing
so, we do a simple derivative calculation: \\[f\_{P, T, R}'(m) = P
\\cdot (T + 1) \\cdot m\^T - (P + R) \\cdot T \\cdot m\^{T - 1}.\\] With
these [formulae](http://dictionary.reference.com/browse/formulae) in
hand, we write a function which will spit out the corresponding <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">f</span>
and <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">f\_prime</span>
given the parameters \\(P\\) (<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">principal</span>),
\\(T\\) (<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">term</span>)
and \\(R\\) (<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">payment</span>):  

~~~~ {.prettyprint style="background-color: white;"}
def generate_polynomials(principal, term, payment):    def f(m):        return (principal*(m**(term + 1)) - (principal + payment)*(m**term) +                payment)    def f_prime(m):        return (principal*(term + 1)*(m**term) -                (principal + payment)*term*(m**(term - 1)))    return (f, f_prime)
~~~~

Note that these functions only take a single argument (<span
style="color: lime; font-family: 'Courier New', Courier, monospace;">m</span>),
but we are able to use the other parameters from the parent scope beyond
the life of the call to <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">generate\_polynomials</span>
due to
[closure](http://en.wikipedia.org/wiki/Closure_(computer_science)) in
Python.  
  
In order to solve, we need an initial <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">guess</span>,
but we need to know the relationship between \\(m\\) and \\(r\\) before
we can determine what sort of <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">guess</span> makes
sense. In addition, once a value for \\(m\\) is returned from
Newton-Raphson, we need to be able to turn it into an \\(r\\) value so
functions <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">m</span>
and <span
style="color: lime; font-family: 'Courier New', Courier, monospace;">m\_inverse</span>
should be implemented. For our dummy case here, we'll assume monthly
payments (and compounding):  

~~~~ {.prettyprint style="background-color: white;"}
def m(r):    return 1 + r/12.0def m_inverse(m_value):    return 12.0*(m_value - 1)
~~~~

Using these, and assuming that an interest rate of **10%** is a good
guess, we can put all the pieces together:  

~~~~ {.prettyprint style="background-color: white;"}
def solve_for_interest_rate(principal, term, payment, m, m_inverse):    f, f_prime = generate_polynomials(principal, term, payment)    guess_m = m(0.10)  # ten percent as a decimal    m_value = newton_raphson_method(guess_m, f, f_prime)    return m_inverse(m_value)
~~~~

To check that this makes sense, let's plug in some values. Using the
[bankrate.com loan
calculator](http://www.bankrate.com/calculators/mortgages/mortgage-calculator.aspx),
if we have a 30-year loan (with \\(12 \\cdot 30 = 360\\) months of
payments) of \$100,000 with an interest rate of 7%, the monthly payment
would be \$665.30. Plugging this into our pipeline:  

~~~~ {.prettyprint style="background-color: white;"}
>>> principal = 100000>>> term = 360>>> payment = 665.30>>> solve_for_interest_rate(principal, term, payment, m, m_inverse)0.0699996284703
~~~~

And we see the rate of 7% is approximated quite well!  
  
**<span style="font-size: large;">Bonus: Analyze the function to make
sure we are right</span>**  
  
Coming soon. We will analyze the derivate and concavity to make sure
that our guess yield the correct (and unique) zero. [About Bossy
Lobster](https://profiles.google.com/114760865724135687241)

</p>

