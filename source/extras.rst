
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

::

    >>> from sympy import Symbol, Lambda, sin

    >>> from sympy.printing.pretty.pretty import PrettyPrinter
    >>> from sympy.printing.pretty.stringpict import prettyForm

    >>> x = Symbol('x')

    >>> class LambdaPrettyPrinter(PrettyPrinter):
    ...     def _print_Lambda(self, expr):
    ...         args = expr.args[0].args + (expr.args[1],)
    ...         pform_head = prettyForm('Lambda')
    ...         pform_tail = self._print_seq(args, '(', ')')
    ...         pform = prettyForm(*pform_head.right(pform_tail))
    ...         return pform
    ...

    >>> LambdaPrettyPrinter().doprint(Lambda(x, sin(1/x)))
          ⎛      ⎛1⎞⎞
    Lambda⎜x, sin⎜─⎟⎟
          ⎝      ⎝x⎠⎠

.. _solution_custom_printers_2:

Solution 2
~~~~~~~~~~

::

    >>> from sympy.printing.pretty.pretty import PrettyPrinter
    >>> from sympy.printing.pretty.stringpict import prettyForm, stringPict

    >>> class PolyPrettyPrinter(PrettyPrinter):
    ...     def _print_Poly(self, poly):
    ...         expr = poly.as_expr()
    ...         gens = list(poly.gens)
    ...         domain = poly.get_domain()
    ...         #
    ...         pform = self._print(expr)
    ...         pform = prettyForm(*stringPict.next(pform, ", "))
    ...         #
    ...         for gen in gens:
    ...             pform = prettyForm(*stringPict.next(pform, self._print(gen)))
    ...             pform = prettyForm(*stringPict.next(pform, ", "))
    ...         #
    ...         pform = prettyForm(*stringPict.next(pform, "domain="))
    ...         pform = prettyForm(*stringPict.next(pform, self._print(domain)))
    ...         #
    ...         pform = prettyForm(*pform.parens("(", ")", ifascii_nougly=True))
    ...         pform = prettyForm(*prettyForm('Poly').right(pform))
    ...         #
    ...         return pform
    ...

    >>> PolyPrettyPrinter().doprint(Poly(x**2 + 1))
        ⎛ 2                 ⎞
    Poly⎝x  + 1, x, domain=ℤ⎠

    >>> PolyPrettyPrinter().doprint(Poly(x**2 + y/2))
        ⎛ 2   y                ⎞
    Poly⎜x  + ─, x, y, domain=ℚ⎟
        ⎝     2                ⎠

Implementing printers from scratch
----------------------------------

.. _solution_new_printers_1:

Solution 1
~~~~~~~~~~

::

    >>> class ExtendedMathematicaPrinter(MathematicaPrinter):
    ...     def _print_Pi(self, expr):
    ...         return 'Pi'
    ...

    >>> MathematicaPrinter().doprint(pi)
    pi
    >>> ExtendedMathematicaPrinter().doprint(pi)
    Pi

.. _solution_new_printers_2:

Solution 2
~~~~~~~~~~

::

    >>> class ExtendedMathematicaPrinter(MathematicaPrinter):
    ...     def _print_Mul(self, expr):
    ...         prec = precedence(expr)
    ...         return "*".join([ self.parenthesize(arg, prec) for arg in expr.args ])
    ...

    >>> MathematicaPrinter().doprint(2*sin(x))
    2*sin(x)
    >>> ExtendedMathematicaPrinter().doprint(2*sin(x))
    2*Sin[x]

Code generation
---------------

.. _solution_codegen_1:

Solution 1
~~~~~~~~~~

::

    >>> from sympy.utilities.codegen import codegen
    >>> from sympy import Symbol, chebyshevt

    >>> x = Symbol('x')

    >>> print codegen(("chebyshevt_20", chebyshevt(20, x)), "C", "file")[0][1]
    /******************************************************************************
     *                      Code generated with sympy 0.7.0                       *
     *                                                                            *
     *              See http://www.sympy.org/ for more information.               *
     *                                                                            *
     *                       This file is part of 'project'                       *
     ******************************************************************************/
    #include "file.h"
    #include <math.h>

    double chebyshevt_20(double x) {

       return 524288*pow(x, 20) - 2621440*pow(x, 18) + 5570560*pow(x, 16) - 6553600*pow(x, 14) + 4659200*pow(x, 12) - 2050048*pow(x, 10) + 549120*pow(x, 8) - 84480*pow(x, 6) + 6600*pow(x, 4) - 200*pow(x, 2) + 1;

    }

.. _solution_codegen_2:

Solution 2
~~~~~~~~~~

::

    >>> from sympy.utilities.codegen import codegen
    >>> from sympy import Symbol, chebyshevt

    >>> x = Symbol('x')

    >>> functions = [ ("chebyshevt_%d" % i, chebyshevt(i, x)) for i in xrange(0, 10) ]
    >>> print codegen(functions, "F95", "file")[0][1]
    !******************************************************************************
    !*                      Code generated with sympy 0.7.0                       *
    !*                                                                            *
    !*              See http://www.sympy.org/ for more information.               *
    !*                                                                            *
    !*                       This file is part of 'project'                       *
    !******************************************************************************

    REAL*8 function chebyshevt_0()
    implicit none

    chebyshevt_0 = 1

    end function

    REAL*8 function chebyshevt_1(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_1 = x

    end function

    REAL*8 function chebyshevt_2(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_2 = 2*x**2 - 1

    end function

    REAL*8 function chebyshevt_3(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_3 = 4*x**3 - 3*x

    end function

    REAL*8 function chebyshevt_4(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_4 = 8*x**4 - 8*x**2 + 1

    end function

    REAL*8 function chebyshevt_5(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_5 = 16*x**5 - 20*x**3 + 5*x

    end function

    REAL*8 function chebyshevt_6(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_6 = 32*x**6 - 48*x**4 + 18*x**2 - 1

    end function

    REAL*8 function chebyshevt_7(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_7 = 64*x**7 - 112*x**5 + 56*x**3 - 7*x

    end function

    REAL*8 function chebyshevt_8(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_8 = 128*x**8 - 256*x**6 + 160*x**4 - 32*x**2 + 1

    end function

    REAL*8 function chebyshevt_9(x)
    implicit none
    REAL*8, intent(in) :: x

    chebyshevt_9 = 256*x**9 - 576*x**7 + 432*x**5 - 120*x**3 + 9*x

    end function
