def migrate_tasks_to_internal(self, kill_event):
        """Pull tasks from the incoming tasks 0mq pipe onto the internal
        pending task queue

        Parameters:
        -----------
        kill_event : threading.Event
              Event to let the thread know when it is time to die.
        """
        logger.info("[TASK_PULL_THREAD] Starting")
        task_counter = 0
        poller = zmq.Poller()
        poller.register(self.task_incoming, zmq.POLLIN)

        while not kill_event.is_set():
            try:
                msg = self.task_incoming.recv_pyobj()
            except zmq.Again:
                # We just timed out while attempting to receive
                logger.debug("[TASK_PULL_THREAD] {} tasks in internal queue".format(self.pending_task_queue.qsize()))
                continue

            if msg == 'STOP':
                kill_event.set()
                break
            else:
                self.pending_task_queue.put(msg)
                task_counter += 1
                logger.debug("[TASK_PULL_THREAD] Fetched task:{}".format(task_counter))