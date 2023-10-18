def html_singleAll(self,template="basic"):
        """generate a data view for every ABF in the project folder."""
        for fname in smartSort(self.cells):
            if template=="fixed":
                self.html_single_fixed(fname)
            else:
                self.html_single_basic(fname)