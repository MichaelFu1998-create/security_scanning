def _update_hook(self, my_task):
        """
        Typically this method should perform the following actions::

            - Update the state of the corresponding task.
            - Update the predictions for its successors.

        Returning non-False will cause the task to go into READY.
        Returning any other value will cause no action.
        """
        if my_task._is_predicted():
            self._predict(my_task)
        LOG.debug("'%s'._update_hook says parent (%s, state=%s) "
                  "is_finished=%s" % (self.name, my_task.parent.get_name(),
                                      my_task.parent.get_state_name(),
                                      my_task.parent._is_finished()))
        if not my_task.parent._is_finished():
            return
        self.entered_event.emit(my_task.workflow, my_task)
        my_task._ready()