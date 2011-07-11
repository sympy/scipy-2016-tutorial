
.. include:: definitions.def

=======================================
Mathematical problem solving with SymPy
=======================================

Knowing the basics of SymPy, let's now solve several mathematical problems
with it. The level of difficulty of examples in this section varies from
simple symbolic manipulation to theorem proving in algebraic geometry.

Each section includes a short theoretical background, that explains all
mathematical knowledge needed to understand a particular example. Code
examples and size of problems were adjusted to make them unobtrusive to
tutorial readers and make it possible to run them even on mobile devices.

Partial fraction decomposition
==============================

The partial fraction decomposition of a univariate rational function:

.. math::

    f(x) = \frac{p(x)}{q(x)}

where `p` and `q` are co-prime and `\deg(p) < \deg(q)`, is an expression
of the form:

.. math::

    \sum_{i=1}^k \sum_{j=1}^{n_i} \frac{a_{ij}(x)}{q_i^j(x)}

where `q_i` for `i=1 \ldots k` are factors (e.g. over rationals or Gaussian
rationals) of `q`:

.. math::

    q(x) = \prod_{i=1}^k q_i^{n_i}

If `p` and `q` aren't co-prime, we can use :func:`cancel` to remove common
factors and if `\deg(p) >= \deg(q)`, then :func:`div` can be used to extract
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
obtain the desired factorization::

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

Based on the definition, the partial fraction expansion of `f` will be of the
following form:

.. math::

    \frac{A}{x} + \frac{B}{x^2} + \frac{C x + D}{x^2 + 1}

Let's do this with SymPy. We will use undetermined coefficients method to
solve this problem. Let's start by defining some symbols::

    >>> var('A:D')
    (A, B, C, D)

We use here the lexicographic syntax of :func:`var`. Next we can define three
rational functions::

    >>> p1 = A/x
    >>> p2 = B/x**2
    >>> p3 = (C*x + D)/(x**2 + 1)

    >>> p1, p2, p3
    ⎛A  B   C⋅x + D⎞
    ⎜─, ──, ───────⎟
    ⎜x   2    2    ⎟
    ⎝   x    x  + 1⎠

Let's add them together to get the desired form::

    >>> h = sum(_)
    >>> h
    A   B    C⋅x + D
    ─ + ── + ───────
    x    2     2
        x     x  + 1

The next step is to rewrite this expression as rational function in `x`::

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

Let's now visually compare the last expression with `f`::

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

    >>> [ Eq(lhs.nth(i), rhs.nth(i)) for i in xrange(4) ]
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

Notice that even though the expressions were not :func:`Eq`'s, this still
worked. This is because SymPy assumes by default that expressions are
identically equal to 0, so ``solve(Eq(expr, 0))`` is the same as
``solve(expr)``.

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

  * `\frac{3 x + 5}{(2 x + 1)^2}`
  * `\frac{3 x + 5}{(u x + v)^2}`
  * `\frac{(3 x + 5)^2}{(2 x + 1)^2}`

2. Can you use :func:`Expr.coeff` in place of :func:`Poly.nth`?

Deriving trigonometric identities
=================================

Let's assume that we need a formula for `\sin(a + b)` in terms of `\sin(a)`,
`\sin(b)`, `\cos(a)` and `\cos(b)`, but we don't remember it, nor do we
know how to get it easily with SymPy. We will derive this formula from
scratch using Taylor series expansions and a little symbolic manipulation.

Let's start with definition of symbols and the expression in consideration::

    >>> var('a,b')
    (a, b)

    >>> f = sin(a + b)
    >>> f
    sin(a + b)

Now let's expand `f` as a power series with respect to `b` around 0::

    >>> f.series(b, 0, 10)
                         2           3           4           5           6           7           8           9
                        b ⋅sin(a)   b ⋅cos(a)   b ⋅sin(a)   b ⋅cos(a)   b ⋅sin(a)   b ⋅cos(a)   b ⋅sin(a)   b ⋅cos(a)
    sin(a) + b⋅cos(a) - ───────── - ───────── + ───────── + ───────── - ───────── - ───────── + ───────── + ───────── + O(b**10)
                            2           6           24         120         720         5040       40320       362880

This isn't very readable but we can clearly see a pattern around `\sin(a)`
and `\cos(a)`. Let's collect terms with respect to those two expressions::

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

We got two subexpression that look very familiar. Let's expand `\sin(b)`
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

This is clearly the second subexpression, so let's substitute it for
`\sin(b)`::

    >>> g.subs(_, sin(b))
    ⎛   8      6    4    2    ⎞
    ⎜  b      b    b    b     ⎟
    ⎜───── - ─── + ── - ── + 1⎟⋅sin(a) + sin(b)⋅cos(a)
    ⎝40320   720   24   2     ⎠

    >>> h = _

Now let's repeat this procedure for `\cos(b)`::

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

#. Repeat this procedure but expand with respect to `a` in the first step.
#. Use this procedure to derive a formula for `\cos(a + b)`.

Not only symbolics: numerical computing
=======================================

Symbolic mathematics can't exist without numerical methods. Most "symbolic"
modules in SymPy take at least some advantage of numerical computing. SymPy
uses the mpmath library for this purpose.

Let's start from something simple and find numerical approximation to `\pi`.
Normally SymPy represents `\pi` as a symbolic entity::

    >>> pi
    π
    >>> type(_)
    <class 'sympy.core.numbers.Pi'>

To obtain numerical approximation of `\pi` we can use either the :func:`evalf`
method or :func:`N`, which is a simple wrapper over the former method::

    >>> pi.evalf()
    3.14159265358979

The default precision is 15 digits. We can change this using the ``n`` parameter::

    >>> pi.evalf(n=30)
    3.14159265358979323846264338328

