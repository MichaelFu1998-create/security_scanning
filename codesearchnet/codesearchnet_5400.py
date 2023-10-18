def _sync_children(self, task_specs, state=MAYBE):
        """
        This method syncs up the task's children with the given list of task
        specs. In other words::

            - Add one child for each given TaskSpec, unless that child already
              exists.
            - Remove all children for which there is no spec in the given list,
              unless it is a "triggered" task.

        .. note::

           It is an error if the task has a non-predicted child that is
           not given in the TaskSpecs.

        :type  task_specs: list(TaskSpec)
        :param task_specs: The list of task specs that may become children.
        :type  state: integer
        :param state: The bitmask of states for the new children.
        """
        LOG.debug("Updating children for %s" % self.get_name())
        if task_specs is None:
            raise ValueError('"task_specs" argument is None')
        add = task_specs[:]

        # Create a list of all children that are no longer needed.
        remove = []
        for child in self.children:
            # Triggered tasks are never removed.
            if child.triggered:
                continue

            # Check whether the task needs to be removed.
            if child.task_spec in add:
                add.remove(child.task_spec)
                continue

            # Non-predicted tasks must not be removed, so they HAVE to be in
            # the given task spec list.
            if child._is_definite():
                raise WorkflowException(self.task_spec,
                                        'removal of non-predicted child %s' %
                                        repr(child))
            remove.append(child)

        # Remove and add the children accordingly.
        for child in remove:
            self.children.remove(child)
        for task_spec in add:
            self._add_child(task_spec, state)