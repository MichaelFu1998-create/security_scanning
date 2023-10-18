def parse_signature_type_comment(type_comment):
    """Parse the fugly signature type comment into AST nodes.

    Caveats: ASTifying **kwargs is impossible with the current grammar so we
    hack it into unary subtraction (to differentiate from Starred in vararg).

    For example from:
    "(str, int, *int, **Any) -> 'SomeReturnType'"

    To:
    ([ast3.Name, ast.Name, ast3.Name, ast.Name], ast3.Str)
    """
    try:
        result = ast3.parse(type_comment, '<func_type>', 'func_type')
    except SyntaxError:
        raise ValueError(f"invalid function signature type comment: {type_comment!r}")

    assert isinstance(result, ast3.FunctionType)
    if len(result.argtypes) == 1:
        argtypes = result.argtypes[0]
    else:
        argtypes = result.argtypes
    return argtypes, result.returns