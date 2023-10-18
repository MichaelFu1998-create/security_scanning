def remove_decorator(source: str):
    """Remove decorators from function definition"""
    lines = source.splitlines()
    atok = asttokens.ASTTokens(source, parse=True)

    for node in ast.walk(atok.tree):
        if isinstance(node, ast.FunctionDef):
            break

    if node.decorator_list:
        deco_first = node.decorator_list[0]
        deco_last = node.decorator_list[-1]
        line_first = atok.tokens[deco_first.first_token.index - 1].start[0]
        line_last = atok.tokens[deco_last.last_token.index + 1].start[0]

        lines = lines[:line_first - 1] + lines[line_last:]

    return "\n".join(lines) + "\n"