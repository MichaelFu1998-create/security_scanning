def handle_exec_update(self, task_id, future):
        """This function is called only as a callback from an execution
        attempt reaching a final state (either successfully or failing).

        It will launch retries if necessary, and update the task
        structure.

        Args:
             task_id (string) : Task id which is a uuid string
             future (Future) : The future object corresponding to the task which
             makes this callback

        KWargs:
             memo_cbk(Bool) : Indicates that the call is coming from a memo update,
             that does not require additional memo updates.
        """

        try:
            res = future.result()
            if isinstance(res, RemoteExceptionWrapper):
                res.reraise()

        except Exception:
            logger.exception("Task {} failed".format(task_id))

            # We keep the history separately, since the future itself could be
            # tossed.
            self.tasks[task_id]['fail_history'].append(future._exception)
            self.tasks[task_id]['fail_count'] += 1

            if not self._config.lazy_errors:
                logger.debug("Eager fail, skipping retry logic")
                self.tasks[task_id]['status'] = States.failed
                if self.monitoring:
                    task_log_info = self._create_task_log_info(task_id, 'eager')
                    self.monitoring.send(MessageType.TASK_INFO, task_log_info)
                return

            if self.tasks[task_id]['fail_count'] <= self._config.retries:
                self.tasks[task_id]['status'] = States.pending
                logger.debug("Task {} marked for retry".format(task_id))

            else:
                logger.info("Task {} failed after {} retry attempts".format(task_id,
                                                                            self._config.retries))
                self.tasks[task_id]['status'] = States.failed
                self.tasks_failed_count += 1
                self.tasks[task_id]['time_returned'] = datetime.datetime.now()

        else:
            self.tasks[task_id]['status'] = States.done
            self.tasks_completed_count += 1

            logger.info("Task {} completed".format(task_id))
            self.tasks[task_id]['time_returned'] = datetime.datetime.now()

        if self.monitoring:
            task_log_info = self._create_task_log_info(task_id, 'lazy')
            self.monitoring.send(MessageType.TASK_INFO, task_log_info)

        # it might be that in the course of the update, we've gone back to being
        # pending - in which case, we should consider ourself for relaunch
        if self.tasks[task_id]['status'] == States.pending:
            self.launch_if_ready(task_id)

        return