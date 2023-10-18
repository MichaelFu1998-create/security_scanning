def update_memo(self, task_id, task, r):
        """Updates the memoization lookup table with the result from a task.

        Args:
             - task_id (int): Integer task id
             - task (dict) : A task dict from dfk.tasks
             - r (Result future): Result future

        A warning is issued when a hash collision occurs during the update.
        This is not likely.
        """
        if not self.memoize or not task['memoize']:
            return

        if task['hashsum'] in self.memo_lookup_table:
            logger.info('Updating appCache entry with latest %s:%s call' %
                        (task['func_name'], task_id))
            self.memo_lookup_table[task['hashsum']] = r
        else:
            self.memo_lookup_table[task['hashsum']] = r