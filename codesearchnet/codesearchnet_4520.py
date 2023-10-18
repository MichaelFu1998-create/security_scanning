def runner(incoming_q, outgoing_q):
    """This is a function that mocks the Swift-T side.

    It listens on the the incoming_q for tasks and posts returns on the outgoing_q.

    Args:
         - incoming_q (Queue object) : The queue to listen on
         - outgoing_q (Queue object) : Queue to post results on

    The messages posted on the incoming_q will be of the form :

    .. code:: python

       {
          "task_id" : <uuid.uuid4 string>,
          "buffer"  : serialized buffer containing the fn, args and kwargs
       }

    If ``None`` is received, the runner will exit.

    Response messages should be of the form:

    .. code:: python

       {
          "task_id" : <uuid.uuid4 string>,
          "result"  : serialized buffer containing result
          "exception" : serialized exception object
       }

    On exiting the runner will post ``None`` to the outgoing_q

    """
    logger.debug("[RUNNER] Starting")

    def execute_task(bufs):
        """Deserialize the buffer and execute the task.

        Returns the serialized result or exception.
        """
        user_ns = locals()
        user_ns.update({'__builtins__': __builtins__})

        f, args, kwargs = unpack_apply_message(bufs, user_ns, copy=False)

        fname = getattr(f, '__name__', 'f')
        prefix = "parsl_"
        fname = prefix + "f"
        argname = prefix + "args"
        kwargname = prefix + "kwargs"
        resultname = prefix + "result"

        user_ns.update({fname: f,
                        argname: args,
                        kwargname: kwargs,
                        resultname: resultname})

        code = "{0} = {1}(*{2}, **{3})".format(resultname, fname,
                                               argname, kwargname)

        try:
            logger.debug("[RUNNER] Executing: {0}".format(code))
            exec(code, user_ns, user_ns)

        except Exception as e:
            logger.warning("Caught exception; will raise it: {}".format(e))
            raise e

        else:
            logger.debug("[RUNNER] Result: {0}".format(user_ns.get(resultname)))
            return user_ns.get(resultname)

    while True:
        try:
            # Blocking wait on the queue
            msg = incoming_q.get(block=True, timeout=10)

        except queue.Empty:
            # Handle case where no items were in the queue
            logger.debug("[RUNNER] Queue is empty")

        except IOError as e:
            logger.debug("[RUNNER] Broken pipe: {}".format(e))
            try:
                # Attempt to send a stop notification to the management thread
                outgoing_q.put(None)

            except Exception:
                pass

            break

        except Exception as e:
            logger.debug("[RUNNER] Caught unknown exception: {}".format(e))

        else:
            # Handle received message
            if not msg:
                # Empty message is a die request
                logger.debug("[RUNNER] Received exit request")
                outgoing_q.put(None)
                break
            else:
                # Received a valid message, handle it
                logger.debug("[RUNNER] Got a valid task with ID {}".format(msg["task_id"]))
                try:
                    response_obj = execute_task(msg['buffer'])
                    response = {"task_id": msg["task_id"],
                                "result": serialize_object(response_obj)}

                    logger.debug("[RUNNER] Returing result: {}".format(
                                   deserialize_object(response["result"])))

                except Exception as e:
                    logger.debug("[RUNNER] Caught task exception: {}".format(e))
                    response = {"task_id": msg["task_id"],
                                "exception": serialize_object(e)}

                outgoing_q.put(response)

    logger.debug("[RUNNER] Terminating")