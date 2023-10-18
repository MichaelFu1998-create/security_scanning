def status(jobs):
    """Handler that calls each status job in a worker pool, attempting to timeout.
    The resulting durations/errors are written to the response
    as JSON.

    eg.

    `{
        "endpoints": [
            { "endpoint": "Jenny's Database", "duration": 1.002556324005127 },
            { "endpoint": "Hotmail", "duration": -1, "error": "Host is down" },
        ]
     }`
    """
    def status_handler():
        endpoints = []
        stats = {"endpoints": None}

        executor = concurrent.futures.ThreadPoolExecutor(max_workers=5)
        # This is basically calling the below within the executor:
        #
        #     >>> timeit(job[2], number=1)
        #
        # job is a tuple of (name, timeout, func) so the above is really:
        #     >>> timeit(func, number=1)
        #
        #gen = ((job, executor.submit(timeit, job[2], number=1)) for job in jobs)
        #for job, future in gen:
        for job, future in [(job, executor.submit(timeit, job[2], number=1)) for job in jobs]:
            name, timeout, _ = job
            endpoint = {"endpoint": name}
            try:
                data = future.result(timeout=timeout)
                endpoint["duration"] = data
            except concurrent.futures.TimeoutError:
                endpoint["error"] = "timeout exceeded"
            except Exception as ex:
                endpoint["error"] = str(ex)
            endpoints.append(endpoint)

        if len(endpoints) > 0:
            stats["endpoints"] = endpoints

        executor.shutdown(wait=False)
        return jsonify(**stats)
        # TODO: Look into potentially cleaning up jobs that have timed-out.
        #
        #       This could be done by changing jobs from a func to an object
        #       that implements `def interrupt(self):` which would be used
        #       to interrupt/stop/close/cleanup any resources.
    return status_handler