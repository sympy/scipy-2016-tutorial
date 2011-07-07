
    $ ipython

    In [1]: x**2 + 1
    ---------------------------------------------------------------------------
    NameError                                 Traceback (most recent call last)

    /home/matt/repo/git/sympy/<ipython console> in <module>()

    NameError: name 'x' is not defined

    In [2]: x = 1

    In [3]: x**2 + 1
    Out[3]: 2

    In [4]: type(_)
    Out[4]: <type 'int'>

    In [5]: lambda x: x**2 + 1
    Out[5]: <function <lambda> at 0x84ae02c>

    In [6]: f = _

    In [7]: f(1)
    Out[7]: 2

    In [8]: type(_)
    Out[8]: <type 'int'>

    In [9]: import math

    In [10]: math.sin(1)
    Out[10]: 0.8414709848078965

    In [11]: math.cos(1)
    Out[11]: 0.54030230586813977

    In [12]: _10**2 + _11**2
    Out[12]: 1.0

    In [13]: math.sin(70)
    Out[13]: 0.77389068155788909

    In [14]: math.cos(70)
    Out[14]: 0.63331920308629985

    In [15]: __**2 + _**2
    Out[15]: 1.0

    In [16]: from sympy import *

    In [17]: x = Symbol('x')

    In [18]: x**2 + 1
    Out[18]: x**2 + 1

    In [19]: f = _

    In [20]: type(f)
    Out[20]: <class 'sympy.core.add.Add'>

    In [21]: f.subs(x, 1)
    Out[21]: 2

    In [22]: type(_)
    Out[22]: <class 'sympy.core.numbers.Integer'>

    In [23]: f(2)
    ---------------------------------------------------------------------------
    TypeError                                 Traceback (most recent call last)

    /home/matt/repo/git/sympy/<ipython console> in <module>()

    TypeError: 'Add' object is not callable




Python/IPython sessions
-----------------------

    $ ipython

    In [1]: import sympy

    In [2]: x = sympy.Symbol('x')

    In [3]: sympy.integrate(3*x**2)
    Out[3]: x**3

    In [5]: sympy.init_printing()

    In [6]: sympy.integrate(3*x**2)
    Out[6]:
     3
    x

isympy sessions
---------------

    $ bin/isympy

    mateusz@raven:~/repo/git/sympy$ bin/isympy
    IPython console for SymPy 0.6.7-git (Python 2.6.6) (ground types: gmpy)

    These commands were executed:
    >>> from __future__ import division
    >>> from sympy import *
    >>> x, y, z, t = symbols('x y z t')
    >>> k, m, n = symbols('k m n', integer=True)
    >>> f, g, h = symbols('f g h', cls=Function)

    Documentation can be found at http://www.sympy.org

    In [1]:

isympy options
--------------

    -h, --help            show this help message and exit
    -c CONSOLE, --console=CONSOLE
                          select type of interactive session: ipython | python
    -p PRETTY, --pretty=PRETTY
                          setup pretty printing: unicode | ascii | no
    -t TYPES, --types=TYPES
                          setup ground types: gmpy | python | sympy
    -o ORDER, --order=ORDER
                          setup ordering of terms: [rev-]lex | [rev-]grlex |
                          [rev-]grevlex | old
    -q, --quiet           print only version information at startup
    -C, --no-cache        disable caching mechanism

Global variables
----------------

SYMPY_USE_CACHE
SYMPY_GROUND_TYPES

Expression cache
----------------



Partial fraction decomposition
==============================

Partial fraction decomposition of a univariate rational function:

.. math::

    f(x) = \frac{p(x)}{q(x)}

where `p` and `q` are co-prime and `\deg(p) < `\deg(q)`, is an expression
of the form:

.. math::

    \sum_{i=1}^k \sum_{j=1}^{n_i} \frac{a_{ij}(x)}{q_i^j(x)}

where `q_i` for `i=1 \ldots k` are factors (e.g. over rationals or Gaussian
rationals) of `q`:

.. math::

    q(x) = \product_{i=1}^k q_i^{n_i}

If `p` and `q` aren't co-prime, we can use :func:`cancel` to remove common
factors and if `\deg(p) >= `\deg(q)`, then :func:`div` can be used to extract
the polynomial part of partial fraction expansion of `f` and reduce the degree
of `p`.

