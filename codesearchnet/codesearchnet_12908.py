def write_bpp_files(self, randomize_order=False, quiet=False):
        """ 
        Writes bpp files (.ctl, .seq, .imap) to the working directory. 

        Parameters:
        ------------
        randomize_order (bool):
            whether to randomize the locus order, this will allow you to 
            sample different subsets of loci in different replicates when
            using the filters.maxloci option.
        quiet (bool):
            whether to print info to stderr when finished.
        """

        ## remove any old jobs with this same job name
        self._name = self.name
        oldjobs = glob.glob(os.path.join(self.workdir, self._name+"*.ctl.txt"))
        for job in oldjobs:
            os.remove(job)

        ## check params types
        ## ...

        ## write tmp files for the job
        self._write_seqfile(randomize_order=randomize_order)
        self._write_mapfile()#name=True)
        self._write_ctlfile()

        if not quiet:
            sys.stderr.write("input files created for job {} ({} loci)\n"\
                             .format(self._name, self._nloci))