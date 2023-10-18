def _queue_management_worker(self):
        """Listen to the queue for task status messages and handle them.

        Depending on the message, tasks will be updated with results, exceptions,
        or updates. It expects the following messages:

        .. code:: python

            {
               "task_id" : <task_id>
               "result"  : serialized result object, if task succeeded
               ... more tags could be added later
            }

            {
               "task_id" : <task_id>
               "exception" : serialized exception object, on failure
            }

        We do not support these yet, but they could be added easily.

        .. code:: python

            {
               "task_id" : <task_id>
               "cpu_stat" : <>
               "mem_stat" : <>
               "io_stat"  : <>
               "started"  : tstamp
            }

        The `None` message is a die request.
        """
        while True:
            logger.debug("[MTHREAD] Management thread active")
            try:
                msg = self.incoming_q.get(block=True, timeout=1)

            except queue.Empty:
                # Timed out.
                pass

            except IOError as e:
                logger.debug("[MTHREAD] Caught broken queue with exception code {}: {}".format(e.errno, e))
                return

            except Exception as e:
                logger.debug("[MTHREAD] Caught unknown exception: {}".format(e))

            else:

                if msg is None:
                    logger.debug("[MTHREAD] Got None")
                    return

                else:
                    logger.debug("[MTHREAD] Received message: {}".format(msg))
                    task_fut = self.tasks[msg['task_id']]
                    if 'result' in msg:
                        result, _ = deserialize_object(msg['result'])
                        task_fut.set_result(result)

                    elif 'exception' in msg:
                        exception, _ = deserialize_object(msg['exception'])
                        task_fut.set_exception(exception)

            if not self.is_alive:
                break