Suppose we would like to compute partial fraction decomposition of::

    >>> f = 1/(x**2*(x**2 + 1))
    >>> f
         1
    ───────────
     2 ⎛ 2    ⎞
    x ⋅⎝x  + 1⎠

This can be achieved with SymPy's built-in function :func:`apart`::

    >>> apart(f)
    >>>
        1      1
    - ────── + ──
       2        2
      x  + 1   x

We can use :func:`together` to verify this result::

    >>> together(_)
         1
    ───────────
     2 ⎛ 2    ⎞
    x ⋅⎝x  + 1⎠

Now we would like to compute this decomposition step-by-step. The rational
function `f` is already in factored form and has two factors `x^2` and
`x^2 + 1`. If `f` was in expanded from, we could use :func:`factor` to
obtain desired factorization::

    >>> numer(f)/expand(denom(f))
       1
    ───────
     4    2
    x  + x

    >>> factor(_)
         1
    ───────────
     2 ⎛ 2    ⎞
    x ⋅⎝x  + 1⎠

Based on the definition, partial fraction expansion of `f` will be of the
following form:

.. math::

    \frac{A}{x} + \frac{B}{x^2} + \frac{C x + D}{x**2 + 1}

Lets do this with SymPy. We will use undetermined coefficients method to
solve this problem. Lets start define symbols first::

    >>> var('A:D')
    (A, B, C, D)

We use here lexicographic syntax of :func:`var`. Next we can define three
rational functions::

    >>> p1 = A/x
    >>> p2 = B/x**2
    >>> p3 = (C*x + D)/(x**2 + 1)

    >>> p1, p2, p3
    ⎛A  B   C⋅x + D⎞
    ⎜─, ──, ───────⎟
    ⎜x   2    2    ⎟
    ⎝   x    x  + 1⎠

Lets add them together to get the desired form::

    >>> h = sum(_)
    >>> h
    A   B    C⋅x + D
    ─ + ── + ───────
    x    2     2
        x     x  + 1

Next step is to rewrite this expression as rational function in `x`::

    >>> together(h)
        ⎛ 2    ⎞     ⎛ 2    ⎞    2
    A⋅x⋅⎝x  + 1⎠ + B⋅⎝x  + 1⎠ + x ⋅(C⋅x + D)
    ────────────────────────────────────────
                   2 ⎛ 2    ⎞
                  x ⋅⎝x  + 1⎠

    >>> factor(_, x)
               3            2
    A⋅x + B + x ⋅(A + C) + x ⋅(B + D)
    ─────────────────────────────────
                2 ⎛ 2    ⎞
               x ⋅⎝x  + 1⎠

Lets now visually compare the last expression with `f`::

    >>> Eq(_, f)
               3            2
    a⋅x + b + x ⋅(a + c) + x ⋅(b + d)        1
    ───────────────────────────────── = ───────────
                2 ⎛ 2    ⎞               2 ⎛ 2    ⎞
               x ⋅⎝x  + 1⎠              x ⋅⎝x  + 1⎠

Our task boils down to finding `A`, `B`, `C` and `D`. We notice that
denominators are equal so we will proceed only with numerators::

    >>> eq = Eq(numer(_.lhs), numer(_.rhs))
    >>> eq
               3            2
    a⋅x + b + x ⋅(a + c) + x ⋅(b + d) = 1

To solve this equation, we use :func:`solve_undetermined_coeffs`::

    >>> solve_undetermined_coeffs(eq, [A, B, C, D], x)
    {A: 0, B: 1, C: 0, D: -1}

This gave us values for our parameters, which now can be put into the initial
expression::

    >>> h.subs(_)
        1      1
    - ────── + ──
       2        2
      x  + 1   x

This result is identical to the result we got from ``apart(f)``. Suppose
however, we would like to see how undetermined coefficients method works.
First we have to extract coefficients of `x` of both sides of the equation::

    >>> lhs, rhs = Poly(eq.lhs, x), Poly(eq.rhs, x)

    >>> lhs
    Poly((A + C)*x**3 + (B + D)*x**2 + A*x + B, x, domain='ZZ[A,B,C,D]')
    >>> rhs
    Poly(1, x, domain='ZZ')

Now we can use :func:`Poly.nth` to obtain coefficients of `x`::

    >>> [ Eq(lhs.nth(i), rhs.nth(i)) for i in xrange(0, 4) ]
    [b = 1, a = 0, b + d = 0, a + c = 0]

