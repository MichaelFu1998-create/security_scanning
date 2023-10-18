def resettable(f):
    """A decorator to simplify the context management of simple object
    attributes. Gets the value of the attribute prior to setting it, and stores
    a function to set the value to the old value in the HistoryManager.
    """

    def wrapper(self, new_value):
        context = get_context(self)
        if context:
            old_value = getattr(self, f.__name__)
            # Don't clutter the context with unchanged variables
            if old_value == new_value:
                return
            context(partial(f, self, old_value))

        f(self, new_value)

    return wrapper