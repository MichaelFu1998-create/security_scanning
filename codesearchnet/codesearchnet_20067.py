def detect(self):
        """runs AP detection on every sweep."""
        self.log.info("initializing AP detection on all sweeps...")
        t1=cm.timeit()
        for sweep in range(self.abf.sweeps):
            self.detectSweep(sweep)
        self.log.info("AP analysis of %d sweeps found %d APs (completed in %s)",
                      self.abf.sweeps,len(self.APs),cm.timeit(t1))