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
        logger.debug("[MTHREAD] queue management worker starting")

        while not self._executor_bad_state.is_set():
            try:
                msgs = self.incoming_q.get(timeout=1)
                # logger.debug("[MTHREAD] get has returned {}".format(len(msgs)))

            except queue.Empty:
                logger.debug("[MTHREAD] queue empty")
                # Timed out.
                pass

            except IOError as e:
                logger.exception("[MTHREAD] Caught broken queue with exception code {}: {}".format(e.errno, e))
                return

            except Exception as e:
                logger.exception("[MTHREAD] Caught unknown exception: {}".format(e))
                return

            else:

                if msgs is None:
                    logger.debug("[MTHREAD] Got None, exiting")
                    return

                else:
                    for serialized_msg in msgs:
                        try:
                            msg = pickle.loads(serialized_msg)
                            tid = msg['task_id']
                        except pickle.UnpicklingError:
                            raise BadMessage("Message received could not be unpickled")

                        except Exception:
                            raise BadMessage("Message received does not contain 'task_id' field")

                        if tid == -1 and 'exception' in msg:
                            logger.warning("Executor shutting down due to exception from interchange")
                            self._executor_exception, _ = deserialize_object(msg['exception'])
                            logger.exception("Exception: {}".format(self._executor_exception))
                            # Set bad state to prevent new tasks from being submitted
                            self._executor_bad_state.set()
                            # We set all current tasks to this exception to make sure that
                            # this is raised in the main context.
                            for task in self.tasks:
                                self.tasks[task].set_exception(self._executor_exception)
                            break

                        task_fut = self.tasks[tid]

                        if 'result' in msg:
                            result, _ = deserialize_object(msg['result'])
                            task_fut.set_result(result)

                        elif 'exception' in msg:
                            try:
                                s, _ = deserialize_object(msg['exception'])
                                # s should be a RemoteExceptionWrapper... so we can reraise it
                                try:
                                    s.reraise()
                                except Exception as e:
                                    task_fut.set_exception(e)
                            except Exception as e:
                                # TODO could be a proper wrapped exception?
                                task_fut.set_exception(
                                    DeserializationError("Received exception, but handling also threw an exception: {}".format(e)))
                        else:
                            raise BadMessage("Message received is neither result or exception")

            if not self.is_alive:
                break
        logger.info("[MTHREAD] queue management worker finished")