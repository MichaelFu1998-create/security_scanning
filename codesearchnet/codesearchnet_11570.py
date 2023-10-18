def wait(self):
        """wait until all jobs finish and return a list of pids
        """
        finished_pids = [ ]
        while self.running_procs:
            finished_pids.extend(self.poll())
        return finished_pids