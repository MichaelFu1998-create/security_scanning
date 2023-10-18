def launch_task(self, task_id, executable, *args, **kwargs):
        """Handle the actual submission of the task to the executor layer.

        If the app task has the executors attributes not set (default=='all')
        the task is launched on a randomly selected executor from the
        list of executors. This behavior could later be updated to support
        binding to executors based on user specified criteria.

        If the app task specifies a particular set of executors, it will be
        targeted at those specific executors.

        Args:
            task_id (uuid string) : A uuid string that uniquely identifies the task
            executable (callable) : A callable object
            args (list of positional args)
            kwargs (arbitrary keyword arguments)


        Returns:
            Future that tracks the execution of the submitted executable
        """
        self.tasks[task_id]['time_submitted'] = datetime.datetime.now()

        hit, memo_fu = self.memoizer.check_memo(task_id, self.tasks[task_id])
        if hit:
            logger.info("Reusing cached result for task {}".format(task_id))
            return memo_fu

        executor_label = self.tasks[task_id]["executor"]
        try:
            executor = self.executors[executor_label]
        except Exception:
            logger.exception("Task {} requested invalid executor {}: config is\n{}".format(task_id, executor_label, self._config))

        if self.monitoring is not None and self.monitoring.resource_monitoring_enabled:
            executable = self.monitoring.monitor_wrapper(executable, task_id,
                                                         self.monitoring.monitoring_hub_url,
                                                         self.run_id,
                                                         self.monitoring.resource_monitoring_interval)

        with self.submitter_lock:
            exec_fu = executor.submit(executable, *args, **kwargs)
        self.tasks[task_id]['status'] = States.launched
        if self.monitoring is not None:
            task_log_info = self._create_task_log_info(task_id, 'lazy')
            self.monitoring.send(MessageType.TASK_INFO, task_log_info)

        exec_fu.retries_left = self._config.retries - \
            self.tasks[task_id]['fail_count']
        logger.info("Task {} launched on executor {}".format(task_id, executor.label))
        return exec_fu