def _obj_display(obj, display=''):
    """Returns string representation of an object, either the default or based
    on the display template passed in.
    """
    result = ''
    if not display:
        result = str(obj)
    else:
        template = Template(display)
        context = Context({'obj':obj})
        result = template.render(context)

    return result