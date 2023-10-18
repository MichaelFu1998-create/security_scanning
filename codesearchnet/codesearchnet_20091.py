def get_task_options():
    """Get the options for each task that will be run"""
    options = ()

    task_classes = get_tasks()
    for cls in task_classes:
        options += cls.option_list

    return options