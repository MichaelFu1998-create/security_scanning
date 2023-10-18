def p_action(p):
    """
    action : CLIENT_KWD KEY DOT KEY LPAREN args RPAREN
    action : SERVER_KWD KEY DOT KEY LPAREN args RPAREN
    action : CLIENT_KWD KEY DOT KEY LPAREN args RPAREN IF_KWD REGEX_MATCH_INCOMING_KWD LPAREN p_string_arg RPAREN
    action : SERVER_KWD KEY DOT KEY LPAREN args RPAREN IF_KWD REGEX_MATCH_INCOMING_KWD LPAREN p_string_arg RPAREN
    """
    if len(p)==8:
        p[0] = [p[1], p[2], p[4], p[6], None]
    elif len(p)==13:
        p[0] = [p[1], p[2], p[4], p[6], p[11]]