def status(self, job_ids):
        '''  Get the status of a list of jobs identified by their ids.

        Args:
            - job_ids (List of ids) : List of identifiers for the jobs

        Returns:
            - List of status codes.

        '''

        logger.debug("Checking status of: {0}".format(job_ids))
        for job_id in self.resources:

            if self.resources[job_id]['proc']:

                poll_code = self.resources[job_id]['proc'].poll()
                if self.resources[job_id]['status'] in ['COMPLETED', 'FAILED']:
                    continue

                if poll_code is None:
                    self.resources[job_id]['status'] = 'RUNNING'
                elif poll_code == 0:
                    self.resources[job_id]['status'] = 'COMPLETED'
                elif poll_code != 0:
                    self.resources[job_id]['status'] = 'FAILED'
                else:
                    logger.error("Internal consistency error: unexpected case in local provider state machine")

            elif self.resources[job_id]['remote_pid']:

                retcode, stdout, stderr = self.channel.execute_wait('ps -p {} &> /dev/null; echo "STATUS:$?" ',
                                                                    self.cmd_timeout)
                for line in stdout.split('\n'):
                    if line.startswith("STATUS:"):
                        status = line.split("STATUS:")[1].strip()
                        if status == "0":
                            self.resources[job_id]['status'] = 'RUNNING'
                        else:
                            self.resources[job_id]['status'] = 'FAILED'

        return [self.resources[jid]['status'] for jid in job_ids]