def p_action_blocks(p):
    """
    action_blocks : action_blocks action_block
    """
    if isinstance(p[1], list):
        if isinstance(p[1][0], list):
            p[0] = p[1][0] + [p[2]]
        else:
            p[0] = p[1] + p[2]
    else:
        p[0] = [p[1], p[2]]