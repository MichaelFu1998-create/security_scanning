def taxon_table(self):
        """
        Returns the .tests list of taxa as a pandas dataframe. 
        By auto-generating this table from tests it means that 
        the table itself cannot be modified unless it is returned 
        and saved. 
        """
        if self.tests:
            keys = sorted(self.tests[0].keys())
            if isinstance(self.tests, list):
                ld = [[(key, i[key]) for key in keys] for i in self.tests]
                dd = [dict(i) for i in ld]
                df = pd.DataFrame(dd)
                return df
            else:
                return pd.DataFrame(pd.Series(self.tests)).T
        else:
            return None