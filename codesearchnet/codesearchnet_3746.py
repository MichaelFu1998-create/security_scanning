def status(self, pk=None, detail=False, **kwargs):
        """Print the status of the most recent update.

        =====API DOCS=====
        Print the status of the most recent update.

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
        # Obtain the most recent project update
        job = self.last_job_data(pk, **kwargs)

        # In most cases, we probably only want to know the status of the job
        # and the amount of time elapsed. However, if we were asked for
        # verbose information, provide it.
        if detail:
            return job

        # Print just the information we need.
        return {
            'elapsed': job['elapsed'],
            'failed': job['failed'],
            'status': job['status'],
        }