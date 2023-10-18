def plot_pairwise_dist(self, labels=None, ax=None, cmap=None, cdict=None, metric="euclidean"):
        """
        Plot pairwise distances between all samples

        labels: bool or list
                by default labels aren't included. If labels == True, then labels are read in
                from the vcf file. Alternatively, labels can be passed in as a list, should
                be same length as the number of samples.
        """
        allele_counts = self.genotypes.to_n_alt()
        dist = allel.pairwise_distance(allele_counts, metric=metric)
        if not ax:
            fig = plt.figure(figsize=(5, 5))
            ax = fig.add_subplot(1, 1, 1)

        if isinstance(labels, bool):
            if labels:
                labels = list(self.samples_vcforder)
        elif isinstance(labels, type(None)):
            pass
        else:
            ## If not bool or None (default), then check to make sure the list passed in
            ## is the right length
            if not len(labels) == len(self.samples_vcforder):
                raise IPyradError(LABELS_LENGTH_ERROR.format(len(labels), len(self.samples_vcforder)))

        allel.plot.pairwise_distance(dist, labels=labels, ax=ax, colorbar=False)