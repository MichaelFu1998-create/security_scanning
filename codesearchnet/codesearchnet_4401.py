def _queue_management_worker(self):
        """ TODO: docstring """
        logger.debug("[MTHREAD] queue management worker starting")

        while True:
            task_id, buf = self.incoming_q.get()  # TODO: why does this hang?
            msg = deserialize_object(buf)[0]
            # TODO: handle exceptions
            task_fut = self.tasks[task_id]
            logger.debug("Got response for task id {}".format(task_id))

            if "result" in msg:
                task_fut.set_result(msg["result"])

            elif "exception" in msg:
                # TODO: handle exception
                pass
            elif 'exception' in msg:
                logger.warning("Task: {} has returned with an exception")
                try:
                    s, _ = deserialize_object(msg['exception'])
                    exception = ValueError("Remote exception description: {}".format(s))
                    task_fut.set_exception(exception)
                except Exception as e:
                    # TODO could be a proper wrapped exception?
                    task_fut.set_exception(
                        DeserializationError("Received exception, but handling also threw an exception: {}".format(e)))

            else:
                raise BadMessage(
                    "Message received is neither result nor exception")

            if not self.is_alive:
                break

        logger.info("[MTHREAD] queue management worker finished")