def summarize_results(self, individual_results=False):
        """ 
        Prints a summarized table of results from replicate runs, or,
        if individual_result=True, then returns a list of separate
        dataframes for each replicate run. 
        """

        ## return results depending on algorithm

        ## algorithm 00
        if (not self.params.infer_delimit) & (not self.params.infer_sptree):
            if individual_results:
                ## return a list of parsed CSV results
                return [_parse_00(i) for i in self.files.outfiles]
            else:
                ## concatenate each CSV and then get stats w/ describe
                return pd.concat(
                    [pd.read_csv(i, sep='\t', index_col=0) \
                    for i in self.files.mcmcfiles]).describe().T

        ## algorithm 01
        if self.params.infer_delimit & (not self.params.infer_sptree):
            return _parse_01(self.files.outfiles, individual=individual_results)

        ## others
        else:
            return "summary function not yet ready for this type of result"