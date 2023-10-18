def pop_option(function, name):
    """
    Used to remove an option applied by the @click.option decorator.

    This is useful for when you want to subclass a decorated resource command
    and *don't* want all of the options provided by the parent class'
    implementation.
    """
    for option in getattr(function, '__click_params__', tuple()):
        if option.name == name:
            function.__click_params__.remove(option)