Solving this system of linear equations gives the same solution set as
previously::

    >>> solve(_)
    {a: 0, b: 1, c: 0, d: -1}

    >>> f.subs(_)
        1      1
    - ────── + ──
       2        2
      x  + 1   x

There are several other ways we can approach undetermined coefficients
method. For example we could use :func:`collect` for this::

    >>> collect(eq.lhs - eq.rhs, x, evaluate=False)
    ⎧                 2          3       ⎫
    ⎨1: B - 1, x: A, x : B + D, x : A + C⎬
    ⎩                                    ⎭

    >>> solve(_.values())
    {A: 0, B: 1, C: 0, D: -1}

This approach is even simpler than using :func:`Poly.nth`. Finally we use a
little trick with :class:`Symbol` and visually present solution to partial
fraction decomposition of `f`::

    >>> Eq(Symbol('apart')(f), f.subs(_))
         ⎛     1     ⎞       1      1
    apart⎜───────────⎟ = - ────── + ──
         ⎜ 2 ⎛ 2    ⎞⎟      2        2
         ⎝x ⋅⎝x  + 1⎠⎠     x  + 1   x

Tasks
-----

1. Compute partial fraction decomposition of:

 * `\frac{3 x + 5}{{2 x + 1)^2}`
 * `\frac{3 x + 5}{{u x + v)^2}`
 * `\frac{(3 x + 5)^2}{{2 x + 1)^2}`

2. Can you use :func:`Expr.coeff` in place of :func:`Poly.nth`?

Deriving trigonometric identities
=================================

Lets assume that we need a formula for `\sin(a + b)` in terms of `\sin(a)`,
`\sin(b)`, `\cos(a)` and `\cos(b)`, be we don't remember it, nor we don't
know how to get it easily with SymPy. We will derive this formula from
scratch using Taylor series expansions and a little symbolic manipulation.

Lets start with definition of symbols and the expression in consideration::

    >>> var('a,b')
    (a, b)

    >>> f = sin(a + b)
    >>> f
    sin(a + b)

Now lets expand `f` with respect to `b` around 0::

    >>> f.series(b, 0, 10)
                         2           3           4           5           6           7           8           9
                        b ⋅sin(a)   b ⋅cos(a)   b ⋅sin(a)   b ⋅cos(a)   b ⋅sin(a)   b ⋅cos(a)   b ⋅sin(a)   b ⋅cos(a)
    sin(a) + b⋅cos(a) - ───────── - ───────── + ───────── + ───────── - ───────── - ───────── + ───────── + ───────── + O(b**10)
                            2           6           24         120         720         5040       40320       362880

This isn't very readable but we can clearly see a pattern around `\sin(a)`
and `\cos(a)`. Lets collect terms with respect to those two expressions::

    >>> collect(_, [sin(a), cos(a)])
    ⎛   9       7      5    3    ⎞          ⎛   8      6    4    2    ⎞
    ⎜  b       b      b    b     ⎟          ⎜  b      b    b    b     ⎟
    ⎜────── - ──── + ─── - ── + b⎟⋅cos(a) + ⎜───── - ─── + ── - ── + 1⎟⋅sin(a) + O(b**10)
    ⎝362880   5040   120   6     ⎠          ⎝40320   720   24   2     ⎠

    >>> _.removeO()
    ⎛   8      6    4    2    ⎞          ⎛   9       7      5    3    ⎞
    ⎜  b      b    b    b     ⎟          ⎜  b       b      b    b     ⎟
    ⎜───── - ─── + ── - ── + 1⎟⋅sin(a) + ⎜────── - ──── + ─── - ── + b⎟⋅cos(a)
    ⎝40320   720   24   2     ⎠          ⎝362880   5040   120   6     ⎠

    >>> g = _

We got two subexpression that look very familiar. Lets expand `\sin(b)`
in `b` around 0 and remove the order term::

    >>> sin(b).series(b, 0, 10)
         3     5     7       9
        b     b     b       b
    b - ── + ─── - ──── + ────── + O(b**10)
        6    120   5040   362880

    >>> _.removeO()
       9       7      5    3
      b       b      b    b
    ────── - ──── + ─── - ── + b
    362880   5040   120   6

