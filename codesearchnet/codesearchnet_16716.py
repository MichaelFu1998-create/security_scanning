def extract_params(source):
    """Extract parameters from a function definition"""

    funcdef = find_funcdef(source)
    params = []
    for node in ast.walk(funcdef.args):
        if isinstance(node, ast.arg):
            if node.arg not in params:
                params.append(node.arg)

    return params