def get_enrich(config, backend_section):
    """Execute the enrich phase for a given backend section

    :param config: a Mordred config object
    :param backend_section: the backend section where the enrich phase is executed
    """

    TaskProjects(config).execute()
    task = TaskEnrich(config, backend_section=backend_section)
    try:
        task.execute()
        logging.info("Loading enriched data finished!")
    except Exception as e:
        logging.error(str(e))
        sys.exit(-1)