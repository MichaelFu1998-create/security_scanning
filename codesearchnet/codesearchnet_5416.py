def _restart(self, my_task):
        """ Abort celery task and retry it"""
        if not my_task._has_state(Task.WAITING):
            raise WorkflowException(my_task, "Cannot refire a task that is not"
                                    "in WAITING state")
        # Check state of existing call and abort it (save history)
        if my_task._get_internal_data('task_id') is not None:
            if not hasattr(my_task, 'async_call'):
                task_id = my_task._get_internal_data('task_id')
                my_task.async_call = default_app.AsyncResult(task_id)
                my_task.deserialized = True
                my_task.async_call.state  # manually refresh
            async_call = my_task.async_call
            if async_call.state == 'FAILED':
                pass
            elif async_call.state in ['RETRY', 'PENDING', 'STARTED']:
                async_call.revoke()
                LOG.info("Celery task '%s' was in %s state and was revoked" % (
                    async_call.state, async_call))
            elif async_call.state == 'SUCCESS':
                LOG.warning("Celery task '%s' succeeded, but a refire was "
                            "requested" % async_call)
            self._clear_celery_task_data(my_task)
        # Retrigger
        return self._start(my_task)