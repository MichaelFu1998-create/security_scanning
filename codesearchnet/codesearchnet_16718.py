def is_funcdef(src):
    """True if src is a function definition"""

    module_node = ast.parse(dedent(src))

    if len(module_node.body) == 1 and isinstance(
            module_node.body[0], ast.FunctionDef
    ):
        return True
    else:
        return False