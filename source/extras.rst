
.. include:: definitions.def

======
Extras
======

Solutions
=========

Arithmetic operators
--------------------

.. _solution_arith_op_1:

Solution 1
~~~~~~~~~~

::

    >>> from sympy import Symbol, Add, Poly

    >>> x = Symbol('x')

    >>> Add(*[ x**i for i in xrange(0, 10+1) ])
     10    9    8    7    6    5    4    3    2
    x   + x  + x  + x  + x  + x  + x  + x  + x  + x + 1

    >>> sum([ x**i for i in xrange(0, 10+1) ])
     10    9    8    7    6    5    4    3    2
    x   + x  + x  + x  + x  + x  + x  + x  + x  + x + 1

    >>> Poly([1]*11, x).as_expr()
     10    9    8    7    6    5    4    3    2
    x   + x  + x  + x  + x  + x  + x  + x  + x  + x + 1

    >>> def build_poly_1(n):
    ...     return Add(*[ x**i for i in xrange(0, n+1) ])
    ...

    >>> build_poly_1(1)
    x + 1
    >>> build_poly_1(2)
     2
    x  + x + 1
    >>> build_poly_1(3)
     3    2
    x  + x  + x + 1

    >>> def build_poly_2(n):
    ...     if n > 0:
    ...         return Add(*[ x**i for i in xrange(0, n+1) ])
    ...     else:
    ...         return Add(*[ x**i for i in xrange(0, n-1, -1) ])
    ...

    >>> build_poly_2(1)
    x + 1
    >>> build_poly_2(0)
    1
    >>> build_poly_2(-1)
        1
    1 + ─
        x

.. _solution_arith_op_2:

Solution 2
~~~~~~~~~~

::

    >>> from sympy import Symbol

    >>> x = Symbol('x')

    >>> def nested_power(expr, n):
    ...     if not n:
    ...         return expr
    ...     else:
    ...         return expr**nested_power(expr, n-1)
    ...

    >>> nested_power(x, 1)
     x
    x
    >>> nested_power(x, 2)
     ⎛ x⎞
     ⎝x ⎠
    x
    >>> nested_power(x, 3)
     ⎛ ⎛ x⎞⎞
     ⎜ ⎝x ⎠⎟
     ⎝x    ⎠
    x

Building blocks of expressions
------------------------------

.. _solution_blocks_1:

Solution 1
~~~~~~~~~~

::

    >>> from sympy import var, exp, sin, Integral, Eq

    >>> var('a,b,c,x,C')
    (a, b, c, x, C)

    >>> expressions = [x**n, a*x**2 + b*x + c, 1/x, 1/(x**2 + 1), exp(a*x), sin(a*x) + b]
    >>> expressions
    ⎡ n     2            1    1      a⋅x              ⎤
    ⎢x , a⋅x  + b⋅x + c, ─, ──────, ℯ   , b + sin(a⋅x)⎥
    ⎢                    x   2                        ⎥
    ⎣                       x  + 1                    ⎦

    >>> integrals_table = []

    >>> for expr in expressions:
    ...     integral = Integral(expr, x)
    ...     integrals_table.append((integral, integral.doit() + C))
    ...

    >>> for integral, antiderivative in integrals_table:
    ...     pprint(Eq(integral, antiderivative))
    ...     print
    ...
    ⌠              n + 1
    ⎮  n          x
    ⎮ x  dx = C + ──────
    ⌡             n + 1

    ⌠                              3      2
    ⎮ ⎛   2          ⎞          a⋅x    b⋅x
    ⎮ ⎝a⋅x  + b⋅x + c⎠ dx = C + ──── + ──── + c⋅x
    ⌡                            3      2

    ⌠
    ⎮ 1
    ⎮ ─ dx = C + log(x)
    ⎮ x
    ⌡

    ⌠
    ⎮   1
    ⎮ ────── dx = C + atan(x)
    ⎮  2
    ⎮ x  + 1
    ⌡

    ⌠                a⋅x
    ⎮  a⋅x          ℯ
    ⎮ ℯ    dx = C + ────
    ⌡                a

    ⌠                               cos(a⋅x)
    ⎮ (b + sin(a⋅x)) dx = C + b⋅x - ────────
    ⌡                                  a

    ⌠              n + 1
    ⎮  n          x
    ⎮ x  dx = C + ──────
    ⌡             n + 1

    ⌠                              3      2
    ⎮ ⎛   2          ⎞          a⋅x    b⋅x
    ⎮ ⎝a⋅x  + b⋅x + c⎠ dx = C + ──── + ──── + c⋅x
    ⌡                            3      2
    ⌠
    ⎮ 1
    ⎮ ─ dx = C + log(x)
    ⎮ x
    ⌡

    ⌠
    ⎮   1
    ⎮ ────── dx = C + atan(x)
    ⎮  2
    ⎮ x  + 1
    ⌡

    ⌠                a⋅x
    ⎮  a⋅x          ℯ
    ⎮ ℯ    dx = C + ────
    ⌡                a

    ⌠                               cos(a⋅x)
    ⎮ (b + sin(a⋅x)) dx = C + b⋅x - ────────
    ⌡                                  a

