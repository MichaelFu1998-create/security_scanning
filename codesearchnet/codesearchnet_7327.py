def parallel_task_queue(pool_size=multiprocessing.cpu_count()):
    """Context manager for setting up a TaskQueue. Upon leaving the
    context manager, all tasks that were enqueued will be executed
    in parallel subject to `pool_size` concurrency constraints."""
    task_queue = TaskQueue(pool_size)
    yield task_queue
    task_queue.execute()