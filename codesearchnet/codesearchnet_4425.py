def launch_if_ready(self, task_id):
        """
        launch_if_ready will launch the specified task, if it is ready
        to run (for example, without dependencies, and in pending state).

        This should be called by any piece of the DataFlowKernel that
        thinks a task may have become ready to run.

        It is not an error to call launch_if_ready on a task that is not
        ready to run - launch_if_ready will not incorrectly launch that
        task.

        launch_if_ready is thread safe, so may be called from any thread
        or callback.
        """
        if self._count_deps(self.tasks[task_id]['depends']) == 0:

            # We can now launch *task*
            new_args, kwargs, exceptions = self.sanitize_and_wrap(task_id,
                                                                  self.tasks[task_id]['args'],
                                                                  self.tasks[task_id]['kwargs'])
            self.tasks[task_id]['args'] = new_args
            self.tasks[task_id]['kwargs'] = kwargs
            if not exceptions:
                # There are no dependency errors
                exec_fu = None
                # Acquire a lock, retest the state, launch
                with self.tasks[task_id]['task_launch_lock']:
                    if self.tasks[task_id]['status'] == States.pending:
                        exec_fu = self.launch_task(
                            task_id, self.tasks[task_id]['func'], *new_args, **kwargs)

                if exec_fu:

                    try:
                        exec_fu.add_done_callback(partial(self.handle_exec_update, task_id))
                    except Exception as e:
                        logger.error("add_done_callback got an exception {} which will be ignored".format(e))

                    self.tasks[task_id]['exec_fu'] = exec_fu
                    try:
                        self.tasks[task_id]['app_fu'].update_parent(exec_fu)
                        self.tasks[task_id]['exec_fu'] = exec_fu
                    except AttributeError as e:
                        logger.error(
                            "Task {}: Caught AttributeError at update_parent".format(task_id))
                        raise e
            else:
                logger.info(
                    "Task {} failed due to dependency failure".format(task_id))
                # Raise a dependency exception
                self.tasks[task_id]['status'] = States.dep_fail
                if self.monitoring is not None:
                    task_log_info = self._create_task_log_info(task_id, 'lazy')
                    self.monitoring.send(MessageType.TASK_INFO, task_log_info)

                try:
                    fu = Future()
                    fu.retries_left = 0
                    self.tasks[task_id]['exec_fu'] = fu
                    self.tasks[task_id]['app_fu'].update_parent(fu)
                    fu.set_exception(DependencyError(exceptions,
                                                     task_id,
                                                     None))

                except AttributeError as e:
                    logger.error(
                        "Task {} AttributeError at update_parent".format(task_id))
                    raise e