def get_features(self):
        """Get the features contained in `self`.

        :return: the list of features.
        :returntype: `list` of `unicode`"""
        l = self.xpath_ctxt.xpathEval("d:feature")
        ret = []
        for f in l:
            if f.hasProp("var"):
                ret.append( f.prop("var").decode("utf-8") )
        return ret