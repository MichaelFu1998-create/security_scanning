def _link_populations(self, popdict=None, popmins=None):
        """
        Creates self.populations dictionary to save mappings of individuals to
        populations/sites, and checks that individual names match with Samples.
        The self.populations dict keys are pop names and the values are lists
        of length 2. The first element is the min number of samples per pop
        for final filtering of loci, and the second element is the list of
        samples per pop.

        Population assigments are used for heirarchical clustering, for
        generating summary stats, and for outputing some file types (.treemix
        for example). Internally stored as a dictionary.

        Note
        ----
        By default a File is read in from `pop_assign_file` with one individual
        per line and space separated pairs of ind pop:

            ind1 pop1
            ind2 pop2
            ind3 pop3
            etc...

        Parameters
        ----------
        TODO: NB: Using API and passing in popdict and popmins is currently 
        unimplemented, or at least looks like it doesn't work. Leaving
        these docs cuz Deren might have ideas about it being useful.

        popdict : dict
            When using the API it may be easier to simply create a dictionary
            to pass in as an argument instead of reading from an input file.
            This can be done with the `popdict` argument like below:

            pops = {'pop1': ['ind1', 'ind2', 'ind3'], 'pop2': ['ind4', 'ind5']}
            [Assembly]._link_populations(popdict=pops).

        popmins : dict
            If you want to apply a minsamples filter based on populations
            you can add a popmins dictionary. This indicates the number of 
            samples in each population that must be present in a locus for 
            the locus to be retained. Example:

            popmins = {'pop1': 3, 'pop2': 2}

        """
        if not popdict:
            ## glob it in case of fuzzy matching
            popfile = glob.glob(self.paramsdict["pop_assign_file"])[0]
            if not os.path.exists(popfile):
                raise IPyradError("Population assignment file not found: {}"\
                                  .format(self.paramsdict["pop_assign_file"]))


            try:
                ## parse populations file
                popdat = pd.read_csv(popfile, header=None,
                                              delim_whitespace=1,
                                              names=["inds", "pops"], 
                                              comment="#")
                popdict = {key: group.inds.values.tolist() for key, group in \
                                                        popdat.groupby("pops")}

                ## parse minsamples per population if present (line with #)
                mindat = [i.lstrip("#").lstrip().rstrip() for i in \
                          open(popfile, 'r').readlines() if i.startswith("#")]
                if mindat:
                    popmins = {}
                    for i in range(len(mindat)):
                        minlist = mindat[i].replace(",", "").split()
                        popmins.update({i.split(':')[0]:int(i.split(':')[1]) \
                                        for i in minlist})
                else:
                    raise IPyradError(MIN_SAMPLES_PER_POP_MALFORMED)

            except (ValueError, IOError):
                LOGGER.warn("Populations file may be malformed.")
                raise IPyradError(MIN_SAMPLES_PER_POP_MALFORMED)

        else:
            ## pop dict is provided by user
            pass

        ## check popdict. Filter for bad samples
        ## Warn user but don't bail out, could be setting the pops file
        ## on a new assembly w/o any linked samples.
        badsamples = [i for i in itertools.chain(*popdict.values()) \
                      if i not in self.samples.keys()]
        if any(badsamples):
            LOGGER.warn("Some names from population input do not match Sample "\
                        + "names: ".format(", ".join(badsamples)))
            LOGGER.warn("If this is a new assembly this is normal.")

        ## If popmins not set, just assume all mins are zero
        if not popmins:
            popmins = {i: 0 for i in popdict.keys()}

        ## check popmins
        ## cannot have higher min for a pop than there are samples in the pop
        popmax = {i: len(popdict[i]) for i in popdict}
        if not all([popmax[i] >= popmins[i] for i in popdict]):
            raise IPyradWarningExit(\
                " minsample per pop value cannot be greater than the "+
                " number of samples in the pop. Modify the populations file.")

        ## return dict
        self.populations = {i: (popmins[i], popdict[i]) for i in popdict}