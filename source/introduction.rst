
.. include:: definitions.def

=====================
Introduction to SymPy
=====================

SymPy (http://www.sympy.org) is a pure Python library for symbolic mathematics.
It aims to become a full-featured computer algebra system (CAS) while keeping the
code as simple as possible in order to be comprehensible and easily extensible.
SymPy is written entirely in Python and does not require any external libraries.

This tutorial gives an overview and introduction to SymPy. We will start by
showing how to install and configure SymPy. Then we will proceed to the basics
of constructing and manipulating mathematical expressions in SymPy. We will
also discuss the most common problems with SymPy and differences between it
and mathematical systems, and how to deal with them. In the last part of this
tutorial we will show how to solve simple, yet illustrative, mathematical
problems with SymPy.

This knowledge should be enough to start using SymPy in daily work and hacking
SymPy's internals (though hacking core modules may require additional expertise).

Installing, configuring and running SymPy
=========================================

The easiest way to get SymPy is to visit `this <http://code.google.com/p/sympy>`_
page and download the latest tarball from *Featured Downloads* section,
or use the following direct link::

    $ wget http://sympy.googlecode.com/files/sympy-0.7.0.tar.gz
    $ tar -xz -C sympy --strip-components 1 -f sympy-0.7.0.tar.gz

You will also find an installer for Windows there. An alternative way is to
clone SymPy's `git <http://www.git-scm.org>`_ repository from `GitHub <http://github.com/sympy/sympy>`_::

    $ git clone git://github.com/sympy/sympy.git

To use it, issue::

    $ cd sympy
    $ python
    Python 2.6.6 (r266:84292, Dec 28 2010, 00:22:44)
    [GCC 4.5.1] on linux2
    Type "help", "copyright", "credits" or "license" for more information.
    >>> from sympy import *
    >>> var('x')
    x
    >>> diff(sin(x), x)
    cos(x)

If you want SymPy to be available globally, you can install it using
``./setup.py install``. SymPy is available in major Linux distributions,
so you can install it also using package manager of your distribution
(for example in Ubuntu install ``python-sympy`` and in Gentoo install
``dev-python/sympy``).

By default, SymPy doesn't have any dependencies besides Python. The following
version of Python are supported: 2.4, 2.5, 2.6, 2.7. Python 3.x is not supported
yet, although there is undergoing work to make SymPy compatible with it. Also
release 0.7.0 of SymPy is the last one that supports Python 2.4. SymPy should
also work smoothly under Jython (IronPython and PyPy have problems with running
SymPy).

Certain features of SymPy may require additional dependencies. For example
:mod:`sympy.polys` module can take advantage of gmpy library for coefficient
arithmetics. However, if gmpy is not available, this module falls back to
pure Python implementation, so ``import sympy`` will work correctly without
gmpy being installed. Other dependencies include IPython, Matplotlib, NumPy,
SciPy, Cython, Pyglet, LaTeX distribution and more.

SymPy in Python/IPython
-----------------------

Sessions in standard Python's interpreter and IPython look very similar,
just the banner and prompt look differently, for example::

    $ python
    Python 2.6.6 (r266:84292, Dec 28 2010, 00:22:44)
    [GCC 4.5.1] on linux2
    >>> import sympy
    >>> x = sympy.Symbol('x')
    >>> sympy.integrate(3*x**2)
    x**3
    >>> sympy.init_printing()
    >>> sympy.integrate(3*x**2)
     3
    x

Interactive SymPy (``isympy``)
------------------------------

For users' convenience, SymPy's distribution includes a simple script called
isympy (see ``bin/isympy``). isympy uses either IPython (if available) or
standard Python's interpreter with readline support. On startup isympy sets
up the environment to make interaction with SymPy more pleasant. It enables
new division, imports everything from :mod:`sympy`, injects a few commonly
used symbols into the global namespace, and initializes the pretty printer.

Here is an example session with isympy:

.. sourcecode:: ipython

    sympy$ bin/isympy
    IPython console for SymPy 0.7.0 (Python 2.6.6) (ground types: gmpy)

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
    select type of interactive session: ``ipython``, ``python``. Default is
    ``ipython`` if IPython is installed, otherwise, ``python``.
``-p PRETTY``, ``--pretty=PRETTY``
    setup pretty printing: ``unicode``, ``ascii`` or ``no``. Default is ``unicode``
    if the terminal supports it, otherwise, ``ascii``.
``-t TYPES``, ``--types=TYPES``
    setup ground types: ``gmpy``, ``python`` or ``sympy``. Default is ``gmpy`` if
    it's installed, otherwise ``python``.
``-o ORDER``, ``--order=ORDER``
    setup ordering of terms: ``[rev-]lex``, ``[rev-]grlex``, ``[rev-]grevlex`` or
    ``old``. Default is ``lex``.
``-q``, ``--quiet``
    print only version information at startup
``-C``, ``--no-cache``
    disable caching

Environment variables
---------------------

``SYMPY_USE_CACHE``
    By default SymPy caches all computations. If this is undesirable, for
    example due to limited amount of memory, set this variable to ``no``
    to disable caching. Note that some operations will run much slower with
    the cache off. Setting this variable to ``no`` is equivalent to running
    isympy with ``-C`` option.
``SYMPY_GROUND_TYPES``
    SymPy is a pure Python library, however to improve the speed of computations
    it can take advantage of gmpy library to speedup coefficient arithmetics
    (also known as ground domain arithmetics). Ground types are set automatically,
    so if gmpy is not available, it simply won't be used. However, if gmpy is
    available but for some reason it is undesirable to use it, set this variable
    to ``python``, to disable usage of gmpy. Use ``-t`` or ``--type`` option to
    achieve the same in isympy.

Running the test suite
----------------------

To verify that SymPy works properly on your computer, you can run SymPy's
test suite. This is done either with ``bin/test`` command or :func:`test`
in an interactive session. For example, to test :mod:`sympy.core` issue::

    $ bin/test sympy/core
    ============================= test process starts ==============================
    executable:   /usr/bin/python2.6  (2.6.6-final-0)
    ground types: gmpy

    sympy/core/tests/test_arit.py[48] ...f..........................................
    ..                                                                          [OK]
    sympy/core/tests/test_assumptions.py[28] ............................       [OK]
    sympy/core/tests/test_basic.py[10] ..........                               [OK]
    sympy/core/tests/test_cache.py[1] .                                         [OK]
    sympy/core/tests/test_complex.py[13] .............                          [OK]
    sympy/core/tests/test_containers.py[5] .....                                [OK]
    sympy/core/tests/test_count_ops.py[2] ..                                    [OK]
    sympy/core/tests/test_diff.py[6] ......                                     [OK]
    sympy/core/tests/test_equal.py[6] ......                                    [OK]
    sympy/core/tests/test_eval.py[8] .....f..                                   [OK]
    sympy/core/tests/test_eval_power.py[13] .............                       [OK]
    sympy/core/tests/test_evalf.py[24] ........................                 [OK]
    sympy/core/tests/test_expand.py[6] ......                                   [OK]
    sympy/core/tests/test_expr.py[59] ..............................................
    .............                                                               [OK]
    sympy/core/tests/test_exprtools.py[4] ....                                  [OK]
    sympy/core/tests/test_facts.py[11] ...........                              [OK]
    sympy/core/tests/test_functions.py[27] .....fff...................          [OK]
    sympy/core/tests/test_logic.py[11] ...........                              [OK]
    sympy/core/tests/test_match.py[26] ...f......................               [OK]
    sympy/core/tests/test_numbers.py[46] ...........................................
    ...                                                                         [OK]
    sympy/core/tests/test_operations.py[4] ....                                 [OK]
    sympy/core/tests/test_priority.py[5] .....                                  [OK]
    sympy/core/tests/test_relational.py[7] .......                              [OK]
    sympy/core/tests/test_sets.py[18] ..................                        [OK]
    sympy/core/tests/test_subs.py[30] ..............................            [OK]
    sympy/core/tests/test_symbol.py[9] ....X....                                [OK]
    sympy/core/tests/test_sympify.py[26] ...f......................             [OK]
    sympy/core/tests/test_truediv.py[3] ...                                     [OK]
    sympy/core/tests/test_var.py[5] .....                                       [OK]

    ________________________________ xpassed tests _________________________________
    sympy/core/tests/test_symbol.py:

    tests finished: 453 passed, 7 expected to fail, 1 expected to fail but passed,
    in 6.30 seconds

This tells us that all standard tests in :mod:`sympy.core`'s  pass (dots).
In case of failure, ``.`` would change to ``F`` and ``OK`` to ``FAIL``
(additionally all failures would be colored in red and listed at the end of
output from SymPy's test utility). Non-standard tests are those marked with
``f`` and ``X`` characters. The former means that the test was supposed to
fail and failed (XFAIL), whereas the later means that the test was supposed
to fail but passed (XPASS).

To run the whole test suite issue ``bin/test`` or :func:`test` without any
arguments. Running the whole test suite takes more than ten minutes on
Pentium-M 1.6 GHz and less than 5 minutes on Xeon 3.0 GHz (one core).

There is another test utility in SymPy, ``bin/doctest``, which verifies
examples in docstrings and documentation. If you are going to contribute
to SymPy, make sure you run both ``bin/test`` and ``bin/doctest`` before
submitting a `pull request <http://help.github.com/send-pull-requests>`_.

SymPy in web browsers
---------------------

SymPy is available in the following web applications:

* SymPy Live (http://live.sympy.org)
* Sage Notebook (http://www.sagenb.org)
* FEMhub Online Lab (http://lab.femhub.org)

SymPy Live was developed specifically for SymPy. It is a simple web shell
that looks similar to isympy under standard Python's interpreter. SymPy
Live uses Google App Engine as computational backend.

Basics of expressions in SymPy
==============================

SymPy is all about construction and manipulation of *expressions*. By the
term expression we mean mathematical expressions represented in the Python
language using SymPy's classes and objects. Expressions may consist of
symbols, numbers, functions and function applications (and many other) and
operators binding them together (addiction, subtraction, multiplication,
division, exponentiation).

Suppose we want to construct an expression for `x + 1`::

    >>> x = Symbol('x')

    >>> x + 1
    x + 1

    >>> type(_)
    <class 'sympy.core.add.Add'>

Entering ``x + 1`` gave us an instance of :class:`Add` class. This expression
consists of a symbol (``x``), a number (``1``) and addition operator, which
is represented by the topmost class (:class:`Add`). This was the simplest way
of entering an expression for `x + 1`. We could also enter::

    >>> y = Symbol('y')

    >>> x - y + 17 + y - 16 + sin(pi)
    x + 1

In this case SymPy automatically rewrote the input expression and gave its
canonical form, which is ``x + 1`` once again. This is a very important
behaviour: all expressions are subject to automatic evaluation, during which
SymPy tries to find a canonical form for expressions, but it doesn't apply
"heroic" measures to achieve this goal. For example the following expression::

    >>> (x**2 - 1)/(x - 1)
     2
    x  - 1
    ──────
    x - 1

is left unsimplified. This is because automatic canonicalization would
lose important information about this expression (`x \not= 1`). We can
use :func:`cancel` remove common factors from the numerator and the
denominator::

    >>> cancel(_)
    x + 1

SymPy never applies any transformations automatically that could cause
information loss or that would result in results that are valid only
almost everywhere. Consider the following expression::

    >>> log(x*y)
    log(x⋅y)

We know that `\log(x y)` is equivalent to `\log x + \log y` and there
is :func:`expand` that is supposed be able to do this::

    >>> expand(_)
    log(x⋅y)

Unfortunately nothing interesting happened. This is because the formula
stated above is not universally valid, e.g.::

    >>> log((-2)*(-3))
    log(6)
    >>> log(-2) + log(-3)
    log(2) + log(3) + 2⋅ⅈ⋅π

It is possible to ignore such cases and expand forcibly::

    >>> expand(log(x*y), force=True)
    log(x) + log(y)

Many other expression manipulation function also support ``force`` option.
Usually a better way is to assign additional knowledge with an expression::

    >>> var('a,b', positive=True)
    (a, b)

    >>> log(a*b)
    log(a⋅b)

    >>> expand(_)
    log(a) + log(b)

In this case ``force=True`` wasn't necessary, because we gave sufficient
information to :func:`expand` so that it was able to decide that the
expansion rule is valid universally for this expression.

Arithmetic operators
--------------------

Arithmetic operators ``+``, ``-``, ``*``, ``/``, ``**`` are mapped to
combinations of three core SymPy's classes: :class:`Add`, :class:`Mul`
and :class:`Pow`, and work the following way:

* ``x + y`` uses :class:`Add` class and ``__add__`` method::

    >>> x + y
    x + y
    >>> type(_)
    <class 'sympy.core.add.Add'>

    >>> x.__add__(y)
    x + y
    >>> type(_)
    <class 'sympy.core.add.Add'>

    >>> Add(x, y)
    x + y
    >>> type(_)
    <class 'sympy.core.add.Add'>

* ``x - y`` uses :class:`Add` and :class:`Mul` classes, and ``__sub__`` method::

    >>> x - y
    x - y
    >>> type(_)
    <class 'sympy.core.add.Add'>
    >>> __.args
    (-y, x)
    >>> type(_[0])
    <class 'sympy.core.mul.Mul'>

    >>> x.__sub__(y)
    x - y
    >>> type(_)
    <class 'sympy.core.add.Add'>
    >>> __.args
    (-y, x)
    >>> type(_[0])
    <class 'sympy.core.mul.Mul'>

    >>> Add(x, -y))
    x - y
    >>> type(_)
    <class 'sympy.core.add.Add'>
    >>> __.args
    (-y, x)
    >>> type(_[0])
    <class 'sympy.core.mul.Mul'>

* ``x*y`` uses :class:`Mul` class and ``__mul__`` method::

    >>> x*y
    x*y
    >>> type(_)
    <class 'sympy.core.mul.Mul'>

    >>> x.__mul__(y)
    x*y
    >>> type(_)
    <class 'sympy.core.mul.Mul'>

    >>> Mul(x, y)
    x*y
    >>> type(_)
    <class 'sympy.core.mul.Mul'>

* ``x/y`` uses :class:`Pow` and :class:`Mul` classes and ``__div__`` method::

    >>> x/y
    x
    ─
    y
    >>> type(_)
    <class 'sympy.core.mul.Mul'>
    >>> __.args
    ⎛   1⎞
    ⎜x, ─⎟
    ⎝   y⎠
    >>> type(_[1])
    <class 'sympy.core.pow.Pow'>

    >>> x.__div__(y)
    x
    ─
    y
    >>> type(_)
    <class 'sympy.core.mul.Mul'>
    >>> __.args
    ⎛   1⎞
    ⎜x, ─⎟
    ⎝   y⎠
    >>> type(_[1])
    <class 'sympy.core.pow.Pow'>

    >>> Mul(x, 1/y)
    x
    ─
    y
    >>> type(_)
    <class 'sympy.core.mul.Mul'>
    >>> __.args
    ⎛   1⎞
    ⎜x, ─⎟
    ⎝   y⎠
    >>> type(_[1])
    <class 'sympy.core.pow.Pow'>

* ``x**y`` uses :class:`Pow` class and ``__pow__`` method::

    >>> x**y
     y
    x
    >>> type(_)
    <class 'sympy.core.pow.Pow'>

    >>> x.__pow__(y)
     y
    x
    >>> type(_)
    <class 'sympy.core.pow.Pow'>

    >>> Pow(x, y)
     y
    x
    >>> type(_)
    <class 'sympy.core.pow.Pow'>

When the first argument is not an instance SymPy's class, e.g. as in ``1 - x``,
then Python falls back to ``__r*__`` methods, which are also implemented in all
SymPy's classes::

    >>> (1).__sub__(x)
    NotImplemented

    >>> x.__rsub__(1)
    -x + 1
    >>> 1 - x
    -x + 1

Tasks
~~~~~

1. Construct an expression for `1 + x + x^2 + \ldots + x^10`. Can you construct
   this expression in a different way? Write a function that could generate an
   expression for `1 + x + x^2 + \ldots + x^n` for any integer `n >= 0`. Extend
   this function to allow `n < 0`.

2. Write a function that can compute nested powers, e.g. `x^x`, `x^{x^x}` and
   so on. The function should take two parameters: an expression and a positive
   integer `n` that specifies the depth.

Building blocks of expressions
------------------------------

Expressions can consist of instances of subclasses of :class:`Expr` class. This
includes:

* numbers::

    >>> Integer(2)
    2
    >>> Rational(1, 2)
    1/2
    >>> Float("1e-1000")
    1.00000000000000e-1000

* symbols::

    >>> Symbol('x')
    x
    >>> Dummy('y')
    y

* numer symbols::

    >>> pi
    π
    >>> E
    ℯ
    >>> Catalan
    Catalan

* functions::

    >>> Function('f')
    f
    >>> sin
    sin
    >>> cos
    cos

* function applications::

    >>> Function('f')(x)
    f(x)
    >>> sin(x)
    sin(x)
    >>> cos(x)
    cos(x)

* operators::

    >>> Add(x, y, z)
    x + y + z
    >>> Mul(x, y, z)
    x⋅y⋅z
    >>> Pow(x, y)
     y
    x
    >>> Or(x, y, z)
    x ∨ y ∨ z
    >>> And(x, y, z)
    x ∧ y ∧ z

* "big" operators::

    >>> Derivative(1/x, x)
    d ⎛1⎞
    ──⎜─⎟
    dx⎝x⎠
    >>> Integral(1/x, x)
    ⌠
    ⎮ 1
    ⎮ ─ dx
    ⎮ x
    ⌡
    >>> Sum(1/k, (k, 1, n))
      n
     ___
     \  `
      \   1
       )  ─
      /   k
     /__,
    k = 1

* other::

    >>> Poly(x**2 + y, x)
    Poly(x**2 + y, x, domain='ZZ[y]')
    >>> RootOf(z**5 + z + 3, 2)
          ⎛ 5           ⎞
    RootOf⎝z  + z + 3, 2⎠

This list isn't at all complete and we included only few classes that SymPy
implements that can be used as expression building blocks. Besides those,
SymPy has also very many classes that represent entities that can't be used
for constructing expressions, but can be useful as containers of expressions
or as utilities for expression building blocks.

Tasks
~~~~~

1. Expressions implement :func:`doit` method. For most types expressions it
   doesn't do anything useful, but in case of "big" operators, it executes
   an action assigned to to a "big" operator (it differentiates, integrates,
   etc.). Take advantage of :func:`doit` and write a function that generates
   integral tables for a few polynomials, rational functions and elementary
   functions.

Foreign types in SymPy
----------------------

SymPy internally expects that all objects it works with are instances of
subclasses of :class:`Basic` class. So why ``x + 1`` works without raising
any exceptions? The number ``1`` is not a SymPy's type, but::

    >>> type(1)
    <type 'int'>

it's a built-in type. SymPy implements :func:`sympify` function for the task
of converting foreign types to SymPy's types (yes, Python's built-in types
are also considered as foreign). All SymPy's classes, methods and functions
use :func:`sympify` and this is the reason you can safely write ``x + 1``
instead of more verbose and less convenient ``x + Integer(1)``. Note that
not all functions return instances of SymPy's types. Usually, if a function
is supposed to return a property of an expression, it will use built-in
Python's types, e.g.::

    >>> Poly(x**2 + y).degree(y)
    1
    >>> type(_)
    <type 'int'>

Now see what :func:`sympify` can do. Let's start with built-ins::

    >>> sympify(1)
    1
    >>> type(_)
    <class 'sympy.core.numbers.One'>

    >>> sympify(117)
    117
    >>> type(_)
    <class 'sympy.core.numbers.Integer'>

    >>> sympify(0.5)
    0.500000000000000
    >>> type(_)
    <class 'sympy.core.numbers.Float'>

    >>> from fractions import Fraction

    >>> sympify(Fraction(1, 2))
    1/2
    >>> type(_)
    <class 'sympy.core.numbers.Rational'>

SymPy implements explicit sympification rules, heuristics based on ``__int__``,
``__float__`` and other attributes, and in the worst case scenario it falls
back to parsing string representation of an object. This usually works fine,
but sometimes :func:`sympify` can be wrong::

    >>> from gmpy import mpz, mpq

    >>> sympify(mpz(117))
    117.000000000000
    >>>> type(_)
    <class 'sympy.core.numbers.Float'>

    >>> sympify(mpq(1, 2))
    0.500000000000000
    >>>> type(_)
    <class 'sympy.core.numbers.Float'>

This happens because :func:`sympify` doesn't know about neither ``mpz`` nor
``mpq``, and it first looks for ``__float__`` attribute, which is implemented
by both those types. Getting float for exact value isn't very useful so let's
extend :func:`sympify` and add support for ``mpz``. The way to achieve this
is to add a new entry to ``converter`` dictionary. ``converter`` takes types
as keys and sympification functions as values. Before we extend this ``dict``,
we have to resolve a little problem with ``mpz``::

    >>> mpz
    <built-in function mpz>

which isn't a type but a function. We can use a little trick here and take
the type of some ``mpz`` object::

    >>> type(mpz(1))
    <type 'mpz'>

Let's now add an entry to ``converter`` for ``mpz``::

    >>> from sympy.core.sympify import converter

    >>> def mpz_to_Integer(obj):
    ...     return Integer(int(obj))
    ...
    ...

    >>> converter[type(mpz(1))] = mpz_to_Integer

We could use ``lambda`` as well. Now we can sympify ``mpz``::

    >>> sympify(mpz(117))
    117
    >>> type(_)
    <class 'sympy.core.numbers.Integer'

Similar thing should be done for ``mpq``. Let's try one more type::

    >>> import numpy

    >>> ar = numpy.array([1, 2, 3])
    >>> sympify(ar)

    >>> sympify(ar)
    Traceback (most recent call last):
    ...
    SympifyError: SympifyError: "could not parse u'[1 2 3]'"

:func:`sympify` isn't aware of ``numpy.ndarray`` and heuristics didn't work,
so it computed string representation of ``ar`` using :func:`str` and tried
to parse is, which failed because::

    >>> str(ar)
    [1 2 3]

We might be tempted to add support for ``numpy.ndarray`` to :func:`sympify`
by treating NumPy's arrays (at least a subset of) as SymPy's matrices, but
matrices aren't sympifiable::

    >>> Matrix(3, 3, lambda i, j: i + j)
    ⎡0  1  2⎤
    ⎢       ⎥
    ⎢1  2  3⎥
    ⎢       ⎥
    ⎣2  3  4⎦
    >>> sympify(_)
    Traceback (most recent call last):
    ...
    SympifyError: SympifyError: 'Matrix cannot be sympified'

We will explain this odd behavior later.

Tasks
~~~~~

1. Add support for ``mpq`` to :func:`sympify`.

2. SymPy implements :class:`Tuple` class, which provides functionality of
   Python's built-in ``tuple``, but is a subclass of :class:`Basic`. Take
   advantage of this and make :func:`sympify` work for 1D horizontal NumPy
   arrays, for which it should return instances of :class:`Tuple`. Raise
   :exc:`SympifyError` for other classes of arrays.

The role of symbols
-------------------

Let's now talk about the most important part of expressions: symbols. Symbols
are placeholders, abstract entities that can be filled in with whatever
content we want (unless there are explicit restrictions given). For example
in expression ``x + 1`` we have one symbol ``x``. Let's start fresh Python's
interpreter and issue::

    >>> from sympy import *
    >>> init_printing()

We want to start work with our very advanced ``x + 1`` expression, so we
may be tempted to simply write::

    >>> x + 1
    Traceback (most recent call last):
    ...
    NameError: name 'x' is not defined

For users that come from other symbolic mathematics systems, this behavior
may seem odd, because in those systems, symbols are constructed implicitly
when necessary. In general purpose programming language like Python, we
have to define all objects we want to use before we actually use them. So,
the first thing we have to always do is to construct symbols and assign
them to Python's variables::

    >>> x = Symbol('x')

    >>> x + 1
    x + 1

Now it worked. Symbols are independent of variables, so nothing prevents
you from issuing::

    >>> t = Symbol('a')

Well, besides taste. It's also perfectly valid to create symbols containing
special characters::

    >>> Symbol('+')
    +

``_`` and ``^`` characters in symbols have special meaning and are used to
denote subscripts and superscripts, respectively::

    >>> Symbol('x_1')
    x₁
    >>> Symbol('x^1')
    x¹

If you need more symbols in your expression, you have to define and assign
them all before using them. Later you can reuse existing symbols for other
purposes. To make life easier, SymPy provides several methods for constructing
symbols. The most low-level method is to use :class:`Symbol` class, as we
have been doing it before. However, if you need more symbols, then your can
use :func:`symbols`::

    >>> symbols('x,y,z')
    (x, y, z)

It takes a textual specification of symbols and returns a ``tuple`` with
constructed symbols. :func:`symbols` supports several syntaxes and can make
your life much simpler, when it comes to constructing symbols. First of all,
commas can be followed by or completely replaced by whitespace::

    >>> symbols('x, y, z')
    (x, y, z)
    >>> symbols('x y z')
    (x, y, z)

If you need indexed symbols, then use range syntax::

    >>> symbols("x:5")
    (x₀, x₁, x₂, x₃, x₄)
    >>> symbols('x5:10')
    (x₅, x₆, x₇, x₈, x₉)

You can also create consecutive symbols with lexicographic syntax::

    >>> symbols('a:d')
    (a, b, c, d)

Note that range syntax simulates :func:`range`'s behavior, so it is exclusive,
lexicographic syntax is inclusive, because it makes more sense in this case.

When we issue::

    >>> symbols('u,v')
    (u, v)

we may be tempted to use ``u`` and ``v``::

    >>> u
    Traceback (most recent call last):
    ...
    NameError: name 'u' is not defined

    >>> v
    Traceback (most recent call last):
    ...
    NameError: name 'v' is not defined

We got :exc:`NameError`, because we constructed those symbols, but we didn't
assign them to any variables. This solves the problem::

    >>> u, v = symbols('u,v')
    >>> u, v
    u, v

but is a little redundant, because we have to repeat the same information
twice. To save time and typing effort, SymPy has another function :func:`var`
for constructing symbols, which has exactly the same syntax and semantics
as :func:`symbols`, but it also injects constructed symbols into the global
namespace, making this function very useful in interactive sessions::

    >>> del u, v
    >>> var('u,v)
    (u, v)

    >>> u + v
    u + v

We don't allow to use :func:`var` in SymPy's library code. There is one
more way of constructing symbols, which is related to indexed symbols.
Sometimes we don't know in advance how many symbols will be required to
solve a certain problem. For this case, SymPy has :func:`numbered_symbols`
generator::

    >>> X = numbered_symbols('x')

    >>> X.next()
    x₀

    >>> [ X.next() for i in xrange(5) ]
    [x₁, x₂, x₃, x₄, x₅]

Tasks
~~~~~

1. Implement a function that would generate an expression for `x_1^1 +
   x_2^2 + \ldots + x_n^n`. This function would take two arguments: base
   name for indexed symbols and integer exponent `n >= 1`. What's the
   best approach among the four presented above?

Obtaining parts of expressions
------------------------------

We already know how to construct expressions, but how to get parts of complex
expressions? The most basic and low-level way of decomposing expressions is to
use ``args`` property::

    >>> x + y + 1
    x + y + 1
    >>> _.args
    (1, y, x)
    >>> map(type)
    [<class 'sympy.core.numbers.One'>, <class 'sympy.core.symbol.Symbol'>, <class 'sympy.core.symbol.Symbol'>]

``args`` always gives a ``tuple`` of instances of SymPy's classes. One should
notice the weird order of elements, which doesn't match printing order. This
happens for classes that in which order of arguments is insignificant. The
most notable examples of such class are :class:`Add` and :class:`Mul` (for
commutative part). In this particular case we can use :func:`as_ordered_terms`
method to get ``args`` in printing order::

    >>> (x + y + 1).as_ordered_terms()
    [x, y, 1]

When dealing which classes that have fixed order of arguments, printing
order and ``args`` order match::

    >>> Derivative(sin(x), x, x)
       2
      d
    ─────(sin(x))
    dx dx

    >>> _.args
    (sin(x), x, x)

Lets suppose that :class:`Cls` represents any SymPy's class and ``expr``
is an instance of this class (``expr = Cls()``). Then the following holds::

    Cls(*expr.args) == expr

This is very useful invariant, because we can easily decompose, modify and
rebuild expressions of various kinds in SymPy exactly the same way. This
invariant is being used in all functions that manipulation expressions.

Let's now use ``args`` to something a little more interesting than simple
decomposition of expressions. Working with expressions, one may be interested
in the depth of such expressions. By viewing expressions as n-ary trees, by
depth we understand the longest path in a tree.

Trees consist of branches and leafs. In SymPy, leafs of expressions are
instances of subclasses of :class:`Atom` class (numbers, symbols, special
constants)::

    >>> Integer(10)
    10
    >>> isinstance(_, Atom)
    True

    >>> pi
    π
    >>> isinstance(_, Atom)
    True

Atoms can be also recognized by the fact that their ``args`` are empty.
Note, however, that this is an implementation detail, and one should use
either :func:`isinstance` built-in function or `is_Atom` property to
recognize atoms properly. Everything else than an :class:`Atom` is a
branch.

Let's implement :func:`depth` function:

.. literalinclude:: python/depth.py

The implementation is straightforward. First we check if the input
expression is an atom. In this case we return ``1`` and terminate
recursion. Otherwise :func:`depth` recurses for every argument of
``expr`` and returns ``1`` plus maximum of depths of all branches.

Let's see :func:`depth` in action::

    >>> depth(x)
    1
    >>> depth(x + 1)
    2
    >>> depth(x + sin(x))
    3
    >>> depth(x + sin(x) + sin(cos(x)))
    4

All those examples work as expected. However, not everything is perfect
with this function. Let's look at the following phenomenon::

    >>> depth(Integer(117))
    1
    >>> depth(117)
    Traceback (most recent call last):
    ...
    AttributeError: 'int' object has no attribute 'args'

``117`` is an instance of Python's built-in type :class:`int`, but this type
is not a subclass of :class:`Atom`, so Python choses the other branch in
:func:`depth` and this must fail. Before the last example we pass only
instances of SymPy's expression to :func:`depth`. If we want :func:`depth` to
work also for non-SymPy types, we have to sympify ``expr`` with :func:`sympify`
before using it.

Tasks
~~~~~

1. Change :func:`depth` so that it sympifies its input argument. Rewrite
   :func:`depth` so that is calls :func:`sympify` only once.

2. Add support for iterable containers to :func:`depth`. Containers should
   be treated as branches and have depth defined the same way.

Immutability of expressions
---------------------------

Expressions in SymPy are immutable and cannot be modified by an in-place
operation. This means that a function will always return an object, and
the original expression will not be modified. Consider the following
code::

    >>> var('x,y,a,b')
    (x, y, a, b)

    >>> original = 3*x + 4*y
    >>> modified = original.subs({x: a, y: b})

    >>> original
    3*x + 4*y
    >>> modified
    3*a + 4*b

The output shows that the :func:`subs` method gave a new expression with
symbol ``x`` replaced with symbol ``a`` and symbol ``y`` replaced with
symbol ``b``. The original expression wasn't modified. This behaviour
applies to all classes that are subclasses of :class:`Basic`. An exception
to immutability rule is :class:`Matrix`, which allows in-place modifications,
but it is not a subclass of :class:`Basic`::

    >>> Matrix.mro()
    [<class 'sympy.matrices.matrices.Matrix'>, <type 'object'>]

Be also aware of the fact that SymPy's symbols aren't Python's variables (they
just can be assigned to Python's variables), so if you issue::

    >>> u = Symbol('u')
    >>> v = u
    >>> v += 1
    >>> v
    u + 1

then in-place operator ``+=`` constructed an new instance of :class:`Add` and
left the original expression stored in variable ``u`` unchanged::

    >>> u
    u

For efficiency reason, any in-place operator used on elements of a matrix,
modifies the matrix in-place and doesn't waste memory for unnecessary copies.

Tasks
~~~~~

1. This is the first time we used :func:`subs`. This is a very important method
   and we will talk more about it later. However, we can also use :func:`subs`
   to generate some cool looking expressions. Start with ``x**x`` expression
   and substitute in it ``x**x`` for ``x``. What do you get? (make sure you
   use pretty printer) Can you achieve the same effect without :func:`subs`?

Comparing expressions with ``==``
---------------------------------

Consider the following two expressions::

    >>> f = (x + 1)**2
    >>> f
           2
    (x + y)

    >>> g = x**2 + 2*x + 1
    >>> g
     2
    x  + 2⋅x + 1

We should remember from calculus 101 that those two expressions are
equivalent, because we can use binomial theorem to expand ``f`` and
we will get ``g``. However in SymPy::

    >>> f == g
    False

This is correct result, because SymPy implements structural understanding
of ``==`` operator, not semantic. So, for SymPy ``f`` and ``g`` are very
different expressions.

What to do if we have two variables and we want to know if their contents
are equivalent, but not necessarily structurally equal? There is no simple
answer to this question in general. In the particular case of ``f`` and
``g``, it is sufficient to issue::

    >>> expand(f) == expand(g)
    True

or, based on `f = g \equiv f - g = 0` equivalence::

    >>> expand(f - g) == 0
    True

In case of more complicated expression, e.g. those involving elementary or
special functions, this approach may be insufficient. For example::

    >>> u = sin(x)**2 - 1
    >>> v = cos(x)**2

    >>> u == v
    False
    >>> expand(u - v) == 0
    False

In this case we have to use more advanced term rewriting function::

    >>> simplify(u - v) == 0
    True

The meaning of expressions
--------------------------

Expressions don't have any meaning assigned to them by default. Thus `x + 1`
is simply an expression, not a function or a univariate polynomial. Meaning
is assigned when we use expressions in a context, e.g.::

    >>> div(x**2 - y, x - y)
    ⎛        2    ⎞
    ⎝x + y, y  - y⎠

In this case, ``x**2 - y`` and ``x - y`` where treated as multivariate
polynomials in variables ``x`` and ``y`` (in this order). We could change
this understanding and ask explicitly for polynomials in variables ``y``
and ``x``. This makes :func:`div` return a different result::

    >>> div(x**2 - y, x - y, y, x)
    ⎛    2    ⎞
    ⎝1, x  - x⎠

Quite often SymPy is capable of deriving the most useful understanding of
expressions in a given context. However, there are situations when expressions
simply don't carry enough information to make SymPy perform computations without
telling it explicitly what to do::

    >>> roots(x**2 - y)
    Traceback (most recent call last):
    ...
    PolynomialError: multivariate polynomials are not supported

Here we have to tell :func:`roots` in which variable roots should be computed::

    >>> roots(x**2 - y, x)
    ⎧   ⎽⎽⎽       ⎽⎽⎽   ⎫
    ⎨-╲╱ y : 1, ╲╱ y : 1⎬
    ⎩                   ⎭

Of course the choice of ``y`` is also a valid one, assuming that this is what
you really want. This of course doesn't apply only to polynomials.

Turning strings into expressions
--------------------------------

Suppose we saved the following expression::

    >>> var('x,y')

    >>> expr = x**2 + sin(y) + S(1)/2
    >>> expr
     2            1
    x  + sin(y) + ─
                  2

by printing it with :func:`sstr` printer and storing to a file::

    >>> sstr(expr)
    x**2 + sin(y) + 1/2

    >>> with open("expression.txt", "w") as f:
    ...     f.write(_)
    ...
    ...

We used this kind of printer because we wanted the file to be fairly readable.
Now we want to restore the original expression. First we have to read the text
form from the file::

    >>> with open("expression.txt") as f:
    ...     text_form = f.read()
    ...
    ...

    >>> text_form
    x**2 + sin(y) + 1/2
    >>> type(_)
    <type 'str'>

We could try to try to use :func:`eval` on ``text_form`` but this doesn't give
expected results::

    >>> eval(text_form)
     2
    x  + sin(y) + 0.5

This happens because ``1/2`` isn't understood by Python as rational number
and is equivalent to a problem we had when entering expressions of this kind
in interactive sessions.

To overcome this problem we have to use :func:`sympify`, which implements
:mod:`tokenize`--based parser that allows us to handle this issue::

    >>> sympify(text_form)
     2            1
    x  + sin(y) + ─
                  2
    >>> _ == expr
    True

Let's now consider a more interesting problem. Suppose we define our own function::

    >>> class my_func(Function):
    ...     """Returns zero for integer values. """
    ...
    ...     @classmethod
    ...     def eval(cls, arg):
    ...         if arg.is_Number:
    ...             return 2*arg
    ...
    ...

This function gives twice the input argument if the argument is a number and
doesn't do anything for all other classes of arguments::

    >>> my_func(117)
    234
    >>> my_func(S(1)/2)
    1

    >>> my_func(x)
    my_func(x)
    >>> _.subs(x, 2.1)
    4.20000000000000

    >>> my_func(1) + 1
    3

Let's create an expression that contains :func:`my_func`::

    >>> expr = my_func(x) + 1
    >>> expr
    my_func(x) + 1

    >>> _.subs(x, 1)
    3

Now we will print it using :func:`sstr` printer and sympify the result::

    >>> sympified = sympify(sstr(expr))
    >>> sympified
    my_func(x) + 1

We can use :func:`subs` method to quickly verify the expression is correct::

    >>> sympified.subs(x, 1)
    my_func(1) + 1

This is not exactly what we expected. This happens because::

    >>> expr == sympified
    False

    >>> expr.args
    (1, my_func(x))
    >>> type(_[1]) is my_func
    True

    >>> sympified.args
    (1, my_func(x))
    >>> type(_[1]) is my_func
    False

:func:`sympify` evaluates the given string in the context of ``from sympy import *``
and is not aware of user defined names. We can explicitly pass a mapping between
names and values to it::

    >>> sympify(sstr(expr), {'my_func': my_func})
    my_func(x) + 1
    >>> _.subs(x, 1)
    3

This time we got the desired result. This shows that we have to be careful when
working with expressions encoded as strings. This happens to be even more tricky
when we put assumptions on symbols. Do you remember the example in which we
tried to expand `\log(a b)`? Lets do it once again::

    >>> var('a,b', positive=True)
    (a, b)
    >>> log(a*b).expand()
    log(a) + log(b)

This worked as previously. However, let's now print `\log(a b)`, sympify the
resulting string and expand the restored expression::

    >>> sympify(sstr(log(a*b))).expand()
    log(a⋅b)

This didn't work, because :func:`sympify` doesn't know what ``a`` and ``b``
are, so it assumed that those are symbols and it created them implicitly.
This issue is similar to what we already experienced with :func:`my_func`.

The most reliable approach to storing expression is to use :mod:`pickle`
module. In the case of `\log(a b)` it works like this::

    >>> import pickle
    >>> pickled = pickle.dumps(log(a*b))
    >>> expr = pickle.loads(pickled)
    >>> expr.expand()
    log(a) + log(b)

Unfortunately, due to :mod:`pickle`'s limitations, this doesn't work for
user defined functions like :func:`my_func`::

    >>> pickle.dumps(my_func(x))
    Traceback (most recent call last):
    ...
    PicklingError: Can't pickle my_func: it's not found as __main__.my_func

Tasks
~~~~~

1. Construct a polynomial of degree, let's say, 1000. Use both techniques
   to save and restore this expression. Compare speed of those approaches.
   Verify that the result is correct.

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

``=`` is not comparison operator
--------------------------------

The equals sign (``=``) is the assignment operator in Python, not equality
operator. In other many mathematical systems, ``=`` is used for comparing
values and/or for constructing equalities, but with SymPy you have to use
``==`` for the former and ``Eq(x, y)`` for the later. Note that instances
of :class:`Eq` class, in boolean context, collapse to ``==``::

    >>> var('x,y')

    >>> x == y
    False

    >>> Eq(x, y)
    x = y
    >>> bool(_)
    False

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
    IPython console for SymPy 0.7.0 (Python 2.6.6) (ground types: gmpy)

    In [1]: f = (x-tan(x)) / tan(x)**2 + tan(x)

    In [2]: %time integrate(f, x);
    CPU times: user 0.46 s, sys: 0.00 s, total: 0.46 s
    Wall time: 0.49 s

    In [4]: %time integrate(f, x);
    CPU times: user 0.24 s, sys: 0.00 s, total: 0.24 s
    Wall time: 0.25 s

    $ bin/isympy -q -C
    IPython console for SymPy 0.7.0 (Python 2.6.6) (ground types: gmpy, cache: off)

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
    IPython console for SymPy 0.7.0 (Python 2.6.6) (ground types: gmpy)

    In [1]: %timeit sin(2*pi);
    10000 loops, best of 3: 28.7 us per loop

    $ bin/isympy -q -C
    IPython console for SymPy 0.7.0 (Python 2.6.6) (ground types: gmpy, cache: off)

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
