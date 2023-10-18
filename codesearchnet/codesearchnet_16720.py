def replace_funcname(source: str, name: str):
    """Replace function name"""

    lines = source.splitlines()
    atok = asttokens.ASTTokens(source, parse=True)

    for node in ast.walk(atok.tree):
        if isinstance(node, ast.FunctionDef):
            break

    i = node.first_token.index
    for i in range(node.first_token.index, node.last_token.index):
        if (atok.tokens[i].type == token.NAME
                and atok.tokens[i].string == "def"):
            break

    lineno, col_begin = atok.tokens[i + 1].start
    lineno_end, col_end = atok.tokens[i + 1].end

    assert lineno == lineno_end

    lines[lineno-1] = (
            lines[lineno-1][:col_begin] + name + lines[lineno-1][col_end:]
    )

    return "\n".join(lines) + "\n"