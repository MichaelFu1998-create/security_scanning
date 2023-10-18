def sync_params(self):
        """ Ensure that shared parameters are the same value everywhere """
        def _normalize(comps, param):
            vals = [c.get_values(param) for c in comps]
            diff = any([vals[i] != vals[i+1] for i in range(len(vals)-1)])

            if diff:
                for c in comps:
                    c.set_values(param, vals[0])

        for param, comps in iteritems(self.lmap):
            if isinstance(comps, list) and len(comps) > 1:
                _normalize(comps, param)