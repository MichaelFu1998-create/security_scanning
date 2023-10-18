def run_command(args, **kwargs):
    """
    Given a list whose first element is a command name, followed by arguments,
    execute it and show timing info.
    """
    assert len(args) > 0
    start_time = time.time()
    process = AsyncProcess(args, **kwargs)
    process.wait()
    elapsed_time = time.time() - start_time
    logger.info("%s took %0.4f seconds", args[0], elapsed_time)