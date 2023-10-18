def _on_trigger(self, my_task):
        """
        Enqueue a trigger, such that this tasks triggers multiple times later
        when _on_complete() is called.
        """
        self.queued += 1
        # All tasks that have already completed need to be put back to
        # READY.
        for thetask in my_task.workflow.task_tree:
            if thetask.thread_id != my_task.thread_id:
                continue
            if (thetask.task_spec == self and
                    thetask._has_state(Task.COMPLETED)):
                thetask._set_state(Task.FUTURE, True)
                thetask._ready()