Foreign types in SymPy
----------------------

.. _solution_foreign_1:

Solution 1
~~~~~~~~~~

::

    >>> from sympy.core.sympify import sympify, converter
    >>> from gmpy import mpq

    >>> def mpq_to_Rational(obj):
    ...     return Rational(obj.numer(), obj.denom())
    ...

    >>> converter[type(mpq(1))] = mpq_to_Rational

    >>> sympify(mpq(1, 2))
    1/2
    >>> type(_)
    <class 'sympy.core.numbers.Rational'>

.. _solution_foreign_2:

Solution 2
~~~~~~~~~~

::

    >>> from sympy.core.sympify import converter, sympify, SympifyError
    >>> from numpy import array, ndarray

    >>> def ndarray_to_Tuple(obj):
    ...     if len(obj.shape) == 1:
    ...         return Tuple(*obj)
    ...     else:
    ...         raise SympifyError("only row NumPy arrays are allowed")
    ...

    >>> converter[ndarray] = ndarray_to_Tuple

    >>> sympify(array([1, 2, 3]))
    Tuple(1, 2, 3)

    >>> sympify(array([[1], [2], [3]]))
    Traceback (most recent call last):
    ...
    SympifyError: SympifyError: 'only row NumPy arrays are allowed'

The role of symbols
-------------------

.. _solution_symbols_1:

Solution 1
~~~~~~~~~~

::

    >>> from sympy import Add, Symbol, symbols, numbered_symbols

    >>> def build_expression_1(name, n):
    ...     return Add(*[ Symbol('%s_%d' % (name, i))**i for i in xrange(1, n+1) ])
    ...

    >>> def build_expression_2(name, n):
    ...     X = symbols('%s1:%d' % (name, n+1))
    ...     return Add([ x**i for x, i in zip(X, xrange(1, n+1)) ])
    ...

    >>> def build_expression_3(name, n):
    ...     X = numbered_symbols(name, start=1)
    ...     return Add([ x**i for x, i in zip(X, xrange(1, n+1)) ])
    ...

    >>> build_expression_1('x', 5):
           2     3     4     5
    x₁ + x₂  + x₃  + x₄  + x₅
    >>> build_expression_2('y', 5):
           2     3     4     5
    y₁ + y₂  + y₃  + y₄  + y₅
    >>> build_expression_2('z', 5):
           2     3     4     5
    z₁ + z₂  + z₃  + z₄  + z₅

Obtaining parts of expressions
------------------------------

.. _solution_parts_1:

Solution 1
~~~~~~~~~~

::

    >>> from sympy.core import Atom, sympify

    >>> def depth_1(expr):
    ...     expr = sympify(expr)
    ...
    ...     if isinstance(expr, Atom):
    ...         return 1
    ...     else:
    ...         return 1 + max([ depth_1(arg) for arg in expr.args ])
    ...

    >>> depth_1(117)
    1

    >>> def depth_2(expr):
    ...     def _depth(expr):
    ...         if isinstance(expr, Atom):
    ...             return 1
    ...         else:
    ...             return 1 + max([ _depth(arg) for arg in expr.args ])
    ...
    ...     return _depth(sympify(expr))
    ...

    >>> depth_2(117)
    1

.. _solution_parts_2:

Solution 2
~~~~~~~~~~

