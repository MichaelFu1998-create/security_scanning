def prepare_options(options):
    """Create options and verbose options from strings and non-string iterables in
    `options` array.
    """
    options_, verbose_options = [], []
    for option in options:
        if is_string(option):
            options_.append(option)
            verbose_options.append(option)
        else:
            options_.append(option[0])
            verbose_options.append(option[1])
    return options_, verbose_options