def validate(self):
        """Checks integrity of workflow and reports any problems with it.

        Detects:
        - loops (tasks that wait on each other in a loop)
        :returns: empty list if valid, a list of errors if not
        """
        results = []
        from ..specs import Join

        def recursive_find_loop(task, history):
            current = history[:]
            current.append(task)
            if isinstance(task, Join):
                if task in history:
                    msg = "Found loop with '%s': %s then '%s' again" % (
                        task.name, '->'.join([p.name for p in history]),
                        task.name)
                    raise Exception(msg)
                for predecessor in task.inputs:
                    recursive_find_loop(predecessor, current)

            for parent in task.inputs:
                recursive_find_loop(parent, current)

        for task_id, task in list(self.task_specs.items()):
            # Check for cyclic waits
            try:
                recursive_find_loop(task, [])
            except Exception as exc:
                results.append(exc.__str__())

            # Check for disconnected tasks
            if not task.inputs and task.name not in ['Start', 'Root']:
                if task.outputs:
                    results.append("Task '%s' is disconnected (no inputs)" %
                                   task.name)
                else:
                    LOG.debug("Task '%s' is not being used" % task.name)

        return results