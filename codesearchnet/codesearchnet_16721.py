def has_lambda(src):
    """True if only one lambda expression is included"""

    module_node = ast.parse(dedent(src))
    lambdaexp = [node for node in ast.walk(module_node)
                 if isinstance(node, ast.Lambda)]

    return bool(lambdaexp)