The mpmath library implements arbitrary precision floating point arithmetics
(limited only by available memory), so we can set ``n`` to a very big value,
e.g. one million::

    >>> million_digits = pi.evalf(n=1000000)
    >>> str(million_digits)[-1]
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
    Traceback (most recent call last):
    ...
    ValueError: Symbolic value, can't compute

    >>> complex(pi*I)
    3.14159265359j
    >>> type(_)
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

    f(x) = x^{(1 - \log(\log(\log(\log(\frac{1}{x})))))}

We would like to compute:

.. math::

    \lim_{x \to 0^{+}} f(x)

Let's define the function `f` in SymPy::

    >>> f = x**(1 - log(log(log(log(1/x)))))
    >>> f
          ⎛   ⎛   ⎛   ⎛1⎞⎞⎞⎞
     - log⎜log⎜log⎜log⎜─⎟⎟⎟⎟ + 1
          ⎝   ⎝   ⎝   ⎝x⎠⎠⎠⎠
    x

A very straight forward approach is to "see" how `f` behaves on the right
hand side of zero. We can try to read the solution from the graph of `f`:

.. plot::
    :align: center

    import matplotlib.pyplot as plt
    from sympy.mpmath import plot, log

    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.set_title(r"Plot of $f(x)$ in $[0, 0.01]$.")

    f = lambda x: x**(1 - log(log(log(log(1/x)))))
    plot(f, xlim=[0, 0.01], axes=axes)

This gives us first hint that the limit might be zero. Of course reading
a graph of a function isn't a very precise method for computing limits.
Instead of analyzing the graph of `f`, we can improve this approach a
little by evaluating `f(x)` for sufficiently small arguments.

Let's start with arguments of the form `x = 10^{-k}`::

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
is zero. Let's now try points of the form `x = 10^{-10^k}`::

    >>> f.subs(x, 10**-10**1).evalf()
    2.17686941815359e-9
    >>> f.subs(x, 10**-10**2).evalf()
    4.87036575966825e-48
    >>> f.subs(x, 10**-10**3).evalf()
    +inf

For `x = 10^{-10^3}` we got a very peculiar value. This happened because::

    >>> 10**-10**3
    0.0

and the reason for this is that we used Python's floating point values.
Instead we can use either exact numbers or SymPy's floating point numbers::

    >>> Integer(10)**-10**3 != 0
    True
    >>> Float(10.0)**-10**3 != 0
    True

Let's continue with SymPy's floating point numbers::

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
now we still can't draw any conclusions about behavior of `f`, because
if we take even smaller numbers we may reach other points of inflection.

The mpmath library implements a function for computing numerical limits
of function, we can try to take advantage of this::

    >>> from sympy.mpmath import limit as nlimit
    >>> F = lambdify(x, f, modules='mpmath')

    >>> nlimit(F, 0)
    (2.23372778188847e-5 + 2.28936592344331e-8j)

This once again suggests that the limit is zero. Let's use an exponential
distribution of points in :func:`nlimit`::

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

1. Compute first 55 digits of numerical approximation of `f(\pi)`.
2. Read this `webcomic <http://www.qwantz.com/index.php?comic=1013>`_.
   What is the first digit of `e` to contain `999999`? What is the first
   digit of `\pi` to contain `789`?
3. In addition to the above example, Gruntz gives another example of ill
   conditioned function in his thesis to show why symbolic computation of
   limits can be preferred to numerical computation:

   .. math::

       \lim_{x \to \infty}{\left(\operatorname{erf}\left(x - {e^{-e^{x}}}\right) -
           \operatorname{erf}\left(x\right)\right) e^{e^{x}}} e^{x^{2}}

   (in SymPy, ``(erf(x - exp(-exp(x))) - erf(x))*exp(exp(x))*exp(x**2)``).
   Compute the above limit in SymPy using methods similar to the ones presented
   in this section. What are the drawbacks of computing this limit numerically?
   What is the limit, exactly?

Summing roots of polynomials
============================

Let's suppose we are given a univariate polynomial `f(z)` and a univariate
rational function `g(z)`, and we wish to compute:

.. math::

    g(r_1) + g(r_2) + \ldots + g(r_n)

where `r_i` for `i = 1 \ldots n` are the roots of `f` (i.e. `f(r_i) = 0`).

In theory this is a very simple task. We just have to compute roots of `f`,
using the :func:`roots` function, substitute those roots for `z` in `g` and add
resulting values together.

Let's consider the following polynomial and rational function::

    >>> f = z**5 + z + 3
    >>> f
     5
    z  + z + 3

    >>> g = 1/z
    >>> g
    1
    ─
    z

Following the trivial approach, let's compute the roots of `f`::

    >>> roots(f)
    {}

We got a very unfortunate result: no roots! By the fundamental theorem
of algebra we should get five, possibly complex, roots, including
multiplicities. Unfortunately, there is no way to express roots in terms
of radicals of some polynomials of degree five and higher. For certain
instances of polynomials of this kind it may be possible to compute
their roots (e.g. :func:`roots` recognizes cyclotomic polynomials of
high degree), but in general we will most likely be unlucky.

Instead, we could switch to numerical root finding algorithms and compute
approximations of roots of `f` and proceed with summation of roots. This
can be done by using :func:`nroots`::

    >>> R = nroots(f)

    >>> for ri, r in zip(numbered_symbols('r'), R):
    ...     pprint(Eq(ri, r))
    ...
    r₀ = -1.13299756588507
    r₁ = -0.47538075666955 - 1.12970172509541⋅ⅈ
    r₂ = -0.47538075666955 + 1.12970172509541⋅ⅈ
    r₃ = 1.04187953961208 - 0.822870338109958⋅ⅈ
    r₄ = 1.04187953961208 + 0.822870338109958⋅ⅈ

