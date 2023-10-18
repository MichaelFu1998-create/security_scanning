def main(path, pid, queue):
    """
    Standalone PSQ worker.

    The queue argument must be the full importable path to a psq.Queue
    instance.

    Example usage:

        psqworker config.q

        psqworker --path /opt/app queues.fast

    """
    setup_logging()

    if pid:
        with open(os.path.expanduser(pid), "w") as f:
            f.write(str(os.getpid()))

    if not path:
        path = os.getcwd()

    sys.path.insert(0, path)

    queue = import_queue(queue)

    import psq

    worker = psq.Worker(queue=queue)

    worker.listen()