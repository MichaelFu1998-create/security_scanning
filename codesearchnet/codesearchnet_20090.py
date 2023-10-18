def get_tasks():
    """Get the imported task classes for each task that will be run"""
    task_classes = []
    for task_path in TASKS:
        try:
            module, classname = task_path.rsplit('.', 1)
        except ValueError:
            raise ImproperlyConfigured('%s isn\'t a task module' % task_path)
        try:
            mod = import_module(module)
        except ImportError as e:
            raise ImproperlyConfigured('Error importing task %s: "%s"'
                                       % (module, e))
        try:
            task_class = getattr(mod, classname)
        except AttributeError:
            raise ImproperlyConfigured('Task module "%s" does not define a '
                                       '"%s" class' % (module, classname))
        task_classes.append(task_class)
    return task_classes