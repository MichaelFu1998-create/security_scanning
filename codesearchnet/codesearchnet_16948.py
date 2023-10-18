def setup(app):
    """ Initializer for Sphinx extension API.

        See http://www.sphinx-doc.org/en/stable/extdev/index.html#dev-extensions.
    """
    lexer = MarkdownLexer()
    for alias in lexer.aliases:
        app.add_lexer(alias, lexer)

    return dict(version=__version__)