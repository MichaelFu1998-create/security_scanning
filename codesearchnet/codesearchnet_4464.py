def transfer_file(cls, src_ep, dst_ep, src_path, dst_path):
        tc = globus_sdk.TransferClient(authorizer=cls.authorizer)
        td = globus_sdk.TransferData(tc, src_ep, dst_ep)
        td.add_item(src_path, dst_path)
        try:
            task = tc.submit_transfer(td)
        except Exception as e:
            raise Exception('Globus transfer from {}{} to {}{} failed due to error: {}'.format(
                src_ep, src_path, dst_ep, dst_path, e))

        last_event_time = None
        """
        A Globus transfer job (task) can be in one of the three states: ACTIVE, SUCCEEDED, FAILED.
        Parsl every 20 seconds polls a status of the transfer job (task) from the Globus Transfer service,
        with 60 second timeout limit. If the task is ACTIVE after time runs out 'task_wait' returns False,
        and True otherwise.
        """
        while not tc.task_wait(task['task_id'], 60, 15):
            task = tc.get_task(task['task_id'])
            # Get the last error Globus event
            events = tc.task_event_list(task['task_id'], num_results=1, filter='is_error:1')
            event = events.data[0]
            # Print the error event to stderr and Parsl file log if it was not yet printed
            if event['time'] != last_event_time:
                last_event_time = event['time']
                logger.warn('Non-critical Globus Transfer error event for globus://{}{}: "{}" at {}. Retrying...'.format(
                    src_ep, src_path, event['description'], event['time']))
                logger.debug('Globus Transfer error details: {}'.format(event['details']))

        """
        The Globus transfer job (task) has been terminated (is not ACTIVE). Check if the transfer
        SUCCEEDED or FAILED.
        """
        task = tc.get_task(task['task_id'])
        if task['status'] == 'SUCCEEDED':
            logger.debug('Globus transfer {}, from {}{} to {}{} succeeded'.format(
                task['task_id'], src_ep, src_path, dst_ep, dst_path))
        else:
            logger.debug('Globus Transfer task: {}'.format(task))
            events = tc.task_event_list(task['task_id'], num_results=1, filter='is_error:1')
            event = events.data[0]
            raise Exception('Globus transfer {}, from {}{} to {}{} failed due to error: "{}"'.format(
                task['task_id'], src_ep, src_path, dst_ep, dst_path, event['details']))