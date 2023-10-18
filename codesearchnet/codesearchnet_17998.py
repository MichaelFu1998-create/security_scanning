def map_vars(self, comps, funcname='get', diffmap=None, **kwargs):
        """
        Map component function ``funcname`` result into model variables
        dictionary for use in eval of the model. If ``diffmap`` is provided then
        that symbol is translated into 'd'+diffmap.key and is replaced by
        diffmap.value. ``**kwargs` are passed to the ``comp.funcname(**kwargs)``.
        """
        out = {}
        diffmap = diffmap or {}

        for c in comps:
            cat = c.category

            if cat in diffmap:
                symbol = self.diffname(self.ivarmap[cat])
                out[symbol] = diffmap[cat]
            else:
                symbol = self.ivarmap[cat]
                out[symbol] = getattr(c, funcname)(**kwargs)

        return out