::

    >>> from sympy.core import Atom

    >>> def depth(expr):
    ...     if isinstance(expr, Atom):
    ...         return 1
    ...     else:
    ...         if isinstance(expr, Basic):
    ...             args = expr.args
    ...         elif hasattr(expr, '__iter__'):
    ...             args = expr
    ...         else:
    ...             raise ValueError("can't compute the depth of %s" % expr)
    ...
    ...         return 1 + max([ depth(arg) for arg in args ])
    ...

    >>> depth(x)
    1
    >>> depth(x + y)
    2
    >>> depth([x, y])
    2
    >>> depth((x, sin(x)))
    3
    >>> depth(set([(x, sin(x), sin(cos(x)))]))
    4

Immutability of expressions
---------------------------

.. _solution_immutability_1:

Solution 1
~~~~~~~~~~

::

    >>> var('x')
    x

    >>> x**x
     x
    x
    >>> _.subs(x, x**x)
        ⎛ x⎞
        ⎝x ⎠
    ⎛ x⎞
    ⎝x ⎠
    >>> _.subs(x, x**x)
              ⎛    ⎛ x⎞⎞
              ⎜    ⎝x ⎠⎟
              ⎜⎛ x⎞    ⎟
              ⎝⎝x ⎠    ⎠
    ⎛    ⎛ x⎞⎞
    ⎜    ⎝x ⎠⎟
    ⎜⎛ x⎞    ⎟
    ⎝⎝x ⎠    ⎠
    >>> _.subs(x, x**x)
                          ⎛          ⎛    ⎛ x⎞⎞⎞
                          ⎜          ⎜    ⎝x ⎠⎟⎟
                          ⎜          ⎜⎛ x⎞    ⎟⎟
                          ⎜          ⎝⎝x ⎠    ⎠⎟
                          ⎜⎛    ⎛ x⎞⎞          ⎟
                          ⎜⎜    ⎝x ⎠⎟          ⎟
                          ⎜⎜⎛ x⎞    ⎟          ⎟
                          ⎝⎝⎝x ⎠    ⎠          ⎠
    ⎛          ⎛    ⎛ x⎞⎞⎞
    ⎜          ⎜    ⎝x ⎠⎟⎟
    ⎜          ⎜⎛ x⎞    ⎟⎟
    ⎜          ⎝⎝x ⎠    ⎠⎟
    ⎜⎛    ⎛ x⎞⎞          ⎟
    ⎜⎜    ⎝x ⎠⎟          ⎟
    ⎜⎜⎛ x⎞    ⎟          ⎟
    ⎝⎝⎝x ⎠    ⎠          ⎠


    >>> expr = x**x

    >>> for i in xrange(3):
    ...     expr = (expr.base**expr.base)**(expr.exp**expr.exp)
    ...

    >>> expr
                          ⎛          ⎛    ⎛ x⎞⎞⎞
                          ⎜          ⎜    ⎝x ⎠⎟⎟
                          ⎜          ⎜⎛ x⎞    ⎟⎟
                          ⎜          ⎝⎝x ⎠    ⎠⎟
                          ⎜⎛    ⎛ x⎞⎞          ⎟
                          ⎜⎜    ⎝x ⎠⎟          ⎟
                          ⎜⎜⎛ x⎞    ⎟          ⎟
                          ⎝⎝⎝x ⎠    ⎠          ⎠
    ⎛          ⎛    ⎛ x⎞⎞⎞
    ⎜          ⎜    ⎝x ⎠⎟⎟
    ⎜          ⎜⎛ x⎞    ⎟⎟
    ⎜          ⎝⎝x ⎠    ⎠⎟
    ⎜⎛    ⎛ x⎞⎞          ⎟
    ⎜⎜    ⎝x ⎠⎟          ⎟
    ⎜⎜⎛ x⎞    ⎟          ⎟
    ⎝⎝⎝x ⎠    ⎠          ⎠


Turning strings into expressions
--------------------------------

.. _solution_sympify_1:

Solution 1
~~~~~~~~~~

.. ::

Customizing built-in printers
-----------------------------

.. _solution_custom_printers_1:

Solution 1
~~~~~~~~~~

.. ::

.. _solution_custom_printers_2:

Solution 2
~~~~~~~~~~

.. ::

Implementing printers from scratch
----------------------------------

.. _solution_new_printers_1:

Solution 1
~~~~~~~~~~

.. ::

.. _solution_new_printers_2:

Solution 2
~~~~~~~~~~

.. ::

Code generation
---------------

.. _solution_codegen_1:

Solution 1
~~~~~~~~~~

.. ::

.. _solution_codegen_2:

Solution 2
~~~~~~~~~~

.. ::
