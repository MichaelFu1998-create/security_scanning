def _join_itemstrs(itemstrs, itemsep, newlines, _leaf_info, nobraces,
                   trailing_sep, compact_brace, lbr, rbr):
    """
    Joins string-ified items with separators newlines and container-braces.
    """
    # positive newlines means start counting from the root
    use_newline = newlines > 0

    # negative countdown values mean start counting from the leafs
    # if compact_brace < 0:
    #     compact_brace = (-compact_brace) >= _leaf_info['max_height']
    if newlines < 0:
        use_newline = (-newlines) < _leaf_info['max_height']

    if use_newline:
        sep = ',\n'
        if nobraces:
            body_str = sep.join(itemstrs)
            if trailing_sep and len(itemstrs) > 0:
                body_str += ','
            retstr = body_str
        else:
            if compact_brace:
                # Why must we modify the indentation below and not here?
                # prefix = ''
                # rest = [ub.indent(s, prefix) for s in itemstrs[1:]]
                # indented = itemstrs[0:1] + rest
                indented = itemstrs
            else:
                import ubelt as ub
                prefix = ' ' * 4
                indented = [ub.indent(s, prefix) for s in itemstrs]

            body_str = sep.join(indented)
            if trailing_sep and len(itemstrs) > 0:
                body_str += ','
            if compact_brace:
                # Why can we modify the indentation here but not above?
                braced_body_str = (lbr + body_str.replace('\n', '\n ') + rbr)
            else:
                braced_body_str = (lbr + '\n' + body_str + '\n' + rbr)
            retstr = braced_body_str
    else:
        sep = ',' + itemsep
        body_str = sep.join(itemstrs)
        if trailing_sep and len(itemstrs) > 0:
            body_str += ','
        retstr  = (lbr + body_str +  rbr)
    return retstr