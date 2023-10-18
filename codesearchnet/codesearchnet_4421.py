def _create_task_log_info(self, task_id, fail_mode=None):
        """
        Create the dictionary that will be included in the log.
        """

        info_to_monitor = ['func_name', 'fn_hash', 'memoize', 'checkpoint', 'fail_count',
                           'fail_history', 'status', 'id', 'time_submitted', 'time_returned', 'executor']

        task_log_info = {"task_" + k: self.tasks[task_id][k] for k in info_to_monitor}
        task_log_info['run_id'] = self.run_id
        task_log_info['timestamp'] = datetime.datetime.now()
        task_log_info['task_status_name'] = self.tasks[task_id]['status'].name
        task_log_info['tasks_failed_count'] = self.tasks_failed_count
        task_log_info['tasks_completed_count'] = self.tasks_completed_count
        task_log_info['task_inputs'] = str(self.tasks[task_id]['kwargs'].get('inputs', None))
        task_log_info['task_outputs'] = str(self.tasks[task_id]['kwargs'].get('outputs', None))
        task_log_info['task_stdin'] = self.tasks[task_id]['kwargs'].get('stdin', None)
        task_log_info['task_stdout'] = self.tasks[task_id]['kwargs'].get('stdout', None)
        task_log_info['task_depends'] = None
        if self.tasks[task_id]['depends'] is not None:
            task_log_info['task_depends'] = ",".join([str(t._tid) for t in self.tasks[task_id]['depends']])
        task_log_info['task_elapsed_time'] = None
        if self.tasks[task_id]['time_returned'] is not None:
            task_log_info['task_elapsed_time'] = (self.tasks[task_id]['time_returned'] -
                                                  self.tasks[task_id]['time_submitted']).total_seconds()
        if fail_mode is not None:
            task_log_info['task_fail_mode'] = fail_mode
        return task_log_info