We can substitute those roots for `z` in `g` and add together::

    >>> sum([ g.subs(z, r) for r in R ]).evalf(chop=True)
    -0.333333333333332

It was necessary to evaluate this sum with :func:`evalf`, because otherwise
we would get an unsimplified result. The additional parameter ``chop=True`` was
necessary to remove a tiny and insignificant imaginary part. Next we can use
:func:`nsimplify` to get an exact result from numerical approximation::

    >>> nsimplify(_)
    -1/3

Is this result correct? The best way is to figure out a purely symbolic
method that doesn't require computing roots of `f`. In SymPy it possible
to represent a root of a univariate polynomial with rational coefficients
using :class:`RootOf`::

    >>> RootOf(f, 0)
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 0⎠

    >>> _.evalf()
    -1.13299756588507

We can obtain all roots using list comprehensions::

    >>> R = [ RootOf(f, i) for i in xrange(degree(f)) ]

    >>> for r in R:
    ...     pprint(r)
    ...
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 0⎠
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 1⎠
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 2⎠
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 3⎠
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 4⎠

Alternatively we can use ``Poly(f).all_roots()`` which gives the same
result, but is much faster when `f` is a composite polynomial, because
the preprocessing step in :class:`RootOf` is executed only once.

Unfortunately we can't get anywhere from here, because SymPy is not yet
capable of simplifying expressions with :class:`RootOf`::

    >>> G = sum([ g.subs(z, r) for r in R ])
    >>> isinstance(G, Add)
    True

    >>> _ = simplify(G)
    >>> isinstance(_, Add)
    True

We can, however, evaluate sums of :class:`RootOf`'s using :func:`evalf`::

    >>> G.evalf()
    -0.333333333333333

    >>> nsimplify(_)
    -1/3

which gave us the same result as before. The difference is that now numerical
approximations of roots of `f` were computed using a hybrid symbolic--numeric
method, where first disjoint isolating intervals (rectangles) where computed
for all roots of `f` and then a numerical root finding algorithm was used in
each interval.

Let's approach this problem differently, using a purely symbolic
approach. We know that a polynomial of degree `n` has exactly `n`
complex roots, counting multiplicities. In our case `f` has five roots::

    >>> R = var('r:5')
    >>> R
    (r₀, r₁, r₂, r₃, r₄)

Let's now substitute those "roots" for `z` in `g`::

    >>> [ g.subs(z, r) for r in R ]
    ⎡1   1   1   1   1 ⎤
    ⎢──, ──, ──, ──, ──⎥
    ⎣r₀  r₁  r₂  r₃  r₄⎦

and add those expressions together::

    >>> sum(_)
    1    1    1    1    1
    ── + ── + ── + ── + ──
    r₄   r₃   r₂   r₁   r₀

We got a sum of simple rational functions. The next step is to put those
rational functions over a common denominator::

    >>> G = together(_)
    >>> G
    r₀⋅r₁⋅r₂⋅r₃ + r₀⋅r₁⋅r₂⋅r₄ + r₀⋅r₁⋅r₃⋅r₄ + r₀⋅r₂⋅r₃⋅r₄ + r₁⋅r₂⋅r₃⋅r₄
    ───────────────────────────────────────────────────────────────────
                               r₀⋅r₁⋅r₂⋅r₃⋅r₄

We got very peculiar numerator and denominator, which are very specific
functions of roots of `f` (symmetric polynomials). Polynomials of this
kind can be generated using :func:`viete`::

    >>> V = viete(f, R, z)

    >>> for lhs, rhs in V:
    ....     pprint(Eq(lhs, rhs))
    ....
    r₀ + r₁ + r₂ + r₃ + r₄ = 0
    r₀⋅r₁ + r₀⋅r₂ + r₀⋅r₃ + r₀⋅r₄ + r₁⋅r₂ + r₁⋅r₃ + r₁⋅r₄ + r₂⋅r₃ + r₂⋅r₄ + r₃⋅r₄ = 0
    r₀⋅r₁⋅r₂ + r₀⋅r₁⋅r₃ + r₀⋅r₁⋅r₄ + r₀⋅r₂⋅r₃ + r₀⋅r₂⋅r₄ + r₀⋅r₃⋅r₄ + r₁⋅r₂⋅r₃ + r₁⋅r₂⋅r₄ + r₁⋅r₃⋅r₄ + r₂⋅r₃⋅r₄ = 0
    r₀⋅r₁⋅r₂⋅r₃ + r₀⋅r₁⋅r₂⋅r₄ + r₀⋅r₁⋅r₃⋅r₄ + r₀⋅r₂⋅r₃⋅r₄ + r₁⋅r₂⋅r₃⋅r₄ = 1
    r₀⋅r₁⋅r₂⋅r₃⋅r₄ = -3

Viete formulas show the relationship between roots of a polynomial and
its coefficients:

.. math::

    V_{i-1} = (-1)^i \frac{a_{n-i}}{a_n}

where `f(z)=a_nz^n + a_{n-1}z^{n-1} + \ldots + a_1z + a_0` and `i = 1 \ldots n`. To obtain the final
result it sufficient to take `V_3` and `V_4` and substitute in `G`::

    >>> numer(G).subs(*V[3])/denom(G).subs(*V[4])
    -1/3

Or we could simply use ``G.subs(V)``, but due to a bug in SymPy (`#2552 <http://code.google.com/p/sympy/issues/detail?id=2552>`_) this
doesn't work as expected, leaving the denominator unchanged.

We obtained the same result as before, just this time using purely symbolic
techniques. This simple procedure can be extended to form an algorithm for
solving the root summation problem in the general setup. SymPy implements this
algorithm in :class:`RootSum`::

    >>> RootSum(f, Lambda(z, g))
    -1/3

