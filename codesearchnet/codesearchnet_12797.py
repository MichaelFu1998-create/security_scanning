def sample_loci(self):
        """ finds loci with sufficient sampling for this test"""

        ## store idx of passing loci
        idxs = np.random.choice(self.idxs, self.ntests)

        ## open handle, make a proper generator to reduce mem
        with open(self.data) as indata:
            liter = (indata.read().strip().split("|\n"))

        ## store data as dict
        seqdata = {i:"" for i in self.samples}

        ## put chunks into a list
        for idx, loc in enumerate(liter):
            if idx in idxs:
                ## parse chunk
                lines = loc.split("\n")[:-1]
                names = [i.split()[0] for i in lines]
                seqs = [i.split()[1] for i in lines]
                dd = {i:j for i,j in zip(names, seqs)}

                ## add data to concatenated seqdict
                for name in seqdata:
                    if name in names:
                        seqdata[name] += dd[name]
                    else:
                        seqdata[name] += "N"*len(seqs[0])
                        
        ## concatenate into a phylip file
        return seqdata