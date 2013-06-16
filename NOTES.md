*Some notes for the tutorial. Feel free to edit it however you want.*

## General notes

- In general, I think we should first write documentation for SymPy, then
  backport that documentation to IPython notebooks for the tutorial. Or, for the
  things that it makes sense for, write IPython notebook examples for SymPy and
  just use them for the tutorial.

  Either way, we should focus on writing narrative documentation for SymPy. It
  is most lacking in this, so this will help. The things we use for the tutorial
  should maybe be toned down in the narration, as we will be speaking the things
  to them.

- It will be a lot easier if we can release before the tutorial, but if we
  don't make sure that everything works with 0.7.2.

## Things to talk about

- We should talk about the important
  [idioms and antipatterns](https://github.com/sympy/sympy/wiki/Idioms-and-Antipatterns).

- All the important expression manipulation functions (i.e., methods of
  Basic). This part should also be first written as documentation for SymPy.

- Documentation on how to do numerics with SymPy. This is something that a lot
  of people at SciPy will care about. It should talk about evalf, lambdify,
  code generation, and so on. *Ondřej, can you do this?*

- All the important modules. We should think about what these are for
  rewriting the tutorial. Right now, I am thinking

  - The core (basic operations)
  - Functions
  - Simplify
  - Solve
  - Matrices

- How to install and set things up (like printers and stuff). A lot of this
  can be borrowed from the 2011 tutorial. Some stuff, like working with
  IPython, will need to be updated.

- Should we talk about plotting?
