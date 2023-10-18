def execute_tools(config, path, progress=None):
    """
    Executes the suite of TidyPy tools upon the project and returns the
    issues that are found.

    :param config: the TidyPy configuration to use
    :type config: dict
    :param path: that path to the project to analyze
    :type path: str
    :param progress:
        the progress reporter object that will receive callbacks during the
        execution of the tool suite. If not specified, not progress
        notifications will occur.
    :type progress: tidypy.Progress
    :rtype: tidypy.Collector
    """

    progress = progress or QuietProgress()
    progress.on_start()

    manager = SyncManager()
    manager.start()

    num_tools = 0
    tools = manager.Queue()
    for name, cls in iteritems(get_tools()):
        if config[name]['use'] and cls.can_be_used():
            num_tools += 1
            tools.put({
                'name': name,
                'config': config[name],
            })

    collector = Collector(config)
    if not num_tools:
        progress.on_finish()
        return collector

    notifications = manager.Queue()
    environment = manager.dict({
        'finder': Finder(path, config),
    })

    workers = []
    for _ in range(config['workers']):
        worker = Worker(
            args=(
                tools,
                notifications,
                environment,
            ),
        )
        worker.start()
        workers.append(worker)

    while num_tools:
        try:
            notification = notifications.get(True, 0.25)
        except Empty:
            pass
        else:
            if notification['type'] == 'start':
                progress.on_tool_start(notification['tool'])
            elif notification['type'] == 'complete':
                collector.add_issues(notification['issues'])
                progress.on_tool_finish(notification['tool'])
                num_tools -= 1

    progress.on_finish()

    return collector