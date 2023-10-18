def run(self, 
        ipyclient=None,
        ):
        """
        Run a batch of dstat tests on a list of tests, where each test is 
        a dictionary mapping sample names to {p1 - p4} (and sometimes p5). 
        Parameters modifying the behavior of the run, such as the number
        of bootstrap replicates (nboots) or the minimum coverage for 
        loci (mincov) can be set in {object}.params.

        Parameters:
        -----------
        ipyclient (ipyparallel.Client object):
            An ipyparallel client object to distribute jobs to a cluster. 
        """
        self.results_table, self.results_boots = batch(self, ipyclient)

        ## skip this for 5-part test results
        if not isinstance(self.results_table, list):
            self.results_table.nloci = np.nan_to_num(self.results_table.nloci)\
                                                 .astype(int)