def cancel(self, job_ids):
        """Cancel the jobs specified by a list of job ids.

        Parameters
        ----------
        job_ids : list of str
            List of of job identifiers

        Returns
        -------
        list of bool
            Each entry in the list will contain False if the operation fails. Otherwise, the entry will be True.
        """

        if self.linger is True:
            logger.debug("Ignoring cancel requests due to linger mode")
            return [False for x in job_ids]

        try:
            self.client.terminate_instances(InstanceIds=list(job_ids))
        except Exception as e:
            logger.error("Caught error while attempting to remove instances: {0}".format(job_ids))
            raise e
        else:
            logger.debug("Removed the instances: {0}".format(job_ids))

        for job_id in job_ids:
            self.resources[job_id]["status"] = "COMPLETED"

        for job_id in job_ids:
            self.instances.remove(job_id)

        return [True for x in job_ids]