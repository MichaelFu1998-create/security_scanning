def failed_runids(self, runids):
        """Provide the run IDs of failed jobs


        Returns
        -------
        None

        """

        # remove failed clusterprocids from self.clusterprocids_finished
        # so that len(self.clusterprocids_finished)) becomes the number
        # of the successfully finished jobs
        for i in runids:
            try:
                self.clusterprocids_finished.remove(i)
            except ValueError:
                pass