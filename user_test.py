#!/usr/bin/env python

try:
    import sympy
except ImportError:
    print("sympy is required")
else:

    if sympy.__version__ < '0.7.5':
        print("SymPy version 0.7.5 or newer is required. You have", sympy.__version__)

    if sympy.__version__ != '0.7.5':
        print("The stable SymPy version 0.7.5 is recommended. You have", sympy.__version__)

try:
    import matplotlib
except ImportError:
    print("matplotlib is required for the plotting section of the tutorial")

try:
    import IPython
except ImportError:
    print("IPython notebook is required.")
else:
    if IPython.__version__ < '2.1.0':
        print("The latest version of IPython is recommended. You have", IPython.__version__)

print("""A fortran and/or C compiler is required for the code generation portion
of the tutorial. However, if you do not have one, you should not worry, as it
will not be a large part of the tutorial.""")
