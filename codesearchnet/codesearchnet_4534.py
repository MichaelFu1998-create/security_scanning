def monitor_wrapper(f, task_id, monitoring_hub_url, run_id, sleep_dur):
        """ Internal
        Wrap the Parsl app with a function that will call the monitor function and point it at the correct pid when the task begins.
        """
        def wrapped(*args, **kwargs):
            p = Process(target=monitor, args=(os.getpid(), task_id, monitoring_hub_url, run_id, sleep_dur))
            p.start()
            try:
                return f(*args, **kwargs)
            finally:
                # There's a chance of zombification if the workers are killed by some signals
                p.terminate()
                p.join()
        return wrapped