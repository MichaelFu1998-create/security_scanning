def wait(self):
        """Wait until all jobs finish and return the run IDs of the finished jobs

        Returns
        -------
        list(str)
            The list of the run IDs of the finished jobs

        """

        sleep = 5
        while True:
            if self.clusterprocids_outstanding:
                self.poll()
            if not self.clusterprocids_outstanding:
                break
            time.sleep(sleep)
        return self.clusterprocids_finished