def numeric_params(self):
        """Return a dict containing all (key, values) stored in '/parameters'
        """
        nparams = dict()
        for p in self.h5file.root.parameters:
            nparams[p.name] = p.read()
        return nparams