def use(**kwargs):
    """
    Updates the active resource configuration to the passed
    keyword arguments.

    Invoking this method without passing arguments will just return the
    active resource configuration.

    @returns
        The previous configuration.
    """
    config = dict(use.config)
    use.config.update(kwargs)
    return config