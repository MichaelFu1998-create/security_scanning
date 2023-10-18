def copy_arguments_to_annotations(args, type_comment, *, is_method=False):
    """Copies AST nodes from `type_comment` into the ast3.arguments in `args`.

    Does validaation of argument count (allowing for untyped self/cls)
    and type (vararg and kwarg).
    """
    if isinstance(type_comment, ast3.Ellipsis):
        return

    expected = len(args.args)
    if args.vararg:
        expected += 1
    expected += len(args.kwonlyargs)
    if args.kwarg:
        expected += 1
    actual = len(type_comment) if isinstance(type_comment, list) else 1
    if expected != actual:
        if is_method and expected - actual == 1:
            pass  # fine, we're just skipping `self`, `cls`, etc.
        else:
            raise ValueError(
                f"number of arguments in type comment doesn't match; " +
                f"expected {expected}, found {actual}"
            )

    if isinstance(type_comment, list):
        next_value = type_comment.pop
    else:
        # If there's just one value, only one of the loops and ifs below will
        # be populated. We ensure this with the expected/actual length check
        # above.
        _tc = type_comment

        def next_value(index: int = 0) -> ast3.expr:
            return _tc

    for arg in args.args[expected - actual:]:
        ensure_no_annotation(arg.annotation)
        arg.annotation = next_value(0)

    if args.vararg:
        ensure_no_annotation(args.vararg.annotation)
        args.vararg.annotation = next_value(0)

    for arg in args.kwonlyargs:
        ensure_no_annotation(arg.annotation)
        arg.annotation = next_value(0)

    if args.kwarg:
        ensure_no_annotation(args.kwarg.annotation)
        args.kwarg.annotation = next_value(0)