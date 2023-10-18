def micro_mordred(cfg_path, backend_sections, raw, arthur, identities, enrich, panels):
    """Execute the raw and/or the enrich phases of a given backend section defined in a Mordred configuration file.

    :param cfg_path: the path of a Mordred configuration file
    :param backend_sections: the backend sections where the raw and/or enrich phases will be executed
    :param raw: if true, it activates the collection of raw data
    :param arthur: if true, it enables Arthur to collect the raw data
    :param identities: if true, it activates the identities merge in SortingHat
    :param enrich: if true, it activates the collection of enrich data
    :param panels: if true, it activates the upload of panels
    """

    config = Config(cfg_path)

    if raw:
        for backend in backend_sections:
            get_raw(config, backend, arthur)

    if identities:
        get_identities(config)

    if enrich:
        for backend in backend_sections:
            get_enrich(config, backend)

    if panels:
        get_panels(config)