The choice of `g` allowed us to recognize Viete formulas very easily in
`G`, but is this the case also for more complicated rational functions?
Let's modify `g` a little::

    >>> g = 1/(z + 2)
      1
    ─────
    z + 2

Now let's repeat the procedure for the new `g`::

    >>> G = together(sum([ g.subs(z, r) for r in R ]))

    >>> p = expand(numer(G))
    >>> q = expand(denom(G))

    >>> p
    r₀⋅r₁⋅r₂⋅r₃ + r₀⋅r₁⋅r₂⋅r₄ + 4⋅r₀⋅r₁⋅r₂ + r₀⋅r₁⋅r₃⋅r₄ + 4⋅r₀⋅r₁⋅r₃ + 4⋅r₀⋅r₁⋅r₄ + 12⋅r₀⋅r₁ + r₀⋅r₂⋅r₃⋅r₄ + \
    4⋅r₀⋅r₂⋅r₃ + 4⋅r₀⋅r₂⋅r₄ + 12⋅r₀⋅r₂ + 4⋅r₀⋅r₃⋅r₄ + 12⋅r₀⋅r₃ + 12⋅r₀⋅r₄ + 32⋅r₀ + r₁⋅r₂⋅r₃⋅r₄ + 4⋅r₁⋅r₂⋅r₃ + \
    4⋅r₁⋅r₂⋅r₄ + 12⋅r₁⋅r₂ + 4⋅r₁⋅r₃⋅r₄ + 12⋅r₁⋅r₃ + 12⋅r₁⋅r₄ + 32⋅r₁ + 4⋅r₂⋅r₃⋅r₄ + 12⋅r₂⋅r₃ + 12⋅r₂⋅r₄ + 32⋅r₂ + \
    12⋅r₃⋅r₄ + 32⋅r₃ + 32⋅r₄ + 80

    >>> q
    r₀⋅r₁⋅r₂⋅r₃⋅r₄ + 2⋅r₀⋅r₁⋅r₂⋅r₃ + 2⋅r₀⋅r₁⋅r₂⋅r₄ + 4⋅r₀⋅r₁⋅r₂ + 2⋅r₀⋅r₁⋅r₃⋅r₄ + 4⋅r₀⋅r₁⋅r₃ + 4⋅r₀⋅r₁⋅r₄ + \
    8⋅r₀⋅r₁ + 2⋅r₀⋅r₂⋅r₃⋅r₄ + 4⋅r₀⋅r₂⋅r₃ + 4⋅r₀⋅r₂⋅r₄ + 8⋅r₀⋅r₂ + 4⋅r₀⋅r₃⋅r₄ + 8⋅r₀⋅r₃ + 8⋅r₀⋅r₄ + 16⋅r₀ + \
    2⋅r₁⋅r₂⋅r₃⋅r₄ + 4⋅r₁⋅r₂⋅r₃ + 4⋅r₁⋅r₂⋅r₄ + 8⋅r₁⋅r₂ + 4⋅r₁⋅r₃⋅r₄ + 8⋅r₁⋅r₃ + 8⋅r₁⋅r₄ + 16⋅r₁ + 4⋅r₂⋅r₃⋅r₄ + \
    8⋅r₂⋅r₃ + 8⋅r₂⋅r₄ + 16⋅r₂ + 8⋅r₃⋅r₄ + 16⋅r₃ + 16⋅r₄ + 32

This doesn't look that familiar anymore. Let's try to apply Viete formulas
to the numerator and denominator::

    >>> p.subs(V).has(*R)
    True
    >>> q.subs(V).has(*R)
    True

We weren't able to get rid of the symbolic roots of `f`. We can, however, try
to rewrite `p` and `q` as polynomials in elementary symmetric polynomials.
This procedure is called symmetric reduction, and an algorithm for this is
implemented in :func:`symmetrize`::

    >>> (P, Q), mapping = symmetrize((p, q), R, formal=True)

    >>> P
    (32⋅s₁ + 12⋅s₂ + 4⋅s₃ + s₄ + 80, 0)
    >>> Q
    (16⋅s₁ + 8⋅s₂ + 4⋅s₃ + 2⋅s₄ + s₅ + 32, 0)

    >>> for s, poly in mapping:
    ...     pprint(Eq(s, poly))
    ...
    s₁ = r₀ + r₁ + r₂ + r₃ + r₄
    s₂ = r₀⋅r₁ + r₀⋅r₂ + r₀⋅r₃ + r₀⋅r₄ + r₁⋅r₂ + r₁⋅r₃ + r₁⋅r₄ + r₂⋅r₃ + r₂⋅r₄ + r₃⋅r₄
    s₃ = r₀⋅r₁⋅r₂ + r₀⋅r₁⋅r₃ + r₀⋅r₁⋅r₄ + r₀⋅r₂⋅r₃ + r₀⋅r₂⋅r₄ + r₀⋅r₃⋅r₄ + r₁⋅r₂⋅r₃ + r₁⋅r₂⋅r₄ + r₁⋅r₃⋅r₄ + r₂⋅r₃⋅r₄
    s₄ = r₀⋅r₁⋅r₂⋅r₃ + r₀⋅r₁⋅r₂⋅r₄ + r₀⋅r₁⋅r₃⋅r₄ + r₀⋅r₂⋅r₃⋅r₄ + r₁⋅r₂⋅r₃⋅r₄
    s₅ = r₀⋅r₁⋅r₂⋅r₃⋅r₄

Here we performed the formal simultaneous symmetric reduction of the polynomials `p`
and `q`, obtaining their representation in terms of elementary symmetric
polynomials, non-symmetric remainders, and elementary symmetric polynomials.
Remainders are always zero for symmetric inputs.

We can zip this mapping and Viete formulas together, obtaining::

    >>> [ (s, c) for (s, _), (_, c) in zip(mapping, V) ]
    [(s₁, 0), (s₂, 0), (s₃, 0), (s₄, 1), (s₅, -3)]

