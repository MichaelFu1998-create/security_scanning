def output_touch(self):
        """ensure the ./swhlab/ folder exists."""
        if not os.path.exists(self.outFolder):
            self.log.debug("creating %s",self.outFolder)
            os.mkdir(self.outFolder)