def copy_type_comments_to_annotations(args):
    """Copies argument type comments from the legacy long form to annotations
    in the entire function signature.
    """
    for arg in args.args:
        copy_type_comment_to_annotation(arg)

    if args.vararg:
        copy_type_comment_to_annotation(args.vararg)

    for arg in args.kwonlyargs:
        copy_type_comment_to_annotation(arg)

    if args.kwarg:
        copy_type_comment_to_annotation(args.kwarg)