def _select_block(str_in, start_tag, end_tag):
    """Select first block delimited by start_tag and end_tag"""
    start_pos = str_in.find(start_tag)
    if start_pos < 0:
        raise ValueError('start_tag not found')
    depth = 0
    for pos in range(start_pos, len(str_in)):
        if str_in[pos] == start_tag:
            depth += 1
        elif str_in[pos] == end_tag:
            depth -= 1

        if depth == 0:
            break
    sel = str_in[start_pos + 1:pos]
    return sel