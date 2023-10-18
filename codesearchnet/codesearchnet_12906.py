def _load_existing_results(self, name, workdir):
        """
        Load existing results files for an object with this workdir and name. 
        This does NOT reload the parameter settings for the object...
        """
        ## get mcmcs
        path = os.path.realpath(os.path.join(self.workdir, self.name))
        mcmcs = glob.glob(path+"_r*.mcmc.txt")
        outs = glob.glob(path+"_r*.out.txt")
        trees = glob.glob(path+"_r*.tre")

        for mcmcfile in mcmcs:
            if mcmcfile not in self.files.mcmcfiles:
                self.files.mcmcfiles.append(mcmcfile)
        for outfile in outs:
            if outfile not in self.files.outfiles:
                self.files.outfiles.append(outfile)
        for tree in trees:
            if tree not in self.files.treefiles:
                self.files.treefiles.append(tree)