def find_funcdef(source):
    """Find the first FuncDef ast object in source"""

    try:
        module_node = compile(
            source, "<string>", mode="exec", flags=ast.PyCF_ONLY_AST
        )
    except SyntaxError:
        return find_funcdef(fix_lamdaline(source))

    for node in ast.walk(module_node):
        if isinstance(node, ast.FunctionDef) or isinstance(node, ast.Lambda):
            return node

    raise ValueError("function definition not found")