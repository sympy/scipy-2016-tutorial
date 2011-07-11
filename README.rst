
Guide to Symbolic Mathematics with SymPy
========================================

:author: Mateusz Paprocki <mattpap@gmail.com>
:author: Aaron Meurer <asmeurer@gmail.com>

SymPy (www.sympy.org) is a pure Python library for symbolic mathematics. It
aims to become a full-featured computer algebra system (CAS) while keeping the
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

We expect attendees of this tutorial to have basic knowledge of Python and
mathematics. However, any more more advanced topics will be explained during
presentation.

Outline
-------

Introduction to SymPy
~~~~~~~~~~~~~~~~~~~~~

* installing, configuring and running SymPy

  * Python, IPython, isympy, SymPy in a web browser
  * configuration variables and their meaning

* basics of expressions in SymPy

  * building blocks of expressions
  * core structure of classes
  * various ways of defining symbols
  * dummy symbols and their role
  * constructing expressions
  * automatic evaluation
  * obtaining parts of expressions
  * substituting subexpressions
  * expressions in data structures
  * turning strings into expressions

* traversal and manipulation of expressions

  * manual and interactive traversal of subexpressions
  * search and replace in expressions
  * most common expression manipulation functions
  * transforming expressions between different forms

* common issues and differences from other CAS

  * why I have to define symbols?
  * ``1/3`` is not a rational number
  * ``^`` is not exponentiation operator
  * why you shouldn't write ``10**(-1000)``
  * how to deal with limited recursion depth
  * expression caching and its consequences

* setting up and using printers

  * repr/str, pretty (ASCII, Unicode), LaTeX, MathML
  * generating code with SymPy (C, Fortran)
  * defining your own customized printers

* not only symbolics: numerical computing (mpmath)

  * evaluation of expressions to arbitrary precision
  * symbolics vs. numerics (limits)

Mathematical problem solving with SymPy
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

1. Step--by--step partial fraction decomposition.

   Given a univariate rational function ``f(z) = p(z)/q(z)`` compute its
   partial fraction decomposition using undetermined coefficients method.

   We will approach this problem by showing how to construct generic partial
   fractions for a given rational function, use simplification functions to
   transform those partial fractions to certain form that we will use to
   construct a system of linear equations from and solve it in SymPy.

2. Computing certain sums of roots of polynomials.

   Given a univariate polynomial ``f(z)`` and a univariate rational function
   ``g(r)`` compute ``g(r_1) + ... + g(r_n)``, where ``r_i``'s are roots of
   ``f`` (i.e. ``f(r_i) = 0``).

   To solve this problem we will use expression manipulation functions to put
   the sum in a certain form and then use symmetric reduction of multivariate
   polynomials and Viete formulas to obtain the final result.

3. Vertex k--coloring of graphs.

   Suppose we are given graph ``G(V, E)``, such that ``V`` is a set of vertices
   and ``E`` a set of edges, and a positive integer ``k``. We ask whether ``G``
   is colorable with ``k`` colors and what are the color assignments.

   To handle this task we will transform a graph theoretic formulation of graph
   ``k``--coloring problem to a system of multivariate polynomial equations and
   solve it using Groebner bases.

4. Theorem proving in algebraic geometry.

   Consider a rhombus in a fixed coordinate system. We will prove that its
   diagonals are mutually perpendicular.

   First we will state the theorem regarding diagonals of a rhombus in the
   language of geometry. Next we will transform this formulation to an
   algebraic form and finally we will use the Groebner bases method to
   obtain the proof of this theorem.

Required software
-----------------

* Python 2.x (Python 3.x is not supported yet)
* SymPy (most recent version)

Additional software
-------------------

* IPython
* Matplotlib
* GMPY

Authors' bio
------------

*Mateusz Paprocki* is SymPy's core developer since 2007. He was Google Summer
of Code student and twice a mentor for SymPy. He also gave talks about SymPy on
various conferences and scientific meetings (most notably EuroSciPy, Py4Science
and PyCon.PL).

*Aaron Meurer* is SymPy's core developer since 2009 and the current leader of
the project. He was twice Google Summer of Code student for SymPy and currently
is pursuing a masters in mathematics at New Mexico Tech.
