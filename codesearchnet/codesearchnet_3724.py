def status(self, pk=None, detail=False, **kwargs):
        """Print the current job status. This is used to check a running job. You can look up the job with
        the same parameters used for a get request.

        =====API DOCS=====
        Retrieve the current job status.

        :param pk: Primary key of the resource to retrieve status from.
        :type pk: int
        :param detail: Flag that if set, return the full JSON of the job resource rather than a status summary.
        :type detail: bool
        :param `**kwargs`: Keyword arguments used to look up resource object to retrieve status from if ``pk``
                           is not provided.
        :returns: full loaded JSON of the specified unified job if ``detail`` flag is on; trimed JSON containing
                  only "elapsed", "failed" and "status" fields of the unified job if ``detail`` flag is off.
        :rtype: dict

        =====API DOCS=====
        """
        # Remove default values (anything where the value is None).
        self._pop_none(kwargs)

        # Search for the record if pk not given
        if not pk:
            job = self.get(include_debug_header=True, **kwargs)
        # Get the job from Ansible Tower if pk given
        else:
            debug.log('Asking for job status.', header='details')
            finished_endpoint = '%s%s/' % (self.endpoint, pk)
            job = client.get(finished_endpoint).json()

        # In most cases, we probably only want to know the status of the job and the amount of time elapsed.
        # However, if we were asked for verbose information, provide it.
        if detail:
            return job

        # Print just the information we need.
        return {
            'elapsed': job['elapsed'],
            'failed': job['failed'],
            'status': job['status'],
        }