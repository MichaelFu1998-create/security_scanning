def scan(self):
        """
        scan folder1 and folder2 into files1 and files2.
        since we are on windows, simplify things by making them all lowercase.
        this WILL cause problems on 'nix operating systems.If this is the case,
        just run a script to rename every file to all lowercase.
        """
        t1=cm.timeit()
        self.files1=cm.list_to_lowercase(sorted(os.listdir(self.folder1)))
        self.files2=cm.list_to_lowercase(sorted(os.listdir(self.folder2)))
        self.files1abf=[x for x in self.files1 if x.endswith(".abf")]
        self.files1abf=cm.list_to_lowercase(cm.abfSort(self.files1abf))
        self.IDs=[x[:-4] for x in self.files1abf]
        self.log.debug("folder1 has %d files",len(self.files1))
        self.log.debug("folder1 has %d abfs",len(self.files1abf))
        self.log.debug("folder2 has %d files",len(self.files2))
        self.log.debug("scanning folders took %s",cm.timeit(t1))