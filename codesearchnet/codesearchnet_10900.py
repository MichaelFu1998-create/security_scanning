def numeric_params_meta(self):
        """Return a dict with all parameters and metadata in '/parameters'.

        This returns the same dict format as returned by get_params() method
        in ParticlesSimulation().
        """
        nparams = dict()
        for p in self.h5file.root.parameters:
            nparams[p.name] = (p.read(), p.title)
        return nparams