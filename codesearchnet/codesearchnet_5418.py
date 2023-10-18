def _start(self, my_task, force=False):
        """Returns False when successfully fired, True otherwise"""

        # Deserialize async call if necessary
        if not hasattr(my_task, 'async_call') and \
                my_task._get_internal_data('task_id') is not None:
            task_id = my_task._get_internal_data('task_id')
            my_task.async_call = default_app.AsyncResult(task_id)
            my_task.deserialized = True
            LOG.debug("Reanimate AsyncCall %s" % task_id)

        # Make the call if not already done
        if not hasattr(my_task, 'async_call'):
            self._send_call(my_task)

        # Get call status (and manually refresh if deserialized)
        if getattr(my_task, "deserialized", False):
            my_task.async_call.state  # must manually refresh if deserialized
        if my_task.async_call.state == 'FAILURE':
            LOG.debug("Async Call for task '%s' failed: %s" % (
                my_task.get_name(), my_task.async_call.info))
            info = {}
            info['traceback'] = my_task.async_call.traceback
            info['info'] = Serializable(my_task.async_call.info)
            info['state'] = my_task.async_call.state
            my_task._set_internal_data(task_state=info)
        elif my_task.async_call.state == 'RETRY':
            info = {}
            info['traceback'] = my_task.async_call.traceback
            info['info'] = Serializable(my_task.async_call.info)
            info['state'] = my_task.async_call.state
            my_task._set_internal_data(task_state=info)
        elif my_task.async_call.ready():
            result = my_task.async_call.result
            if isinstance(result, Exception):
                LOG.warn("Celery call %s failed: %s" % (self.call, result))
                my_task._set_internal_data(error=Serializable(result))
                return False
            LOG.debug("Completed celery call %s with result=%s" % (self.call,
                                                                   result))
            # Format result
            if self.result_key:
                data = {self.result_key: result}
            else:
                if isinstance(result, dict):
                    data = result
                else:
                    data = {'result': result}
            # Load formatted result into internal_data
            if self.merge_results:
                merge_dictionary(my_task.internal_data, data)
            else:
                my_task.set_data(**data)
            return True
        else:
            LOG.debug("async_call.ready()=%s. TryFire for '%s' "
                      "returning False" % (my_task.async_call.ready(),
                                           my_task.get_name()))
            return False