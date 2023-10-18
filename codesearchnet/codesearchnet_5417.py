def _clear_celery_task_data(self, my_task):
        """ Clear celery task data """
        # Save history
        if 'task_id' in my_task.internal_data:
            # Save history for diagnostics/forensics
            history = my_task._get_internal_data('task_history', [])
            history.append(my_task._get_internal_data('task_id'))
            del my_task.internal_data['task_id']
            my_task._set_internal_data(task_history=history)
        if 'task_state' in my_task.internal_data:
            del my_task.internal_data['task_state']
        if 'error' in my_task.internal_data:
            del my_task.internal_data['error']
        if hasattr(my_task, 'async_call'):
            delattr(my_task, 'async_call')
        if hasattr(my_task, 'deserialized'):
            delattr(my_task, 'deserialized')