def _build_stat(self, idx):
        """ Returns a data frame with Sample stats for each step """
        nameordered = self.samples.keys()
        nameordered.sort()
        newdat = pd.DataFrame([self.samples[i].stats_dfs[idx] \
                               for i in nameordered], index=nameordered)\
                               .dropna(axis=1, how='all')
        return newdat