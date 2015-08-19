import sys


PY2 = sys.version_info[0] == 2

if PY2:
    import __builtin__ as _builtins
    from itertools import imap
else:
    import builtins as _builtins
    imap = _builtins.map


if PY2:
    exec("""
def reraise(tp, value, tb=None):
    raise tp, value, tb
""", locals(), globals())
else:
    def reraise(tp, value, tb=None):
        if value.__traceback__ is not tb:
            raise value.with_traceback(tb)
        raise value
