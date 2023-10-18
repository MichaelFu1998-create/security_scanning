def refresh(self):
        """ 
        Remove all existing results files and reinit the h5 arrays 
        so that the tetrad object is just like fresh from a CLI start.
        """

        ## clear any existing results files
        oldfiles = [self.files.qdump] + \
                    self.database.__dict__.values() + \
                    self.trees.__dict__.values()
        for oldfile in oldfiles:
            if oldfile:
                if os.path.exists(oldfile):
                    os.remove(oldfile)

        ## store old ipcluster info
        oldcluster = copy.deepcopy(self._ipcluster)

        ## reinit the tetrad object data.
        self.__init__(
            name=self.name, 
            data=self.files.data, 
            mapfile=self.files.mapfile,
            workdir=self.dirs,
            method=self.params.method,
            guidetreefile=self.files.guidetreefile,
            resolve=self._resolve, 
            nboots=self.params.nboots, 
            nquartets=self.params.nquartets, 
            initarr=True, 
            quiet=True,
            cli=self.kwargs.get("cli")
            )

        ## retain the same ipcluster info
        self._ipcluster = oldcluster