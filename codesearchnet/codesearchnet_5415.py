def _send_call(self, my_task):
        """Sends Celery asynchronous call and stores async call information for
        retrieval laster"""
        args, kwargs = None, None
        if self.args:
            args = _eval_args(self.args, my_task)
        if self.kwargs:
            kwargs = _eval_kwargs(self.kwargs, my_task)
        LOG.debug(
            "%s (task id %s) calling %s" % (self.name, my_task.id, self.call),
            extra=dict(data=dict(args=args, kwargs=kwargs)))
        async_call = default_app.send_task(self.call, args=args, kwargs=kwargs)
        my_task._set_internal_data(task_id=async_call.task_id)
        my_task.async_call = async_call
        LOG.debug("'%s' called: %s" % (self.call, my_task.async_call.task_id))