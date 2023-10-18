def extract_names(source):
    """Extract names from a function definition

    Looks for a function definition in the source.
    Only the first function definition is examined.

    Returns:
         a list names(identifiers) used in the body of the function
         excluding function parameters.
    """
    if source is None:
        return None

    source = dedent(source)
    funcdef = find_funcdef(source)
    params = extract_params(source)
    names = []

    if isinstance(funcdef, ast.FunctionDef):
        stmts = funcdef.body
    elif isinstance(funcdef, ast.Lambda):
        stmts = [funcdef.body]
    else:
        raise ValueError("must not happen")

    for stmt in stmts:
        for node in ast.walk(stmt):
            if isinstance(node, ast.Name):
                if node.id not in names and node.id not in params:
                    names.append(node.id)

    return names