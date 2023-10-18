def print_read(self, rid):
        """
        Prints nonzero rows of the read wanted

        """
        if self.rname is not None:
            print self.rname[rid]
            print '--'
        r = self.get_read_data(rid)
        aligned_loci = np.unique(r.nonzero()[1])
        for locus in aligned_loci:
            nzvec = r[:, locus].todense().transpose()[0].A.flatten()
            if self.lname is not None:
                print self.lname[locus],
            else:
                print locus,
            print nzvec