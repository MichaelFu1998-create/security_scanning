def create_pipe_workers(configfile, directory):
    """
        Creates the workers based on the given configfile to provide named pipes in the directory.
    """
    type_map = {'service': ServiceSearch,
                'host': HostSearch, 'range': RangeSearch,
                'user': UserSearch}
    config = configparser.ConfigParser()
    config.read(configfile)

    if not len(config.sections()):
        print_error("No named pipes configured")
        return

    print_notification("Starting {} pipes in directory {}".format(
        len(config.sections()), directory))

    workers = []
    for name in config.sections():
        section = config[name]
        query = create_query(section)
        object_type = type_map[section['type']]
        args = (name, os.path.join(directory, name), object_type, query,
                section['format'], bool(section.get('unique', 0)))
        workers.append(multiprocessing.Process(target=pipe_worker, args=args))

    return workers