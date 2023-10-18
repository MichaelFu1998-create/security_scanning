def check_memo(self, task_id, task):
        """Create a hash of the task and its inputs and check the lookup table for this hash.

        If present, the results are returned. The result is a tuple indicating whether a memo
        exists and the result, since a Null result is possible and could be confusing.
        This seems like a reasonable option without relying on an cache_miss exception.

        Args:
            - task(task) : task from the dfk.tasks table

        Returns:
            Tuple of the following:
            - present (Bool): Is this present in the memo_lookup_table
            - Result (Py Obj): Result of the function if present in table

        This call will also set task['hashsum'] to the unique hashsum for the func+inputs.
        """
        if not self.memoize or not task['memoize']:
            task['hashsum'] = None
            return None, None

        hashsum = self.make_hash(task)
        present = False
        result = None
        if hashsum in self.memo_lookup_table:
            present = True
            result = self.memo_lookup_table[hashsum]
            logger.info("Task %s using result from cache", task_id)

        task['hashsum'] = hashsum
        return present, result