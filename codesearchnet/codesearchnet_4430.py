def submit(self, func, *args, executors='all', fn_hash=None, cache=False, **kwargs):
        """Add task to the dataflow system.

        If the app task has the executors attributes not set (default=='all')
        the task will be launched on a randomly selected executor from the
        list of executors. If the app task specifies a particular set of
        executors, it will be targeted at the specified executors.

        >>> IF all deps are met:
        >>>   send to the runnable queue and launch the task
        >>> ELSE:
        >>>   post the task in the pending queue

        Args:
            - func : A function object
            - *args : Args to the function

        KWargs :
            - executors (list or string) : List of executors this call could go to.
                    Default='all'
            - fn_hash (Str) : Hash of the function and inputs
                    Default=None
            - cache (Bool) : To enable memoization or not
            - kwargs (dict) : Rest of the kwargs to the fn passed as dict.

        Returns:
               (AppFuture) [DataFutures,]

        """

        if self.cleanup_called:
            raise ValueError("Cannot submit to a DFK that has been cleaned up")

        task_id = self.task_count
        self.task_count += 1
        if isinstance(executors, str) and executors.lower() == 'all':
            choices = list(e for e in self.executors if e != 'data_manager')
        elif isinstance(executors, list):
            choices = executors
        executor = random.choice(choices)

        # Transform remote input files to data futures
        args, kwargs = self._add_input_deps(executor, args, kwargs)

        task_def = {'depends': None,
                    'executor': executor,
                    'func': func,
                    'func_name': func.__name__,
                    'args': args,
                    'kwargs': kwargs,
                    'fn_hash': fn_hash,
                    'memoize': cache,
                    'callback': None,
                    'exec_fu': None,
                    'checkpoint': None,
                    'fail_count': 0,
                    'fail_history': [],
                    'env': None,
                    'status': States.unsched,
                    'id': task_id,
                    'time_submitted': None,
                    'time_returned': None,
                    'app_fu': None}

        if task_id in self.tasks:
            raise DuplicateTaskError(
                "internal consistency error: Task {0} already exists in task list".format(task_id))
        else:
            self.tasks[task_id] = task_def

        # Get the dep count and a list of dependencies for the task
        dep_cnt, depends = self._gather_all_deps(args, kwargs)
        self.tasks[task_id]['depends'] = depends

        # Extract stdout and stderr to pass to AppFuture:
        task_stdout = kwargs.get('stdout')
        task_stderr = kwargs.get('stderr')

        logger.info("Task {} submitted for App {}, waiting on tasks {}".format(task_id,
                                                                               task_def['func_name'],
                                                                               [fu.tid for fu in depends]))

        self.tasks[task_id]['task_launch_lock'] = threading.Lock()
        app_fu = AppFuture(tid=task_id,
                           stdout=task_stdout,
                           stderr=task_stderr)

        self.tasks[task_id]['app_fu'] = app_fu
        app_fu.add_done_callback(partial(self.handle_app_update, task_id))
        self.tasks[task_id]['status'] = States.pending
        logger.debug("Task {} set to pending state with AppFuture: {}".format(task_id, task_def['app_fu']))

        # at this point add callbacks to all dependencies to do a launch_if_ready
        # call whenever a dependency completes.

        # we need to be careful about the order of setting the state to pending,
        # adding the callbacks, and caling launch_if_ready explicitly once always below.

        # I think as long as we call launch_if_ready once after setting pending, then
        # we can add the callback dependencies at any point: if the callbacks all fire
        # before then, they won't cause a launch, but the one below will. if they fire
        # after we set it pending, then the last one will cause a launch, and the
        # explicit one won't.

        for d in depends:

            def callback_adapter(dep_fut):
                self.launch_if_ready(task_id)

            try:
                d.add_done_callback(callback_adapter)
            except Exception as e:
                logger.error("add_done_callback got an exception {} which will be ignored".format(e))

        self.launch_if_ready(task_id)

        return task_def['app_fu']