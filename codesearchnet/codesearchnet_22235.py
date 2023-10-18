def selected_exercise(func):
    """
    Passes the selected exercise as the first argument to func.
    """
    @wraps(func)
    def inner(*args, **kwargs):
        exercise = Exercise.get_selected()
        return func(exercise, *args, **kwargs)
    return inner