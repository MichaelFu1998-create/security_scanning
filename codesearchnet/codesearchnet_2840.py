def add_task_hook(self, task_hook):
    """Registers a specified task hook to this context

    :type task_hook: heron.instance.src.python.utils.topology.ITaskHook
    :param task_hook: Implementation of ITaskHook
    """
    if not isinstance(task_hook, ITaskHook):
      raise TypeError("In add_task_hook(): attempt to add non ITaskHook instance, given: %s"
                      % str(type(task_hook)))
    self.task_hooks.append(task_hook)