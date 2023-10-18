def get_raw(config, backend_section, arthur):
    """Execute the raw phase for a given backend section, optionally using Arthur

    :param config: a Mordred config object
    :param backend_section: the backend section where the raw phase is executed
    :param arthur: if true, it enables Arthur to collect the raw data
    """

    if arthur:
        task = TaskRawDataArthurCollection(config, backend_section=backend_section)
    else:
        task = TaskRawDataCollection(config, backend_section=backend_section)

    TaskProjects(config).execute()
    try:
        task.execute()
        logging.info("Loading raw data finished!")
    except Exception as e:
        logging.error(str(e))
        sys.exit(-1)