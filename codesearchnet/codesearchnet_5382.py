def _on_complete_hook(self, my_task):
        """
        Runs the task. Should not be called directly.
        Returns True if completed, False otherwise.
        """
        # Find all matching conditions.
        outputs = []
        for condition, output in self.cond_task_specs:
            if self.choice is not None and output not in self.choice:
                continue
            if condition is None:
                outputs.append(self._wf_spec.get_task_spec_from_name(output))
                continue
            if not condition._matches(my_task):
                continue
            outputs.append(self._wf_spec.get_task_spec_from_name(output))

        my_task._sync_children(outputs, Task.FUTURE)
        for child in my_task.children:
            child.task_spec._update(child)