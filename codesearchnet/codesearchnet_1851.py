def ndiff(a, b, linejunk=None, charjunk=IS_CHARACTER_JUNK):
    r"""
    Compare `a` and `b` (lists of strings); return a `Differ`-style delta.

    Optional keyword parameters `linejunk` and `charjunk` are for filter
    functions (or None):

    - linejunk: A function that should accept a single string argument, and
      return true iff the string is junk.  The default is None, and is
      recommended; as of Python 2.3, an adaptive notion of "noise" lines is
      used that does a good job on its own.

    - charjunk: A function that should accept a string of length 1. The
      default is module-level function IS_CHARACTER_JUNK, which filters out
      whitespace characters (a blank or tab; note: bad idea to include newline
      in this!).

    Tools/scripts/ndiff.py is a command-line front-end to this function.

    Example:

    >>> diff = ndiff('one\ntwo\nthree\n'.splitlines(1),
    ...              'ore\ntree\nemu\n'.splitlines(1))
    >>> print ''.join(diff),
    - one
    ?  ^
    + ore
    ?  ^
    - two
    - three
    ?  -
    + tree
    + emu
    """
    return Differ(linejunk, charjunk).compare(a, b)