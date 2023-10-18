def get_offset_and_prefix(body, skip_assignments=False):
    """Returns the offset after which a statement can be inserted to the `body`.

    This offset is calculated to come after all imports, and maybe existing
    (possibly annotated) assignments if `skip_assignments` is True.

    Also returns the indentation prefix that should be applied to the inserted
    node.
    """
    assert body.type in (syms.file_input, syms.suite)

    _offset = 0
    prefix = ''
    for _offset, child in enumerate(body.children):
        if child.type == syms.simple_stmt:
            stmt = child.children[0]
            if stmt.type == syms.expr_stmt:
                expr = stmt.children
                if not skip_assignments:
                    break

                if (
                    len(expr) != 2 or
                    expr[0].type != token.NAME or
                    expr[1].type != syms.annassign or
                    _eq in expr[1].children
                ):
                    break

            elif stmt.type not in (syms.import_name, syms.import_from, token.STRING):
                break

        elif child.type == token.INDENT:
            assert isinstance(child, Leaf)
            prefix = child.value
        elif child.type != token.NEWLINE:
            break

    prefix, child.prefix = child.prefix, prefix
    return _offset, prefix