def analyzeABF(self,ID):
        """
        Analye a single ABF: make data, index it.
        If called directly, will delete all ID_data_ and recreate it.
        """
        for fname in self.files2:
            if fname.startswith(ID+"_data_"):
                self.log.debug("deleting [%s]",fname)
                os.remove(os.path.join(self.folder2,fname))
        self.log.info("analyzing (with overwrite) [%s]",ID)
        protocols.analyze(os.path.join(self.folder1,ID+".abf"))