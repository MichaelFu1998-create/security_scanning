def get_panels(config):
    """Execute the panels phase

    :param config: a Mordred config object
    """

    task = TaskPanels(config)
    task.execute()

    task = TaskPanelsMenu(config)
    task.execute()

    logging.info("Panels creation finished!")