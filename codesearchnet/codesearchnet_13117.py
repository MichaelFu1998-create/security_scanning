def get_clumpp_table(self, kvalues, max_var_multiple=0, quiet=False):
        """
        Returns a dictionary of results tables for making structure barplots.
        This calls the same functions used in get_evanno_table() to call 
        CLUMPP to permute replicates.

        Parameters:
        -----------
        kvalues : list or int
            A kvalue or list of kvalues to run CLUMPP on and return a 
            results table. 

        max_var_multiple: int
            A multiplier value to use as a filter for convergence of runs. 
            Default=0=no filtering. As an example, if 10 replicates 
            were run then the variance of the run with the minimum variance is
            used as a benchmark. If other runs have a variance that is N times 
            greater then that run will be excluded. Remember, if replicate runs 
            sampled different distributions of SNPs then it is not unexpected that 
            they will have very different variances. However, you may still want 
            to exclude runs with very high variance since they likely have 
            not converged. 

        Returns:
        --------
        table : dict or pd.DataFrame
            A dictionary of dataframes with admixture proportions.
        """
        ## do not allow bad vals
        if max_var_multiple:
            if max_var_multiple < 1:
                raise ValueError('max_var_multiple must be >1')

        if isinstance(kvalues, int):
            return _get_clumpp_table(self, kvalues, max_var_multiple, quiet)
        else:
            tabledict = {}
            for kpop in kvalues:
                table = _get_clumpp_table(self, kpop, max_var_multiple, quiet)
                tabledict[kpop] = table
            return tabledict