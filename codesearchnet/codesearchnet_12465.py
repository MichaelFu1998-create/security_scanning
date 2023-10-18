def fix_remaining_type_comments(node):
    """Converts type comments in `node` to proper annotated assignments."""
    assert node.type == syms.file_input

    last_n = None
    for n in node.post_order():
        if last_n is not None:
            if n.type == token.NEWLINE and is_assignment(last_n):
                fix_variable_annotation_type_comment(n, last_n)
            elif n.type == syms.funcdef and last_n.type == syms.suite:
                fix_signature_annotation_type_comment(n, last_n, offset=1)
            elif n.type == syms.async_funcdef and last_n.type == syms.suite:
                fix_signature_annotation_type_comment(n, last_n, offset=2)
        last_n = n