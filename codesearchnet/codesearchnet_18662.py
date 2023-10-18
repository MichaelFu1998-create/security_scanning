def err(format_msg, *args, **kwargs):
    '''print format_msg to stderr'''
    exc_info = kwargs.pop("exc_info", False)
    stderr.warning(str(format_msg).format(*args, **kwargs), exc_info=exc_info)