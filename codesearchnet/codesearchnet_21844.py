def add_status_job(self, job_func, name=None, timeout=3):
        """Adds a job to be included during calls to the `/status` endpoint.

        :param job_func: the status function.
        :param name: the name used in the JSON response for the given status
                     function. The name of the function is the default.
        :param timeout: the time limit before the job status is set to
                        "timeout exceeded".
        """
        job_name = job_func.__name__ if name is None else name
        job = (job_name, timeout, job_func)
        self._jobs.append(job)