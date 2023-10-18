def get_default_config():
    """
    Produces a stock/out-of-the-box TidyPy configuration.

    :rtype: dict
    """

    config = {}

    for name, cls in iteritems(get_tools()):
        config[name] = cls.get_default_config()

    try:
        workers = multiprocessing.cpu_count() - 1
    except NotImplementedError:  # pragma: no cover
        workers = 1
    workers = max(1, min(4, workers))

    config.update({
        'exclude': [],
        'merge-issues': True,
        'workers': workers,
        'requested_reports': [
            {
                'type': 'console',
            },
        ],
        'disabled': [],
        'noqa': True,
        'extends': [],
        'ignore-missing-extends': False,
    })

    return config