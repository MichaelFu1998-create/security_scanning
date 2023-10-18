def run_splitted_processing(max_simultaneous_processes, process_name,
                            filenames):
    """
        Run processes which push the routing dump of the RIPE in a redis
        database.
        The dump has been splitted in multiple files and each process run
        on one of this files.
    """
    pids = []
    while len(filenames) > 0:
        while len(filenames) > 0 and len(pids) < max_simultaneous_processes:
            filename = filenames.pop()
            pids.append(service_start(service=process_name,
                                      param=['-f', filename, '-d',
                                             imported_day]))
        while len(pids) == max_simultaneous_processes:
            time.sleep(sleep_timer)
            pids = update_running_pids(pids)
    while len(pids) > 0:
        # Wait until all the processes are finished
        time.sleep(sleep_timer)
        pids = update_running_pids(pids)