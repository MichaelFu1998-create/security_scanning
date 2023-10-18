def parse_buffer(buffer, mode="exec", flags=[], version=None, engine=None):
    """
    Like :meth:`parse`, but accepts a :class:`source.Buffer` instead of
    source and filename, and returns comments as well.

    :see: :meth:`parse`
    :return: (:class:`ast.AST`, list of :class:`source.Comment`)
        Abstract syntax tree and comments
    """

    if version is None:
        version = sys.version_info[0:2]

    if engine is None:
        engine = pythonparser_diagnostic.Engine()

    lexer = pythonparser_lexer.Lexer(buffer, version, engine)
    if mode in ("single", "eval"):
        lexer.interactive = True

    parser = pythonparser_parser.Parser(lexer, version, engine)
    parser.add_flags(flags)

    if mode == "exec":
        return parser.file_input(), lexer.comments
    elif mode == "single":
        return parser.single_input(), lexer.comments
    elif mode == "eval":
        return parser.eval_input(), lexer.comments