Now we can take head of ``P`` and ``Q`` and perform substitution::

    >>> P[0].subs(_)/Q[0].subs(_)
    81
    ──
    31

Let's verify this result using :class:`RootSum`::

    >>> RootSum(f, Lambda(z, g))
    81
    ──
    31

The numerical approach also works in this case::

    >>> sum([ g.subs(z, r) for r in Poly(f).all_roots() ]).evalf()
    2.61290322580645

    >>> nsimplify(_)
    81
    ──
    31

Tasks
-----

1. Repeat this procedure for:

 * `f = z^5 + z + a` and `g = \frac{1}{z + 1}`
 * `f = z^5 + z + a` and `g = \frac{1}{z + b}`

2. Can this or a similar procedure be used with other classes of expressions
   than rational functions? If so, what kind of expressions can be allowed?

.. _groebner-bases:

Applications of |groebner| bases
================================

The |groebner| bases method is an attractive tool in computer algebra and
symbolic mathematics because it is relatively simple to understand and it
can be applied to a wide variety of problems in mathematics and engineering.

Let's consider a set `F` of multivariate polynomial equations over a field:

.. math::

    F = \{ f \in \mathrm{K}[x_1, \ldots, x_n] \}

A |groebner| basis `G` of `F` with respect to a fixed ordering of monomials
is another set of polynomial equations with certain *nice* properties that
depend on the choice of the order of monomials and variables. `G` will be
structurally different from `F`, but has exactly the same set of solutions.

The |groebner| bases theory tells us that:

#. problems that are difficult to solve using `F` are *easier* to solve using `G`
#. there exists an *algorithm* for computing `G` for arbitrary `F`

We will take advantage of this and in the following subsections we will solve
two interesting problems in graph theory and algebraic geometry by formulating
those problems as systems of polynomial equations, computing |groebner| bases,
and reading solutions from them.

Vertex `k`--coloring of graphs
------------------------------

Given a graph `\mathcal{G}(V, E)`, where `V` is the set of vertices and `E`
is the set of edges of `\mathcal{G}`, and a positive integer `k`, we ask if
it is possible to assign a color to every vertex from `V`, such that adjacent
vertices have different colors assigned. Moreover, if graph `\mathcal{G}` is
`k`--colorable, we would like to enumerate all possible `k`--colorings this
graph.

We will solve this problem using the |groebner| bases method. First of all, we
have to transform this graph--theoretical definition of `k`--coloring problem
into a form that is understandable by the |groebner| bases machinery. This means
we have to construct a system of polynomial equations that embeds the structure
of a graph and constraints related to the `k`--coloring problem.

We start by assigning a variable to each vertex. Given that `\mathcal{G}` has
`n` vertices, i.e. `|V| = n`, then we will introduce variables `x_1, \ldots,
x_n`. Next we will write a set of equations describing the fact that we allow
assignment of one of `k` possible colors to each vertex. The best approach
currently known is to map colors to the `k`--th roots of unity, which are the
solutions to the equation `x^k - 1 = 0`.

Let `\zeta = \exp(\frac{2\pi\mathrm{i}}{k})` be a `k`--th root of unity.
We map the colors `1, \ldots, k` to `1, \zeta, \ldots, \zeta^{k-1}`.
Then the statement that every vertex has to be assigned one of `k`
colors is equivalent to writing the following set of polynomial
equations:

.. math::

    F_k = \{ x_i^k - 1 = 0 : i = 1, 2, \ldots, n \}

We also require that two adjacent vertices `x_i` and `x_j` are assigned different
colors. From the previous discussion we know that `x_i^k = 1` and `x_j^k = 1`, so
`x_i^k = x_j^k` or, equivalently, `x_i^k - x_j^k = 0`. By factorization we obtain
that:

.. math::

    x_i^k - x_j^k = (x_i - x_j) \cdot f(x_i, x_j) = 0

where `f(x_i, x_j)` is a bivariate polynomial of degree `k-1` in both variables.
Since we require that `x_i \not= x_j` then `x_i^k - x_j^k` can vanish only when
`f(x_i, x_j) = 0`. This allows us to write another set of polynomial equations:

.. math::

    F_{\mathcal{G}} = \{ f(x_i, x_j) = 0 : (i, j) \in E \}

Next we combine `F_k` and `F_{\mathcal{G}}` into one system of equations `F`. The
graph `\mathcal{G}(V, E)` is `k`-colorable if the |groebner| basis `G` of `F` is
non-trivial, i.e., `G \not= \{1\}`. If this is not the case, then the graph isn't
`k`--colorable. Otherwise the |groebner| basis gives us information about all
possible `k`--colorings of `\mathcal{G}`.

Let's now focus on a particular `k`--coloring where `k = 3`. In this case:

.. math::

    F_3 = \{ x_i^3 - 1 : i = 1, \ldots, n \}

Using SymPy's built--in multivariate polynomial factorization routine::

    >>> var('xi, xj')
    (xi, xj)

    >>> factor(xi**3 - xj**3)
              ⎛  2             2⎞
    (xi - xj)⋅⎝xi  + xi⋅xj + xj ⎠

we derive the set of equations `F_{\mathcal{G}}` describing an admissible
`3`--coloring of a graph:

.. math::

    F_{\mathcal{G}} = \{ x_i^2 + x_i x_j + x_j^2 : (i, j) \in E \}

At this point it is sufficient to compute the |groebner| basis `G` of
`F = F_3 \cup F_{\mathcal{G}}` to find out if a graph `\mathcal{G}` is
`3`--colorable, or not.

Let's see how this procedure works for a particular graph:

.. tikz:: source/img/tikz/graph-nocolor.tex

.. _fig-graph-nocolor:
.. figure:: img/tikz/graph-nocolor.*
    :align: center

    The graph `\mathcal{G}(V, E)`.

