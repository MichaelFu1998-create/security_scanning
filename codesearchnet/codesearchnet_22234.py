def selected_course(func):
    """
    Passes the selected course as the first argument to func.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        course = Course.get_selected()
        return func(course, *args, **kwargs)
    return inner