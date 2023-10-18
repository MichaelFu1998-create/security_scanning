def cancel(self, job_ids):
        ''' Cancels the jobs specified by a list of job ids

        Args:
        job_ids : [<job_id> ...]

        Returns :
        [True/False...] : If the cancel operation fails the entire list will be False.
        '''
        for job in job_ids:
            logger.debug("Terminating job/proc_id: {0}".format(job))
            # Here we are assuming that for local, the job_ids are the process id's
            if self.resources[job]['proc']:
                proc = self.resources[job]['proc']
                os.killpg(os.getpgid(proc.pid), signal.SIGTERM)
                self.resources[job]['status'] = 'CANCELLED'

            elif self.resources[job]['remote_pid']:
                cmd = "kill -- -$(ps -o pgid={} | grep -o '[0-9]*')".format(self.resources[job]['remote_pid'])
                retcode, stdout, stderr = self.channel.execute_wait(cmd, self.cmd_timeout)
                if retcode != 0:
                    logger.warning("Failed to kill PID: {} and child processes on {}".format(self.resources[job]['remote_pid'],
                                                                                             self.label))

        rets = [True for i in job_ids]
        return rets