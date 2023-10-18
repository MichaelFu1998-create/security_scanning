def plot(self, pcs=[1, 2], ax=None, cmap=None, cdict=None, legend=True, title=None, outfile=None):
        """
        Do the PCA and plot it.

        Parameters
        ---------
        pcs: list of ints
        ...
        ax: matplotlib axis
        ...
        cmap: matplotlib colormap
        ...
        cdict: dictionary mapping pop names to colors
        ...
        legend: boolean, whether or not to show the legend

        """
        ## Specify which 2 pcs to plot, default is pc1 and pc2
        pc1 = pcs[0] - 1
        pc2 = pcs[1] - 1
        if pc1 < 0 or pc2 > self.ncomponents - 1:
            raise IPyradError("PCs are 1-indexed. 1 is min & {} is max".format(self.ncomponents))

        ## Convert genotype data to allele count data
        ## We do this here because we might want to try different ways
        ## of accounting for missing data and "alt" allele counts treat
        ## missing data as "ref"
        allele_counts = self.genotypes.to_n_alt()

        ## Actually do the pca
        if self.ncomponents > len(self.samples_vcforder):
            self.ncomponents = len(self.samples_vcforder)
            print("  INFO: # PCs < # samples. Forcing # PCs = {}".format(self.ncomponents))
        coords, model = allel.pca(allele_counts, n_components=self.ncomponents, scaler='patterson')

        self.pcs = pd.DataFrame(coords,
                                index=self.samples_vcforder,
                                columns=["PC{}".format(x) for x in range(1,self.ncomponents+1)])

        ## Just allow folks to pass in the name of the cmap they want to use
        if isinstance(cmap, str):
            try:
                cmap = cm.get_cmap(cmap)
            except:
                raise IPyradError("  Bad cmap value: {}".format(cmap))


        if not cmap and not cdict:
            if not self.quiet:
                print("  Using default cmap: Spectral")
            cmap = cm.get_cmap('Spectral')

        if cmap:
            if cdict:
                print("  Passing in both cmap and cdict defaults to using the cmap value.")
            popcolors = cmap(np.arange(len(self.pops))/len(self.pops))
            cdict = {i:j for i, j in zip(self.pops.keys(), popcolors)}

        fig = ""
        if not ax:
            fig = plt.figure(figsize=(6, 5))
            ax = fig.add_subplot(1, 1, 1)

        x = coords[:, pc1]
        y = coords[:, pc2]
        for pop in self.pops:
            ## Don't include pops with no samples, it makes the legend look stupid
            ## TODO: This doesn't prevent empty pops from showing up in the legend for some reason.
            if len(self.pops[pop]) > 0:
                mask = np.isin(self.samples_vcforder, self.pops[pop])
                ax.plot(x[mask], y[mask], marker='o', linestyle=' ', color=cdict[pop], label=pop, markersize=6, mec='k', mew=.5)

        ax.set_xlabel('PC%s (%.1f%%)' % (pc1+1, model.explained_variance_ratio_[pc1]*100))
        ax.set_ylabel('PC%s (%.1f%%)' % (pc2+1, model.explained_variance_ratio_[pc2]*100))

        if legend:
            ax.legend(bbox_to_anchor=(1, 1), loc='upper left')

        if fig:
            fig.tight_layout()

        if title:
            ax.set_title(title)

        if outfile:
            try:
                plt.savefig(outfile, format="png", bbox_inches="tight")
            except:
                print("  Saving pca.plot() failed to save figure to {}".format(outfile))

        return ax