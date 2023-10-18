def _init_seqarray(self, quiet=False):
        """ 
        Fills the seqarr with the full data set, and creates a bootsarr copy
        with the following modifications:

        1) converts "-" into "N"s, since they are similarly treated as missing. 
        2) randomly resolve ambiguities (RSKWYM)
        3) convert to uint8 for smaller memory load and faster computation
        """

        ## read in the data (seqfile)
        try:
            spath = open(self.files.data, 'r')
        except IOError:
            raise IPyradWarningExit(NO_SNP_FILE.format(self.files.data))
        line = spath.readline().strip().split()
        ntax = int(line[0])
        nbp = int(line[1])

        ## make a tmp seq array
        if not quiet:
            print("loading seq array [{} taxa x {} bp]".format(ntax, nbp))        
        tmpseq = np.zeros((ntax, nbp), dtype=np.uint8)
    
        ## create array storage for real seq and the tmp bootstrap seqarray
        with h5py.File(self.database.input, 'w') as io5:
            io5.create_dataset("seqarr", (ntax, nbp), dtype=np.uint8)
            io5.create_dataset("bootsarr", (ntax, nbp), dtype=np.uint8)
            io5.create_dataset("bootsmap", (nbp, 2), dtype=np.uint32)

            ## if there is a map file, load it into the bootsmap
            if self.files.mapfile:
                with open(self.files.mapfile, 'r') as inmap:
                    ## parse the map file from txt and save as dataset
                    maparr = np.genfromtxt(inmap, dtype=np.uint64)
                    io5["bootsmap"][:] = maparr[:, [0, 3]]

                    ## parse the span info from maparr and save to dataset
                    spans = np.zeros((maparr[-1, 0], 2), np.uint64)
                    spans = get_spans(maparr, spans)
                    io5.create_dataset("spans", data=spans)
                    if not quiet:
                        print("max unlinked SNPs per quartet (nloci): {}"\
                              .format(spans.shape[0]))
            else:
                io5["bootsmap"][:, 0] = np.arange(io5["bootsmap"].shape[0])

            ## fill the tmp array from the input phy
            for line, seq in enumerate(spath.readlines()):
                tmpseq[line] = np.array(list(seq.split()[-1])).view(np.uint8)

            ## convert '-' or '_' into 'N'
            tmpseq[tmpseq == 45] = 78
            tmpseq[tmpseq == 95] = 78            

            ## save array to disk so it can be easily accessed by slicing
            ## This unmodified array is used again later for sampling boots
            io5["seqarr"][:] = tmpseq

            ## resolve ambiguous IUPAC codes
            if self._resolve:
                tmpseq = resolve_ambigs(tmpseq)

            ## convert CATG bases to matrix indices
            tmpseq[tmpseq == 65] = 0
            tmpseq[tmpseq == 67] = 1
            tmpseq[tmpseq == 71] = 2
            tmpseq[tmpseq == 84] = 3

            ## save modified array to disk            
            io5["bootsarr"][:] = tmpseq

            ## memory cleanup
            #del tmpseq

            ## get initial array
            LOGGER.info("original seqarr \n %s", io5["seqarr"][:, :20])
            LOGGER.info("original bootsarr \n %s", io5["bootsarr"][:, :20])
            LOGGER.info("original bootsmap \n %s", io5["bootsmap"][:20, :])