`\mathcal{G}(V, E)` has 12 vertices and 23 edges. We ask if the graph is
`3`--colorable. Let's first encode `V` and `E` using Python's built--in
data structures::

    >>> V = range(1, 12+1)
    >>> E = [(1,2),(2,3),(1,4),(1,6),(1,12),(2,5),(2,7),(3,8),
    ... (3,10),(4,11),(4,9),(5,6),(6,7),(7,8),(8,9),(9,10),
    ... (10,11),(11,12),(5,12),(5,9),(6,10),(7,11),(8,12)]

We encoded the set of vertices as a list of consecutive integers and the
set of edges as a list of tuples of adjacent vertex indices. Next we will
transform the graph into an algebraic form by mapping vertices to variables
and tuples of indices in tuples of variables::

    >>> V = [ var('x%d' % i) for i in V ]
    >>> E = [ (V[i-1], V[j-1]) for i, j in E ]

As the last step of this construction we write equations for `F_3` and
`F_{\mathcal{G}}`::

    >>> F3 = [ xi**3 - 1 for xi in V ]
    >>> Fg = [ xi**2 + xi*xj + xj**2 for xi, xj in E ]

Everything is set following the theoretical introduction, so now we can
compute the |groebner| basis of `F_3 \cup F_{\mathcal{G}}` with respect
to *lexicographic* ordering of terms::

    >>> G = groebner(F3 + Fg, *V, order='lex')

We know that if the constructed system of polynomial equations has a solution
then `G` should be non--trivial, which can be easily verified::

    >>> G != [1]
    True

The answer is that the graph `\mathcal{G}` is `3`--colorable. A sample coloring
is shown on the following figure:

.. tikz:: source/img/tikz/graph-color.tex

.. _fig-graph-color:
.. figure:: img/tikz/graph-color.*
    :align: center

    A sample `3`--coloring of the graph `\mathcal{G}(V, E)`.

Suppose we add an edge between vertices `i = 3` and `j = 4`. Is the new graph
still `3`--colorable? To check this it is sufficient to construct `F_{\mathcal{G'}}`
by extending `F_{\mathcal{G}}` with `x_3^2 + x_3 x_4 + x_4^2` and recomputing the
|groebner| basis::

    >>> groebner(F3 + Fg + [x3**2 + x3*x4 + x4**2], *V, order='lex')
    [1]

We got the trivial |groebner| basis as the result, so the graph `\mathcal{G'}`
isn't `3`--colorable. We could continue this discussion and ask, for example,
if the original graph `\mathcal{G}` can be colored with only two colors. To
achieve this, we would have to construct `F_2` and `F_{\mathcal{G}}`
and recompute the basis.

Let's return to the original graph. We already know that it is `3`--colorable,
but now we would like to enumerate all colorings. We will start from revising
properties of roots of unity. Let's construct the `k`--th root of unity, where
`k = 3`, in algebraic number form::

    >>> zeta = exp(2*pi*I/3).expand(complex=True)

    >>> zeta
            ⎽⎽⎽
      1   ╲╱ 3 ⋅ⅈ
    - ─ + ───────
      2      2

Altogether we consider three roots of unity in this example::

    >>> zeta**0
    1
    >>> zeta**1
            ⎽⎽⎽
      1   ╲╱ 3 ⋅ⅈ
    - ─ + ───────
      2      2
    >>> expand(zeta**2)
            ⎽⎽⎽
      1   ╲╱ 3 ⋅ⅈ
    - ─ - ───────
      2      2

Just to be extra cautious, let's check if `\zeta^3` gives `1`::

    >>> expand(zeta**3)
    1

Alternatively, we could obtain all `k`--th roots of unity by factorization
of `x^3 - 1` over an algebraic number field or by computing its roots via
radicals::

    >>> factor(x**3 - 1, extension=zeta)
            ⎛          ⎽⎽⎽  ⎞ ⎛          ⎽⎽⎽  ⎞
            ⎜    1   ╲╱ 3 ⋅ⅈ⎟ ⎜    1   ╲╱ 3 ⋅ⅈ⎟
    (x - 1)⋅⎜x + ─ - ───────⎟⋅⎜x + ─ + ───────⎟
            ⎝    2      2   ⎠ ⎝    2      2   ⎠

    >>> roots(x**3 - 1, multiple=True)
    ⎡           ⎽⎽⎽            ⎽⎽⎽  ⎤
    ⎢     1   ╲╱ 3 ⋅ⅈ    1   ╲╱ 3 ⋅ⅈ⎥
    ⎢1, - ─ - ───────, - ─ + ───────⎥
    ⎣     2      2       2      2   ⎦

We can visualize roots of `x^3 - 1` with a little help from mpmath and matplotlib:

.. plot::
    :align: center

    import matplotlib.pyplot as plt
    from sympy.mpmath import cplot

    fig = plt.figure()
    axes = fig.add_subplot(111)
    axes.set_title(r"Density plot of $z^3 - 1$ in the complex plane.")

    cplot(lambda z: z**3 - 1, re=[-2, 2], im=[-2, 2], axes=axes)

Going one step ahead, let's declare three variables which will nicely represent
colors in the `3`--coloring problem and let's put together, in an arbitrary but
fixed order, those variables and the previously computed roots of unity::

    >>> var('red,green,blue')
    (red, green, blue)

    >>> colors = zip(__, _)
    >>> colors

    ⎡          ⎛        ⎽⎽⎽         ⎞  ⎛        ⎽⎽⎽        ⎞⎤
    ⎢          ⎜  1   ╲╱ 3 ⋅ⅈ       ⎟  ⎜  1   ╲╱ 3 ⋅ⅈ      ⎟⎥
    ⎢(1, red), ⎜- ─ - ───────, green⎟, ⎜- ─ + ───────, blue⎟⎥
    ⎣          ⎝  2      2          ⎠  ⎝  2      2         ⎠⎦

