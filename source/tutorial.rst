
.. |groebner| replace:: Gröbner

=====================
Introduction to SymPy
=====================

SymPy (http://www.sympy.org) is a pure Python library for symbolic mathematics.
It aims to become a full-featured computer algebra system (CAS) while keeping the
code as simple as possible in order to be comprehensible and easily extensible.
SymPy is written entirely in Python and does not require any external libraries.

In this tutorial we will introduce attendees to SymPy. We will start by showing
how to install and configure this Python module. Then we will proceed to the
basics of constructing and manipulating mathematical expressions in SymPy. We
will also discuss the most common issues and differences from other computer
algebra systems, and how to deal with them. In the last part of this tutorial
we will show how to solve simple, yet illustrative, mathematical problems with
SymPy.

This knowledge should be enough for attendees to start using SymPy for solving
mathematical problems and hacking SymPy's internals (though hacking core modules
may require additional expertise).

Installing, configuring and running SymPy
=========================================

SymPy in Python/IPython
-----------------------

Sessions in standard Python's interpreter and IPython look very similar,
for example:

.. sourcecode:: ipython

    $ ipython

    In [1]: import sympy

    In [2]: x = sympy.Symbol('x')

    In [3]: sympy.integrate(3*x**2)
    Out[3]: x**3

    In [4]: sympy.init_printing()

    In [5]: sympy.integrate(3*x**2)
    Out[5]:
     3
    x

Interactive SymPy (``isympy``)
------------------------------

For users' convenience, SymPy's distribution includes a simple shell script called
isympy that uses either IPython (if available) or standard Python's interpreter
with readline support (see ``bin/isympy``). On startup isympy enables new
division, imports everything from :mod:`sympy`, sets up a few commonly used
symbols and undefined functions, and initializes the pretty printer.

Here is an example session with isympy:

.. sourcecode:: ipython

    sympy$ bin/isympy
    IPython console for SymPy 0.7.0 (Python 2.6.6-64-bit) (ground types: gmpy)

    These commands were executed:
    >>> from __future__ import division
    >>> from sympy import *
    >>> x, y, z, t = symbols('x y z t')
    >>> k, m, n = symbols('k m n', integer=True)
    >>> f, g, h = symbols('f g h', cls=Function)

    Documentation can be found at http://www.sympy.org

    In [1]: integrate(3*x**2, x)
    Out[1]:
     3
    x

    In [2]: %quit
    Do you really want to exit ([y]/n)? y
    Exiting ...
    sympy $

Command-line arguments
~~~~~~~~~~~~~~~~~~~~~~

There are a variety of command-line options supported by isympy:

``-h``, ``--help``
    show help
``-c CONSOLE``, ``--console=CONSOLE``
    select type of interactive session: ``ipython``, ``python``. Default is ``ipython`` if IPython is installed, otherwise, ``python``.
``-p PRETTY``, ``--pretty=PRETTY``
    setup pretty printing: ``unicode``, ``ascii`` or ``no``. Default is ``unicode`` if the terminal supports it, otherwise, ``ascii``.
``-t TYPES``, ``--types=TYPES``
    setup ground types: ``gmpy``, ``python`` or ``sympy``. Default is ``gmpy`` if it's installed, otherwise ``python``.
``-o ORDER``, ``--order=ORDER``
    setup ordering of terms: ``[rev-]lex``, ``[rev-]grlex``, ``[rev-]grevlex`` or ``old``. Default is ``lex``.
``-q``, ``--quiet``
    print only version information at startup
``-C``, ``--no-cache``
    disable caching

Environment variables
-----------------------

``SYMPY_USE_CACHE``
    By default SymPy caches all computations. If this is undesirable, for
    example due to limited amount of memory, set this variable to ``no``
    to disable caching. Note that some operations will run much slower with
    the cache off.
