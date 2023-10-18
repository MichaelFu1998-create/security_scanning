def do_engine_steps(self):
        """
        Execute any READY tasks that are engine specific (for example, gateways
        or script tasks). This is done in a loop, so it will keep completing
        those tasks until there are only READY User tasks, or WAITING tasks
        left.
        """
        assert not self.read_only
        engine_steps = list(
            [t for t in self.get_tasks(Task.READY)
             if self._is_engine_task(t.task_spec)])
        while engine_steps:
            for task in engine_steps:
                task.complete()
            engine_steps = list(
                [t for t in self.get_tasks(Task.READY)
                 if self._is_engine_task(t.task_spec)])