This is clearly the second subexpression, so lets substitute it for
`\sin(b)`::

    >>> g.subs(_, sin(b))
    ⎛   8      6    4    2    ⎞
    ⎜  b      b    b    b     ⎟
    ⎜───── - ─── + ── - ── + 1⎟⋅sin(a) + sin(b)⋅cos(a)
    ⎝40320   720   24   2     ⎠

    >>> h = _

Now lets repeat this procedure for `\cos(b)`::

    >>> cos(b).series(b, 0, 10)
         2    4     6      8
        b    b     b      b
    1 - ── + ── - ─── + ───── + O(b**10)
        2    24   720   40320

    >>> _.removeO()
       8      6    4    2
      b      b    b    b
    ───── - ─── + ── - ── + 1
    40320   720   24   2

    >>> h.subs(_, cos(b))
    sin(a)⋅cos(b) + sin(b)⋅cos(a)

This gave us a formula for `\sin(a + b)`::

    >>> Eq(f, _)
    sin(a + b) = sin(a)⋅cos(b) + sin(b)⋅cos(a)

There is, however, a much simpler way to get the same result::

    >>> Eq(f, sin(a + b).expand(trig=True))
    sin(a + b) = sin(a)⋅cos(b) + sin(b)⋅cos(a)

Tasks
-----

1. Repeat this procedure but expand wrt `a` in the first step.
2. Use this procedure to derive a formula for `\cos(a + b)`.

Not only symbolics: numerical computing
=======================================

Symbolic mathematics can't exist without numerical methods. Most "symbolic"
modules in SymPy take at least some advantage of numerical computing. SymPy
uses mpmath library for this purpose.

Lets start from something simple and find numerical approximation to `\pi`.
Normally SymPy represents `\pi` as a symbolic entity::

    >>> pi
    π
    >>> type(_)
    <class 'sympy.core.numbers.Pi'>

To obtain numerical approximation of `\pi` we can use either :func:`evalf`
method or :func:`N`, which is a simple wrapper over the former method::

    >>> pi.evalf()
    3.14159265358979

The default precision is 15 digits. We can change this using ``n`` parameter::

    >>> pi.evalf(n=30)
    3.14159265358979323846264338328

The mpmath library implements arbitrary precision floating point arithmetics
(limited only by available memory), so we can set ``n`` to a very big value,
e.g. one million::

    >>> million_digits = pi.evalf(n=1000000)
    >>> str(million_digist)[-1]
    5

:func:`evalf` can handle much more complex expressions than `\pi`, for
example::

    >>> exp(sin(1) + E**pi - I)
               π
     sin(1) + ℯ  - ⅈ
    ℯ

    >>> _.evalf()
    14059120207.1707 - 21895782412.4995⋅ⅈ

or::

    >>> zeta(S(14)/17)
     ⎛14⎞
    ζ⎜──⎟
     ⎝17⎠

    >>> zeta(S(14)/17).evalf()
    -5.10244976858838

Symbolic entities are ignored::

    >>> pi*x
    π⋅x
    >>> _.evalf()
    3.14159265358979⋅x

Built-in functions :func:`float` and :func:`complex` take advantage of
:func:`evalf`::

    >>> float(pi)
    3.14159265359
    >>> type(_)
    <type 'float'>

    >>> float(pi*I)
    ...
    ValueError: Symbolic value, can't compute

    >>> complex(pi*I)
    3.14159265359j
    >>> type(_20)
    <type 'complex'>

The base type for computing with floating point numbers in SymPy is
:class:`Float`. It allows for several flavors of initialization and
keeps track of precision::

    >>> 2.0
    2.0
    >>> type(_)
    <type 'float'>

    >>> Float(2.0)
    2.00000000000000
    >>> type(_)
    <class 'sympy.core.numbers.Float'>

    >>> sympify(2.0)
    2.00000000000000
    >>> type(_)
    <class 'sympy.core.numbers.Float'>

    >>> Float("3.14")
    3.14000000000000
    >>> Float("3.14e-400")
    3.14000000000000e-400

Notice that the last value is out of range for ``float``::

    >>> 3.14e-400
    0.0

We expected a very small value but not zero. This raises an important issue,
because if we try to construct a :class:`Float` this way, we will still get
zero::

    >>> Float(3.14e-400)
    0

The only way to fix this is to pass a string argument to :class:`Float`.

When symbolic mathematics matter?
---------------------------------

Consider a univariate function:

.. math::

    f(x) = x^(1 - \log(\log(\log(\log(\frac{1}{x})))))

We would like to compute:

