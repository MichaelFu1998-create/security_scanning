def put(self, task, *args, **kwargs):
        """put a task and its arguments

        If you need to put multiple tasks, it can be faster to put
        multiple tasks with `put_multiple()` than to use this method
        multiple times.

        Parameters
        ----------
        task : a function
            A function to be executed
        args : list
            A list of positional arguments to the `task`
        kwargs : dict
            A dict with keyword arguments to the `task`

        Returns
        -------
        int, str, or any hashable and sortable
            A task ID. IDs are sortable in the order in which the
            corresponding tasks are put.

        """
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return
        package = TaskPackage(task=task, args=args, kwargs=kwargs)
        return self.dropbox.put(package)