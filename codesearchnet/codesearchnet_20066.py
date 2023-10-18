def ensureDetection(self):
        """
        run this before analysis. Checks if event detection occured.
        If not, runs AP detection on all sweeps.
        """
        if self.APs==False:
            self.log.debug("analysis attempted before event detection...")
            self.detect()