.. math::

    \limit_{x \to 0^{+}} f(x)

Lets define function `f` in SymPy::

    >>> f = x**(1 - log(log(log(log(1/x)))))
    >>> f
          ⎛   ⎛   ⎛   ⎛1⎞⎞⎞⎞
     - log⎜log⎜log⎜log⎜─⎟⎟⎟⎟ + 1
          ⎝   ⎝   ⎝   ⎝x⎠⎠⎠⎠
    x

A very straight forward approach is to "see" how `f` behaves on the right
hand side of zero, is to evaluate `f` at a few sufficiently small points.

Lets start with points of the form `x = 10^{-k}`::

    >>> f.subs(x, 10**-1).evalf()
    0.00114216521536353 + 0.00159920801047526⋅ⅈ
    >>> f.subs(x, 10**-2).evalf()
    0.000191087007486009
    >>> f.subs(x, 10**-3).evalf()
    5.60274947776528e-5
    >>> f.subs(x, 10**-4).evalf()
    1.24646630615307e-5
    >>> f.subs(x, 10**-5).evalf()
    2.73214471781554e-6
    >>> f.subs(x, 10**-6).evalf()
    6.14631623897124e-7
    >>> f.subs(x, 10**-7).evalf()
    1.42980539541700e-7
    >>> f.subs(x, 10**-8).evalf()
    3.43858142726788e-8

We obtained a decreasing sequence values which suggests that the limit
is zero. Lets now try points of the form `x = 10^{-10^k}`::

    >>> f.subs(x, 10**-10**1).evalf()
    2.17686941815359e-9
    >>> f.subs(x, 10**-10**2).evalf()
    4.87036575966825e-48
    >>> f.subs(x, 10**-10**3).evalf()
    +inf

For `x = 10^{-10^3}` we got a very peculiar value. This happened because::

    >>> 10**-10**3
    0.0

we used Python's floating point values. Instead we can use either exact
numbers or SymPy's floating point numbers::

    >>> Integer(10)**-10**3 != 0
    True
    >>> Float(10.0)**-10**3 != 0
    True

Lets continue with SymPy's floating point numbers::

    >>> f.subs(x, Float(10.0)**-10**1).evalf()
    2.17686941815359e-9
    >>> f.subs(x, Float(10.0)**-10**2).evalf()
    4.87036575966825e-48
    >>> f.subs(x, Float(10.0)**-10**3).evalf()
    1.56972853078736e-284
    >>> f.subs(x, Float(10.0)**-10**4).evalf()
    3.42160969045530e-1641
    >>> f.subs(x, Float(10.0)**-10**5).evalf()
    1.06692865269193e-7836
    >>> f.subs(x, Float(10.0)**-10**6).evalf()
    4.40959214078817e-12540
    >>> f.subs(x, Float(10.0)**-10**7).evalf()
    1.11148303902275e+404157
    >>> f.subs(x, Float(10.0)**-10**8).evalf()
    8.63427256445142e+8443082

This time the sequence of values is rapidly decreasing, but only until
a sufficiently small numer where `f` has an inflexion point. After that,
values of `f` increase very rapidly, which may suggest that the actual
limit is ``+\inf``. It seems that our initial guess is wrong. However, for
now we still can't draw any conclusions about behaviour of `f`, because
if we take even smaller numbers we may reach other points of inflection.

The mpmath library implements a function for computing numerical limits
of function, we can try to take advantage of this::

    >>> from sympy.mpmath import limit as nlimit
    >>> F = lambdify(x, f, modules='mpmath')

    >>> nlimit(F, 0)
    (2.23372778188847e-5 + 2.28936592344331e-8j)

This once again suggests that the limit is zero. Lets use exponential
distribution of pints in :func:`nlimit`::

    >>> nlimit(F, 0, exp=True)
    (3.43571317799366e-20 + 4.71360839667667e-23j)

This didn't help much. Still zero. The only solution to this problem
is to use analytic methods. For this we will use :func:`limit`::

    >>> limit(f, x, 0)
    ∞

which shows us that our initial guess was completely wrong. This nicely
shows that solving ill conditioned problems may require assistance of
symbolic mathematics system. More about this can be found in Dominic
Gruntz's PhD tesis (http://www.cybertester.com/data/gruntz.pdf), where
this problem is explained in detail and an algorithm shown, which can
solve this problem and which is implemented in SymPy.

Tasks
-----

.. TODO
