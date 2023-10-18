def folderScan(self,abfFolder=None):
        """populate class properties relating to files in the folder."""
        if abfFolder is None and 'abfFolder' in dir(self):
            abfFolder=self.abfFolder
        else:
            self.abfFolder=abfFolder
        self.abfFolder=os.path.abspath(self.abfFolder)
        self.log.info("scanning [%s]",self.abfFolder)
        if not os.path.exists(self.abfFolder):
            self.log.error("path doesn't exist: [%s]",abfFolder)
            return
        self.abfFolder2=os.path.abspath(self.abfFolder+"/swhlab/")
        if not os.path.exists(self.abfFolder2):
            self.log.error("./swhlab/ doesn't exist. creating it...")            
            os.mkdir(self.abfFolder2)
        self.fnames=os.listdir(self.abfFolder)
        self.fnames2=os.listdir(self.abfFolder2)
        self.log.debug("./ has %d files",len(self.fnames))
        self.log.debug("./swhlab/ has %d files",len(self.fnames2))
        self.fnamesByExt = filesByExtension(self.fnames)
        if not "abf" in self.fnamesByExt.keys():
            self.log.error("no ABF files found")
        self.log.debug("found %d ABFs",len(self.fnamesByExt["abf"]))
        
        self.cells=findCells(self.fnames) # list of cells by their ID
        self.log.debug("found %d cells"%len(self.cells))
        
        self.fnamesByCell = filesByCell(self.fnames,self.cells) # only ABFs
        self.log.debug("grouped cells by number of source files: %s"%\
            str([len(self.fnamesByCell[elem]) for elem in self.fnamesByCell]))