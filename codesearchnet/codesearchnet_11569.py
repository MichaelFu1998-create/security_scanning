def poll(self):
        """check if the jobs are running and return a list of pids for
        finished jobs

        """
        finished_procs = [p for p in self.running_procs if p.poll() is not None]
        self.running_procs = collections.deque([p for p in self.running_procs if p not in finished_procs])

        for proc in finished_procs:
            stdout, stderr = proc.communicate()
            ## proc.communicate() returns (stdout, stderr) when
            ## self.pipe = True. Otherwise they are (None, None)

        finished_pids = [p.pid for p in finished_procs]
        self.finished_pids.extend(finished_pids)

        logger = logging.getLogger(__name__)
        messages = 'Running: {}, Finished: {}'.format(len(self.running_procs), len(self.finished_pids))
        logger.info(messages)

        return finished_pids