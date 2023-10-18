def _dump_qmc(self):
        """ 
        Makes a reduced array that excludes quartets with no information and 
        prints the quartets and weights to a file formatted for wQMC 
        """
        ## open the h5 database
        io5 = h5py.File(self.database.output, 'r')

        ## create an output file for writing
        self.files.qdump = os.path.join(self.dirs, self.name+".quartets.txt")
        LOGGER.info("qdump file %s", self.files.qdump)
        outfile = open(self.files.qdump, 'w')

        ## todo: should pull quarts order in randomly? or doesn't matter?
        for idx in xrange(0, self.params.nquartets, self._chunksize):
            ## get mask of zero weight quartets
            #mask = io5["weights"][idx:idx+self.chunksize] != 0
            #weight = io5["weights"][idx:idx+self.chunksize][mask]
            #LOGGER.info("exluded = %s, mask shape %s", 
            #            self._chunksize - mask.shape[0], mask.shape)
            #LOGGER.info('q shape %s', io5["quartets"][idx:idx+self._chunksize].shape)
            masked_quartets = io5["quartets"][idx:idx+self._chunksize, :]#[mask, :]
            quarts = [list(j) for j in masked_quartets]

            ## format and print
            #chunk = ["{},{}|{},{}:{}".format(*i+[j]) for i, j \
            #                                        in zip(quarts, weight)]
            chunk = ["{},{}|{},{}".format(*i) for i in quarts]
            outfile.write("\n".join(chunk)+"\n")


        ## close output file and h5 database
        outfile.close()
        io5.close()