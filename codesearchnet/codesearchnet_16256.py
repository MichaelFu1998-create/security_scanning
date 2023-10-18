def pydevd(context):
    """
    Start a pydev settrace
    """
    global pdevd_not_available
    if pdevd_not_available:
        return ''
    try:
        import pydevd
    except ImportError:
        pdevd_not_available = True
        return ''
    render = lambda s: template.Template(s).render(context)
    availables = get_variables(context)
    for var in availables:
        locals()[var] = context[var]
    #catch the case where no client is listening
    try:
        pydevd.settrace()
    except socket.error:
        pdevd_not_available = True
    return ''