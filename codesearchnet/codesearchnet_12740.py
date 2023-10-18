def run_multiple_commands_redirect_stdout(
        multiple_args_dict,
        print_commands=True,
        process_limit=-1,
        polling_freq=0.5,
        **kwargs):
    """
    Run multiple shell commands in parallel, write each of their
    stdout output to files associated with each command.

    Parameters
    ----------
    multiple_args_dict : dict
        A dictionary whose keys are files and values are args list.
        Run each args list as a subprocess and write stdout to the
        corresponding file.

    print_commands : bool
        Print shell commands before running them.

    process_limit : int
        Limit the number of concurrent processes to this number. 0
        if there is no limit, -1 to use max number of processors

    polling_freq : int
        Number of seconds between checking for done processes, if
        we have a process limit
    """
    assert len(multiple_args_dict) > 0
    assert all(len(args) > 0 for args in multiple_args_dict.values())
    assert all(hasattr(f, 'name') for f in multiple_args_dict.keys())
    if process_limit < 0:
        logger.debug("Using %d processes" % cpu_count())
        process_limit = cpu_count()

    start_time = time.time()
    processes = Queue(maxsize=process_limit)

    def add_to_queue(process):
        process.start()
        if print_commands:
            handler = logging.FileHandler(process.redirect_stdout_file.name)
            handler.setLevel(logging.DEBUG)
            logger.addHandler(handler)
            logger.debug(" ".join(process.args))
            logger.removeHandler(handler)
        processes.put(process)

    for f, args in multiple_args_dict.items():
        p = AsyncProcess(
                args,
                redirect_stdout_file=f,
                **kwargs)
        if not processes.full():
            add_to_queue(p)
        else:
            while processes.full():
                # Are there any done processes?
                to_remove = []
                for possibly_done in processes.queue:
                    if possibly_done.poll() is not None:
                        possibly_done.wait()
                        to_remove.append(possibly_done)
                # Remove them from the queue and stop checking
                if to_remove:
                    for process_to_remove in to_remove:
                        processes.queue.remove(process_to_remove)
                    break
                # Check again in a second if there weren't
                time.sleep(polling_freq)
            add_to_queue(p)

    # Wait for all the rest of the processes
    while not processes.empty():
        processes.get().wait()

    elapsed_time = time.time() - start_time
    logger.info(
        "Ran %d commands in %0.4f seconds",
        len(multiple_args_dict),
        elapsed_time)