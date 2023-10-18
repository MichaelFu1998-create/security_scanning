def put_multiple(self, task_args_kwargs_list):
        """put a list of tasks and their arguments

        This method can be used to put multiple tasks at once. Calling
        this method once with multiple tasks can be much faster than
        calling `put()` multiple times.

        Parameters
        ----------
        task_args_kwargs_list : list

            A list of lists with three items that can be parameters of
            `put()`, i.e., `task`, `args`, `kwargs`.

        Returns
        -------
        list
            A list of task IDs.

        """
        if not self.isopen:
            logger = logging.getLogger(__name__)
            logger.warning('the drop box is not open')
            return

        packages = [ ]
        for t in task_args_kwargs_list:
            try:
                task = t['task']
                args = t.get('args', ())
                kwargs = t.get('kwargs', {})
                package = TaskPackage(task=task, args=args, kwargs=kwargs)
            except TypeError:
                package = TaskPackage(task=t, args=(), kwargs={})
            packages.append(package)
        return self.dropbox.put_multiple(packages)