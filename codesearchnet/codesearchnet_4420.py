def start(self, priority_queue, resource_queue):

        self._kill_event = threading.Event()
        self._priority_queue_pull_thread = threading.Thread(target=self._migrate_logs_to_internal,
                                                            args=(
                                                                priority_queue, 'priority', self._kill_event,)
                                                            )
        self._priority_queue_pull_thread.start()

        self._resource_queue_pull_thread = threading.Thread(target=self._migrate_logs_to_internal,
                                                            args=(
                                                                resource_queue, 'resource', self._kill_event,)
                                                            )
        self._resource_queue_pull_thread.start()

        """
        maintain a set to track the tasks that are already INSERTED into database
        to prevent race condition that the first resource message (indicate 'running' state)
        arrives before the first task message.
        If race condition happens, add to left_messages and operate them later

        """
        inserted_tasks = set()
        left_messages = {}

        while (not self._kill_event.is_set() or
               self.pending_priority_queue.qsize() != 0 or self.pending_resource_queue.qsize() != 0 or
               priority_queue.qsize() != 0 or resource_queue.qsize() != 0):

            """
            WORKFLOW_INFO and TASK_INFO messages

            """
            self.logger.debug("""Checking STOP conditions: {}, {}, {}, {}, {}""".format(
                              self._kill_event.is_set(),
                              self.pending_priority_queue.qsize() != 0, self.pending_resource_queue.qsize() != 0,
                              priority_queue.qsize() != 0, resource_queue.qsize() != 0))

            # This is the list of first resource messages indicating that task starts running
            first_messages = []

            # Get a batch of priority messages
            messages = self._get_messages_in_batch(self.pending_priority_queue,
                                                   interval=self.batching_interval,
                                                   threshold=self.batching_threshold)
            if messages:
                self.logger.debug(
                    "Got {} messages from priority queue".format(len(messages)))
                update_messages, insert_messages, all_messages = [], [], []
                for msg_type, msg in messages:
                    if msg_type.value == MessageType.WORKFLOW_INFO.value:
                        if "python_version" in msg:   # workflow start message
                            self.logger.debug(
                                "Inserting workflow start info to WORKFLOW table")
                            self._insert(table=WORKFLOW, messages=[msg])
                        else:                         # workflow end message
                            self.logger.debug(
                                "Updating workflow end info to WORKFLOW table")
                            self._update(table=WORKFLOW,
                                         columns=['run_id', 'tasks_failed_count',
                                                  'tasks_completed_count', 'time_completed',
                                                  'workflow_duration'],
                                         messages=[msg])
                    else:                             # TASK_INFO message
                        all_messages.append(msg)
                        if msg['task_time_returned'] is not None:
                            update_messages.append(msg)
                        else:
                            inserted_tasks.add(msg['task_id'])
                            insert_messages.append(msg)

                            # check if there is an left_message for this task
                            if msg['task_id'] in left_messages:
                                first_messages.append(
                                    left_messages.pop(msg['task_id']))

                self.logger.debug(
                    "Updating and inserting TASK_INFO to all tables")
                self._update(table=WORKFLOW,
                             columns=['run_id', 'tasks_failed_count',
                                      'tasks_completed_count'],
                             messages=update_messages)

                if insert_messages:
                    self._insert(table=TASK, messages=insert_messages)
                    self.logger.debug(
                        "There are {} inserted task records".format(len(inserted_tasks)))
                if update_messages:
                    self._update(table=TASK,
                                 columns=['task_time_returned',
                                          'task_elapsed_time', 'run_id', 'task_id'],
                                 messages=update_messages)
                self._insert(table=STATUS, messages=all_messages)

            """
            RESOURCE_INFO messages

            """
            messages = self._get_messages_in_batch(self.pending_resource_queue,
                                                   interval=self.batching_interval,
                                                   threshold=self.batching_threshold)

            if messages or first_messages:
                self.logger.debug(
                    "Got {} messages from resource queue".format(len(messages)))
                self._insert(table=RESOURCE, messages=messages)
                for msg in messages:
                    if msg['first_msg']:
                        msg['task_status_name'] = States.running.name
                        msg['task_time_running'] = msg['timestamp']
                        if msg['task_id'] in inserted_tasks:
                            first_messages.append(msg)
                        else:
                            left_messages[msg['task_id']] = msg
                if first_messages:
                    self._insert(table=STATUS, messages=first_messages)
                    self._update(table=TASK,
                                 columns=['task_time_running',
                                          'run_id', 'task_id'],
                                 messages=first_messages)