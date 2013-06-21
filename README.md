SymPy tutorial for SciPy 2013
=============================

This is the tutorial that Aaron Meurer and Ondřej Čertík are giving at SciPy
2013 for SymPy.  If you are attending the tutorial, please install
Anaconda. You will need SymPy 0.7.2 and IPython 0.13.2.  The exercises for
attendees are in the tutorial_exercises directory. Everything else is
presentation materials for us.

If you want to build the tutorial presentation, use `make html` in the
tutorial_sphinx directory. It is basically the same as the new SymPy tutorial
at http://docs.sympy.org/tutorial/tutorial/.

If you clone the git repo, be sure to run

    git submodule init

to initialize the ipython_doctest submodule. Otherwise, the exercise notebooks
won't work.
