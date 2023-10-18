def get_identities(config):
    """Execute the merge identities phase

    :param config: a Mordred config object
    """

    TaskProjects(config).execute()
    task = TaskIdentitiesMerge(config)
    task.execute()
    logging.info("Merging identities finished!")