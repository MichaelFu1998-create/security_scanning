def _dump_qmc(self):
        """
        Writes the inferred quartet sets from the database to a text 
        file to be used as input for QMC. Quartets that had no information
        available (i.e., no SNPs) were written to the database as 0,0,0,0
        and are excluded here from the output.
        """

        ## open the h5 database
        with h5py.File(self.database.output, 'r') as io5:

            ## create an output file for writing
            self.files.qdump = os.path.join(self.dirs, self.name+".quartets.txt")
            with open(self.files.qdump, 'w') as qdump:

                ## pull from db
                for idx in xrange(0, self.params.nquartets, self._chunksize):
                    qchunk = io5["quartets"][idx:idx+self._chunksize, :]
                    quarts = [tuple(j) for j in qchunk if np.any(j)]

                    ## shuffle and format for qmc
                    np.random.shuffle(quarts)
                    chunk = ["{},{}|{},{}".format(*i) for i in quarts]
                    qdump.write("\n".join(chunk)+"\n")