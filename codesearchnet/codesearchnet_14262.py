def create_bot(src=None, grammar=NODEBOX, format=None, outputfile=None, iterations=1, buff=None, window=False,
               title=None, fullscreen=None, server=False, port=7777, show_vars=False, vars=None, namespace=None):
    """
    Create a canvas and a bot with the same canvas attached to it

    bot parameters
    :param grammar: DRAWBOT or NODEBOX - decides what kind of bot is created
    :param vars: preset dictionary of vars from the called

    canvas parameters:
    ... everything else ...

    See create_canvas for details on those parameters.

    """
    canvas = create_canvas(src, format, outputfile, iterations > 1, buff, window, title, fullscreen=fullscreen,
                           show_vars=show_vars)

    if grammar == DRAWBOT:
        from shoebot.grammar import DrawBot
        bot = DrawBot(canvas, namespace=namespace, vars=vars)
    else:
        from shoebot.grammar import NodeBot
        bot = NodeBot(canvas, namespace=namespace, vars=vars)

    if server:
        from shoebot.sbio import SocketServer
        socket_server = SocketServer(bot, "", port=port)
    return bot