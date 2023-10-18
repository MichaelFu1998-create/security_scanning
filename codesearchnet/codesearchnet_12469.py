def parse_arguments(arguments):
    """parse_arguments('(a, b, *, c=False, **d)') -> ast3.arguments

    Parse a string with function arguments into an AST node.
    """
    arguments = f"def f{arguments}: ..."
    try:
        result = ast3.parse(arguments, '<arguments>', 'exec')
    except SyntaxError:
        raise ValueError(f"invalid arguments: {arguments!r}") from None

    assert isinstance(result, ast3.Module)
    assert len(result.body) == 1
    assert isinstance(result.body[0], ast3.FunctionDef)
    args = result.body[0].args
    copy_type_comments_to_annotations(args)
    return args