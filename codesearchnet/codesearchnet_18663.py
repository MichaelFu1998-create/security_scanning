def out(format_msg="", *args, **kwargs):
    '''print format_msg to stdout, taking into account --quiet setting'''
    logmethod = kwargs.get("logmethod", stdout.info)

    if format_msg != "":
        if Prefix.has():
            if isinstance(format_msg, basestring):
                format_msg = Prefix.get() + format_msg
            else:
                format_msg = Prefix.get() + str(format_msg)

        if isinstance(format_msg, basestring):
            if args or kwargs:
                s = format_msg.format(*args, **kwargs)
            else:
                s = format_msg
            logmethod(s)
#             width = globals()["width"]
#             s = textwrap.fill(s, width=width)
#             stdout.info(s)

        else:
            logmethod(str(format_msg))

    else:
        logmethod("")