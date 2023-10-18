def get_evanno_table(self, kvalues, max_var_multiple=0, quiet=False):
        """
        Calculates the Evanno table from results files for tests with 
        K-values in the input list kvalues. The values lnPK, lnPPK,
        and deltaK are calculated. The max_var_multiplier arg can be used
        to exclude results files based on variance of the likelihood as a 
        proxy for convergence. 

        Parameters:
        -----------
        kvalues : list
            The list of K-values for which structure was run for this object.
            e.g., kvalues = [3, 4, 5]

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

        quiet: bool
            Suppresses printed messages about convergence.

        Returns:
        --------
        table : pandas.DataFrame
            A data frame with LPK, LNPPK, and delta K. The latter is typically
            used to find the best fitting value of K. But be wary of over
            interpreting a single best K value. 
        """
        ## do not allow bad vals
        if max_var_multiple:
            if max_var_multiple < 1:
                raise ValueError('max_variance_multiplier must be >1')

        table = _get_evanno_table(self, kvalues, max_var_multiple, quiet)
        return table