def eventhandler(*args, **kwargs):
    """
    Decorator.  Marks a function as a receiver for the specified slack event(s).

    * events - String or list of events to handle
    """

    def wrapper(func):
        if isinstance(kwargs['events'], basestring):
            kwargs['events'] = [kwargs['events']]
        func.is_eventhandler = True
        func.events = kwargs['events']
        return func

    return wrapper