This gives as a mapping between algebra of `3`--coloring problem and a nice
visual representation, which we will take advantage of later.

Let's look at `G`::

    >>> key = lambda f: (degree(f), len(f.args))
    >>> groups = sorted(sift(G, key).items(), reverse=True)

    >>> for _, group in groups:
    ...     pprint(group)
    ...
    ⎡   3    ⎤
    ⎣x₁₂  - 1⎦
    ⎡   2                2⎤
    ⎣x₁₁  + x₁₁⋅x₁₂ + x₁₂ ⎦
    [x₁ + x₁₁ + x₁₂, x₁₁ + x₁₂ + x₅, x₁₁ + x₁₂ + x₈, x₁₀ + x₁₁ + x₁₂]
    [-x₁₁ + x₂, -x₁₂ + x₃, -x₁₂ + x₄, -x₁₁ + x₆, -x₁₂ + x₇, -x₁₁ + x₉]

Here we split the basis into four groups with respect to the total degree
and length of polynomials. Treating all those polynomials as equations of
the form `f = 0`, we can solve them one--by--one, to obtain all colorings
of `\mathcal{G}`.

From the previous discussion we know that `x_{12}^3 - 1 = 0` has three solutions
in terms of roots of unity::

    >>> f = x12**3 - 1

    >>> f.subs(x12, zeta**0).expand()
    0
    >>> f.subs(x12, zeta**1).expand()
    0
    >>> f.subs(x12, zeta**2).expand()
    0

This also tells us that `x_{12}` can have any of the three colors assigned.
Next, the equation `x_{11}^2 + x_{11} x_{12} + x_{12}^2 = 0` relates colors
of `x_{11}` and `x_{12}`, and vanishes only when `x_{11} \not= x_{12}`::

    >>> f = x11**2 + x11*x12 + x12**2

    >>> f.subs({x11: zeta**0, x12: zeta**1}).expand()
    0
    >>> f.subs({x11: zeta**0, x12: zeta**2}).expand()
    0
    >>> f.subs({x11: zeta**1, x12: zeta**2}).expand()
    0

but::

    >>> f.subs({x11: zeta**0, x12: zeta**0}).expand() == 0
    False
    >>> f.subs({x11: zeta**1, x12: zeta**1}).expand() == 0
    False
    >>> f.subs({x11: zeta**2, x12: zeta**2}).expand() == 0
    False

This means that, when `x_{12}` is assigned a color, there are two possible
color assignments to `x_{11}`. Equations in the third group vanish only when
all three vertices of that particular equation have different colors assigned. This
follows from the fact that the sum of roots of unity vanishes::

    >>> expand(zeta**0 + zeta**1 + zeta**2)
    0

but (for example)::

    >>> expand(zeta**1 + zeta**1 + zeta**2) == 0
    False

Finally, equations in the last group are trivial and vanish when vertices of
each particular equation have the same color assigned. This gives us `3 \cdot 2
\cdot 1 \cdot 1 = 6` combinations of color assignments, i.e. there are six
solutions to `3`--coloring problem of graph `\mathcal{G}`.

Based on this analysis it is straightforward to enumerate all six color
assignments, however we can make this process fully automatic. Let's solve
the |groebner| basis `G`::

    >>> colorings = solve(G, *V)

    >>> len(colorings)
    6

This confirms that there are six solutions. At this point we could simply
print the computed solutions to see what are the admissible `3`--colorings.
This is, however, not a good idea, because we use algebraic numbers (roots
of unity) for representing colors and :func:`solve` returned solutions in
terms of those algebraic numbers, possibly even in a non--simplified form.

To overcome this difficulty we will use previously defined mapping between
roots of unity and literal colors and substitute symbols for numbers::

    >>> for coloring in colorings:
    ...     print [ color.expand(complex=True).subs(colors) for color in coloring ]
    ...
    [blue, green, red, red, blue, green, red, blue, green, blue, green, red]
    [green, blue, red, red, green, blue, red, green, blue, green, blue, red]
    [green, red, blue, blue, green, red, blue, green, red, green, red, blue]
    [blue, red, green, green, blue, red, green, blue, red, blue, red, green]
    [red, blue, green, green, red, blue, green, red, blue, red, blue, green]
    [red, green, blue, blue, red, green, blue, red, green, red, green, blue]

This is the result we were looking for, but a few words of explanation
are needed. :func:`solve` may return unsimplified results so we may need
to simplify any algebraic numbers that don't match structurally the
precomputed roots of unity. Taking advantage of the domain of
computation, we use the complex expansion algorithm for this purpose
(``expand(complex=True)``). Once we have the solutions in this canonical
form, to get this nice *visual* form with literal colors it is
sufficient to substitute color variables for roots of unity.

Tasks
~~~~~

1. Instead of computing |groebner| basis of `F`, simply solve it using
   :func:`solve`. Can you enumerate color assignments this way? If so, why?
2. Use this procedure to check if:

   * the graph with 12 vertices and 23 edges is `2`--colorable.
   * the graph with 12 vertices and 24 edges is `4`--colorable.

Algebraic geometry
------------------

Let's consider a geometric entity (e.g. line, square), whose properties can
be described using a system of `m` polynomials:

.. math::

    \mathcal{H} = \{h_1, \ldots, h_m\}

We will call `\mathcal{H}` a hypothesis. Given a theorem concerning this
geometric entity, the algebraic formulation is as follows:

.. math::

    \forall_{x_1, \ldots, x_n, y_1, \ldots, y_n} (h_1 = 0 \vee \ldots \vee h_m = 0) \Rightarrow g = 0

