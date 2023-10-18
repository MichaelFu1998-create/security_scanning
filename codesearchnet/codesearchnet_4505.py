def worker(worker_id, task_url, debug=True, logdir="workers", uid="1"):
    """ TODO: docstring

    TODO : Cleanup debug, logdir and uid to function correctly
    """

    start_file_logger('{}/{}/worker_{}.log'.format(logdir, uid, worker_id),
                      0,
                      level=logging.DEBUG if debug is True else logging.INFO)

    logger.info("Starting worker {}".format(worker_id))

    task_ids_received = []

    message_q = zmq_pipes.WorkerMessages(task_url)

    while True:
        print("Worker loop iteration starting")
        task_id, buf = message_q.get()
        task_ids_received.append(task_id)

        user_ns = locals()
        user_ns.update({'__builtins__': __builtins__})
        f, args, kwargs = unpack_apply_message(buf, user_ns, copy=False)

        logger.debug("Worker {} received task {}".format(worker_id, task_id))
        result = execute_task(f, args, kwargs, user_ns)
        logger.debug("Worker {} completed task {}".format(worker_id, task_id))

        reply = {"result": result, "worker_id": worker_id}
        message_q.put(task_id, serialize_object(reply))
        logger.debug("Result sent")