def get_function_signature(fun, *, is_method=False):
    """Returns (args, returns).

    `args` is ast3.arguments, `returns` is the return type AST node. The kicker
    about this function is that it pushes type comments into proper annotation
    fields, standardizing type handling.
    """
    args = fun.args
    returns = fun.returns
    if fun.type_comment:
        try:
            args_tc, returns_tc = parse_signature_type_comment(fun.type_comment)
            if returns and returns_tc:
                raise ValueError(
                    "using both a type annotation and a type comment is not allowed"
                )
            returns = returns_tc
            copy_arguments_to_annotations(args, args_tc, is_method=is_method)
        except (SyntaxError, ValueError) as exc:
            raise ValueError(
                f"Annotation problem in function {fun.name!r}: " +
                f"{fun.lineno}:{fun.col_offset + 1}: {exc}"
            )
    copy_type_comments_to_annotations(args)

    return args, returns