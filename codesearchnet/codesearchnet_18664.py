def verbose(format_msg="", *args, **kwargs):
    '''print format_msg to stdout, taking into account --verbose flag'''
    kwargs["logmethod"] = stdout.debug
    out(format_msg, *args, **kwargs)