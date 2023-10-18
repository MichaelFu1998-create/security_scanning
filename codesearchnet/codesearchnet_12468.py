def parse_type_comment(type_comment):
    """Parse a type comment string into AST nodes."""
    try:
        result = ast3.parse(type_comment, '<type_comment>', 'eval')
    except SyntaxError:
        raise ValueError(f"invalid type comment: {type_comment!r}") from None

    assert isinstance(result, ast3.Expression)
    return result.body