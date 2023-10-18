def put(xy, *args):
    """
    put text on on screen
    a tuple as first argument tells absolute position for the text
    does not change TermCursor position
    args = list of optional position, formatting tokens and strings
    """
    cmd = [TermCursor.save, TermCursor.move(*xy), ''.join(args), TermCursor.restore]
    write(''.join(cmd))