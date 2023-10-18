def parse(source, filename="<unknown>", mode="exec",
          flags=[], version=None, engine=None):
    """
    Parse a string into an abstract syntax tree.
    This is the replacement for the built-in :meth:`..ast.parse`.

    :param source: (string) Source code in the correct encoding
    :param filename: (string) Filename of the source (used in diagnostics)
    :param mode: (string) Execution mode. Pass ``"exec"`` to parse a module,
        ``"single"`` to parse a single (interactive) statement,
        and ``"eval"`` to parse an expression. In the last two cases,
        ``source`` must be terminated with an empty line
        (i.e. end with ``"\\n\\n"``).
    :param flags: (list of string) Future flags.
        Equivalent to ``from __future__ import <flags>``.
    :param version: (2-tuple of int) Major and minor version of Python
        syntax to recognize, ``sys.version_info[0:2]`` by default.
    :param engine: (:class:`diagnostic.Engine`) Diagnostic engine,
        a fresh one is created by default
    :return: (:class:`ast.AST`) Abstract syntax tree
    :raise: :class:`diagnostic.Error`
        if the source code is not well-formed
    """
    ast, comments = parse_buffer(pythonparser_source.Buffer(source, filename),
                                 mode, flags, version, engine)
    return ast