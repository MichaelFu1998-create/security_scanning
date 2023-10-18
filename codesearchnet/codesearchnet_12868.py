def _to_fulldict(self):
        """ 
        Write to dict including data frames. All sample dicts 
        are combined in save() to dump JSON output """
        
        ## 
        returndict = OrderedDict([
            ("name", self.name),
            ("barcode", self.barcode),
            ("files", self.files),
            ("stats_dfs", {
                "s1": self.stats_dfs.s1.to_dict(),
                "s2": self.stats_dfs.s2.to_dict(),                
                "s3": self.stats_dfs.s3.to_dict(),
                "s4": self.stats_dfs.s4.to_dict(),
                "s5": self.stats_dfs.s5.to_dict(),
            }),
            ("stats", self.stats.to_dict()),
            ("depths", self.depths)
            ])

        return returndict