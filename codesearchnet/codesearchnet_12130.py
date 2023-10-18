def initialize(self, currentdir, assetpath, cplist,
                   cplistfile, executor, readonly, baseurl):
        '''
        handles initial setup.

        '''

        self.currentdir = currentdir
        self.assetpath = assetpath
        self.currentproject = cplist
        self.cplistfile = cplistfile
        self.executor = executor
        self.readonly = readonly
        self.baseurl = baseurl