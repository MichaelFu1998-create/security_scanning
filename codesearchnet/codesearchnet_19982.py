def filter_gaussian(self,sigmaMs=100,applyFiltered=False,applyBaseline=False):
        """RETURNS filtered trace. Desn't filter it in place."""
        if sigmaMs==0:
            return self.dataY
        filtered=cm.filter_gaussian(self.dataY,sigmaMs)
        if applyBaseline:
            self.dataY=self.dataY-filtered
        elif applyFiltered:
            self.dataY=filtered
        else:
            return filtered