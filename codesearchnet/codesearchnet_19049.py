def bundle(self, reset=False, shallow=False): # Copies the original matrix (Use lots of memory)
        """
        Returns ``AlignmentPropertyMatrix`` object in which loci are bundled using grouping information.

        :param reset: whether to reset the values at the loci
        :param shallow: whether to copy all the meta data
        """
        if self.finalized:
            # if self.num_groups > 0:
            if self.groups is not None and self.gname is not None:
                grp_conv_mat = lil_matrix((self.num_loci, self.num_groups))
                for i in xrange(self.num_groups):
                    grp_conv_mat[self.groups[i], i] = 1.0
                grp_align = Sparse3DMatrix.__mul__(self, grp_conv_mat) # The core of the bundling
                grp_align.num_loci = self.num_groups
                grp_align.num_haplotypes = self.num_haplotypes
                grp_align.num_reads = self.num_reads
                grp_align.shape = (grp_align.num_loci, grp_align.num_haplotypes, grp_align.num_reads)
                if not shallow:
                    grp_align.lname = copy.copy(self.gname)
                    grp_align.hname = self.hname
                    grp_align.rname = copy.copy(self.rname)
                    grp_align.lid   = dict(zip(grp_align.lname, np.arange(grp_align.num_loci)))
                    grp_align.rid   = copy.copy(self.rid)
                if reset:
                    grp_align.reset()
                return grp_align
            else:
                raise RuntimeError('No group information is available for bundling.')
        else:
            raise RuntimeError('The matrix is not finalized.')