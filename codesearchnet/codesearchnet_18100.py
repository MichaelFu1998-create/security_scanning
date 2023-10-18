def split_params(self, params, values=None):
        """
        Split params, values into groups that correspond to the ordering in
        self.comps. For example, given a sphere collection and slab::

            [
                (spheres) [pos rad etc] [pos val, rad val, etc]
                (slab) [slab params] [slab vals]
            ]
        """
        pc, vc = [], []

        returnvalues = values is not None
        if values is None:
            values = [0]*len(util.listify(params))

        for c in self.comps:
            tp, tv = [], []
            for p,v in zip(util.listify(params), util.listify(values)):
                if not p in self.lmap:
                    raise NotAParameterError("%r does not belong to %r" % (p, self))

                if c in self.pmap[p]:
                    tp.append(p)
                    tv.append(v)

            pc.append(tp)
            vc.append(tv)

        if returnvalues:
            return pc, vc
        return pc