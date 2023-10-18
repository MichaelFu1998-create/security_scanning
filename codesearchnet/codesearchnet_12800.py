def plot(self):
        """
        return a toyplot barplot of the results table.
        """
        if self.results_table == None:
            return "no results found"
        else:
            bb = self.results_table.sort_values(
                by=["ABCD", "ACBD"], 
                ascending=[False, True],
                )

            ## make a barplot
            import toyplot
            c = toyplot.Canvas(width=600, height=200)
            a = c.cartesian()
            m = a.bars(bb)
            return c, a, m