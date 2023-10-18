def task(func, **config):
    """Declare a function or method to be a Yaz task

    @yaz.task
    def talk(message: str = "Hello World!"):
        return message

    Or... group multiple tasks together

    class Tools(yaz.Plugin):
        @yaz.task
        def say(self, message: str = "Hello World!"):
            return message

        @yaz.task(option__choices=["A", "B", "C"])
        def choose(self, option: str = "A"):
            return option
    """
    if func.__name__ == func.__qualname__:
        assert not func.__qualname__ in _task_list, "Can not define the same task \"{}\" twice".format(func.__qualname__)
        logger.debug("Found task %s", func)
        _task_list[func.__qualname__] = Task(plugin_class=None, func=func, config=config)
    else:
        func.yaz_task_config = config

    return func