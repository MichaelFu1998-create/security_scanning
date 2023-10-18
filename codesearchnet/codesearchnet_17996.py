def check_inputs(self, comps):
        """
        Check that the list of components `comp` is compatible with both the
        varmap and modelstr for this Model
        """
        error = False
        compcats = [c.category for c in comps]

        # Check that the components are all provided, given the categories
        for k, v in iteritems(self.varmap):
            if k not in self.modelstr['full']:
                log.warn('Component (%s : %s) not used in model.' % (k,v))

            if v not in compcats:
                log.error('Map component (%s : %s) not found in list of components.' % (k,v))
                error = True

        if error:
            raise ModelError('Component list incomplete or incorrect')