def smush_config(sources, initial=None):
    """Merge the configuration sources and return the resulting DotDict."""
    if initial is None:
        initial = {}
    config = DotDict(initial)

    for fn in sources:
        log.debug('Merging %s', fn)
        mod = get_config_module(fn)
        config = mod.update(config)
        log.debug('Current config:\n%s', json.dumps(config, indent=4,
                                                    cls=LenientJSONEncoder))
    return config