where `g` is the conclusion of the theorem and `h_1, \ldots h_m` and `g`
are polynomials in `\mathrm{K}[x_1, \ldots, x_n, y_1, \ldots, y_n]`. It
follows from the |groebner| bases theory that the above statement is true
when `g` belongs to the ideal generated by `\mathcal{H}`. To check this,
i.e. to prove the theorem, it is sufficient to compute a |groebner| basis
of `\mathcal{H}` with respect to any admissible monomial ordering and
reduce `g` with respect to this basis. If the theorem is true then the
remainder from the reduction will vanish. In this example, for the sake
of simplicity, we assume that the geometric entity is non--degenerate,
i.e. it does not collapse into a line or a point.

Let's consider the following rhombus:

.. tikz:: source/img/tikz/geometry-rhombus.tex

.. _fig-geometry-rhombus:
.. figure:: img/tikz/geometry-rhombus.*
    :align: center

    A rhombus in a fixed coordinate system.

This geometric entity consists of four points `A`, `B`, `C` and `D`. To
setup a fixed coordinate system, without loss of generality, we can assume
that `A = (0, 0)`, `B = (x_B, 0)`, `C = (x_C, y_C)` and `D = (x_D, y_D)`.
This is possible by taking rotational invariance of the geometric entity.
We will prove that the diagonals of this rhombus, i.e. `AD` and `BC` are
mutually perpendicular. We have the following conditions describing `ABCD`:

#. Line `AD` is parallel to `BC`, i.e. `AD \parallel BC`.
#. Sides of `ABCD` are of the equal length, i.e. `AB = BC`.
#. The rhombus is non--degenerate, i.e. is not a line or a point.

Our conclusion is that `AC \bot BD`. To prove this theorem, first we need to
transform the above conditions and the conclusion into a set of polynomials.
How we can achieve this? Let's focus on the first condition. In general, we
are given two lines `A_1A_2` and `B_1B_2`. To express the relation between
those two lines, i.e. that `A_1A_2` is parallel `B_1B_2`, we can relate
slopes of those lines:

.. math::

    \frac{y_{A_2} - y_{A_1}}{x_{A_2} - x_{A_1}} = \frac{y_{B_2} - y_{B_1}}{x_{B_2} - x_{B_1}}

Clearing denominators in the above expression and putting all terms on the
left hand side of the equation, we derive a general polynomial describing the
first condition. This can be literally translated into Python::

    def parallel(A1, A2, B1, B2):
        """Line [A1, A2] is parallel to line [B1, B2]. """
        return (A2.y - A1.y)*(B2.x - B1.x) - (B2.y - B1.y)*(A2.x - A1.x)

assuming that ``A1``, ``A2``, ``B1`` and ``B2`` are instances of :class:`Point`
class. In the case of our rhombus, we will take advantage of the fixed coordinate
system and simplify the resulting polynomials as much as possible. The same
approach can be used to derive polynomial representation of the other conditions
and the conclusion. To construct `\mathcal{H}` and `g` we will use the following
functions::

    def distance(A1, A2):
        """The squared distance between points A1 and A2. """
        return (A2.x - A1.x)**2 + (A2.y - A1.y)**2

    def equal(A1, A2, B1, B2):
        """Lines [A1, A2] and [B1, B2] are of the same width. """
        return distance(A1, A2) - distance(B1, B2)

    def perpendicular(A1, A2, B1, B2):
        """Line [A1, A2] is perpendicular to line [B1, B2]. """
        return (A2.x - A1.x)*(B2.x - B1.x) + (A2.y - A1.y)*(B2.y - B1.y)

The non--degeneracy statement requires a few words of comment. Many theorems
in geometry are true only in the non--degenerative case and false or undefined
otherwise. In our approach to theorem proving in algebraic geometry, we must
supply sufficient non--degeneracy conditions manually. In the case of our
rhombus this is `x_B > 0` and `y_C > 0` (we don't need to take `x_C` into
account because `AB = BC`). At first, this seems to be a show stopper, as
|groebner| bases don't support inequalities. However, we can use Rabinovich's
trick and transform those inequalities into a single polynomial condition by
introducing an additional variable, e.g. `a`, about which we will assume that
is positive. This gives us a non--degeneracy condition `x_B y_C - a`.

With all this knowledge we are ready to prove the main theorem. First, let's
declare variables::

    >>> var('x_B, x_C, y_C, x_D, a')
    (x_B, x_C, y_C, x_D, a)

    >>> V = _[:-1]

We declared the additional variable `a`, but we don't consider it a variable
of our problem. Let's now define the four points `A`, `B`, `C` and `D`::

    >>> A = Point(0, 0)
    >>> B = Point(x_B, 0)
    >>> C = Point(x_C, y_C)
    >>> D = Point(x_D, y_C)

Using the previously defined functions we can formulate the hypothesis::

    >>> h1 = parallel(A, D, B, C)
    >>> h2 = equal(A, B, B, C)
    >>> h3 = x_B*y_C - a

and compute its |groebner| basis::

    >>> G = groebner([f1, h2, h3], *V, order='grlex')

We had to specify the variables of the problem explicitly in
:func:`groebner`, because otherwise it would treat `a` also as a
variable, which we don't want. Now we can verify the theorem::

    >>> reduced(perpendicular(A, C, B, D), G, *V, order='grlex')[1]
    0

The remainder vanished, which proves that `AC \bot BD`. Although, the theorem
we described and proved here is a simple one, one can handle much more advanced
problems as well using |groebner| bases techniques. One should refer to Franz
Winkler's papers for more advanced examples.

Tasks
~~~~~

1. The |groebner| bases method is a generalization of Gaussian elimination
   and Euclid's algorithms. Try to solve a linear system and compute GCD
   of polynomials using :func:`groebner`. Compare the results and speed of
   computations with :func:`solve` and :func:`gcd`.
