def p_transition(p):
    """
    transition : START_KWD KEY NULL_KWD FLOAT
    transition : KEY KEY NULL_KWD FLOAT
    transition : KEY END_KWD NULL_KWD FLOAT
    transition : START_KWD KEY KEY FLOAT
    transition : KEY KEY KEY FLOAT
    transition : KEY END_KWD KEY FLOAT
    transition : START_KWD KEY NULL_KWD INTEGER
    transition : KEY KEY NULL_KWD INTEGER
    transition : KEY END_KWD NULL_KWD INTEGER
    transition : START_KWD KEY KEY INTEGER
    transition : KEY KEY KEY INTEGER
    transition : KEY END_KWD KEY INTEGER
    transition : START_KWD KEY NULL_KWD KEY
    transition : KEY KEY NULL_KWD KEY
    transition : KEY END_KWD NULL_KWD KEY
    transition : START_KWD KEY KEY KEY
    transition : KEY KEY KEY KEY
    transition : KEY END_KWD KEY KEY
    """
    p[3] = None if p[3] == 'NULL' else p[3]
    if p[4] == 'error':
        p[0] = MarionetteTransition(p[1], p[2], p[3], 0, True)
    else:
        p[0] = MarionetteTransition(p[1], p[2], p[3], p[4], False)