def get_task_tree(white_list=None):
    """Returns a tree of Task instances

    The tree is comprised of dictionaries containing strings for
    keys and either dictionaries or Task instances for values.

    When WHITE_LIST is given, only the tasks and plugins in this
    list will become part of the task tree.  The WHITE_LIST may
    contain either strings, corresponding to the task of plugin
    __qualname__, or, preferable, the WHITE_LIST contains
    links to the task function or plugin class instead.
    """
    assert white_list is None or isinstance(white_list, list), type(white_list)

    if white_list is not None:
        white_list = set(item if isinstance(item, str) else item.__qualname__ for item in white_list)

    tree = dict((task.qualified_name, task)
                for task
                in _task_list.values()
                if white_list is None or task.qualified_name in white_list)

    plugins = get_plugin_list()
    for plugin in [plugin for plugin in plugins.values() if white_list is None or plugin.__qualname__ in white_list]:
        tasks = [func
                 for _, func
                 in inspect.getmembers(plugin)
                 if inspect.isfunction(func) and hasattr(func, "yaz_task_config")]
        if len(tasks) == 0:
            continue

        node = tree
        for name in plugin.__qualname__.split("."):
            if not name in node:
                node[name] = {}
            node = node[name]

        for func in tasks:
            logger.debug("Found task %s", func)
            node[func.__name__] = Task(plugin_class=plugin, func=func, config=func.yaz_task_config)

    return tree