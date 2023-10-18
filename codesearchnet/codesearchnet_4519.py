def cancel(self, job_ids):
        ''' Cancels the resources identified by the job_ids provided by the user.

        Args:
             - job_ids (list): A list of job identifiers

        Returns:
             - A list of status from cancelling the job which can be True, False

        Raises:
             - ExecutionProviderException or its subclasses
        '''
        statuses = []
        for job_id in job_ids:
            try:
                self.delete_instance(job_id)
                statuses.append(True)
                self.provisioned_blocks -= 1
            except Exception:
                statuses.append(False)
        return statuses