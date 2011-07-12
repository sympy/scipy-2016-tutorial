
.. include:: definitions.def

======
Extras
======

Solutions
=========

1. Construct an expression for `1 + x + x^2 + \ldots + x^{10}`. Can you
   construct this expression in a different way? Write a function that
   could generate an expression for `1 + x + x^2 + \ldots + x^n` for any
   integer `n >= 0`. Extend this function to allow `n < 0`.

::

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
    ...

    >>> def build_poly_2(n):
    ...     if n > 0:
    ...         return Add(*[ x**i for i in xrange(0, n+1) ])
    ...     else:
    ...         return Add(*[ x**i for i in xrange(0, n-1, -1) ])
    ...
    ...


2. Write a function that can compute nested powers, e.g. `x^x`, `x^{x^x}` and
   so on. The function should take two parameters: an expression and a positive
   integer `n` that specifies the depth.

::

    >>> def nested_power(expr, n):
    ...     if not n:
    ...         return expr
    ...     else:
    ...         return expr**nested_power(expr, n-1)
    ...
    ...

1. Expressions implement a :func:`doit` method. For most types expressions
   it doesn't do anything useful, but in the case of unevaluated operators,
   it executes an action assigned to to an unevaluated operator (it
   differentiates, integrates, etc.). Take advantage of :func:`doit` and
   write a function that generates integral tables for a few polynomials,
   rational functions and elementary functions.

::

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
    ...

    >>> for integral, antiderivative in integrals_table:
    ...     pprint(Eq(integral, antiderivative))
    ...
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

1. Add support for ``mpq`` to :func:`sympify`.

::

    >>> from sympy.core.sympify import converter
    >>> from gmpy import mpq

    >>> def mpq_to_Rational(obj):
    ...     return Rational(obj.numer(), obj.denom())
    ...
    ...

    >>> converter[type(mpq(1))] = mpq_to_Rational

    >>> sympify(mpq(1, 2))
    1/2
    >>> type(_)
    <class 'sympy.core.numbers.Rational'>

2. SymPy implements :class:`Tuple` class, which provides functionality of
   Python's built-in ``tuple``, but is a subclass of :class:`Basic`. Take
   advantage of this and make :func:`sympify` work for 1D horizontal NumPy
   arrays, for which it should return instances of :class:`Tuple`. Raise
   :exc:`SympifyError` for other classes of arrays.

::

    >>> from sympy.core.sympify import converter, SympifyError
    >>> from numpy import array, ndarray

    >>> def 1D_horizontal_ndarray_to_Tuple(obj):
    ...     if len(obj.shape) == 1:
    ...         return Tuple(*obj)
    ...     else:
    ...         raise SympifyError("only 1D horizontal NumPy arrays are allowed")
    ...
    ...

    >>> converter[ndarray] = 1D_horizontal_ndarray_to_Tuple

    >>> array([1, 2, 3])
    [1 2 3]
    >>> sympify(_)
    Tuple(1, 2, 3)

    >>> array([[1], [2], [3]])
     [[1]
      [2]
      [3]]
    >>> sympify(_)
    Traceback (most recent call last):
    ...
    SympifyError: only 1D horizontal NumPy arrays are allowed

1. Implement a function that would generate an expression for `x_1^1 +
   x_2^2 + \ldots + x_n^n`. This function would take two arguments: base
   name for indexed symbols and integer exponent `n >= 1`. What's the
   best approach among the four presented above?

::

    >>> def build_expression_1(name, n):
    ...     return Add(*Symbol('%s_%d' % (name, i))**i for i in xrange(1, n+1) ])
    ...
    ...

    >>> def build_expression_2(name, n):
    ...     X = symbols('%s1:%d' % (name, n+1))
    ...     return Add(*Symbol('%s_%d' % (name, i))**i for i in xrange(1, n+1) ])
    ...
    ...

    >>> def build_expression_3(name, n):
    ...     X = numbered_symbols(name, start=1)
    ...     return Add([ x**i for x, i in zip(X, xrange(1, n+1)) ])
    ...
    ...

    >>> build_expression_1('x', 10):
    TODO
    >>> build_expression_2('y', 10):
    TODO
    >>> build_expression_2('z', 10):
    TODO

1. Change :func:`depth` so that it sympifies its input argument. Rewrite
   :func:`depth` so that is calls :func:`sympify` only once.

::

    >>> from sympy.core import Atom, sympify

    >>> def sympified_depth(expr):
    ...     expr = sympify(expr)
    ...
    ...     if isinstance(expr, Atom):
    ...         return 1
    ...     else:
    ...         return 1 + max([ sympified_depth(arg) for arg in expr.args ])
    ...
    ...

    >>> def better_sympified_depth(expr):
    ...     def _depth(expr):
    ...         if isinstance(expr, Atom):
    ...             return 1
    ...         else:
    ...             return 1 + max([ _depth(arg) for arg in expr.args ])
    ...
    ...     return _depth(sympify(expr))
    ...
    ...

    >>> sympified_depth(117)
    1
    >>> better_sympified_depth(117)
    1

2. Add support for iterable containers to :func:`depth`. Containers should
   be treated as branches and have depth defined the same way.

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

1. This is the first time we used :func:`subs`. This is a very important method
   and we will talk more about it later. However, we can also use :func:`subs`
   to generate some cool looking expressions. Start with ``x**x`` expression
   and substitute in it ``x**x`` for ``x``. What do you get? (make sure you
   use pretty printer) Can you achieve the same effect without :func:`subs`?

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


