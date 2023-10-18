def p_action_block(p):
    """
    action_block : ACTION_KWD KEY COLON actions
    """
    p[0] = []
    for i in range(len(p[4])):
        p[0] += [marionette_tg.action.MarionetteAction(p[2], p[4][i][0],
                                                          p[4][i][1],
                                                          p[4][i][2],
                                                          p[4][i][3],
                                                          p[4][i][4])]