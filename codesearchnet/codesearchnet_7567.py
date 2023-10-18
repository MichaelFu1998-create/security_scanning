def get_docstring_and_rest(filename):
    """Separate `filename` content between docstring and the rest

    Strongly inspired from ast.get_docstring.

    Returns
    -------
    docstring: str
        docstring of `filename`
    rest: str
        `filename` content without the docstring
    """
    with open(filename) as f:
        content = f.read()

    node = ast.parse(content)
    if not isinstance(node, ast.Module):
        raise TypeError("This function only supports modules. "
                        "You provided {0}".format(node.__class__.__name__))
    if node.body and isinstance(node.body[0], ast.Expr) and \
       isinstance(node.body[0].value, ast.Str):
        docstring_node = node.body[0]
        docstring = docstring_node.value.s
        # This get the content of the file after the docstring last line
        # Note: 'maxsplit' argument is not a keyword argument in python2
        rest = content.split('\n', docstring_node.lineno)[-1]
        return docstring, rest
    else:
        raise ValueError(('Could not find docstring in file "{0}". '
                          'A docstring is required by sphinx-gallery')
                         .format(filename))