``SYMPY_GROUND_TYPES``
    SymPy is a pure Python library, however to improve the speed of computations
    it can take advantage of third-party compiled libraries (for now only gmpy).
    Ground types are set automatically, so if gmpy is not available, it simply
    won't be used. However, if gmpy is available but for some reason it is
    undesirable to use it, set this variable to ``python``, to disable usage
    of gmpy.

SymPy in web browsers
---------------------

SymPy is available in the following web applications:

* SymPy Live (http://live.sympy.org)
* Sage Notebook (http://www.sagenb.org)
* FEMhub Online Lab (http://lab.femhub.org)

Gotchas and pitfalls
====================

SymPy is being written in and runs under `Python <http://www.python.org/>`_,
a general purpose programming language, so there are a few things that may
be quite different from what can be experienced in other symbolic mathematics
or computer algebra systems like Maple or Mathematica. These are some of the
gotchas and pitfalls that you may encounter when using SymPy.

``1/3`` is not a rational number
--------------------------------

Users of classical symbolic mathematics systems like Maple or Mathematica,
are accustomed to typing ``1/3`` and get the rational number one over three. In
SymPy this gives either ``0`` or a floating point number, depending on whether
we use old or new division. This is considered most disturbing difference
between SymPy and other mathematical systems.

First, this strange behavior comes from the fact that Python is a
general purpose programming language  and for a very long time it didn't
have support for rational numbers in the standard library. This changed
in Python 2.6, where the :class:`Fraction` class was introduced, but it would
be anyway unusual for Python to make ``/`` return a rational number.

To construct a rational number in SymPy, one can use :class:`Rational`
class::

    >>> r = Rational(1, 3)
    >>> r
    1/3

    >>> type(r)
    <class 'sympy.core.numbers.Rational'>

    >>> int(r)
    0
    >>> float(r)
    0.333333333333

    >>> r.evalf()
    0.333333333333333

There are also other ways::

    >>> Integer(1)/3
    1/3
    >>> S(1)/3
    1/3

``S`` is SymPy's registry of singletons. It implements the ``__call__`` method,
which is a shorthand for :func:`sympify`. Using ``S`` is the most concise
way to construct rational numbers. The last way is to pass a string with
``1/3`` to :func:`sympify`::

    >>> sympify("1/3")
    1/3
    >>> type(_)
    <class 'sympy.core.numbers.Rational'>

:func:`sympify` implements a :mod:`tokenize`--based preparser that puts
Python's numeric types in envelopes consisting of SymPy's numeric class
constructors.

You can also avoid this problem by not typing ``int/int`` when other
terms are involved. For example, write ``2*x/3`` instead of ``2/3*x``.
And you can type ``sqrt(x)`` instead of ``x**Rational(1, 2)``, as the
two are equivalent.

``^`` is not exponentiation operator
------------------------------------

SymPy uses the same default arithmetic operators as Python. Most of these,
like ``+``, ``-``, ``*`` and ``/``, are standard. There are, however, some
differences when comparing SymPy to standalone mathematical systems. One
of the differences is lack of implied multiplication, to which Mathematica
users may be accustomed::

    >>> var('x')

    >>> 2*x
    2*x

    >>> 2x
    Traceback (most recent call last):
    ...
    SyntaxError: invalid syntax

    >>> 2 x
    Traceback (most recent call last):
    ...
    SyntaxError: invalid syntax

More importantly, Python uses ``**`` to denote exponentiation, whereas
other mathematical systems use ``^`` operator. Notable exceptions to
this rule are Axiom and Maple, which allow both, though most users may
not be aware of this. For example in Mathematica, ``**`` operator is
used for non-commutative multiplication. So in Sympy the following
expression is perfectly valid::

    >>> (x + 1)**2
           2
    (x + 1)

    >>> type(_)
    <class 'sympy.core.power.Pow'>

but using ``^``::

    >>> (x + 1)^2
    Traceback (most recent call last):
    ...
    TypeError: unsupported operand type(s) for ^: 'Add' and 'int'

gives use :exc:`TypeError`. For users' convenience, :func:`sympify` converts
``^`` to ``**`` by default in a string::

    >>> sympify("(x + 1)^2")
           2
    (x + 1)

    >>> type(_)
    <class 'sympy.core.power.Pow'>

People who what pure Python behaviour of :func:`sympify` can disable this
automatic conversion by passing ``convert_xor=False`` to it.

Why you shouldn't write ``10**-1000``
-------------------------------------

Symbolic mathematics systems are expected to work with expressions of
arbitrary size, limited only by the size of available memory. Python
supports arbitrary precision integers by default, but allows only fixed
precision floats. Thus you can write::

    >>> 10**-10
    1e-10

but::

    >>> 10**-1000
    0.0

is not what we expect. To overcome this, we have to make the base an
instance of SymPy's floating point type::

    >>> Float(10.0)**-1000
    1.00000000000000e-1000

Note that we can't write simply ``Float(10)``, because SymPy automatically
converts this to an instance of :class:`Integer` class and thus::

    >>> type(Float(10)**-1000)
    <class 'sympy.core.numbers.Rational'>

Of course we could issue::

    >>> (Float(10)**-1000).evalf()
    1.00000000000000e-1000

but this it is neither readable, nor efficient.

You can also pass the entire number as a string to :class:`Float`. If you
do this, you must use the scientific notation syntax::

    >>> Float("1e-1000")
    1.00000000000000e-1000

Finally, we note that it is preferable to use exact (i.e., rational)
numbers when the values of the numbers are exactly known. Many parts of
SymPy work better when rational numbers are used instead of floating
point numbers. This is because rational numbers do not suffer from some
of the problems of floating point numbers, like rounding errors.

This is especially the case for exponents::

    >>> factor(x**2.0 - 1)
    x**2.0 - 1

    >>> factor(x**2 - 1)
    (x - 1)*(x + 1)

The first expression is not factored because the factorization only
holds for the exponent of `2` *exactly*. This problem can also come
up when using floating point coefficients::

    >>> solve([2*x + y**2, y - x], [x, y])
    [(-2, -2), (0, 0)]

    >>> solve([2.0*x + y**2, y - x], [x, y])
    Traceback (most recent call last):
    ...
    DomainError: can't compute a Groebner basis over RR

Here, the algorithm for solving systems of polynomial equations relies
on computing a |groebner| basis (see the :ref:`groebner-bases` section
below for more information on these). But the algorithm for computing
this currently does not support floating point coefficients, so
:func:`solve` fails in that case.

How to deal with limited recursion depth
----------------------------------------

Very often algorithms in symbolic mathematics and computer algebra are
highly recursive in nature. This can be a problem even for relatively
small inputs in SymPy, because Python interpreters set a limit on the
depth of recursion. Suppose we want to compute, manipulate and print the
following function composition:

.. math::

    \underbrace{(f \circ f \circ \ldots \circ f)}_{1000}(x)

Computing this isn't a problem::

    >>> f = Function('f')
    >>> x = Symbol('x')

    >>> u = x

    >>> for i in xrange(1000):
    ...     u = f(x)
    ...

    >>> type(u)
    f

However, if we try to get the number of all subexpressions of ``u`` that
contain ``f``, we get the following error::

    >>> len(u.find(f))
    Traceback (most recent call last):
    ...
    RuntimeError: maximum recursion depth exceeded while calling a Python object

The same happens when we try to print ``u``::

    >>> len([ c for c in str(u) if c == 'f' ])
    Traceback (most recent call last):
    ...
    RuntimeError: maximum recursion depth exceeded while calling a Python object

Python provides, at least partially, a solution to this problem by
allowing the user to relax the limit on recursion depth::

    >>> import sys
    >>> sys.setrecursionlimit(1050)

    >>> len(u.find(f))
    1000

To print ``u`` we have to relax the limit even more::

    >>> len([ c for c in str(u) if c == 'f' ])
    Traceback (most recent call last):
    ...
    RuntimeError: maximum recursion depth exceeded while calling a Python object

    >>> sys.setrecursionlimit(5500)

    >>> len([ c for c in str(u) if c == 'f' ])
    1000

This should be a warning about the fact that often it is possible to
perform computations with highly nested expressions, but it is not
possible to print those expressions without relaxing the recursion depth
limit. SymPy never uses ``sys.setrecursionlimit`` automatically, so
it's users responsibility to relax the limit whenever needed.

Unless you are using a highly nested expression like the one above, you
generally won't encounter this problem, as the default limit of 1000 is
generally high enough for the most common expressions.

Expression caching and its consequences
---------------------------------------

To improve speed of computations, SymPy by default caches all intermediate
subexpressions. The difference is easily visible when running tests::

    $ SYMPY_USE_CACHE=yes bin/test sympy/integrals/tests/test_risch.py
    ============================= test process starts ==============================
    executable:   /usr/bin/python2.6  (2.6.6-final-0)
    architecture: 64-bit
    ground types: gmpy

    sympy/integrals/tests/test_risch.py[20] .....ffff...........                [OK]

    ======= tests finished: 16 passed, 4 expected to fail, in 28.18 seconds ========

    $ SYMPY_USE_CACHE=no bin/test sympy/integrals/tests/test_risch.py
    ============================= test process starts ==============================
    executable:   /usr/bin/python2.6  (2.6.6-final-0)
    architecture: 64-bit
    ground types: gmpy

    sympy/integrals/tests/test_risch.py[20] .....ffff...........                [OK]

    ======= tests finished: 16 passed, 4 expected to fail, in 64.82 seconds ========

(note the time needed to run the tests at the end of the each test run)
and in interactive sessions:

.. sourcecode:: ipython

    $ bin/isympy -q
    IPython console for SymPy 0.7.0-git (Python 2.6.6-64-bit) (ground types: gmpy)

    In [1]: f = (x-tan(x)) / tan(x)**2 + tan(x)

    In [2]: %time integrate(f, x);
    CPU times: user 0.46 s, sys: 0.00 s, total: 0.46 s
    Wall time: 0.49 s

    In [4]: %time integrate(f, x);
    CPU times: user 0.24 s, sys: 0.00 s, total: 0.24 s
    Wall time: 0.25 s

    $ bin/isympy -q -C
    IPython console for SymPy 0.7.0-git (Python 2.6.6-64-bit) (ground types: gmpy, cache: off)

    In [1]: f = (x-tan(x)) / tan(x)**2 + tan(x)

    In [2]: %time integrate(f, x);
    CPU times: user 1.82 s, sys: 0.00 s, total: 1.82 s
    Wall time: 1.84 s

    In [4]: %time integrate(f, x);
    CPU times: user 1.82 s, sys: 0.00 s, total: 1.82 s
    Wall time: 1.83 s

(``-C`` is equivalent to setting ``SYMPY_USE_CACHE="no"``).

The main consequence of caching is that SymPy can use a lot of resources
in certain situations. One can use :func:`clear_cache` to reduce memory
consumption:

.. sourcecode:: ipython

    In [6]: from sympy.core.cache import clear_cache

    In [7]: clear_cache()

    In [8]: %time integrate(f, x);
    CPU times: user 0.46 s, sys: 0.00 s, total: 0.46 s
    Wall time: 0.47 s

As caching influences computation times, any benchmarking must be performed
with cache off. Otherwise those measurements will be either inaccurate or
completely wrong (measuring how fast SymPy can retrieve data from cache,
rather than actual computing times):

.. sourcecode:: ipython

    $ bin/isympy -q
    IPython console for SymPy 0.7.0-git (Python 2.6.6-64-bit) (ground types: gmpy)

    In [1]: %timeit sin(2*pi);
    10000 loops, best of 3: 28.7 us per loop

    $ bin/isympy -q -C
    IPython console for SymPy 0.7.0-git (Python 2.6.6-64-bit) (ground types: gmpy, cache: off)

    In [1]: %timeit sin(2*pi);
    100 loops, best of 3: 2.75 ms per loop

The difference between using and not using cache is two orders of magnitude.

Naming convention of trigonometric inverses
-------------------------------------------

SymPy uses different names than most computer algebra systems for some
of the commonly used elementary functions. In particular, the inverse
trigonometric and hyperbolic functions use Python's naming convention,
so we have :func:`asin`, :func:`asinh`, :func:`acos` and so on, instead
of :func:`arcsin`, :func:`arcsinh`, :func:`arccos`, etc.

Container indices start at zero
-------------------------------

It should be obvious for people using Python, even for beginners, that when
indexing containers like ``list`` or ``tuple``, indexes start at zero, not
one::

    >>> L = symbols('x:5')
    >>> L
    (x₀, x₁, x₂, x₃, x₄)

    >>> L[0]
    x₀
    >>> L[1]
    x₁

This is a common thing in general purpose programming languages. However,
most symbolic mathematics systems, especially those which invent their own
mathematical programming language, use `1`--based indexing, sometimes reserving
the `0`--th index for special purpose (e.g. head of expressions in Mathematica).

Setting up and using printers
=============================

Computations are at the heart of symbolic mathematics systems, but very
often presentation and visualization of results or intermediate steps
is also very important, for example for sharing results. SymPy implements
a very generic and flexible framework for implementing printers of
mathematical expressions, Python's data types and date structures, and
foreign types.

Built-in printers
-----------------

There are many ways how expressions can be printed in Sympy.

Standard
~~~~~~~~

This is what ``str(expression)`` returns and it looks like this::

    >>> print x**2
    x**2
    >>> print 1/x
    1/x
    >>> print Integral(x**2, x)
    Integral(x**2, x)

Note that :func:`str` is by design not aware of global configuration,
so if you for example run ``bin/isympy -o grlex``, :func:`str` will
ignore this. There is another function :func:`sstr` that take global
configuration into account.

Low-level
~~~~~~~~~

Due to internal implementation of Python, SymPy can't use :func:`repr`
for generating low-level textual representation of expressions. To get
this kind of representation, :func:`srepr` was invented::

    >>> srepr(x**2)
    Pow(Symbol('x'), Integer(2))

    >>> srepr(1/x)
    Pow(Symbol('x'), Integer(-1))

    >>> srepr(Integral(x**2, x))
    Integral(Pow(Symbol('x'), Integer(2)), Tuple(Symbol('x')))

:func:`repr` gives the same result as :func:`str`::

    >>> repr(x**2)
    x**2

Note that :func:`repr` is also not aware of global configuration.

Pretty printing
~~~~~~~~~~~~~~~

This is a nice 2D ASCII-art printing produced by :func:`pprint`::

    >>> pprint(x**2, use_unicode=False)
     2
    x
    >>> pprint(1/x, use_unicode=False)
    1
    -
    x
    >>> pprint(Integral(x**2, x), use_unicde=False)
      /
     |
     |  2
     | x  dx
     |
    /

It also has support for Unicode character set, which makes shapes look
much more natural than in ASCII case::

    >>> pprint(Integral(x**2, x), use_unicode=True)
    ⌠
    ⎮  2
    ⎮ x  dx
    ⌡

By default :func:`pprint` tries to figure out the best of Unicode and
ASCII art for generating output. If Unicode is supported, then this will
be the default. Otherwise it falls back to ASCII art. User can select
desired character set by setting ``use_unicode`` option in :func:`pprint`.

Python printing
~~~~~~~~~~~~~~~

::

    >>> print python(x**2)
    x = Symbol('x')
    e = x**2
    >>> print python(1/x)
    x = Symbol('x')
    e = 1/x
    >>> print python(Integral(x**2, x))
    x = Symbol('x')
    e = Integral(x**2, x)


LaTeX printing
~~~~~~~~~~~~~~

::

    >>> latex(x**2)
    x^{2}
    >>> latex(x**2, mode='inline')
    $x^{2}$
    >>> latex(x**2, mode='equation')
    \begin{equation}x^{2}\end{equation}
    >>> latex(x**2, mode='equation*')
    \begin{equation*}x^{2}\end{equation*}
    >>> latex(1/x)
    \frac{1}{x}
    >>> latex(Integral(x**2, x))
    \int x^{2}\,dx
    >>>

MathML printing
~~~~~~~~~~~~~~~

::

    >>> from sympy.printing.mathml import mathml
    >>> from sympy import Integral, latex
    >>> from sympy.abc import x
    >>> print mathml(x**2)
    <apply><power/><ci>x</ci><cn>2</cn></apply>
    >>> print mathml(1/x)
    <apply><power/><ci>x</ci><cn>-1</cn></apply>

Printing with Pyglet
~~~~~~~~~~~~~~~~~~~~

This allows for printing expressions in a separate GUI window. Issue::

    >>> preview(x**2 + Integral(x**2, x) + 1/x)

and a Pyglet window with the LaTeX rendered expression will popup:

.. image:: _static/preview-pyglet.png

Setting up printers
-------------------

By default SymPy uses :func:`str`/:func:`sstr` printer. Other printers can
be used explicitly as in examples in subsections above. This is efficient
only when printing at most a few times with a non-standard printer. To make
Python use a different printer than the default one, the typical approach
is to modify ``sys.displayhook``::

    >>> 1/x
    1/x

    >>> import sys
    >>> oldhook = sys.displayhook
    >>> sys.displayhook = pprint

    >>> 1/x
    1
    ─
    x

    >>> sys.displayhook = oldhook

Alternatively one can use SymPy's function :func:`init_printing`. This works
only for pretty printer, but is the fastest way to setup this type of printer.

Customizing built-in printers
-----------------------------

Suppose we dislike how certain classes of expressions are printed. One such
issue may be pretty printing of polynomials (instances of :class:`Poly` class),
in which case :class:`PrettyPrinter` simply doesn't have support for printing
polynomials and falls back to :class:`StrPrinter`::

    >>> Poly(x**2 + 1)
    Poly(x**2 + 1, x, domain='ZZ')

One way to add support for pretty printing polynomials is to extend pretty
printer's class and implement ``_print_Poly`` method. We would choose this
approach if we wanted this to be a permanent change in SymPy. We will choose
a different way and subclass :class:`PrettyPrinter` and implement ``_print_Poly``
in the new class.

Let's call the new pretty printer :class:`PolyPrettyPrinter`. It's implementation
looks like this:

.. literalinclude:: python/pretty_poly.py

Using :func:`pretty_poly` allows us to print polynomials in 2D and Unicode::

    >>> pretty_poly(Poly(x**2 + 1))
        ⎛ 2          ⎞
    Poly⎝x  + 1, x, ℤ⎠

We can use techniques from previous section to make this new pretty printer
the default for all inputs.

Implementing printers from scratch
----------------------------------

SymPy implements a variety of printers and often extending those existent
may be sufficient, to optimize them for certain problem domain or specific
mathematical notation. However, we can also add completely new ones, for
example to allow printing SymPy's expression with other symbolic mathematics
systems' syntax.

Suppose we would like to translate SymPy's expressions to Mathematica syntax.
As of version 0.7.0, SymPy doesn't implement such a printer, so we get do it
right now. Adding a new printer basically boils down to adding a new class,
let's say :class:`MathematicaPrinter`, which derives from :class:`Printer`
and implements ``_print_*`` methods for all kinds of expressions we want to
support. In this particular example we would like to be able to translate:

* numbers
* symbols
* functions
* exponentiation

and compositions of all of those. A prototype implementation is as follows:

.. literalinclude:: python/mathematica.py

Before we explain this code, let's see what it can do::

    >>> mathematica(S(1)/2)
    1/2
    >>> mathematica(x)
    x

    >>> mathematica(x**2)
    x^2

    >>> mathematica(f(x))
    f[x]
    >>> mathematica(sin(x))
    Sin[x]
    >>> mathematica(asin(x))
    ArcSin[x]

    >>> mathematica(sin(x**2))
    Sin[x^2]
    >>> mathematica(sin(x**(S(1)/2)))
    Sin[x^(1/2)]

However, as we didn't include support for :class:`Add`, this doesn't work::

    >>> mathematica(x**2 + 1)
    x**2 + 1

and very many other classes of expressions are printed improperly. If we
need support for a particular class, we have to add another ``_print_*``
method to :class:`MathematicaPrinter``. For example, to make the above
example work, we have to implement ``_print_Add``.

Code generation
---------------

Besides printing of mathematical expressions, SymPy also implements Fortran
and C code generation. The simplest way to proceed is to use :func:`codegen`
which takes a tuple consisting of function name and an expression, or a list
of tuples of this kind, language in which it will generate code (``C`` for
C programming language and ``F95`` for Fortran, and file name::

    >>> print codegen(("chebyshevt_20", chebyshevt(20, x)), "F95", "file")[0][1]
    !******************************************************************************
    !*                      Code generated with sympy 0.7.0                       *
    !*                                                                            *
    !*              See http://www.sympy.org/ for more information.               *
    !*                                                                            *
    !*                       This file is part of 'project'                       *
    !******************************************************************************

    REAL*8 function chebyshevt_20(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_20 = 524288*x**20 - 2621440*x**18 + 5570560*x**16 - 6553600*x &
          **14 + 4659200*x**12 - 2050048*x**10 + 549120*x**8 - 84480*x**6 + &
          6600*x**4 - 200*x**2 + 1

    end function

In this example we generated Fortran code for function ``chebyshevt_20`` which
allows use to evaluate Chebyshev polynomial of first kind of degree 20. Almost
the same way one can generate C code for this expression.

Tasks
-----

1. Make Mathematica printer correctly print `\pi`.
2. Add support for :class:`Add` and :class:`Mul` to Mathematica printer. In
   the case of products, allow both explicit and implied multiplication, and
   allow users to choose desired behavior by parametrization of Mathematica
   printer.
3. Generate C code for ``chebyshevt(20, x)``.
4. Make SymPy generate one file of Fortran or/and C code that contains
   definitions of functions that would allow us to evaluate each of the
   first ten Chebyshev polynomials of the first kind.

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

#. Repeat this procedure but expand wrt `a` in the first step.
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
   than rational functions? If so, what kind of expressions can be used?

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

    >>> reduced(perpendicular(A, C, B, D), G, vars, order='grlex')[1]
    0

The remainder vanished, which proves that `AC \bot BD`. Although, the theorem
we described and proved here is a simple one, one can handle much more advanced
problems as well using |groebner| bases techniques. One should refer to Franz
Winkler's papers for more interesting examples.

Tasks
-----

#. The |groebner| bases method is a generalization of Gaussian elimination
   and Euclid's algorithms. Try to solve a linear system and compute GCD
   of polynomials using :func:`groebner`. Compare the results and speed of
   computations with :func:`solve` and :func:`gcd`.
#. Check if the graph with 12 vertices and 23 edges is `2`--colorable.
#. In the graph coloring example solve `F` instead of computing its |groebner|
   basis. Can you enumerate color assignments this way? If so, why?
#. Recompute |groebner| bases from this section using different
   orderings of monomials (e.g. ``grlex`` instead of ``lex``) and check
   if the resulting bases are still useful in the context they were
   used. If they are, compare the time to compute the bases in the
   different orderings.
