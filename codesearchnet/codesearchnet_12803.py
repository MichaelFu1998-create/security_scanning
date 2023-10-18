def copy(self):
        """ returns a copy of the pca analysis object """
        cp = copy.deepcopy(self)
        cp.genotypes = allel.GenotypeArray(self.genotypes, copy=True)
        return cp