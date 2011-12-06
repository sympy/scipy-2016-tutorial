from sympy import pretty

def print_basic_unicode(obj, printer, cycle):
    out = pretty(obj, use_unicode=True)
    printer.text(out)

_loaded = False

def load_ipython_extension(ip):
    global _loaded

    if not _loaded:
        plaintext_formatter = ip.display_formatter.formatters['text/plain']

        for cls in (object, tuple, list, set, frozenset, dict, str):
            plaintext_formatter.for_type(cls, print_basic_unicode)

        _loaded = True
