def analyzeAll(self):
        """analyze every unanalyzed ABF in the folder."""
        searchableData=str(self.files2)
        self.log.debug("considering analysis for %d ABFs",len(self.IDs))
        for ID in self.IDs:
            if not ID+"_" in searchableData:
                self.log.debug("%s needs analysis",ID)
                try:
                    self.analyzeABF(ID)
                except:
                    print("EXCEPTION! "*100)
            else:
                self.log.debug("%s has existing analysis, not overwriting",ID)
        self.log.debug("verified analysis of %d ABFs",len(self.IDs))